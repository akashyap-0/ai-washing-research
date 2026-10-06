"""Diagnostic spot-check, requested before finalizing results: for Verizon,
American Express, and UnitedHealth -- the three AI-peripheral companies
whose 8-Ks produced ~0 usable pairs in extract_ai_sentiment.py -- is that a
genuine "these companies don't talk about AI in press releases" finding, or
a keyword-filter gap like the Agentforce/watsonx miss spotcheck_excluded_
sentences.py caught for the original 4 companies?

Mirrors that script's method exactly, just applied to 8-K filings (not 10-K
Item 1A) for these three tickers: reuse extract_ai_sentiment.py's own
sentence-splitting/word-count-bounds/dedup logic (via a temporary
match-everything keyword pattern, same trick spotcheck_excluded_sentences.py
uses) to get every qualifying sentence per 8-K, then flag sentences that (a)
don't match the current strict AI_KEYWORD_PATTERN but (b) do match a
deliberately wider net (generic AI/automation/digital-assistant terms, plus
company-specific product names found by scanning each company's own text for
capitalized terms sitting near automation/AI/digital language).

Read-only: no CSV output, does not modify AI_KEYWORD_PATTERN or any
production file. Also prints per-filing sentence/char counts as a sanity
check on whether "~0 AI sentences" reflects genuinely sparse documents.

Run:
    python spotcheck_8k_ai_gap.py
"""
import os
import re
from collections import Counter, defaultdict

import config
import extract_ai_sentiment as ais
import sentiment_distance as sd
import spotcheck_excluded_sentences as spot

EIGHTK_PATH = os.path.join(config.EXPORT_DIR, "ai_washing_8-K.csv")
TARGET_TICKERS = {"VZ", "AXP", "UNH"}
TRUNCATE_CHARS = 220

# Same generic candidate terms spotcheck_excluded_sentences.py used for the
# original 4 companies, so this is an apples-to-apples wider net rather than
# a differently-tuned one.
LOOSE_TERMS = [
    "powered", r"-powered", "automation", r"automat\w*", "copilot",
    "gemini", "assistant", "digital assistant", r"algorithm\w*", "model",
    "chatbot", "generative", "cognitive",
]

# Company-specific product-name candidates: found by first scanning each
# company's own 8-K text (see find_capitalized_candidates below) for
# capitalized terms sitting near automation/AI/digital language, then
# hand-picking the ones that look like a real named initiative rather than a
# generic capitalized word (a person's name, a state, "Inc.", etc.).
COMPANY_EXTRA_TERMS = {
    "VZ": [],
    "AXP": [],
    "UNH": [],
}


def build_loose_pattern(ticker):
    terms = LOOSE_TERMS + COMPANY_EXTRA_TERMS.get(ticker, [])
    return re.compile(r"\b(" + "|".join(terms) + r")\b", re.IGNORECASE)


def load_target_filings():
    rows = sd._load_csv(EIGHTK_PATH)
    rows = [r for r in rows if r["ticker"] in TARGET_TICKERS]
    filings = sd.group_filings(rows)
    by_ticker = defaultdict(list)
    for f in filings:
        by_ticker[f["ticker"]].append(f)
    for ticker in by_ticker:
        by_ticker[ticker].sort(key=lambda f: f["filing_date"])
    return by_ticker


# --- part 0: capitalized-term scan, to surface candidate product names -----

# Words capitalized terms need to sit near to be worth a look -- generic
# tech/automation/digital vocabulary, not AI-specific (that's the point:
# these are the words a branded product name would plausibly appear next to
# even if the sentence itself doesn't say "AI").
_NEAR_WORDS = re.compile(
    r"\b(automat\w*|digital|platform|technology|tool\w*|intelligent|"
    r"virtual|smart|assistant|insight\w*|analytics|data-driven|algorithm\w*)\b",
    re.IGNORECASE,
)
# A capitalized "product-name-shaped" span: 1-3 Title-Case words, or an
# all-caps acronym of 2-6 letters, not at the very start of a sentence
# (to cut down on ordinary sentence-initial capitalization).
_CAP_SPAN = re.compile(
    r"\b([A-Z][a-zA-Z]+(?:\s+[A-Z][a-zA-Z]+){0,2}|[A-Z]{2,6})\b"
)
_COMMON_NOISE = {
    "The", "This", "That", "These", "Those", "We", "Our", "In", "On", "At",
    "For", "With", "As", "It", "Its", "A", "An", "And", "Or", "But", "If",
    "Item", "Inc", "Corp", "Company", "Verizon", "American Express", "Amex",
    "UnitedHealth", "UnitedHealth Group", "Optum", "United States", "U.S.",
    "New York", "SEC", "GAAP", "Q1", "Q2", "Q3", "Q4", "CEO", "CFO", "EPS",
    "Non", "Note", "Notes", "Table", "Contents", "See", "Please",
}


