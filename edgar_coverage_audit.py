"""How far back does EDGAR actually go for each firm, and how much of that did
this project ever pull?

WHY
---
The AI-centrality result (permutation_test.py GROUPING 1) is the paper's
headline, and it is fragile under the thin-evidence filter for one reason:
too few filings survive per firm. Oracle drops 11 -> 3 and IBM 7 -> 2 once
filings with fewer than extract_ai_sentiment.MIN_AI_SENTENCES scoreable AI
sentences are excluded. With 5 firms a side, that is a very small amount of
evidence holding up the comparison.

The legitimate fix is more real filings, not a looser threshold. This script
answers the prerequisite question: are there more filings to get? For each of
the ten firms in AI_CENTRALITY it compares

    what EDGAR holds   (submissions API, full history via edgar.all_filings)
    what we pulled     (distinct filing_date per ticker in the 10-K export)

and prints the gap, oldest-first, so the backfill in
edgar_backfill_10k.py has an explicit target list rather than a guess.

WHAT IT DOES *NOT* DO
---------------------
It does not judge whether an un-pulled filing is worth pulling. A 1996 10-K
almost certainly contains no AI language and will score as thin evidence
regardless -- but that is a finding to report per company, not a reason to
quietly leave it out of the count here. The audit reports availability; the
scoring pipeline decides usability.

Forms: "10-K" plus the historical variants EDGAR files separately. 10-K405
(a pre-2003 checkbox variant) and 10-KSB (small business) are counted and
labelled, since ignoring them would understate how far back a company's
annual-report history runs. Amendments (10-K/A) are NOT counted: they restate
part of an already-counted filing rather than adding a period.

Read-only. Hits public SEC endpoints only. Requires SEC_USER_AGENT.

Run:
    python edgar_coverage_audit.py
"""
import csv
import os
import sys
from collections import defaultdict

import config
import edgar
import firm_characteristics_test as fct

TENK_EXPORT = os.path.join(config.EXPORT_DIR, "ai_washing_10-K.csv")

# Annual-report forms that represent a distinct fiscal period.
ANNUAL_FORMS = ("10-K", "10-K405", "10-KSB")

# The ten firms whose per-firm filing counts are the binding constraint.
SHORT_TO_TICKER = {short: tic for tic, short in fct.TICKER_SHORT.items()}
TARGET_SHORTS = sorted(set(fct.AI_CENTRALITY["AI-core"])
                       | set(fct.AI_CENTRALITY["AI-peripheral"]))


def pulled_dates_by_ticker(path=TENK_EXPORT):
    """ticker -> set of filing_date strings already in the 10-K export."""
    if not os.path.exists(path):
        print(f"[error] {path} not found; nothing to compare against.")
        return {}
    # Item 1A bodies blow past csv's default 128 KB field cap.
    csv.field_size_limit(min(sys.maxsize, 2 ** 31 - 1))
    out = defaultdict(set)
    with open(path, newline="", encoding="utf-8-sig") as f:
        for row in csv.DictReader(f):
            out[row["ticker"]].add(row["filing_date"])
    return out


def edgar_annual_filings(ticker):
    """Every annual report EDGAR holds for `ticker`, oldest first."""
    cik = edgar.resolve_ticker(ticker)
    if not cik:
        return None, []
    filings = edgar.all_filings(cik, forms=ANNUAL_FORMS)
    return cik, filings


def audit():
    if not config.SEC_USER_AGENT:
        print("[error] SEC_USER_AGENT is not set. SEC blocks unidentified "
              "clients. Set it to 'Your Name your@email.com' and re-run.")
        return []

    pulled = pulled_dates_by_ticker()
    rows = []

    header = (f"{'firm':<14}{'ticker':<8}{'EDGAR n':>9}{'EDGAR earliest':>16}"
              f"{'pulled n':>10}{'pulled earliest':>17}{'missing':>9}")
    print("=" * len(header))
    print("EDGAR 10-K AVAILABILITY vs. WHAT THIS PROJECT PULLED")
    print("=" * len(header))
    print(header)
    print("-" * len(header))

    for short in TARGET_SHORTS:
        ticker = SHORT_TO_TICKER.get(short, short)
        cik, filings = edgar_annual_filings(ticker)
        if cik is None:
            print(f"{short:<14}{ticker:<8}{'CIK resolve failed':>60}")
            continue
        have = pulled.get(ticker, set())
        missing = [f for f in filings if f["filing_date"] not in have]
        rows.append({
            "firm": short, "ticker": ticker, "cik": cik,
            "edgar_n": len(filings),
            "edgar_earliest": filings[0]["filing_date"] if filings else "",
            "pulled_n": len(have),
            "pulled_earliest": min(have) if have else "",
            "missing_n": len(missing),
            "missing_dates": ";".join(f["filing_date"] for f in missing),
            "filings": filings,
        })
        print(f"{short:<14}{ticker:<8}{len(filings):>9}"
              f"{(filings[0]['filing_date'] if filings else '--'):>16}"
              f"{len(have):>10}{(min(have) if have else '--'):>17}"
              f"{len(missing):>9}")

    print("\n" + "=" * len(header))
    print("MISSING FILINGS, oldest first (candidates for backfill)")
    print("=" * len(header))
    for r in rows:
        if not r["missing_n"]:
            print(f"\n{r['firm']} ({r['ticker']}): nothing missing -- the "
                  f"export already has every annual report EDGAR holds.")
            continue
        print(f"\n{r['firm']} ({r['ticker']}): {r['missing_n']} missing of "
              f"{r['edgar_n']} on EDGAR")
        for f in r["filings"]:
            if f["filing_date"] in pulled.get(r["ticker"], set()):
                continue
            print(f"    {f['filing_date']}  {f['form']:<8} "
                  f"period={f['period_end'] or '?':<12} {f['accession']}")

    return rows


def write_csv(rows, path=None):
    path = path or os.path.join(config.EXPORT_DIR, "edgar_coverage_audit.csv")
    if not rows:
        return None
    fields = ["firm", "ticker", "cik", "edgar_n", "edgar_earliest",
              "pulled_n", "pulled_earliest", "missing_n", "missing_dates"]
    os.makedirs(config.EXPORT_DIR, exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for r in rows:
            w.writerow({k: r[k] for k in fields})
    print(f"\nWritten to {path}")
    return path


def main():
    rows = audit()
    write_csv(rows)


if __name__ == "__main__":
    main()
