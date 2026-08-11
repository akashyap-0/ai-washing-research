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
  excluded_numeric_passages.csv        numeric-density exclusions, with numfrac
  excluded_segment_name_passages.csv   known-false-positive-phrase exclusions

Two extraction-time exclusions run here, both following the pattern established by
`extract_ai_sentiment.is_ai_related` / `risk_factor_composition.check_automat_only_excluded`:
the text never becomes a candidate in the first place, the exclusion is written to
its own auditable CSV rather than silently dropped, and a post-condition self-check
fails the run loudly if an excluded case reaches the retained set. See
MAX_NUMERIC_TOKEN_FRACTION and KNOWN_SEGMENT_NAME_FALSE_POSITIVES.
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

# 1.1.0 adds the two extraction-time exclusions (numeric density, known
# segment-name false positives). Bumped because the version is stamped on every
# retained row: a 1.0.0 row and a 1.1.0 row are not from the same candidate set.
PIPELINE_VERSION = "1.1.0"
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

# The exclusion files carry the retained schema plus what the exclusion decided
# on, so an excluded row can be read, re-scored, and reinstated by hand without
# re-running the pipeline. `retrieval_reasons` on these rows is the UNMASKED
# reason set -- why the passage was retrieved at all -- and for segment-name
# exclusions `removed_reasons` says which of those the phrase list withdrew.
EXCLUDED_NUMERIC_FIELDS = PASSAGE_FIELDS + ("numeric_token_fraction",)
EXCLUDED_SEGMENT_FIELDS = EXCLUDED_NUMERIC_FIELDS + ("removed_reasons",)

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

# ---------------------------------------------------------------------------
# Exclusion 1: numeric-density (GAAP reconciliation tables)
# ---------------------------------------------------------------------------
# The first real run of this script produced 9,581 candidates, of which 528
# (5.5%) were financial tables rather than prose -- 486 of those 528 were 8-K
# `prepared_remarks` exhibits, concentrated in Oracle (177), Broadcom (84),
# IBM (70), Microsoft (63). They are retrieved because WORKFORCE_PATTERN fires
# on "employee severance" / "restructuring charges" appearing as line items in
# a GAAP-to-non-GAAP reconciliation (438 of the 528), not because the filing
# makes any workforce claim. An annotator would otherwise see a GAAP table
# roughly 1 passage in 18.
#
# _NUMERIC_TOKEN_ONLY is the diagnostic heuristic that measured the problem,
# promoted here unchanged so the filter and the measurement agree by
# construction. It matches a whitespace-split token that is entirely numeric
# once currency/sign/parenthesis/percent decoration is stripped, which is what
# a table cell looks like after the HTML structure is gone.
_NUMERIC_TOKEN_ONLY = re.compile(r"^[\$\(\)\-\+]*[\d,\.]+%?[\)\s]*$")

# > 0.25 excludes. At this threshold the retained tail is ordinary prose that
# happens to quote figures ("revenue was $41.5 billion, an increase of ten
# percent"); above it the text is a table.
MAX_NUMERIC_TOKEN_FRACTION = 0.25

# ---------------------------------------------------------------------------
# Exclusion 2: reporting-segment names that collide with keyword patterns
# ---------------------------------------------------------------------------
# Microsoft's reporting segment is literally named "Productivity and Business
# Processes", so PRODUCTIVITY_PATTERN fires on a segment label in every
# quarterly earnings-release table. On the first run, 147 of Microsoft's 250
# productivity-flagged passages (59%) contained that segment name and made no
# productivity claim at all.
#
# This is a verified-phrase list, deliberately NOT a general heuristic: the
# phrase is masked before PRODUCTIVITY_PATTERN is evaluated, so it cannot be
# the reason a passage is retrieved. A passage keeps `productivity` if a real
# productivity term appears elsewhere in it.
#
# NOT EXHAUSTIVE. Other filers in this universe may have segment or product
# names that collide with these patterns the same way -- none has been verified
# yet, so none is listed. Add an entry only after confirming the collision in
# actual filing text; do not guess at segment names, and do not generalize this
# into a pattern that would silently drop real claims.
KNOWN_SEGMENT_NAME_FALSE_POSITIVES = (
    "Productivity and Business Processes",   # Microsoft reporting segment
)