def find_capitalized_candidates(filings):
    """Return Counter of capitalized spans found within ~60 chars of a
    _NEAR_WORDS hit, across all sentences in `filings` -- candidates for a
    company-specific product name worth adding to COMPANY_EXTRA_TERMS."""
    counts = Counter()
    for f in filings:
        for sentence in spot.get_all_bounded_sentences(f["text"]):
            for m in _NEAR_WORDS.finditer(sentence):
                window = sentence[max(0, m.start() - 60): m.end() + 60]
                for cm in _CAP_SPAN.finditer(window):
                    span = cm.group(1)
                    if span in _COMMON_NOISE or len(span) < 3:
                        continue
                    counts[span] += 1
    return counts


# --- part 1: candidate sentences the strict filter misses but the wide net catches --

def spotcheck_ticker(ticker, filings):
    print(f"\n{'=' * 90}")
    print(f"{ticker}: {len(filings)} 8-K filings")
    print(f"{'=' * 90}")

    total_sentences = 0
    total_chars = 0
    n_strict_ai = 0
    candidates = []  # (filing_date, sentence, matched_terms)

    loose_pattern = build_loose_pattern(ticker)

    for f in filings:
        all_sentences = spot.get_all_bounded_sentences(f["text"])
        total_sentences += len(all_sentences)
        total_chars += len(f["text"])
        strict_hits = [s for s in all_sentences if ais.AI_KEYWORD_PATTERN.search(s)]
        n_strict_ai += len(strict_hits)

        for sentence in all_sentences:
            if ais.AI_KEYWORD_PATTERN.search(sentence):
                continue  # already caught by the real filter
            matches = [m.lower() for m in loose_pattern.findall(sentence)]
            if not matches:
                continue
            candidates.append((f["filing_date"], sentence, matches))

    print(f"\n-- Sanity check: volume --")
    print(f"  total bounds-passing sentences across all filings: {total_sentences}")
    print(f"  total characters across all filings:               {total_chars}")
    print(f"  sentences matching CURRENT AI_KEYWORD_PATTERN:      {n_strict_ai}")

    print(f"\n-- Capitalized-term scan (candidates for a company-specific product name) --")
    cap_counts = find_capitalized_candidates(filings)
    if cap_counts:
        for term, n in cap_counts.most_common(15):
            print(f"  {term:<30}{n}")
    else:
        print("  (none found)")

    print(f"\n-- Candidate sentences missed by AI_KEYWORD_PATTERN but caught by the wider net "
          f"({len(candidates)} total) --")
    if not candidates:
        print("  None. The strict filter and the wider net agree on every 8-K sentence for "
              f"{ticker} -- no evidence of a keyword-gap artifact here.")
        return

    for filing_date, sentence, matches in sorted(candidates):
        unique_terms = ", ".join(sorted(set(matches)))
        truncated = sentence if len(sentence) <= TRUNCATE_CHARS else sentence[:TRUNCATE_CHARS].rstrip() + "..."
        print(f"  [{filing_date}] [{unique_terms}] {truncated}")


def main():
    ais.es.ensure_punkt()
    by_ticker = load_target_filings()
    for ticker in sorted(TARGET_TICKERS):
        filings = by_ticker.get(ticker, [])
        if not filings:
            print(f"\n{ticker}: no 8-K filings found in {EIGHTK_PATH}")
            continue
        spotcheck_ticker(ticker, filings)


if __name__ == "__main__":
    main()
