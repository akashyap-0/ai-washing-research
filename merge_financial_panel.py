"""Validate and merge company-period text scores with structured financials.

The financial file must contain `period_id` matching the text-score file and
must be unique at that key. This deliberately refuses to infer a fiscal year
from the 10-K filing year. Add the actual SEC report period to the financial
crosswalk, then construct period_id as TICKER:anchor_10k_filing_date for the
current exports (future manifests will use CIK and period_end directly).
"""

import argparse
import csv
import os
from collections import Counter


def load(path):
    with open(path, newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def unique_index(rows, key, name):
    counts = Counter(row.get(key, "") for row in rows)
    missing = counts.get("", 0)
    duplicates = [value for value, count in counts.items() if value and count > 1]
    if missing or duplicates:
        raise ValueError(
            f"{name} must be unique and nonblank on {key}; "
            f"missing={missing}, duplicate_keys={duplicates[:10]}")
    return {row[key]: row for row in rows}


def merge(text_rows, financial_rows):
    text = unique_index(text_rows, "period_id", "text scores")
    financial = unique_index(financial_rows, "period_id", "financial data")
    financial_fields = list(financial_rows[0]) if financial_rows else []
    overlap = (set(text_rows[0]) & set(financial_fields)) - {"period_id"}
    if overlap:
        raise ValueError(f"Rename overlapping financial columns before merge: {sorted(overlap)}")

    output = []
    for period_id, text_row in text.items():
        if period_id not in financial:
            continue
        output.append({**text_row, **financial[period_id]})
    return output, sorted(set(text) - set(financial)), sorted(set(financial) - set(text))


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--text-scores", default="derived/company_period_text_scores.csv")
    parser.add_argument("--financials", required=True)
    parser.add_argument("--output", default="derived/analysis_panel.csv")
    args = parser.parse_args(argv)

    rows, text_only, financial_only = merge(load(args.text_scores), load(args.financials))
    if not rows:
        raise ValueError("Merge produced zero rows; verify period_id construction")
    fields = list(rows[0])
    os.makedirs(os.path.dirname(args.output) or ".", exist_ok=True)
    with open(args.output, "w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    print(f"Merged {len(rows):,} rows -> {args.output}")
    print(f"Unmatched text periods: {len(text_only):,}")
    print(f"Unmatched financial periods: {len(financial_only):,}")


if __name__ == "__main__":
    main()
