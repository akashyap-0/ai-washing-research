"""Prof. Schloetzer's second suggestion: alongside comparing a company's
AI-related language across its 8-K vs. its 10-K (extract_ai_sentiment.py),
also compare *within* a single 10-K whether the AI-related risk-factor
language reads more or less severe than that same document's other risk
language. His framing: does a company present AI as an opportunity-type
risk ("we might fall behind competitors") or an existential one ("our core
business is threatened")? He guessed IBM might read as the former and
Salesforce as the latter, but flagged that as speculation, not a finding.

This reuses, rather than reimplements, everything already built for the
8-K/10-K comparison:
  - extract_ai_sentiment.py's Item 1A extraction/validation
    (group_tenk_risk_factors), its AI_KEYWORD_PATTERN (so AI/non-AI
    classification here can't drift out of sync with the AI-sentence
    extraction already done), its per-sentence FinBERT scorer
    (score_sentences), and its MIN_AI_SENTENCES low-confidence threshold.
  - spotcheck_excluded_sentences.py's get_all_bounded_sentences helper,
    which reuses extract_ai_sentiment.extract_ai_sentences()'s own
    sentence-splitting/word-count-bounds/dedup logic (via a temporary
    match-everything keyword pattern) to get every qualifying sentence in a
    document, not just the AI-matching ones.
  - significance_tests.py's one-sample t-test / Wilcoxon signed-rank
    helpers. A paired test of (ai_tone vs. other_tone) across documents is
    mathematically identical to a one-sample test of their per-document
    difference (within_doc_distance) against 0, so those helpers apply
    directly without modification.

Pipeline:
  1. Take every 10-K with a usable Item 1A section (see
     extract_ai_sentiment.group_tenk_risk_factors). Currently 150 filings
     across 25 companies -- this said "25 10-Ks" back when the sample was
     4 companies, and the unit is one filing, not one company.
  2. Split each into all qualifying sentences, then split those into an
     AI-related subset and a non-AI ("other") subset via AI_KEYWORD_PATTERN.
  3. FinBERT-score both subsets per document, average to a per-subset net
     tone, and take ai_tone minus other_tone as the within-document
     distance. Flag any document where either subset has fewer than
     MIN_AI_SENTENCES (5) sentences.
  4. Write export/ai_vs_other_risk_factors_results.csv.
  5. Test whether within_doc_distance differs from 0, pooled and per
     company, with both a t-test and Wilcoxon (n=118 scored filings of the
     150 -- the other 32 contain no AI sentence at all, so there is no AI
     tone to difference -- and as few as 1 per company, so the
     nonparametric check matters here).

     CAVEAT ON THAT POOLED n: these 118 filings come from only 25 firms and
     are NOT independent (lag-1 within-firm autocorrelation +0.66, ICC 0.48,
     effective n ~= 41). The pooled t-test/Wilcoxon below treat each filing
     as independent and are therefore anticonservative. For between-group
     comparisons use the firm-level permutation test in permutation_test.py,
     which collapses each firm to one value first.

Run:
    python ai_vs_other_risk_factors.py
"""
import csv
import os

import config
import extract_ai_sentiment as ais
import significance_tests as sigt
import spotcheck_excluded_sentences as spot

OUTPUT_PATH = os.path.join(config.EXPORT_DIR, "ai_vs_other_risk_factors_results.csv")

TICKER_SHORT = {
    "IBM": "IBM", "ORCL": "Oracle", "DELL": "Dell", "CRM": "Salesforce",
    "MSFT": "Microsoft", "AMD": "AMD", "NVDA": "NVIDIA",
    "VZ": "Verizon", "AXP": "Amex", "UNH": "UnitedHealth",
    "GOOGL": "Alphabet", "AMZN": "Amazon", "AAPL": "Apple", "META": "Meta",
    "TSLA": "Tesla", "AVGO": "Broadcom", "ACN": "Accenture", "WMT": "Walmart",
    "JPM": "JPMorgan", "LLY": "EliLilly", "DE": "Deere", "SPGI": "S&PGlobal",
    "INTU": "Intuit", "NOW": "ServiceNow", "UBER": "Uber",
}
COMPANY_ORDER = ["IBM", "Oracle", "Dell", "Salesforce",
                 "Microsoft", "AMD", "NVIDIA", "Verizon", "Amex", "UnitedHealth",
                 "Alphabet", "Amazon", "Apple", "Meta", "Tesla", "Broadcom",
                 "Accenture", "Walmart", "JPMorgan", "EliLilly", "Deere",
                 "S&PGlobal", "Intuit", "ServiceNow", "Uber"]

