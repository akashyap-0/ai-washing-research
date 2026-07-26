"""Like sentiment_distance.py, but narrower: instead of comparing whole-document
sentiment between a company's 8-K and its matching 10-K, this isolates just the
AI-related sentences within each document and compares sentiment between those
two subsets only.

Why: sentiment_distance.py runs FinBERT over the *entire* Item 1A Risk Factors
section of a 10-K. Risk Factors sections are written by counsel to be
structurally negative regardless of subject matter ("our business may be
harmed by...", "we may be unable to...", etc.), so a whole-document distance
score is confounded — it may just be measuring "10-Ks are legally hedged
documents", not anything specific to AI language. Restricting both sides of
the comparison to only the sentences that actually mention AI/ML/automation
isolates the thing this research is actually trying to measure.

This script deliberately duplicates rather than imports the two things it
would otherwise need to modify in the other files (its own AI-only keyword
list, since extract_sentences.py's KEYWORD_PATTERN also matches unrelated
workforce/layoff terms; and a per-sentence FinBERT scorer, since
sentiment_distance.py's document_sentiment() is a chunked-whole-document
scorer, not a per-sentence one). Everything else — CSV loading, fiscal-year
pairing, FinBERT model loading, and the net-tone reduction — is imported
directly from sentiment_distance.py and extract_sentences.py rather than
reimplemented.

Pipeline:
  1. Load the same export/ai_washing_10-K.csv and export/ai_washing_8-K.csv
     as sentiment_distance.py.
  2. Unlike sentiment_distance.py, do NOT concatenate a 10-K's Item 1A and
     Item 7 sections together. Keep only the Item 1A Risk Factors section per
     10-K (that's the section AI-washing concerns are usually about), and
     skip/flag any 10-K where that section is missing or too short to be
     meaningful.
  3. Reuse sentiment_distance.py's fiscal-year-window pairing to match each
     8-K to its covering 10-K, exactly as before.
  4. Within each document (10-K's Item 1A text, 8-K's full text), keep only
     the sentences matching an AI-specific keyword filter (adapted from
     extract_sentences.py's KEYWORD_PATTERN, minus its workforce/layoff terms
     which aren't AI-specific, plus a few additional AI terms).
  5. Score each matched sentence individually with FinBERT (not chunked
     concatenation — these subsets are a handful of short sentences, not a
     50,000-character section) and average the net-tone scores per subset.
     Flag any pair where either side matched too few AI sentences to trust.
  6. Write export/ai_sentiment_distance_results.csv and print a summary,
     including whether the "10-K reads negative" pattern from the
     whole-document analysis still holds once non-AI text is excluded.

Run:
    python extract_ai_sentiment.py             full run
    python extract_ai_sentiment.py --dry-run   pairing + sentence extraction
                                                only, no FinBERT (fast; use
                                                this to sanity-check counts
                                                first)
"""
import argparse
import csv
import os
import re
import sys
from collections import defaultdict

import nltk

import config
import extract_sentences as es
import sentiment_distance as sd

EXPORT_DIR = config.EXPORT_DIR
TENK_PATH = os.path.join(EXPORT_DIR, "ai_washing_10-K.csv")
EIGHTK_PATH = os.path.join(EXPORT_DIR, "ai_washing_8-K.csv")
OUTPUT_PATH = os.path.join(EXPORT_DIR, "ai_sentiment_distance_results.csv")

RISK_FACTORS_SECTION = "Item 1A Risk Factors"

# Below this many characters, an Item 1A section is either a parsing artifact
# or a placeholder, not real risk-factors prose (real ones in this dataset
# run 35,000-150,000 characters; see the module docstring in
# sentiment_distance.py for the analogous IBM Item 7 issue this mirrors).
MIN_SECTION_CHARS = 500

# A subset's mean sentiment isn't trustworthy if it's an average of only one
# or two sentences. There's no principled cutoff here, so this is a
# documented judgment call, not a statistical threshold: 5 is enough
# sentences that a single unusually positive/negative one can't swing the
# subset mean on its own.
MIN_AI_SENTENCES = 5

