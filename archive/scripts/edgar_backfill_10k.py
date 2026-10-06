"""Backfill the historical 10-Ks the AI-centrality firms have on EDGAR but
this project never pulled.

WHY
---
permutation_test.py GROUPING 1 (AI-core vs. AI-peripheral) is the paper's
pre-specified headline, and it is thin: 5 firms a side, and once filings with
fewer than extract_ai_sentiment.MIN_AI_SENTENCES scoreable AI sentences are
excluded, Oracle falls 11 -> 3 filings and IBM 7 -> 2. The fix for that is more
real filings, NOT a lower evidence threshold -- lowering the threshold would
reintroduce exactly the thin-evidence problem the strict filter exists to
catch. edgar_coverage_audit.py showed the headroom is real: these ten firms
have 215 annual reports on EDGAR that were never pulled.

WHAT IT ACTUALLY PULLS, AND THE HARD FLOOR AT 2006
--------------------------------------------------
Not all 215. "Item 1A Risk Factors" did not exist as a required 10-K item
until the SEC's 2005 disclosure overhaul, which applied to fiscal years ending
on or after 2005-12-01 (Securities Act Release 33-8591). Every 10-K filed
before roughly calendar 2006 therefore has NO Item 1A section to extract --
not "an Item 1A with no AI in it", but no such item at all. The entire
measurement chain here (extract_ai_sentiment.group_tenk_risk_factors ->
ai_vs_other_risk_factors.classify_sentences -> within_doc_distance) is defined
on Item 1A, so those filings cannot produce a data point by construction.

That is a fact about the form, not a judgment about the content, so this
script draws the line there and says so per company rather than silently
skipping. Of the 215 un-pulled filings, 136 are from 2006 on and are what this
script attempts. The remaining 79 are pre-Item-1A and are reported as
structurally unavailable.

Filings from 2006-2015 will mostly still score as thin evidence, because they
predate meaningful AI risk-factor disclosure -- but that is the scoring
pipeline's call to make on real text, not this script's to make in advance.
They are pulled and scored like everything else.

HOW IT STAYS CONSISTENT WITH THE EXISTING SAMPLE
------------------------------------------------
It reuses main.collect_for_company's exact path -- edgar.fetch_filing_text,
edgar.extract_sections with the same four 10-K sections, normalize.
from_edgar_section, storage.Dataset.save_document -- so backfilled rows are
indistinguishable in schema and provenance from the originals. Dataset dedups
on doc_id, so re-running is safe and will not duplicate a filing.

Downstream is unchanged and must be re-run afterwards:
    python ai_vs_other_risk_factors.py
    python risk_factor_composition.py
    python permutation_test.py

Requires SEC_USER_AGENT. Writes export/ai_washing_10-K.{csv,json}.

Run:
    python edgar_backfill_10k.py             # the ten AI-centrality firms
    python edgar_backfill_10k.py --dry-run   # list what would be pulled
"""
import argparse

import config
import edgar
import normalize
import storage
from edgar_coverage_audit import (ANNUAL_FORMS, SHORT_TO_TICKER, TARGET_SHORTS,
                                  pulled_dates_by_ticker)

# Item 1A Risk Factors became a required 10-K item for fiscal years ending on
# or after 2005-12-01. Filings before this have no Item 1A to extract at all.
ITEM_1A_ERA_START = "2006-01-01"

# Same four sections main.py pulls for a 10-K, so backfilled rows match.
TENK_SECTIONS = ("Item 1 Business", "Item 1A Risk Factors",
                 "Item 7 MD&A", "Item 8 Financial Statements")


def missing_filings(ticker, already_pulled):
    """(pre_item1a, pullable) split of this ticker's un-pulled annual reports."""
    cik = edgar.resolve_ticker(ticker)
    if not cik:
        return None, [], []
    filings = edgar.all_filings(cik, forms=ANNUAL_FORMS)
    missing = [f for f in filings if f["filing_date"] not in already_pulled]
    pre = [f for f in missing if f["filing_date"] < ITEM_1A_ERA_START]
    pullable = [f for f in missing if f["filing_date"] >= ITEM_1A_ERA_START]
    return cik, pre, pullable