_SEGMENT_NAME_MASK = re.compile(
    "|".join(re.escape(phrase) for phrase in KNOWN_SEGMENT_NAME_FALSE_POSITIVES),
    re.IGNORECASE,
)


def numeric_token_fraction(text):
    """Fraction of whitespace-split tokens that are numeric-only.

    0.0 for empty text so a caller can compare against a threshold without
    special-casing.
    """
    tokens = (text or "").split()
    if not tokens:
        return 0.0
    numeric = sum(1 for t in tokens if _NUMERIC_TOKEN_ONLY.match(t))
    return numeric / len(tokens)


def mask_segment_names(text):
    """Blank out known false-positive segment names before keyword matching."""
    return _SEGMENT_NAME_MASK.sub(" ", text or "")


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


def retrieval_reasons(text, mask_known_false_positives=True):
    """Why this text is a candidate.

    With mask_known_false_positives (the default, and what the pipeline uses),
    KNOWN_SEGMENT_NAME_FALSE_POSITIVES are blanked out before the productivity
    pattern is evaluated, so a reporting-segment name cannot be a retrieval
    reason. Pass False to get the unmasked reasons, which is how the exclusion
    is measured and audited -- a passage whose only unmasked reason disappears
    under masking is a segment-name false positive.
    """
    productivity_text = (mask_segment_names(text) if mask_known_false_positives
                         else text)
    reasons = []
    if AI_PATTERN.search(text):
        reasons.append("ai")
    if WORKFORCE_PATTERN.search(text):
        reasons.append("workforce")
    if PRODUCTIVITY_PATTERN.search(productivity_text):
        reasons.append("productivity")
    return reasons


# ---------------------------------------------------------------------------
# Post-condition self-checks on the two extraction-time exclusions
# ---------------------------------------------------------------------------
# Same contract as risk_factor_composition.check_automat_only_excluded: these
# must return empty on every run. A non-empty return means the filter and the
# retained set have diverged, and main() fails the run loudly rather than
# letting an excluded case back into the annotation candidates unnoticed.

def check_numeric_dense_excluded(passages):
    """No retained passage may exceed the numeric-density threshold."""
    return [p for p in passages
            if numeric_token_fraction(p["text"]) > MAX_NUMERIC_TOKEN_FRACTION]


