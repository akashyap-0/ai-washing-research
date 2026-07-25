"""Measure the sentiment gap between each company's 8-K press release and the
10-K covering the same fiscal period, as a bias-free stand-in for hand-labeling
AI-washing language.

Why this approach (per advisor feedback): hand-scoring sentences for
"AI-washing" bakes in the scorer's own judgment about which words count as
hype, which a reviewer can challenge. Comparing a company's tone in two
SEC filings about the *same period* sidesteps that: the 8-K press release is
written to move the stock (promotional), while the 10-K is drafted by/with
counsel under liability exposure (legally cautious, hedged). A large gap
between how positive/confident the same company sounds across the two filings
is evidence of promotional framing without requiring us to personally judge
any individual sentence.

Pipeline:
  1. Load export/ai_washing_10-K.csv and export/ai_washing_8-K.csv (written by
     main.py / storage.py). Each row is one *section* of a filing (10-Ks are
     split into "Item 1A Risk Factors" / "Item 7 MD&A"; 8-Ks are split into
     one row per EX-99.* exhibit). We first collapse those back into one
     record per actual filing (grouped by company + filing_date), so a 10-K
     with two sections and an 8-K with two exhibits are each treated as a
     single document.
  2. Fiscal-year matching (see `build_fiscal_windows` below for the exact
     rule and the assumption it relies on).
  3. Run FinBERT (ProsusAI/finbert) on each document's full text, chunked to
     fit the model's 512-token limit, and average the resulting
     positive/negative/neutral probabilities across chunks.
  4. Reduce each document's distribution to a single net-tone scalar
     (P(positive) - P(negative); see `net_tone_score` for why) and take
     8-K score minus 10-K score as the distance.
  5. Write export/sentiment_distance_results.csv and print a summary.

Fiscal-year-matching assumption (read this before trusting the output):
Our data only has `filing_date` for each document -- not the fiscal period a
10-K actually covers. But 10-Ks are filed annually, shortly after fiscal
year-end (e.g. Oracle's fiscal year ends ~May 31 and its 10-K is filed each
~June 20; IBM's calendar fiscal year ends Dec 31 and its 10-K is filed each
~February). That means the stretch of time between one 10-K's filing_date and
the *next* 10-K's filing_date is a good proxy for "the fiscal year that next
10-K reports on" -- it starts right after the prior year's annual report was
filed and ends when this year's annual report is filed (capturing that year's
Q1-Q3 earnings releases plus the Q4/full-year release, which is often filed
just weeks before the 10-K itself). So: for company C, sort its 10-Ks by
filing_date; 10-K_i's fiscal-year window is (10-K_{i-1}.filing_date,
10-K_i.filing_date]. Every 8-K whose filing_date falls in that window is
matched to 10-K_i. For a company's *earliest* 10-K in our dataset there is no
prior 10-K to anchor the window's start, so we fall back to
(that 10-K's filing_date - 400 days) as a stand-in for "about one fiscal year
back" -- generous enough to catch an early Q4/full-year earnings 8-K filed
well before the 10-K, without reaching back far enough to sweep in an
unrelated earlier fiscal year. 8-Ks filed after a company's most recent 10-K
in our dataset (i.e. during a fiscal year that hasn't been closed out by a
10-K yet) have no valid match and are skipped and logged, not guessed at.

Run:
    python sentiment_distance.py            # full run
    python sentiment_distance.py --dry-run   # pairing only, no FinBERT (fast;
                                              # use this to sanity-check matches)
"""
import argparse
import csv
import glob
import os
import sys
from collections import defaultdict
from datetime import datetime, timedelta

import config

# --- CSV field size: 10-K/8-K `text` fields hold whole filing sections and
# blow past csv's default 131072-byte-per-field cap. Same fix as
# extract_sentences.py. -----------------------------------------------------


def _raise_csv_field_limit():
    limit = sys.maxsize
    while True:
        try:
            csv.field_size_limit(limit)
            return
        except OverflowError:
            limit //= 10


_raise_csv_field_limit()

EXPORT_DIR = config.EXPORT_DIR
TENK_PATH = os.path.join(EXPORT_DIR, "ai_washing_10-K.csv")
EIGHTK_PATH = os.path.join(EXPORT_DIR, "ai_washing_8-K.csv")
OUTPUT_PATH = os.path.join(EXPORT_DIR, "sentiment_distance_results.csv")

