"""Turn the raw filing/exhibit text in export/ai_washing_*.csv into a flat,
sentence-level CSV ready for hand-labeling.

Each source CSV (grouped by source_type, see storage.py) has one row per
document with a `text` field holding the whole risk-factors section, press
release, etc. This script splits that text into individual sentences with
nltk's Punkt tokenizer (not naive period-splitting, since financial text is
full of abbreviations like "Inc." and decimal numbers), keeps only sentences
that plausibly mention AI/automation/workforce topics, drops fragments too
short or too long to label meaningfully, deduplicates exact repeats, and
writes everything to export/labeling_dataset.csv with a blank `label` column
for you to fill in by hand.

Merge-safe: if export/labeling_dataset.csv already exists, its rows (and any
labels you've already filled in) are kept exactly as-is. Only sentences not
already in that file get appended underneath, with sentence_id continuing on
from the existing max. Nothing already there is ever rewritten or dropped.

The earnings_call_snippet file is skipped since it only holds short Google
search snippets, not real source text.

Run:
    python extract_sentences.py
"""
import csv
import glob
import os
import re
import sys
from collections import Counter

import nltk

import config


def _raise_csv_field_limit():
    """csv's default per-field size cap (131072 bytes) is too small for a
    whole 10-K risk-factors section or 8-K exhibit. Raise it as high as the
    platform's C long allows. sys.maxsize can overflow that on some
    platforms, notably Windows, so back off by 10x until it's accepted.
    """
    limit = sys.maxsize
    while True:
        try:
            csv.field_size_limit(limit)
            return
        except OverflowError:
            limit //= 10


_raise_csv_field_limit()

EXPORT_DIR = config.EXPORT_DIR
OUTPUT_PATH = os.path.join(EXPORT_DIR, "labeling_dataset.csv")
SKIP_SOURCE_TYPE = "earnings_call_snippet"

MIN_WORDS = 6
MAX_WORDS = 60

KEYWORD_PATTERN = re.compile(
    r"\b("
    r"AI|artificial intelligence|automat\w*|machine learning|"
    r"generative AI|efficienc\w*|headcount|layoff\w*|"
    r"workforce reduction|restructuring"
    r")\b",
    re.IGNORECASE,
)


def ensure_punkt():
    """Make sure nltk's sentence tokenizer data is available, downloading it
    on first run. Different nltk versions look for different resource
    names, so we just try tokenizing and download what's missing."""
    try:
        nltk.sent_tokenize("Testing setup. This confirms Punkt is ready.")
        return
    except LookupError:
        pass
    for package in ("punkt", "punkt_tab"):
        print(f"[setup] downloading nltk '{package}' tokenizer data (one-time)...")
        nltk.download(package, quiet=True)
    # Let a real LookupError surface here if the download didn't fix it.
    nltk.sent_tokenize("Testing setup. This confirms Punkt is ready.")


def load_rows():
    rows = []
    paths = sorted(glob.glob(os.path.join(EXPORT_DIR, "ai_washing_*.csv")))
    for path in paths:
        if SKIP_SOURCE_TYPE in os.path.basename(path):
            print(f"[skip] {path} (search snippets, not source text)")
            continue
        with open(path, newline="", encoding="utf-8-sig") as f:
            file_rows = list(csv.DictReader(f))
        print(f"[read] {path} ({len(file_rows)} documents)")
        rows.extend(file_rows)
    return rows


FIELDNAMES = ["sentence_id", "company", "source_type", "filing_date", "url",
              "sentence", "label"]


def load_existing(path):
    """Return (existing_rows, seen_sentences, next_id) for a prior output
    file, or ([], set(), 1) if there isn't one yet."""
    if not os.path.exists(path):
        return [], set(), 1
    # utf-8-sig handles both BOM and no-BOM UTF-8; cp1252 is a fallback in
    # case Excel re-saved the file in the system codepage after hand-editing.
    try:
        with open(path, newline="", encoding="utf-8-sig") as f:
            rows = list(csv.DictReader(f))
    except UnicodeDecodeError:
        with open(path, newline="", encoding="cp1252") as f:
            rows = list(csv.DictReader(f))
    seen = {r["sentence"] for r in rows}
    max_id = 0
    for r in rows:
        try:
            max_id = max(max_id, int(r["sentence_id"]))
        except (KeyError, ValueError):
            pass
    return rows, seen, max_id + 1


def extract_sentences(rows, seen=None):
    """Return new, qualifying, deduplicated sentences from `rows`.

    `seen` is a set of sentence strings to treat as already-captured (e.g.
    ones already sitting in labeling_dataset.csv from a prior run). They're
    skipped here so the caller only gets genuinely new sentences back.
    """
    seen = set() if seen is None else set(seen)
    out = []
    for row in rows:
        text = row.get("text") or ""
        if not text.strip():
            continue
        for raw_sentence in nltk.sent_tokenize(text):
            sentence = " ".join(raw_sentence.split())  # collapse whitespace/newlines
            if not sentence:
                continue
            n_words = len(sentence.split())
            if n_words < MIN_WORDS or n_words > MAX_WORDS:
                continue
            if not KEYWORD_PATTERN.search(sentence):
                continue
            if sentence in seen:
                continue
            seen.add(sentence)
            out.append({
                "company": row.get("company", ""),
                "source_type": row.get("source_type", ""),
                "filing_date": row.get("filing_date", ""),
                "url": row.get("url", ""),
                "sentence": sentence,
            })
    return out


def write_output(existing_rows, new_sentences, next_id):
    os.makedirs(EXPORT_DIR, exist_ok=True)
    with open(OUTPUT_PATH, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()
        for r in existing_rows:
            writer.writerow({k: r.get(k, "") for k in FIELDNAMES})
        for i, s in enumerate(new_sentences, start=next_id):
            writer.writerow({
                "sentence_id": i,
                "company": s["company"],
                "source_type": s["source_type"],
                "filing_date": s["filing_date"],
                "url": s["url"],
                "sentence": s["sentence"],
                "label": "",
            })


def print_summary(existing_rows, new_sentences):
    combined = existing_rows + new_sentences
    by_company = Counter(r["company"] or "(unknown)" for r in combined)
    by_source = Counter(r["source_type"] or "(unknown)" for r in combined)

    print(f"\nExisting rows kept as-is (labels preserved): {len(existing_rows)}")
    print(f"New sentences added: {len(new_sentences)}")
    print(f"Total rows in {OUTPUT_PATH}: {len(combined)}")

    print("\nBy company:")
    for company, n in sorted(by_company.items(), key=lambda kv: -kv[1]):
        print(f"  {company}: {n}")

    print("\nBy source_type:")
    for source_type, n in sorted(by_source.items(), key=lambda kv: -kv[1]):
        print(f"  {source_type}: {n}")


def main():
    ensure_punkt()
    rows = load_rows()
    if not rows:
        print(f"No matching CSV files found in {EXPORT_DIR}. Run main.py first.")
        return
    existing_rows, seen, next_id = load_existing(OUTPUT_PATH)
    new_sentences = extract_sentences(rows, seen=seen)
    write_output(existing_rows, new_sentences, next_id)
    print_summary(existing_rows, new_sentences)


if __name__ == "__main__":
    main()
