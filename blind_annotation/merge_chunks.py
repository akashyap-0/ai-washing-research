"""Fold subagent chunk labels back into derived/annotation_llm_blind.csv.

Idempotent: re-running only fills rows that are still blank, so it can be run
repeatedly as chunks land. Validates every merged row against label_schema.
"""
import csv, glob, json, os, sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, REPO)
from label_schema import MODEL_LABELS, SCHEMA_VERSION, derived_neutral, validate_annotation

CSV_PATH = os.path.join(REPO, "derived", "annotation_llm_blind.csv")
CODER_ID = "llm_blind_subagent:prompt-1.0.0"

ENUMS = {
    "actuality": ("realized", "ongoing", "planned", "hypothetical", "unclear"),
    "specificity": ("quantified", "specific_unquantified", "vague", "unclear"),
    "causal_link_strength": ("explicit", "strongly_implied", "co_occurring_only", "none", "unclear"),
}


def main():
    labels = {}
    files = sorted(glob.glob(os.path.join(os.path.dirname(__file__), "out", "chunk_*.json")))
    for path in files:
        try:
            for rec in json.load(open(path, encoding="utf-8")):
                labels[rec["id"]] = rec
        except Exception as e:
            print(f"  skip {os.path.basename(path)}: {e}", file=sys.stderr)
    print(f"loaded {len(labels)} labels from {len(files)} chunk files")

    with open(CSV_PATH, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        fieldnames, rows = reader.fieldnames, list(reader)

    filled = skipped = bad = 0
    for row in rows:
        if row["ai_opportunity"] in ("0", "1"):
            continue  # already labeled (API pass or earlier merge)
        rec = labels.get(row["passage_id"])
        if not rec:
            skipped += 1
            continue

        for lab in MODEL_LABELS:
            row[lab] = 1 if int(rec.get(lab, 0)) else 0
        for field, allowed in ENUMS.items():
            row[field] = rec.get(field) if rec.get(field) in allowed else "unclear"
        row["neutral"] = derived_neutral(row)
        row["coder_id"] = CODER_ID
        row["review_status"] = "unreviewed"
        row["annotation_notes"] = (rec.get("evidence") or "").strip()
        row["label_schema_version"] = SCHEMA_VERSION

        errs = validate_annotation(row)
        if errs:
            bad += 1
            print(f"  INVALID {row['passage_id']}: {errs}", file=sys.stderr)
        filled += 1

    with open(CSV_PATH, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(rows)

    done = sum(1 for r in rows if r["ai_opportunity"] in ("0", "1"))
    print(f"filled {filled} rows this pass ({bad} invalid), {skipped} still awaiting chunks")
    print(f"TOTAL LABELED: {done}/{len(rows)}  ({len(rows)-done} remaining)")


if __name__ == "__main__":
    main()