FINBERT_MODEL = "ProsusAI/finbert"
MAX_TOKENS = 512  # FinBERT's (BERT-base) hard sequence limit
CHUNK_TOKENS = MAX_TOKENS - 2  # leave room for [CLS]/[SEP] on every chunk

# Fallback window (see module docstring) for a company's earliest 10-K, which
# has no prior 10-K in our dataset to anchor its fiscal-year window's start.
EARLIEST_WINDOW_FALLBACK_DAYS = 400

OUTPUT_FIELDS = [
    "company", "ticker", "8k_doc_id", "8k_filing_date", "10k_doc_id",
    "10k_fiscal_year", "8k_sentiment_score", "10k_sentiment_score",
    "distance", "8k_url", "10k_url",
]


# --- Step 1: load + collapse section/exhibit rows into one row per filing --

def _load_csv(path):
    if not os.path.exists(path):
        print(f"[error] {path} not found -- run main.py first.")
        return []
    with open(path, newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def _parse_date(s):
    return datetime.strptime(s, "%Y-%m-%d").date()


def group_filings(rows):
    """Collapse per-section/per-exhibit rows into one record per actual
    filing, keyed by (company, filing_date).

    A 10-K's two item sections share one url (verified against the real
    export/ data), so grouping just concatenates their text. An 8-K's
    exhibits (e.g. ex99.1 press release + ex99.2 prepared remarks) live at
    *different* urls, so we join urls/doc_ids with "; " to keep both
    traceable while still producing the single distance-worthy document the
    professor's method calls for.
    """
    groups = defaultdict(list)
    for row in rows:
        key = (row["company"], row["ticker"], row["filing_date"])
        groups[key].append(row)

    filings = []
    for (company, ticker, filing_date), group_rows in groups.items():
        group_rows.sort(key=lambda r: r.get("section", ""))
        filings.append({
            "company": company,
            "ticker": ticker,
            "filing_date": _parse_date(filing_date),
            "doc_id": "; ".join(r["doc_id"] for r in group_rows),
            "url": "; ".join(dict.fromkeys(r["url"] for r in group_rows)),
            "text": "\n\n".join(r["text"] for r in group_rows if r["text"]),
        })
    return filings


# --- Step 2: fiscal-year window matching ------------------------------------

def build_fiscal_windows(tenk_filings):
    """For one company's sorted 10-Ks, return a list of
    (window_start_exclusive, window_end_inclusive, tenk) tuples."""
    windows = []
    prev_filing_date = None
    for tenk in sorted(tenk_filings, key=lambda f: f["filing_date"]):
        if prev_filing_date is None:
            window_start = tenk["filing_date"] - timedelta(
                days=EARLIEST_WINDOW_FALLBACK_DAYS)
        else:
            window_start = prev_filing_date
        windows.append((window_start, tenk["filing_date"], tenk))
        prev_filing_date = tenk["filing_date"]
    return windows


def match_8k_to_10k(eightk, windows):
    """Return (matched_10k_or_None, skip_reason_or_None)."""
    if not windows:
        return None, "company has no 10-K filings in this dataset"
    date = eightk["filing_date"]
    for window_start, window_end, tenk in windows:
        if window_start < date <= window_end:
            return tenk, None
    if date > windows[-1][1]:
        return None, ("filed after the company's most recent 10-K in this "
                       "dataset -- that fiscal year hasn't been closed out "
                       "by a 10-K yet")
    return None, ("filed before the earliest 10-K's estimated fiscal-year "
                  "window in this dataset")


def build_pairs(tenk_filings, eightk_filings):
    """Returns (pairs, skipped) where pairs is a list of
    {tenk, eightk} dicts and skipped is a list of {eightk, reason} dicts."""
    by_company = defaultdict(list)
    for tenk in tenk_filings:
        by_company[tenk["company"]].append(tenk)

    pairs, skipped = [], []
    for eightk in eightk_filings:
        windows = build_fiscal_windows(by_company.get(eightk["company"], []))
        tenk, reason = match_8k_to_10k(eightk, windows)
        if tenk is None:
            skipped.append({"eightk": eightk, "reason": reason})
        else:
            pairs.append({"tenk": tenk, "eightk": eightk})
    return pairs, skipped


def print_pairing_preview(pairs, skipped):
    print(f"\n=== Pairing preview ({len(pairs)} matched, {len(skipped)} skipped) ===")
    for p in sorted(pairs, key=lambda p: (p["eightk"]["company"], p["eightk"]["filing_date"])):
        print(f"  {p['eightk']['company']:<40} 8-K {p['eightk']['filing_date']} "
              f"-> 10-K {p['tenk']['filing_date']}")
    if skipped:
        print(f"\n  Skipped 8-Ks ({len(skipped)}):")
        for s in sorted(skipped, key=lambda s: (s["eightk"]["company"], s["eightk"]["filing_date"])):
            print(f"    {s['eightk']['company']:<40} 8-K {s['eightk']['filing_date']} "
                  f"-- {s['reason']}")


# --- Step 3+4: FinBERT sentiment + net-tone scalar --------------------------

def load_finbert():
    """Load FinBERT once, on GPU if available (nice-to-have speedup on this
    dataset's size; CPU works fine too, just slower)."""
    import torch
    from transformers import AutoModelForSequenceClassification, AutoTokenizer

    device = "cuda" if torch.cuda.is_available() else "cpu"
    tokenizer = AutoTokenizer.from_pretrained(FINBERT_MODEL)
    model = AutoModelForSequenceClassification.from_pretrained(FINBERT_MODEL)
    model.to(device)
    model.eval()
    # FinBERT's config.id2label is {0: 'positive', 1: 'negative', 2: 'neutral'}
    label_index = {label: i for i, label in model.config.id2label.items()}
    return tokenizer, model, device, label_index


def _chunk_token_ids(token_ids, chunk_size):
    return [token_ids[i:i + chunk_size]
            for i in range(0, len(token_ids), chunk_size)] or [[]]


def document_sentiment(text, tokenizer, model, device, label_index):
    """Run FinBERT over `text`, chunked to CHUNK_TOKENS, and return the
    average (positive, negative, neutral) probability across chunks.

    FinBERT's standard output is a 3-way softmax distribution over
    positive/negative/neutral -- there's no single "official" scalar, so we
    keep the full distribution here and reduce it to one number in
    `net_tone_score` (see that function for the reduction we chose and why).
    Chunks are averaged with equal weight rather than weighted by length:
    with FinBERT's small (510-token) chunk size, unequal weighting would
    mostly just up-weight whichever chunk happens to be the last, no-longer
    full one -- equal weighting is simpler and standard practice for
    document-level aggregation of sentence/paragraph-level classifiers.
    """
    import torch

    token_ids = tokenizer.encode(text, add_special_tokens=False)
    chunks = _chunk_token_ids(token_ids, CHUNK_TOKENS)

    cls_id, sep_id = tokenizer.cls_token_id, tokenizer.sep_token_id
    pad_id = tokenizer.pad_token_id or 0

    max_len = max(len(c) for c in chunks) + 2
    input_ids, attention_mask = [], []
    for c in chunks:
        ids = [cls_id] + c + [sep_id]
        pad_len = max_len - len(ids)
        input_ids.append(ids + [pad_id] * pad_len)
        attention_mask.append([1] * len(ids) + [0] * pad_len)

    with torch.no_grad():
        batch = {
            "input_ids": torch.tensor(input_ids, device=device),
            "attention_mask": torch.tensor(attention_mask, device=device),
        }
        logits = model(**batch).logits
        probs = torch.softmax(logits, dim=-1).mean(dim=0)  # average over chunks

    return {
        "positive": probs[label_index["positive"]].item(),
        "negative": probs[label_index["negative"]].item(),
        "neutral": probs[label_index["neutral"]].item(),
    }


def net_tone_score(dist):
    """Reduce FinBERT's 3-class distribution to one scalar: P(positive) -
    P(negative), ignoring the neutral mass.

    This is the standard reduction used for finance-text sentiment scalars
    (the FinBERT-based analog of a Loughran-McDonald net-tone score): it
    ranges from -1 (entirely negative) to +1 (entirely positive), reads
    intuitively, and -- crucially for a distance metric -- differences of
    this scalar are directly interpretable as "how much more positive one
    document is than another." A pure P(positive) scalar would instead
    conflate "genuinely negative" and "hedged/neutral" text into the same
    low score, which would blur exactly the 8-K-vs-10-K contrast (promotional
    vs. legally cautious) this analysis is trying to isolate.
    """
    return dist["positive"] - dist["negative"]


# --- Step 5: compute distances, write output, summarize --------------------

def compute_results(pairs, tokenizer, model, device, label_index):
    results = []
    sentiment_cache = {}  # doc_id -> (dist, scalar); 10-Ks get reused across their matched 8-Ks

    total = len(pairs)
    for i, pair in enumerate(pairs, start=1):
        tenk, eightk = pair["tenk"], pair["eightk"]
        print(f"  [{i}/{total}] {eightk['company']} 8-K {eightk['filing_date']} "
              f"vs 10-K {tenk['filing_date']}")

        if tenk["doc_id"] not in sentiment_cache:
            dist = document_sentiment(tenk["text"], tokenizer, model, device, label_index)
            sentiment_cache[tenk["doc_id"]] = net_tone_score(dist)
        tenk_score = sentiment_cache[tenk["doc_id"]]

        if eightk["doc_id"] not in sentiment_cache:
            dist = document_sentiment(eightk["text"], tokenizer, model, device, label_index)
            sentiment_cache[eightk["doc_id"]] = net_tone_score(dist)
        eightk_score = sentiment_cache[eightk["doc_id"]]

        results.append({
            "company": eightk["company"],
            "ticker": eightk["ticker"],
            "8k_doc_id": eightk["doc_id"],
            "8k_filing_date": eightk["filing_date"].isoformat(),
            "10k_doc_id": tenk["doc_id"],
            "10k_fiscal_year": str(tenk["filing_date"].year),
            "8k_sentiment_score": round(eightk_score, 4),
            "10k_sentiment_score": round(tenk_score, 4),
            "distance": round(eightk_score - tenk_score, 4),
            "8k_url": eightk["url"],
            "10k_url": tenk["url"],
        })
    return results


def write_results(results):
    os.makedirs(EXPORT_DIR, exist_ok=True)
    with open(OUTPUT_PATH, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=OUTPUT_FIELDS)
        writer.writeheader()
        for r in results:
            writer.writerow(r)


def print_summary(results, skipped):
    print(f"\n=== Summary ===")
    print(f"Pairs matched: {len(results)}")
    print(f"8-Ks skipped (no match): {len(skipped)}")
    if skipped:
        reason_counts = defaultdict(int)
        for s in skipped:
            reason_counts[s["reason"]] += 1
        for reason, n in reason_counts.items():
            print(f"  - {n}x: {reason}")

    print(f"\nResults written to {OUTPUT_PATH}")

    print("\n=== Top 5 highest-distance pairs per company ===")
    print("(distance = 8-K net tone minus 10-K net tone; large positive "
          "values mean the press release sounded far more upbeat than the "
          "matched annual report -- the AI-washing signal per the advisor's "
          "hypothesis)")
    by_company = defaultdict(list)
    for r in results:
        by_company[r["company"]].append(r)
    for company, rows in by_company.items():
        print(f"\n  {company}:")
        top5 = sorted(rows, key=lambda r: r["distance"], reverse=True)[:5]
        for r in top5:
            print(f"    distance={r['distance']:+.4f}  8-K {r['8k_filing_date']} "
                  f"(score={r['8k_sentiment_score']:+.4f})  vs  "
                  f"10-K FY{r['10k_fiscal_year']} (score={r['10k_sentiment_score']:+.4f})")


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Compute 8-K vs 10-K sentiment distance (AI-washing proxy)")
    parser.add_argument("--dry-run", action="store_true",
                        help="only run the pairing step and print the preview; skip FinBERT")
    args = parser.parse_args(argv)

    tenk_rows = _load_csv(TENK_PATH)
    eightk_rows = _load_csv(EIGHTK_PATH)
    if not tenk_rows or not eightk_rows:
        return

    tenk_filings = group_filings(tenk_rows)
    eightk_filings = group_filings(eightk_rows)
    print(f"Loaded {len(tenk_filings)} 10-K filings and {len(eightk_filings)} "
          f"8-K filings (after collapsing sections/exhibits).")

    pairs, skipped = build_pairs(tenk_filings, eightk_filings)
    print_pairing_preview(pairs, skipped)

    if args.dry_run:
        print("\n[dry-run] Skipping FinBERT. Re-run without --dry-run once "
              "the pairing above looks right.")
        return

    print("\nLoading FinBERT (ProsusAI/finbert)...")
    tokenizer, model, device, label_index = load_finbert()
    print(f"Running sentiment analysis on {device}...")

    results = compute_results(pairs, tokenizer, model, device, label_index)
    write_results(results)
    print_summary(results, skipped)


if __name__ == "__main__":
    main()
