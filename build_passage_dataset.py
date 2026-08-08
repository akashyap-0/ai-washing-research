"""Build the clean, matched 10-K/8-K candidate-passage dataset.

This is the first executable stage of RESEARCH_PIPELINE.md. It reads the
existing normalized exports, keeps companies represented in both forms,
assigns each 8-K to a 10-K reporting window, creates section-bounded passages,
and retains candidates related to AI, automation, workforce, restructuring,
or productivity. Keyword retrieval is deliberately broader than the label
schema: it creates candidates and is not treated as ground truth.

Outputs (default: derived/):
  clean_passages.csv       one row per auditable passage
  annotation_template.csv  deterministic stratified sample for human coding
  passage_qa.json          counts, exclusions, and coverage checks
"""

import argparse
import csv
import hashlib
import json
import os
import random
import re
import sys
from collections import Counter, defaultdict
from datetime import datetime, timedelta

import config
import label_schema

PIPELINE_VERSION = "1.0.0"
MIN_WORDS = 60
HARD_MIN_WORDS = 20
TARGET_WORDS = 160
MAX_WORDS = 220
EARLIEST_WINDOW_DAYS = 400

# Predeclared current research universe. Palantir exists in the raw exports
# from an older exploratory pull but is intentionally excluded because its
# provenance and inclusion were never approved (see extract_ai_sentiment.py).
APPROVED_TICKERS = {
    "IBM", "ORCL", "DELL", "CRM", "MSFT", "AMD", "NVDA", "VZ", "AXP",
    "UNH", "GOOGL", "AMZN", "AAPL", "META", "TSLA", "AVGO", "ACN", "WMT",
    "JPM", "LLY", "DE", "SPGI", "INTU", "NOW", "UBER",
}

PASSAGE_FIELDS = (
    "passage_id", "ticker", "company", "form", "filing_date",
    "anchor_10k_filing_date", "period_id", "section", "passage_index",
    "source_doc_id", "source_url", "word_count", "retrieval_reasons",
    "content_sha256", "text", "pipeline_version",
)

AI_PATTERN = re.compile(
    r"\b(?:AI|artificial intelligence|generative AI|genAI|machine learning|"
    r"deep learning|neural network\w*|large language model\w*|LLM\w*|"
    r"automat(?:e|ed|es|ing|ion|ions)|robotic\w*|cognitive computing|"
    r"Agentforce|watsonx|Watson)\b",
    re.IGNORECASE,
)

WORKFORCE_PATTERN = re.compile(
    r"\b(?:employee\w*|workforce|worker\w*|headcount|personnel|labor|labour|"
    r"hiring|hire[ds]?|job cuts?|layoffs?|laid off|role eliminat\w*|"
    r"restructur\w*|severance|redundan(?:cy|cies|t)|attrition|reskill\w*|"
    r"upskill\w*)\b",
    re.IGNORECASE,
)

PRODUCTIVITY_PATTERN = re.compile(
    r"\b(?:productiv\w*|efficien\w*|cost sav\w*|cost reduc\w*|"
    r"operating leverage|streamlin\w*|manual (?:task|process|work)|"
    r"time sav\w*|process improvement\w*|do more with less)\b",
    re.IGNORECASE,
)

PAGE_NOISE = re.compile(
    r"(?im)^\s*(?:table of contents|page\s+\d+|\d{1,3})\s*$"
)
SENTENCE_BOUNDARY = re.compile(r"(?<=[.!?])\s+(?=[A-Z0-9(\[])")


def raise_csv_limit():
    limit = sys.maxsize
    while True:
        try:
            csv.field_size_limit(limit)
            return
        except OverflowError:
            limit //= 10