def backfill_company(short, ticker, already_pulled, dataset, dry_run=False):
    """Pull every Item-1A-era annual report we don't already have. Returns a
    per-company summary dict."""
    cik, pre, pullable = missing_filings(ticker, already_pulled)
    summary = {
        "firm": short, "ticker": ticker, "cik": cik,
        "n_pre_item1a": len(pre), "n_pullable": len(pullable),
        "n_fetched": 0, "n_new_rows": 0, "n_with_item1a": 0,
        "no_item1a": [], "errors": [],
    }
    if cik is None:
        summary["errors"].append("CIK resolve failed")
        return summary

    print(f"\n{short} ({ticker}): {len(pullable)} to pull, "
          f"{len(pre)} pre-Item-1A (unavailable by construction)")
    if dry_run:
        for f in pullable:
            print(f"    would pull {f['filing_date']}  {f['form']:<8} "
                  f"{f['accession']}")
        return summary

    for i, filing in enumerate(pullable, start=1):
        label = f"{filing['filing_date']} {filing['form']}"
        try:
            text = edgar.fetch_filing_text(filing["url"])
        except Exception as e:
            print(f"    [{i}/{len(pullable)}] {label}: FETCH FAILED ({e})")
            summary["errors"].append(f"{filing['filing_date']}: fetch: {e}")
            continue
        summary["n_fetched"] += 1

        try:
            sections = edgar.extract_sections(text, sections=TENK_SECTIONS)
        except Exception as e:
            print(f"    [{i}/{len(pullable)}] {label}: PARSE FAILED ({e})")
            summary["errors"].append(f"{filing['filing_date']}: parse: {e}")
            continue

        company = filing.get("company") or short
        new_rows = 0
        for section_label, section_text in sections.items():
            if not section_text:
                continue
            doc = normalize.from_edgar_section(
                company, ticker, filing, section_label, section_text)
            _, is_new = dataset.save_document(doc)
            new_rows += int(is_new)
        summary["n_new_rows"] += new_rows

        item1a = sections.get("Item 1A Risk Factors") or ""
        if item1a.strip():
            summary["n_with_item1a"] += 1
        else:
            summary["no_item1a"].append(filing["filing_date"])
        print(f"    [{i}/{len(pullable)}] {label}: {new_rows} new rows, "
              f"Item 1A {'found' if item1a.strip() else 'NOT FOUND'} "
              f"({len(item1a):,} chars)")

    return summary


def print_report(summaries, dry_run=False):
    print("\n" + "=" * 92)
    print("BACKFILL SUMMARY")
    print("=" * 92)
    hdr = (f"{'firm':<14}{'pullable':>10}{'fetched':>9}{'w/ Item 1A':>12}"
           f"{'new rows':>10}{'pre-2006':>10}{'errors':>8}")
    print(hdr)
    print("-" * len(hdr))
    for s in summaries:
        print(f"{s['firm']:<14}{s['n_pullable']:>10}{s['n_fetched']:>9}"
              f"{s['n_with_item1a']:>12}{s['n_new_rows']:>10}"
              f"{s['n_pre_item1a']:>10}{len(s['errors']):>8}")

    print("\nPER-COMPANY NOTES")
    print("-" * 92)
    for s in summaries:
        bits = []
        if s["n_pullable"] == 0:
            bits.append("no Item-1A-era filings were missing; the export "
                        "already had every one EDGAR holds")
        if s["n_pre_item1a"]:
            bits.append(f"{s['n_pre_item1a']} older annual reports exist on "
                        f"EDGAR but predate Item 1A (fiscal years ending "
                        f"before 2005-12-01), so they cannot yield a risk-"
                        f"factor observation at all")
        if s["no_item1a"]:
            bits.append(f"Item 1A not extractable from {len(s['no_item1a'])} "
                        f"filing(s): {', '.join(s['no_item1a'])}")
        if s["errors"]:
            bits.append(f"{len(s['errors'])} error(s): "
                        f"{'; '.join(s['errors'][:3])}")
        if not bits:
            bits.append(f"{s['n_pullable']} Item-1A-era filings available to "
                        f"pull" if dry_run else
                        f"{s['n_with_item1a']} of {s['n_pullable']} pulled "
                        f"filings yielded an Item 1A section")
        print(f"  {s['firm']} ({s['ticker']}): {'; '.join(bits)}.")


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--dry-run", action="store_true",
                    help="list what would be pulled, fetch nothing")
    ap.add_argument("--companies", default="",
                    help="comma-separated short names (default: all ten "
                         "AI-centrality firms)")
    args = ap.parse_args()

    if not config.SEC_USER_AGENT:
        print("[error] SEC_USER_AGENT is not set. SEC blocks unidentified "
              "clients. Set it to 'Your Name your@email.com' and re-run.")
        return

    shorts = ([s.strip() for s in args.companies.split(",") if s.strip()]
              or TARGET_SHORTS)
    pulled = pulled_dates_by_ticker()
    dataset = storage.Dataset()

    summaries = []
    for short in shorts:
        ticker = SHORT_TO_TICKER.get(short, short)
        summaries.append(backfill_company(
            short, ticker, pulled.get(ticker, set()), dataset,
            dry_run=args.dry_run))

    print_report(summaries, dry_run=args.dry_run)

    if args.dry_run:
        print("\n(dry run -- nothing written)")
        return

    results = dataset.export()
    for group, (csv_path, _json_path, n) in sorted(results.items()):
        print(f"\nWrote {group}: {n} documents -> {csv_path}")
    print("\nNow re-run, in order:")
    print("    python ai_vs_other_risk_factors.py")
    print("    python risk_factor_composition.py")
    print("    python permutation_test.py")


if __name__ == "__main__":
    main()
