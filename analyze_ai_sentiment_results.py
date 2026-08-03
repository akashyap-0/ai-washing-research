"""Standalone diagnostic over export/ai_sentiment_distance_results.csv (the
output of extract_ai_sentiment.py). Doesn't modify or re-run the pipeline --
just answers three sanity-check questions before trusting the aggregate
+0.61 distance / 83% net-negative 10-K finding:

  1. Does the aggregate hold up per-company, or is one company (by pair
     count) driving it?
  2. Is the LOW_AI_SENTENCE_COUNT flagging concentrated in one company
     (e.g. Salesforce, which only has 5 8-Ks in this dataset at all)?
  3. Do flagged/low-sentence pairs cluster before ~2023 (before "AI" became
     common press-release/filing language), or are they scattered across
     the whole date range (which would suggest the keyword filter itself
     is missing AI language, not just that AI wasn't discussed yet)?

Run:
    python analyze_ai_sentiment_results.py
"""
import csv
import os
from collections import defaultdict

import config

RESULTS_PATH = os.path.join(config.EXPORT_DIR, "ai_sentiment_distance_results.csv")

TICKER_TO_NAME = {
    "IBM": "IBM",
    "ORCL": "Oracle",
    "DELL": "Dell",
    "CRM": "Salesforce",
    "MSFT": "Microsoft",
    "AMD": "AMD",
    "NVDA": "NVIDIA",
    "VZ": "Verizon",
    "AXP": "Amex",
    "UNH": "UnitedHealth",
}
COMPANY_ORDER = ["IBM", "Oracle", "Dell", "Salesforce",
                 "Microsoft", "AMD", "NVIDIA", "Verizon", "Amex", "UnitedHealth"]


def load_rows():
    with open(RESULTS_PATH, newline="", encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))
    for r in rows:
        r["company_short"] = TICKER_TO_NAME.get(r["ticker"], r["ticker"])
        r["n_ai_sentences_8k"] = int(r["n_ai_sentences_8k"])
        r["n_ai_sentences_10k"] = int(r["n_ai_sentences_10k"])
        r["ai_sentiment_8k"] = float(r["ai_sentiment_8k"]) if r["ai_sentiment_8k"] != "" else None
        r["ai_sentiment_10k"] = float(r["ai_sentiment_10k"]) if r["ai_sentiment_10k"] != "" else None
        r["sentiment_distance"] = float(r["sentiment_distance"]) if r["sentiment_distance"] != "" else None
        r["8k_year"] = r["8k_filing_date"][:4]
    return rows


def mean(values):
    return sum(values) / len(values) if values else None


def print_per_company_sentiment(rows):
    usable = [r for r in rows if r["sentiment_distance"] is not None]
    print("=== 1. Per-company sentiment breakdown (usable pairs only, "
          f"n={len(usable)} of {len(rows)}) ===")
    header = (f"{'Company':<12}{'n':>5}{'mean 10-K':>12}{'mean 8-K':>12}"
              f"{'mean dist':>12}{'% 10-K neg':>12}")
    print(header)
    print("-" * len(header))
    for company in COMPANY_ORDER:
        crows = [r for r in usable if r["company_short"] == company]
        if not crows:
            print(f"{company:<12}{0:>5}{'--':>12}{'--':>12}{'--':>12}{'--':>12}")
            continue
        n = len(crows)
        mean_10k = mean([r["ai_sentiment_10k"] for r in crows])
        mean_8k = mean([r["ai_sentiment_8k"] for r in crows])
        mean_dist = mean([r["sentiment_distance"] for r in crows])
        pct_neg = 100 * sum(1 for r in crows if r["ai_sentiment_10k"] < 0) / n
        print(f"{company:<12}{n:>5}{mean_10k:>+12.4f}{mean_8k:>+12.4f}"
              f"{mean_dist:>+12.4f}{pct_neg:>11.0f}%")
    print(f"{'ALL':<12}{len(usable):>5}{mean([r['ai_sentiment_10k'] for r in usable]):>+12.4f}"
          f"{mean([r['ai_sentiment_8k'] for r in usable]):>+12.4f}"
          f"{mean([r['sentiment_distance'] for r in usable]):>+12.4f}"
          f"{100 * sum(1 for r in usable if r['ai_sentiment_10k'] < 0) / len(usable):>11.0f}%")


def print_per_company_flags(rows):
    print("\n=== 2. Per-company flagged vs. usable pair counts (all pairs) ===")
    header = f"{'Company':<12}{'total':>7}{'usable':>9}{'flagged':>9}{'% flagged':>11}"
    print(header)
    print("-" * len(header))
    for company in COMPANY_ORDER:
        crows = [r for r in rows if r["company_short"] == company]
        total = len(crows)
        flagged = sum(1 for r in crows if r["flag"])
        usable = total - flagged
        pct = 100 * flagged / total if total else 0
        print(f"{company:<12}{total:>7}{usable:>9}{flagged:>9}{pct:>10.0f}%")
    total = len(rows)
    flagged = sum(1 for r in rows if r["flag"])
    print(f"{'ALL':<12}{total:>7}{total - flagged:>9}{flagged:>9}"
          f"{100 * flagged / total:>10.0f}%")


def print_year_breakdown(rows):
    print("\n=== 3. Flagged vs. usable pairs by 8-K filing year ===")
    by_year = defaultdict(lambda: {"usable": 0, "flagged": 0})
    for r in rows:
        bucket = by_year[r["8k_year"]]
        if r["flag"]:
            bucket["flagged"] += 1
        else:
            bucket["usable"] += 1

    header = f"{'Year':<8}{'usable':>9}{'flagged':>9}{'% flagged':>11}"
    print(header)
    print("-" * len(header))
    for year in sorted(by_year):
        counts = by_year[year]
        total = counts["usable"] + counts["flagged"]
        pct = 100 * counts["flagged"] / total if total else 0
        print(f"{year:<8}{counts['usable']:>9}{counts['flagged']:>9}{pct:>10.0f}%")


def main():
    if not os.path.exists(RESULTS_PATH):
        print(f"[error] {RESULTS_PATH} not found. Run extract_ai_sentiment.py first.")
        return
    rows = load_rows()
    print_per_company_sentiment(rows)
    print_per_company_flags(rows)
    print_year_breakdown(rows)


if __name__ == "__main__":
    main()