def load_csv(path):
    raise_csv_limit()
    with open(path, newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def normalize_text(text):
    text = (text or "").replace("\u00a0", " ").replace("\u00ad", "")
    text = PAGE_NOISE.sub("\n", text)
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n[ \t]+", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def sentence_split(text):
    """Conservative filing-text splitter without a runtime model download."""
    flattened = re.sub(r"\s+", " ", text).strip()
    if not flattened:
        return []
    return [part.strip() for part in SENTENCE_BOUNDARY.split(flattened)
            if part.strip()]


def chunk_text(text, min_words=MIN_WORDS, target_words=TARGET_WORDS,
               max_words=MAX_WORDS):
    """Return bounded chunks, never crossing the caller's section boundary."""
    sentences = sentence_split(normalize_text(text))
    chunks = []
    current = []
    current_words = 0

    def flush():
        nonlocal current, current_words
        if current:
            chunks.append(" ".join(current))
        current, current_words = [], 0

    for sentence in sentences:
        words = sentence.split()
        if len(words) > max_words:
            flush()
            for start in range(0, len(words), max_words):
                chunks.append(" ".join(words[start:start + max_words]))
            continue

        if current and current_words + len(words) > max_words:
            flush()
        current.append(sentence)
        current_words += len(words)
        if current_words >= target_words:
            flush()
    flush()

    # Preserve short sections and tails by joining a short tail backward.
    if len(chunks) > 1 and len(chunks[-1].split()) < min_words:
        tail = chunks.pop()
        if len(chunks[-1].split()) + len(tail.split()) <= max_words:
            chunks[-1] = f"{chunks[-1]} {tail}"
        else:
            chunks.append(tail)
    return chunks


def retrieval_reasons(text):
    reasons = []
    if AI_PATTERN.search(text):
        reasons.append("ai")
    if WORKFORCE_PATTERN.search(text):
        reasons.append("workforce")
    if PRODUCTIVITY_PATTERN.search(text):
        reasons.append("productivity")
    return reasons


def parse_date(value):
    return datetime.strptime(value, "%Y-%m-%d").date()


def tenk_anchors(rows):
    """Return unique 10-K anchors keyed by ticker and filing date."""
    anchors = defaultdict(dict)
    for row in rows:
        ticker = row.get("ticker", "").upper()
        date = row.get("filing_date", "")
        if ticker and date:
            anchors[ticker][date] = {
                "ticker": ticker,
                "company": row.get("company", ""),
                "filing_date": date,
            }
    return {ticker: sorted(values.values(), key=lambda x: x["filing_date"])
            for ticker, values in anchors.items()}


def match_anchor(filing_date, anchors):
    """Match an 8-K to (previous 10-K filing, current 10-K filing]."""
    date = parse_date(filing_date)
    previous = None
    for anchor in anchors:
        end = parse_date(anchor["filing_date"])
        start = (parse_date(previous["filing_date"]) if previous else
                 end - timedelta(days=EARLIEST_WINDOW_DAYS))
        if start < date <= end:
            return anchor, "matched"
        previous = anchor
    if anchors and date > parse_date(anchors[-1]["filing_date"]):
        return None, "after_latest_10k"
    return None, "before_earliest_window"


def stable_passage_id(row, index, text):
    basis = "|".join([
        row.get("ticker", ""), row.get("source_type", ""),
        row.get("filing_date", ""), row.get("section", ""),
        row.get("doc_id", ""), str(index), text,
    ])
    return hashlib.sha256(basis.encode("utf-8")).hexdigest()[:24]


def build_passages(tenk_rows, eightk_rows, allowed_tickers=APPROVED_TICKERS,
                   require_matched_period=True):
    anchors_by_ticker = tenk_anchors(tenk_rows)
    both_forms = set(anchors_by_ticker) & {
        row.get("ticker", "").upper() for row in eightk_rows
    }
    if allowed_tickers is not None:
        both_forms &= set(allowed_tickers)
    qa = {
        "pipeline_version": PIPELINE_VERSION,
        "input_10k_rows": len(tenk_rows),
        "input_8k_rows": len(eightk_rows),
        "companies_in_both_forms": len(both_forms),
        "matched_8k_rows": 0,
        "excluded_8k_rows": Counter(),
        "candidate_passages_by_form": Counter(),
        "candidate_passages_by_reason": Counter(),
        "candidate_passages_by_ticker": Counter(),
    }

    source_rows = []
    for row in tenk_rows:
        ticker = row.get("ticker", "").upper()
        if ticker not in both_forms:
            continue
        adapted = dict(row)
        adapted["anchor_10k_filing_date"] = row["filing_date"]
        adapted["period_id"] = f"{ticker}:{row['filing_date']}"
        source_rows.append(adapted)

    matched_period_ids = set()
    for row in eightk_rows:
        ticker = row.get("ticker", "").upper()
        if ticker not in both_forms:
            qa["excluded_8k_rows"]["company_not_in_both_forms"] += 1
            continue
        anchor, status = match_anchor(row["filing_date"], anchors_by_ticker[ticker])
        if not anchor:
            qa["excluded_8k_rows"][status] += 1
            continue
        adapted = dict(row)
        adapted["anchor_10k_filing_date"] = anchor["filing_date"]
        adapted["period_id"] = f"{ticker}:{anchor['filing_date']}"
        source_rows.append(adapted)
        matched_period_ids.add(adapted["period_id"])
        qa["matched_8k_rows"] += 1

    qa["raw_periods_with_matched_8k"] = len(matched_period_ids)
    if require_matched_period:
        before = len(source_rows)
        source_rows = [row for row in source_rows
                       if row["period_id"] in matched_period_ids]
        qa["source_rows_excluded_without_matched_8k_period"] = before - len(source_rows)

    passages = []
    seen_content = set()
    per_source_index = defaultdict(int)
    for row in source_rows:
        source_key = (row.get("doc_id", ""), row.get("section", ""))
        for chunk in chunk_text(row.get("text", "")):
            if len(chunk.split()) < HARD_MIN_WORDS:
                continue
            reasons = retrieval_reasons(chunk)
            if not reasons:
                continue
            content_hash = hashlib.sha256(chunk.encode("utf-8")).hexdigest()
            duplicate_key = (row["period_id"], row.get("source_type", ""),
                             row.get("section", ""), content_hash)
            if duplicate_key in seen_content:
                continue
            seen_content.add(duplicate_key)
            index = per_source_index[source_key]
            per_source_index[source_key] += 1
            passage = {
                "passage_id": stable_passage_id(row, index, chunk),
                "ticker": row.get("ticker", "").upper(),
                "company": row.get("company", ""),
                "form": row.get("source_type", ""),
                "filing_date": row.get("filing_date", ""),
                "anchor_10k_filing_date": row["anchor_10k_filing_date"],
                "period_id": row["period_id"],
                "section": row.get("section", ""),
                "passage_index": index,
                "source_doc_id": row.get("doc_id", ""),
                "source_url": row.get("url", ""),
                "word_count": len(chunk.split()),
                "retrieval_reasons": ";".join(reasons),
                "content_sha256": content_hash,
                "text": chunk,
                "pipeline_version": PIPELINE_VERSION,
            }
            passages.append(passage)
            qa["candidate_passages_by_form"][passage["form"]] += 1
            qa["candidate_passages_by_ticker"][passage["ticker"]] += 1
            for reason in reasons:
                qa["candidate_passages_by_reason"][reason] += 1

    passages.sort(key=lambda r: (
        r["ticker"], r["period_id"], r["form"], r["filing_date"],
        r["section"], int(r["passage_index"]),
    ))
    qa["candidate_passages"] = len(passages)
    qa["matched_periods"] = len({p["period_id"] for p in passages})
    qa["passage_id_unique"] = len({p["passage_id"] for p in passages}) == len(passages)
    return passages, qa


def write_csv(path, rows, fields):
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def annotation_sample(passages, size, seed):
    """Deterministically balance the sample across form and retrieval family."""
    rng = random.Random(seed)
    strata = defaultdict(list)
    for row in passages:
        strata[(row["form"], row["retrieval_reasons"])].append(row)
    for rows in strata.values():
        rng.shuffle(rows)

    chosen = []
    ordered_keys = sorted(strata)
    while len(chosen) < min(size, len(passages)):
        progressed = False
        for key in ordered_keys:
            if strata[key] and len(chosen) < size:
                chosen.append(strata[key].pop())
                progressed = True
        if not progressed:
            break

    output = []
    for row in chosen:
        annotation = dict(row)
        for label in label_schema.MODEL_LABELS:
            annotation[label] = ""
        annotation.update({
            "neutral": "",
            "actuality": "",
            "specificity": "",
            "causal_link_strength": "",
            "coder_id": "",
            "review_status": "unreviewed",
            "annotation_notes": "",
            "label_schema_version": label_schema.SCHEMA_VERSION,
        })
        output.append(annotation)
    return output


def json_ready(value):
    if isinstance(value, Counter):
        return dict(sorted(value.items()))
    if isinstance(value, dict):
        return {key: json_ready(item) for key, item in value.items()}
    return value


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--10k", dest="tenk_path", default=os.path.join(
        config.EXPORT_DIR, "ai_washing_10-K.csv"))
    parser.add_argument("--8k", dest="eightk_path", default=os.path.join(
        config.EXPORT_DIR, "ai_washing_8-K.csv"))
    parser.add_argument("--output-dir", default="derived")
    parser.add_argument("--annotation-sample", type=int, default=1200)
    parser.add_argument("--seed", type=int, default=20260808)
    parser.add_argument(
        "--companies", default=",".join(sorted(APPROVED_TICKERS)),
        help="comma-separated predeclared ticker universe; use an empty value "
             "only to use every ticker present in both exports")
    parser.add_argument(
        "--allow-unmatched-10k-periods", action="store_true",
        help="retain 10-K periods with no matched 8-K; disabled by default "
             "because the primary corpus requires the same company-periods")
    args = parser.parse_args(argv)

    tenk_rows = load_csv(args.tenk_path)
    eightk_rows = load_csv(args.eightk_path)
    allowed = ({ticker.strip().upper() for ticker in args.companies.split(",")
                if ticker.strip()} if args.companies else None)
    passages, qa = build_passages(
        tenk_rows, eightk_rows, allowed,
        require_matched_period=not args.allow_unmatched_10k_periods)

    passage_path = os.path.join(args.output_dir, "clean_passages.csv")
    annotation_path = os.path.join(args.output_dir, "annotation_template.csv")
    qa_path = os.path.join(args.output_dir, "passage_qa.json")
    write_csv(passage_path, passages, PASSAGE_FIELDS)
    sample = annotation_sample(passages, args.annotation_sample, args.seed)
    write_csv(annotation_path, sample, PASSAGE_FIELDS + label_schema.ANNOTATION_FIELDS[1:])
    with open(qa_path, "w", encoding="utf-8") as handle:
        json.dump(json_ready(qa), handle, indent=2, sort_keys=True)

    print(f"Wrote {len(passages):,} passages to {passage_path}")
    print(f"Wrote {len(sample):,} annotation rows to {annotation_path}")
    print(f"Wrote QA report to {qa_path}")


if __name__ == "__main__":
    main()