# Filings whose stored Item 1A text is known-bad because of a filer-specific
# section-boundary extraction failure, NOT because of anything about the
# company's actual AI disclosure. Excluded here so a parsing artifact can't
# be read as a substantive finding about the company. This is deliberately a
# suppression list, not a fix: repairing edgar.extract_sections()'s heading
# heuristics is explicitly out of scope for this task.
#
#   ACN  -- every Accenture 10-K anchors on a repeated running page header
#           ("Item 1A. Risk Factors \n25\nclaim that we or our clients are
#           infringing...") instead of the real section heading, yielding an
#           11-20K-char fragment that starts mid-sentence. Real Item 1A
#           sections in this dataset run 40-250K chars. All filings affected.
#   DE   -- Deere's 2014-2018 10-Ks extract only the table-of-contents block
#           (~380-415 chars: "ITEM 1A. RISK FACTORS 11 ITEM 1B. UNRESOLVED
#           STAFF COMMENTS 16 ..."). These are already dropped by
#           MIN_SECTION_CHARS, but they're enumerated here so they get
#           reported as an extraction failure instead of silently vanishing.
#           Deere's 2019+ filings parse correctly and are kept.
# NOW EMPTY: the underlying extract_sections() defect was fixed in edgar.py
# (four separate root causes -- running page headers being picked over the real
# heading, a too-tight separator tolerance between the item number and title,
# line-anchored cross-references masquerading as headings, and same-item
# running headers being treated as section boundaries). After the fix,
# Accenture's 3 filings extract at 92.8-108.4K characters and Deere's 2014-2018
# filings at 38.9-46.6K, all starting at the real heading, so there is nothing
# left to suppress. Walmart, which was never extracting correctly either
# (previously a 48K mid-sentence fragment, now 99-108K), was fixed by the same
# change.
#
# The machinery is kept rather than deleted: it is the right place to quarantine
# any future filer whose text is a parsing artifact rather than a real
# disclosure, and keeping it documents why these companies were once excluded.
KNOWN_EXTRACTION_BUG = {}


def extraction_bug_excluded(ticker, filing_date):
    """True if this filing's Item 1A text is known-unreliable (see
    KNOWN_EXTRACTION_BUG). `filing_date` is a date or ISO string."""
    rule = KNOWN_EXTRACTION_BUG.get(ticker)
    if rule is None:
        return False
    if rule == "ALL":
        return True
    return str(filing_date) in rule

OUTPUT_FIELDS = [
    "company", "ticker", "filing_date", "10k_doc_id",
    "n_ai_sentences", "ai_tone", "n_other_sentences", "other_tone",
    "within_doc_distance", "flag",
]


def classify_sentences(text):
    """Return (ai_sentences, other_sentences): every bounds-passing sentence
    in `text`, split by whether AI_KEYWORD_PATTERN matches it."""
    all_sentences = spot.get_all_bounded_sentences(text)
    ai_sentences, other_sentences = [], []
    for sentence in all_sentences:
        if ais.AI_KEYWORD_PATTERN.search(sentence):
            ai_sentences.append(sentence)
        else:
            other_sentences.append(sentence)
    return ai_sentences, other_sentences


def subset_tone(sentences, tokenizer, model, device, label_index):
    if not sentences:
        return 0, None
    scores = ais.score_sentences(sentences, tokenizer, model, device, label_index)
    return len(sentences), sum(scores) / len(scores)


def compute_results(filings, tokenizer, model, device, label_index):
    results = []
    total = len(filings)
    for i, filing in enumerate(sorted(filings, key=lambda f: (f["company"], f["filing_date"])), start=1):
        print(f"  [{i}/{total}] {filing['company']} 10-K {filing['filing_date']}")

        ai_sentences, other_sentences = classify_sentences(filing["text"])
        n_ai, ai_tone = subset_tone(ai_sentences, tokenizer, model, device, label_index)
        n_other, other_tone = subset_tone(other_sentences, tokenizer, model, device, label_index)

        distance = (ai_tone - other_tone
                    if ai_tone is not None and other_tone is not None else None)
        low_confidence = n_ai < ais.MIN_AI_SENTENCES or n_other < ais.MIN_AI_SENTENCES

        results.append({
            "company": filing["company"],
            "ticker": filing["ticker"],
            "filing_date": filing["filing_date"].isoformat(),
            "10k_doc_id": filing["doc_id"],
            "n_ai_sentences": n_ai,
            "ai_tone": round(ai_tone, 4) if ai_tone is not None else "",
            "n_other_sentences": n_other,
            "other_tone": round(other_tone, 4) if other_tone is not None else "",
            "within_doc_distance": round(distance, 4) if distance is not None else "",
            "flag": "LOW_SENTENCE_COUNT" if low_confidence else "",
        })
    return results


def write_results(results):
    os.makedirs(config.EXPORT_DIR, exist_ok=True)
    with open(OUTPUT_PATH, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=OUTPUT_FIELDS)
        writer.writeheader()
        for r in results:
            writer.writerow(r)


