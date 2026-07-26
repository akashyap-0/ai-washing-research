"""Read-only qualitative diagnostic: print every AI-related sentence from
Oracle's Item 1A Risk Factors section across all 11 of its 10-Ks in
export/ai_washing_10-K.csv, grouped by filing year.

Context: ai_vs_other_risk_factors.py found Oracle's AI-related risk-factor
sentences read notably more negative than its other risk factors
(ai_tone -0.57 vs other_tone -0.33), the only company trending toward an
"AI is existential" framing, but the difference wasn't statistically
significant (n=11). This script doesn't run any stats -- it just lets a
human read the actual sentences behind that number to see whether the
negative tone comes from a few strong "AI threatens our core business"
statements or from scattered generic risk-factor boilerplate that happens
to score negative, and whether the framing has visibly shifted between
Oracle's earliest (2016) and latest (2026) 10-Ks in this dataset.

Reuses extract_ai_sentiment.py's Item 1A extraction/validation
(group_tenk_risk_factors) and its AI_KEYWORD_PATTERN-driven sentence
extraction (extract_ai_sentences) directly, so the sentences shown here are
guaranteed to be exactly the same set FinBERT was scored on -- nothing here
is reimplemented or re-derived by hand.

Console output only. Doesn't modify or re-run any existing script.

Run:
    python oracle_ai_risk_sentences.py
"""
import extract_ai_sentiment as ais

TRUNCATE_CHARS = 250
ORACLE_TICKER = "ORCL"


def truncate(sentence):
    if len(sentence) <= TRUNCATE_CHARS:
        return sentence
    return sentence[:TRUNCATE_CHARS].rstrip() + "..."


def main():
    ais.es.ensure_punkt()

    tenk_rows = ais.sd._load_csv(ais.TENK_PATH)
    if not tenk_rows:
        return
    filings, skipped = ais.group_tenk_risk_factors(tenk_rows)
    oracle_filings = [f for f in filings if f["ticker"] == ORACLE_TICKER]
    print(f"Found {len(oracle_filings)} Oracle 10-Ks with a usable Item 1A section.\n")

    total_sentences = 0
    for filing in sorted(oracle_filings, key=lambda f: f["filing_date"]):
        sentences = ais.extract_ai_sentences(filing["text"])
        total_sentences += len(sentences)
        year = filing["filing_date"].year
        print(f"--- Oracle FY{year} 10-K (filed {filing['filing_date']}) "
              f"-- {len(sentences)} AI-related sentence(s) ---")
        if not sentences:
            print("  (none)")
        for s in sentences:
            print(f"  {truncate(s)}")
        print()

    print(f"=== Total AI-related Item 1A sentences across all Oracle 10-Ks: "
          f"{total_sentences} ===")


if __name__ == "__main__":
    main()