# AI-specific subset of extract_sentences.py's KEYWORD_PATTERN: keeps the
# AI/ML/automation terms, drops the workforce/layoff/restructuring terms
# (headcount, layoffs, restructuring, etc.) since those aren't AI-specific
# and would let non-AI sentences into the "AI" subset, and adds a few more
# AI-specific terms (LLMs, neural nets, cognitive computing) that show up in
# this dataset's tech-company filings but weren't needed for the broader
# workforce-focused labeling task extract_sentences.py was built for.
AI_KEYWORD_PATTERN = re.compile(
    r"\b("
    r"AI|artificial intelligence|generative AI|genAI|"
    r"machine learning|deep learning|neural network\w*|"
    r"large language model\w*|LLM\w*|automat\w*|"
    r"cognitive computing"
    r")\b",
    re.IGNORECASE,
)

OUTPUT_FIELDS = [
    "company", "ticker", "fiscal_year",
    "n_ai_sentences_8k", "ai_sentiment_8k",
    "n_ai_sentences_10k", "ai_sentiment_10k",
    "sentiment_distance", "flag",
    "8k_doc_id", "8k_filing_date", "10k_doc_id", "8k_url", "10k_url",
]


# Step 1/2: load the 10-K CSV and keep only the Item 1A Risk Factors section
# per filing (not concatenated with Item 7, unlike sentiment_distance.py's
# group_filings, since Item 7 MD&A isn't what AI-washing concerns are about).

def group_tenk_risk_factors(rows):
    """Return (filings, skipped) where filings is one record per 10-K that
    has a usable Item 1A section, and skipped is a list of
    {company, ticker, filing_date, reason} dicts for 10-Ks that don't.
    """
    all_keys = set()
    risk_factor_groups = defaultdict(list)
    for row in rows:
        key = (row["company"], row["ticker"], row["filing_date"])
        all_keys.add(key)
        if row.get("section") == RISK_FACTORS_SECTION:
            risk_factor_groups[key].append(row)

    filings, skipped = [], []
    for key in sorted(all_keys):
        company, ticker, filing_date = key
        group_rows = risk_factor_groups.get(key)
        if not group_rows:
            skipped.append({"company": company, "ticker": ticker,
                             "filing_date": filing_date,
                             "reason": "no Item 1A Risk Factors section found"})
            continue
        text = "\n\n".join(r["text"] for r in group_rows if r["text"])
        if len(text.strip()) < MIN_SECTION_CHARS:
            skipped.append({"company": company, "ticker": ticker,
                             "filing_date": filing_date,
                             "reason": f"Item 1A section too short "
                                       f"({len(text.strip())} chars < {MIN_SECTION_CHARS})"})
            continue
        filings.append({
            "company": company,
            "ticker": ticker,
            "filing_date": sd._parse_date(filing_date),
            "doc_id": "; ".join(r["doc_id"] for r in group_rows),
            "url": "; ".join(dict.fromkeys(r["url"] for r in group_rows)),
            "text": text,
        })
    return filings, skipped


# Step 4: AI-specific sentence extraction (reuses extract_sentences.py's
# tokenizer setup and word-count bounds, swaps in the AI-only keyword filter)

def extract_ai_sentences(text):
    if not text or not text.strip():
        return []
    seen = set()
    out = []
    for raw_sentence in nltk.sent_tokenize(text):
        sentence = " ".join(raw_sentence.split())
        if not sentence:
            continue
        n_words = len(sentence.split())
        if n_words < es.MIN_WORDS or n_words > es.MAX_WORDS:
            continue
        if not AI_KEYWORD_PATTERN.search(sentence):
            continue
        if sentence in seen:
            continue
        seen.add(sentence)
        out.append(sentence)
    return out


# Step 5: per-sentence FinBERT scoring (reuses sd.load_finbert's model/
# tokenizer and sd.net_tone_score's positive-minus-negative reduction; the
# batched per-sentence forward pass itself is new since document_sentiment()
# is built around chunking one long document, not scoring many short ones)

def score_sentences(sentences, tokenizer, model, device, label_index, batch_size=16):
    if not sentences:
        return []
    import torch

    scores = []
    for i in range(0, len(sentences), batch_size):
        batch = sentences[i:i + batch_size]
        encoded = tokenizer(
            batch, padding=True, truncation=True,
            max_length=sd.MAX_TOKENS, return_tensors="pt",
        ).to(device)
        with torch.no_grad():
            logits = model(**encoded).logits
            probs = torch.softmax(logits, dim=-1)
        for row in probs:
            dist = {
                "positive": row[label_index["positive"]].item(),
                "negative": row[label_index["negative"]].item(),
                "neutral": row[label_index["neutral"]].item(),
            }
            scores.append(sd.net_tone_score(dist))
    return scores