def print_company_summary(results):
    print(f"\n=== Company summary (AI-related vs. other Item 1A risk-factor tone) ===")
    header = (f"{'Company':<12}{'n docs':>8}{'mean ai_tone':>14}"
              f"{'mean other_tone':>17}{'mean distance':>15}")
    print(header)
    print("-" * len(header))
    for c in COMPANY_ORDER:
        rows = [r for r in results if TICKER_SHORT.get(r["ticker"], r["ticker"]) == c
                and r["within_doc_distance"] != ""]
        if not rows:
            print(f"{c:<12}{0:>8}{'--':>14}{'--':>17}{'--':>15}")
            continue
        mean_ai = sum(r["ai_tone"] for r in rows) / len(rows)
        mean_other = sum(r["other_tone"] for r in rows) / len(rows)
        mean_dist = sum(r["within_doc_distance"] for r in rows) / len(rows)
        print(f"{c:<12}{len(rows):>8}{mean_ai:>+14.4f}{mean_other:>+17.4f}{mean_dist:>+15.4f}")
    scored = [r for r in results if r["within_doc_distance"] != ""]
    print(f"{'ALL':<12}{len(scored):>8}"
          f"{sum(r['ai_tone'] for r in scored) / len(scored):>+14.4f}"
          f"{sum(r['other_tone'] for r in scored) / len(scored):>+17.4f}"
          f"{sum(r['within_doc_distance'] for r in scored) / len(scored):>+15.4f}")


def run_stats(results):
    scored = [r for r in results if r["within_doc_distance"] != ""]
    groups = [(c, [r["within_doc_distance"] for r in scored
                   if TICKER_SHORT.get(r["ticker"], r["ticker"]) == c])
              for c in COMPANY_ORDER]
    groups.append(("ALL (pooled)", [r["within_doc_distance"] for r in scored]))
    sigt.print_one_sample_block(
        "within_doc_distance vs. 0 (ai_tone minus other_tone; a paired t-test/"
        "Wilcoxon of ai_tone vs. other_tone is mathematically identical to a "
        "one-sample test of their difference against 0)",
        groups)
    print(f"\n(n<{sigt.SMALL_N_CUTOFF} flagged above -- t-test normality assumption is "
          f"questionable at that sample size; prefer the Wilcoxon result there.)")


def main():
    ais.es.ensure_punkt()

    tenk_rows = ais.sd._load_csv(ais.TENK_PATH)
    if not tenk_rows:
        return
    n_before = len(tenk_rows)
    tenk_rows = [r for r in tenk_rows if r["ticker"] in ais.APPROVED_TICKERS]
    print(f"Filtered to approved companies: {n_before} -> {len(tenk_rows)} 10-K rows.")
    filings, skipped = ais.group_tenk_risk_factors(tenk_rows)
    print(f"Loaded {len(filings)} 10-Ks with a usable Item 1A section "
          f"({len(skipped)} excluded).")

    # Drop filings whose Item 1A text is known-bad from a parsing failure
    # (see KNOWN_EXTRACTION_BUG). Reported separately from every other
    # exclusion reason so a data-quality problem never reads as a finding
    # about the company's AI disclosure.
    bug_excluded = [f for f in filings
                    if extraction_bug_excluded(f["ticker"], f["filing_date"])]
    filings = [f for f in filings
               if not extraction_bug_excluded(f["ticker"], f["filing_date"])]
    # MIN_SECTION_CHARS already dropped some of the same filings upstream;
    # surface those too so the count reconciles.
    skipped_bug = [s for s in skipped
                   if extraction_bug_excluded(s["ticker"], s["filing_date"])]
    if bug_excluded or skipped_bug:
        print(f"\nExcluded for KNOWN EXTRACTION BUG (parsing failure, not a "
              f"company characteristic): {len(bug_excluded)} scored-eligible "
              f"+ {len(skipped_bug)} already dropped upstream")
        for f in sorted(bug_excluded, key=lambda f: (f["ticker"], f["filing_date"])):
            print(f"    {TICKER_SHORT.get(f['ticker'], f['ticker']):<12} "
                  f"{f['filing_date']}  ({len(f['text'])} chars) "
                  f"-- section-boundary anchoring failure")
        for s in sorted(skipped_bug, key=lambda s: (s["ticker"], s["filing_date"])):
            print(f"    {TICKER_SHORT.get(s['ticker'], s['ticker']):<12} "
                  f"{s['filing_date']}  -- {s['reason']}")

    print("\nLoading FinBERT (ProsusAI/finbert)...")
    tokenizer, model, device, label_index = ais.sd.load_finbert()
    print(f"Running sentiment analysis on {device}...")

    results = compute_results(filings, tokenizer, model, device, label_index)
    write_results(results)
    print_company_summary(results)
    run_stats(results)
    print(f"\nResults written to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
