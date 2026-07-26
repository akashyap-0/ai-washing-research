"""Diagnostic spot-check for extract_ai_sentiment.py's AI_KEYWORD_PATTERN.

The pipeline's diagnostic breakdown (see analyze_ai_sentiment_results.py)
showed 2024 and 2025 10-K/8-K pairs still get flagged for too few AI
sentences 59% and 32% of the time, even though these are the most
AI-saturated years -- suggesting the keyword filter may be missing genuine
AI-related sentences rather than AI genuinely being under-discussed.

This script re-splits each 2024/2025 10-K's Item 1A Risk Factors section
into sentences, reusing extract_ai_sentiment.py's own sentence-splitting and
AI_KEYWORD_PATTERN (imported, not retyped, so it can't drift out of sync),
and prints sentences that:
  (a) do NOT match the current, strict AI_KEYWORD_PATTERN, but
  (b) DO match a deliberately wider, looser "candidate" pattern (product
      names, "powered", "assistant", "model", etc.)
so a human can read through them and judge whether they're genuine misses
worth adding to the real filter, or false positives the wider net just
happens to catch.

This is read-only: no sentiment scoring, no CSV output, console only. Does
not modify extract_ai_sentiment.py.

Run:
    python spotcheck_excluded_sentences.py
"""
import os
import re
from collections import Counter, defaultdict

import config
import extract_ai_sentiment as ais

TENK_PATH = os.path.join(config.EXPORT_DIR, "ai_washing_10-K.csv")
TARGET_YEARS = {2024, 2025}
TRUNCATE_CHARS = 200

TICKER_SHORT = {"IBM": "IBM", "ORCL": "Oracle", "DELL": "Dell", "CRM": "Salesforce"}

# Deliberately wide net for surfacing human-review candidates -- not a
# proposed replacement for AI_KEYWORD_PATTERN. Terms per the review request,
# plus a few company-specific AI product names that wouldn't otherwise
# contain "AI"/"automat"/etc. and so would never hit the strict pattern.
LOOSE_TERMS = [
    "powered", "automation", r"automat\w*", "copilot", "einstein", "watsonx",
    "gemini", "assistant", r"algorithm\w*", "model", "chatbot", "generative",
    "cognitive",
]
COMPANY_EXTRA_TERMS = {
    "IBM": ["watson"],
    "Oracle": ["oci ai", "fusion ai"],
    "Dell": ["ai factory", "apex ai"],
    "Salesforce": ["agentforce"],
}


def build_loose_pattern(company_short):
    terms = LOOSE_TERMS + COMPANY_EXTRA_TERMS.get(company_short, [])
    return re.compile(r"\b(" + "|".join(terms) + r")\b", re.IGNORECASE)


# extract_ai_sentiment.extract_ai_sentences() bundles sentence-splitting,
# word-count bounds, dedup, AND the strict AI-keyword filter into one
# function. To reuse the splitting/bounds/dedup logic without reimplementing
# it, and without touching the AI-keyword filter itself, temporarily swap in
# a match-everything pattern so every bounds-passing sentence comes back,
# then restore the real pattern immediately after.
_MATCH_ANYTHING = re.compile(r".")


def get_all_bounded_sentences(text):
    original_pattern = ais.AI_KEYWORD_PATTERN
    ais.AI_KEYWORD_PATTERN = _MATCH_ANYTHING
    try:
        return ais.extract_ai_sentences(text)
    finally:
        ais.AI_KEYWORD_PATTERN = original_pattern


def truncate(sentence):
    if len(sentence) <= TRUNCATE_CHARS:
        return sentence
    return sentence[:TRUNCATE_CHARS].rstrip() + "..."


def main():
    ais.es.ensure_punkt()

    tenk_rows = ais.sd._load_csv(TENK_PATH)
    if not tenk_rows:
        return

    filings, skipped = ais.group_tenk_risk_factors(tenk_rows)
    target_filings = [f for f in filings if f["filing_date"].year in TARGET_YEARS]
    print(f"Loaded {len(filings)} 10-Ks with a usable Item 1A section; "
          f"{len(target_filings)} fall in {sorted(TARGET_YEARS)}.")
    skipped_in_range = [s for s in skipped
                         if s["filing_date"][:4] in {str(y) for y in TARGET_YEARS}]
    if skipped_in_range:
        print(f"({len(skipped_in_range)} 2024/2025 10-Ks excluded for missing/"
              f"too-short Item 1A -- not spot-checked here.)")

    # (company_short, year) -> list of (sentence, matched_loose_terms)
    candidates = defaultdict(list)
    term_counts = Counter()

    for filing in sorted(target_filings, key=lambda f: (f["company"], f["filing_date"])):
        company_short = TICKER_SHORT.get(filing["ticker"], filing["ticker"])
        loose_pattern = build_loose_pattern(company_short)
        year = filing["filing_date"].year

        for sentence in get_all_bounded_sentences(filing["text"]):
            if ais.AI_KEYWORD_PATTERN.search(sentence):
                continue  # already caught by the real filter, not a "miss"
            matches = [m.lower() for m in loose_pattern.findall(sentence)]
            if not matches:
                continue
            candidates[(company_short, year)].append((sentence, matches))
            term_counts.update(set(matches))

    total_candidates = sum(len(v) for v in candidates.values())
    print(f"\n=== Candidate sentences missed by AI_KEYWORD_PATTERN but caught "
          f"by the wider net ({total_candidates} total) ===")

    for (company_short, year), sentences in sorted(candidates.items()):
        print(f"\n--- {company_short} FY{year} 10-K Item 1A "
              f"({len(sentences)} candidate sentence(s)) ---")
        for sentence, matches in sentences:
            unique_terms = ", ".join(sorted(set(matches)))
            print(f"  [{unique_terms}] {truncate(sentence)}")

    if not candidates:
        print("\nNone found -- the strict filter and the wider net agree on "
              "every 2024/2025 Item 1A sentence.")
        return

    print(f"\n=== Missed-term frequency across all {total_candidates} candidates ===")
    for term, n in term_counts.most_common():
        print(f"  {term:<15}{n}")


if __name__ == "__main__":
    main()