def check_segment_name_false_positives_excluded(passages):
    """No retained passage may carry `productivity` solely because of a known
    false-positive segment name."""
    offenders = []
    for p in passages:
        if "productivity" not in p["retrieval_reasons"].split(";"):
            continue
        if not PRODUCTIVITY_PATTERN.search(mask_segment_names(p["text"])):
            offenders.append(p)
    return offenders


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
        # Extraction-time exclusions. A chunk can be caught by both filters, so
        # the per-filter counts overlap by design and `caught_by_both` reports
        # the intersection rather than the counts being made disjoint.
        "exclusions": {
            "numeric_density_threshold": MAX_NUMERIC_TOKEN_FRACTION,
            "numeric_density": 0,
            "numeric_density_by_form": Counter(),
            "numeric_density_by_section": Counter(),
            "numeric_density_by_reason": Counter(),
            "numeric_density_by_ticker": Counter(),
            "segment_name_false_positive": 0,
            "segment_name_by_form": Counter(),
            "segment_name_by_section": Counter(),
            "segment_name_by_ticker": Counter(),
            "caught_by_both": 0,
            "productivity_reason_stripped_passage_retained": 0,
        },
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
    excluded_numeric = []
    excluded_segment_name = []
    seen_content = set()
    per_source_index = defaultdict(int)
    ex = qa["exclusions"]
    for row in source_rows:
        source_key = (row.get("doc_id", ""), row.get("section", ""))
        for chunk in chunk_text(row.get("text", "")):
            if len(chunk.split()) < HARD_MIN_WORDS:
                continue
            raw_reasons = retrieval_reasons(chunk,
                                            mask_known_false_positives=False)
            if not raw_reasons:
                # Never a candidate under any configuration: no keyword family
                # matched at all. Not an exclusion, so not traced.
                continue
            reasons = retrieval_reasons(chunk)
            numfrac = numeric_token_fraction(chunk)

            # Dedup and index assignment run BEFORE the exclusion decision, in
            # the same order as they did before these filters existed, so a
            # retained passage keeps the passage_index -- and therefore the
            # passage_id -- it had under pipeline 1.0.0. An excluded passage
            # consumes its index too, so the retained sequence has a gap
            # exactly where an exclusion happened, and the excluded row records
            # its real position in the source document.
            content_hash = hashlib.sha256(chunk.encode("utf-8")).hexdigest()
            duplicate_key = (row["period_id"], row.get("source_type", ""),
                             row.get("section", ""), content_hash)
            if duplicate_key in seen_content:
                continue
            seen_content.add(duplicate_key)
            index = per_source_index[source_key]
            per_source_index[source_key] += 1

            form = row.get("source_type", "")
            section = row.get("section", "")
            ticker = row.get("ticker", "").upper()

            # Evaluate both filters independently so the overlap is reportable.
            numeric_excluded = numfrac > MAX_NUMERIC_TOKEN_FRACTION
            segment_excluded = not reasons

            if numeric_excluded or segment_excluded:
                record = {
                    "passage_id": stable_passage_id(row, index, chunk),
                    "ticker": ticker,
                    "company": row.get("company", ""),
                    "form": form,
                    "filing_date": row.get("filing_date", ""),
                    "anchor_10k_filing_date": row["anchor_10k_filing_date"],
                    "period_id": row["period_id"],
                    "section": section,
                    "passage_index": index,
                    "source_doc_id": row.get("doc_id", ""),
                    "source_url": row.get("url", ""),
                    "word_count": len(chunk.split()),
                    "retrieval_reasons": ";".join(raw_reasons),
                    "content_sha256": content_hash,
                    "text": chunk,
                    "pipeline_version": PIPELINE_VERSION,
                    "numeric_token_fraction": round(numfrac, 4),
                }
                if numeric_excluded:
                    ex["numeric_density"] += 1
                    ex["numeric_density_by_form"][form] += 1
                    ex["numeric_density_by_section"][section] += 1
                    ex["numeric_density_by_reason"][";".join(raw_reasons)] += 1
                    ex["numeric_density_by_ticker"][ticker] += 1
                    excluded_numeric.append(record)
                if segment_excluded:
                    ex["segment_name_false_positive"] += 1
                    ex["segment_name_by_form"][form] += 1
                    ex["segment_name_by_section"][section] += 1
                    ex["segment_name_by_ticker"][ticker] += 1
                    excluded_segment_name.append(dict(
                        record, removed_reasons=";".join(
                            r for r in raw_reasons if r not in reasons)))
                if numeric_excluded and segment_excluded:
                    ex["caught_by_both"] += 1
                continue

            if "productivity" in raw_reasons and "productivity" not in reasons:
                # Retained on another reason, but the segment name no longer
                # counts toward why. Worth counting: it is the same false
                # positive, just not decisive for this passage.
                ex["productivity_reason_stripped_passage_retained"] += 1

            passage = {
                "passage_id": stable_passage_id(row, index, chunk),
                "ticker": ticker,
                "company": row.get("company", ""),
                "form": form,
                "filing_date": row.get("filing_date", ""),
                "anchor_10k_filing_date": row["anchor_10k_filing_date"],
                "period_id": row["period_id"],
                "section": section,
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
    ex["candidates_before_exclusions"] = (
        len(passages) + len(excluded_numeric)
        + len(excluded_segment_name) - ex["caught_by_both"])
    ex["excluded_total"] = (len(excluded_numeric) + len(excluded_segment_name)
                            - ex["caught_by_both"])
    # Post-conditions: both must be empty. Reported here and enforced in main().
    ex["postcondition_numeric_dense_retained"] = len(
        check_numeric_dense_excluded(passages))
    ex["postcondition_segment_name_retained"] = len(
        check_segment_name_false_positives_excluded(passages))
    for key in ("numeric_density_by_reason",):
        # deterministic ordering for the JSON report
        ex[key] = Counter(dict(ex[key].most_common()))
    return passages, qa, excluded_numeric, excluded_segment_name


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
            "risk_type": "",
            "risk_type_secondary": "",
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
    passages, qa, excluded_numeric, excluded_segment = build_passages(
        tenk_rows, eightk_rows, allowed,
        require_matched_period=not args.allow_unmatched_10k_periods)

    passage_path = os.path.join(args.output_dir, "clean_passages.csv")
    annotation_path = os.path.join(args.output_dir, "annotation_template.csv")
    qa_path = os.path.join(args.output_dir, "passage_qa.json")
    numeric_path = os.path.join(args.output_dir,
                                "excluded_numeric_passages.csv")
    segment_path = os.path.join(args.output_dir,
                                "excluded_segment_name_passages.csv")
    write_csv(passage_path, passages, PASSAGE_FIELDS)
    write_csv(numeric_path, excluded_numeric, EXCLUDED_NUMERIC_FIELDS)
    write_csv(segment_path, excluded_segment, EXCLUDED_SEGMENT_FIELDS)
    sample = annotation_sample(passages, args.annotation_sample, args.seed)
    write_csv(annotation_path, sample, PASSAGE_FIELDS + label_schema.ANNOTATION_FIELDS[1:])
    with open(qa_path, "w", encoding="utf-8") as handle:
        json.dump(json_ready(qa), handle, indent=2, sort_keys=True)

    print(f"Wrote {len(passages):,} passages to {passage_path}")
    print(f"Wrote {len(sample):,} annotation rows to {annotation_path}")
    print(f"Wrote QA report to {qa_path}")

    ex = qa["exclusions"]
    before = ex["candidates_before_exclusions"]
    print(f"\nEXTRACTION-TIME EXCLUSIONS "
          f"({before:,} candidates before -> {len(passages):,} retained)")
    print(f"  numeric density > {MAX_NUMERIC_TOKEN_FRACTION:g}: "
          f"{ex['numeric_density']:,} "
          f"({100.0 * ex['numeric_density'] / max(before, 1):.1f}%) "
          f"-> {numeric_path}")
    for label, key in (("by form", "numeric_density_by_form"),
                       ("by section", "numeric_density_by_section")):
        print(f"      {label}: {dict(ex[key].most_common())}")
    print(f"  known segment-name false positive: "
          f"{ex['segment_name_false_positive']:,} "
          f"({100.0 * ex['segment_name_false_positive'] / max(before, 1):.1f}%) "
          f"-> {segment_path}")
    for label, key in (("by form", "segment_name_by_form"),
                       ("by ticker", "segment_name_by_ticker")):
        print(f"      {label}: {dict(ex[key].most_common())}")
    print(f"  caught by BOTH filters: {ex['caught_by_both']:,}")
    print(f"  retained but `productivity` reason stripped: "
          f"{ex['productivity_reason_stripped_passage_retained']:,}")

    fp_numeric = check_numeric_dense_excluded(passages)
    fp_segment = check_segment_name_false_positives_excluded(passages)
    if fp_numeric or fp_segment:
        print("\n  *** POST-CONDITION FAILED ***")
        print("  These exclusions are supposed to happen at extraction time, so")
        print("  both lists must be empty. A non-empty list means a filter and")
        print("  the retained set have diverged -- investigate before annotating.")
        for p in fp_numeric[:10]:
            print(f"    numeric-dense retained: {p['ticker']} "
                  f"{p['filing_date']} {p['passage_id']} "
                  f"numfrac={numeric_token_fraction(p['text']):.3f}")
        for p in fp_segment[:10]:
            print(f"    segment-name retained:  {p['ticker']} "
                  f"{p['filing_date']} {p['passage_id']}")
        raise SystemExit(1)
    print("\n  post-condition OK: 0 numeric-dense and 0 segment-name-only "
          "passages in the retained set.")


if __name__ == "__main__":
    main()