def subset_sentiment(text, tokenizer, model, device, label_index):
    """Return (n_sentences, mean_score_or_None) for the AI-specific subset
    of `text`."""
    sentences = extract_ai_sentences(text)
    if not sentences:
        return 0, None
    scores = score_sentences(sentences, tokenizer, model, device, label_index)
    return len(sentences), sum(scores) / len(scores)


# Step 6: compute results, write output, summarize

def compute_results(pairs, tokenizer, model, device, label_index):
    results = []
    cache = {}  # doc_id -> (n_sentences, mean_score)

    total = len(pairs)
    for i, pair in enumerate(pairs, start=1):
        tenk, eightk = pair["tenk"], pair["eightk"]
        print(f"  [{i}/{total}] {eightk['company']} 8-K {eightk['filing_date']} "
              f"vs 10-K {tenk['filing_date']} (Item 1A only)")

        if tenk["doc_id"] not in cache:
            cache[tenk["doc_id"]] = subset_sentiment(
                tenk["text"], tokenizer, model, device, label_index)
        n_10k, score_10k = cache[tenk["doc_id"]]

        if eightk["doc_id"] not in cache:
            cache[eightk["doc_id"]] = subset_sentiment(
                eightk["text"], tokenizer, model, device, label_index)
        n_8k, score_8k = cache[eightk["doc_id"]]

        low_confidence = n_10k < MIN_AI_SENTENCES or n_8k < MIN_AI_SENTENCES
        distance = (score_8k - score_10k
                    if score_8k is not None and score_10k is not None else None)

        results.append({
            "company": eightk["company"],
            "ticker": eightk["ticker"],
            "fiscal_year": str(tenk["filing_date"].year),
            "n_ai_sentences_8k": n_8k,
            "ai_sentiment_8k": round(score_8k, 4) if score_8k is not None else "",
            "n_ai_sentences_10k": n_10k,
            "ai_sentiment_10k": round(score_10k, 4) if score_10k is not None else "",
            "sentiment_distance": round(distance, 4) if distance is not None else "",
            "flag": "LOW_AI_SENTENCE_COUNT" if low_confidence else "",
            "8k_doc_id": eightk["doc_id"],
            "8k_filing_date": eightk["filing_date"].isoformat(),
            "10k_doc_id": tenk["doc_id"],
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


def print_pairing_preview(pairs, skipped_8k, skipped_10k):
    print(f"\n=== Pairing preview ({len(pairs)} matched, {len(skipped_8k)} 8-Ks skipped) ===")
    for p in sorted(pairs, key=lambda p: (p["eightk"]["company"], p["eightk"]["filing_date"])):
        print(f"  {p['eightk']['company']:<40} 8-K {p['eightk']['filing_date']} "
              f"-> 10-K {p['tenk']['filing_date']}")
    if skipped_8k:
        print(f"\n  Skipped 8-Ks ({len(skipped_8k)}):")
        for s in sorted(skipped_8k, key=lambda s: (s["eightk"]["company"], s["eightk"]["filing_date"])):
            print(f"    {s['eightk']['company']:<40} 8-K {s['eightk']['filing_date']} "
                  f": {s['reason']}")
    if skipped_10k:
        print(f"\n  10-Ks excluded for missing/too-short Item 1A ({len(skipped_10k)}):")
        for s in skipped_10k:
            print(f"    {s['company']:<40} {s['filing_date']} : {s['reason']}")


def print_summary(results, skipped_10k):
    scored = [r for r in results if r["sentiment_distance"] != ""]
    flagged = [r for r in results if r["flag"]]
    zero_ai = [r for r in results if r["n_ai_sentences_8k"] == 0 or r["n_ai_sentences_10k"] == 0]

    print(f"\n=== Summary ===")
    print(f"Pairs total: {len(results)}")
    print(f"Pairs with a computable AI-sentiment distance: {len(scored)}")
    print(f"Pairs flagged (fewer than {MIN_AI_SENTENCES} AI sentences on "
          f"one or both sides): {len(flagged)}")
    print(f"  of which, zero AI sentences found on at least one side: {len(zero_ai)}")
    print(f"10-Ks excluded before pairing (missing/too-short Item 1A): {len(skipped_10k)}")

    if scored:
        mean_10k = sum(r["ai_sentiment_10k"] for r in scored) / len(scored)
        mean_8k = sum(r["ai_sentiment_8k"] for r in scored) / len(scored)
        mean_distance = sum(r["sentiment_distance"] for r in scored) / len(scored)
        pct_10k_negative = 100 * sum(1 for r in scored if r["ai_sentiment_10k"] < 0) / len(scored)
        pct_8k_negative = 100 * sum(1 for r in scored if r["ai_sentiment_8k"] < 0) / len(scored)

        print(f"\nMean AI-sentence net tone, 10-K (Item 1A): {mean_10k:+.4f} "
              f"({pct_10k_negative:.0f}% of pairs net-negative)")
        print(f"Mean AI-sentence net tone, 8-K: {mean_8k:+.4f} "
              f"({pct_8k_negative:.0f}% of pairs net-negative)")
        print(f"Mean sentiment distance (8-K minus 10-K): {mean_distance:+.4f}")

        print("\n[interpretation] sentiment_distance_results.csv (whole-document) found "
              "10-Ks reading uniformly negative regardless of AI content. Once restricted "
              "to only AI-related sentences:")
        if mean_10k < 0 and mean_distance > 0:
            print("  -> the pattern still holds: AI-specific language in the 10-K is "
                  "still net-negative on average, and the 8-K still reads more positive.")
        elif mean_10k >= 0:
            print("  -> the pattern weakens/disappears: AI-specific sentences in the 10-K "
                  "are not net-negative on average, suggesting the original whole-document "
                  "negativity was mostly non-AI Risk Factors boilerplate.")
        else:
            print("  -> mixed: AI-specific 10-K sentences are still net-negative, but the "
                  "8-K/10-K gap narrowed compared to the whole-document analysis.")
    else:
        print("\nNo pairs had a computable distance (every pair was missing AI sentences "
              "on at least one side) -- nothing to compare.")

    print(f"\nResults written to {OUTPUT_PATH}")


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Compute AI-specific-sentence 8-K vs 10-K sentiment distance")
    parser.add_argument("--dry-run", action="store_true",
                         help="only run pairing + sentence extraction counts; skip FinBERT")
    args = parser.parse_args(argv)

    es.ensure_punkt()

    tenk_rows = sd._load_csv(TENK_PATH)
    eightk_rows = sd._load_csv(EIGHTK_PATH)
    if not tenk_rows or not eightk_rows:
        return

    tenk_filings, skipped_10k = group_tenk_risk_factors(tenk_rows)
    eightk_filings = sd.group_filings(eightk_rows)
    print(f"Loaded {len(tenk_filings)} 10-Ks with a usable Item 1A section "
          f"({len(skipped_10k)} excluded) and {len(eightk_filings)} 8-K filings.")

    pairs, skipped_8k = sd.build_pairs(tenk_filings, eightk_filings)
    print_pairing_preview(pairs, skipped_8k, skipped_10k)

    if args.dry_run:
        print("\n[dry-run] Checking AI-sentence counts per document (no FinBERT)...")
        counts = {}
        for pair in pairs:
            for doc in (pair["tenk"], pair["eightk"]):
                if doc["doc_id"] not in counts:
                    counts[doc["doc_id"]] = len(extract_ai_sentences(doc["text"]))
        for doc_id, n in sorted(counts.items(), key=lambda kv: kv[1]):
            flag = " [LOW]" if n < MIN_AI_SENTENCES else ""
            print(f"  {n:>4} AI sentences  {doc_id}{flag}")
        print("\n[dry-run] Skipping FinBERT. Re-run without --dry-run once this looks right.")
        return

    print("\nLoading FinBERT (ProsusAI/finbert)...")
    tokenizer, model, device, label_index = sd.load_finbert()
    print(f"Running sentiment analysis on {device}...")

    results = compute_results(pairs, tokenizer, model, device, label_index)
    write_results(results)
    print_summary(results, skipped_10k)


if __name__ == "__main__":
    main()
