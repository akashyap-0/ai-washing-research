"""Single-pass LLM annotation of derived/annotation_template.csv.

Per RESEARCH_PIPELINE.md, these are single-pass LLM labels: useful for rubric
development, weak supervision, and pre-filling the gold-annotation workflow,
but never a substitute for the two-coder human adjudication the pipeline
requires before training data is called "adjudicated". Rows written by this
script get coder_id="llm_v1" and review_status="unreviewed" so downstream
code (validate_annotation, training scripts) cannot mistake them for
human-reviewed labels.

Usage:
    export ANTHROPIC_API_KEY=...
    python llm_annotate.py \
        --input derived/annotation_template.csv \
        --output derived/annotation_llm.csv \
        [--limit 50] [--workers 8] [--model claude-sonnet-5]
"""
import argparse
import csv
import json
import sys
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed

import anthropic

from label_schema import (
    MODEL_LABELS,
    ACTUALITY_VALUES,
    SPECIFICITY_VALUES,
    CAUSAL_LINK_VALUES,
    SCHEMA_VERSION,
    derived_neutral,
)

RUBRIC = """You are annotating one SEC filing passage for a research pipeline studying
how companies frame AI relative to workforce and financial outcomes.

Label each of these 8 fields as 0 or 1 (multi-label; more than one may be 1):

- ai_opportunity: AI is presented as a commercial, strategic, growth, or capability
  opportunity. Generic praise without evidence still counts here (mark generic_ai_marketing too).
- ai_risk: AI creates competitive, operational, regulatory, security, implementation,
  financial, or workforce risk for the company.
- ai_efficiency: AI is claimed or expected to increase output, speed, productivity, or
  cost efficiency.
- ai_workforce_reduction: AI is linked to layoffs, headcount reduction, reduced hiring,
  or role elimination.
- ai_adoption: AI has actually been deployed or is actively used. Planned exploration
  alone does NOT qualify.
- ai_worker_augmentation: AI is described as assisting, augmenting, or upskilling
  employees rather than replacing them.
- generic_ai_marketing: Vague promotional AI language with no concrete evidence,
  deployment, or mechanism.
- explicit_ai_job_link: The passage explicitly and causally ties AI to a specific job,
  headcount, or hiring outcome. Merely mentioning AI and layoffs/jobs in the same
  passage without an explicit causal link does NOT qualify -- use ai_workforce_reduction
  and causal_link_strength=co_occurring_only instead.

Also label:
- actuality: one of realized, ongoing, planned, hypothetical, unclear
- specificity: one of quantified, specific_unquantified, vague, unclear
- causal_link_strength (AI -> workforce/job outcome specifically): one of
  explicit, strongly_implied, co_occurring_only, none, unclear

Respond with ONLY a JSON object with exactly these keys (all label keys are 0/1 ints,
the other three are strings from the allowed lists above):
ai_opportunity, ai_risk, ai_efficiency, ai_workforce_reduction, ai_adoption,
ai_worker_augmentation, generic_ai_marketing, explicit_ai_job_link,
actuality, specificity, causal_link_strength
"""

FIELDNAMES = None  # set from input file header
_client = anthropic.Anthropic()
_print_lock = threading.Lock()


def label_passage(row, model):
    prompt = (
        f"Company: {row.get('company')} ({row.get('ticker')})\n"
        f"Form: {row.get('form')}  Section: {row.get('section')}\n"
        f"Passage:\n{row.get('text')}\n"
    )
    resp = _client.messages.create(
        model=model,
        max_tokens=400,
        system=RUBRIC,
        messages=[{"role": "user", "content": prompt}],
    )
    raw = resp.content[0].text.strip()
    if raw.startswith("```"):
        raw = raw.strip("`")
        if raw.startswith("json"):
            raw = raw[4:]
    data = json.loads(raw)

    for label in MODEL_LABELS:
        data[label] = 1 if int(data.get(label, 0)) else 0
    if data.get("actuality") not in ACTUALITY_VALUES:
        data["actuality"] = "unclear"
    if data.get("specificity") not in SPECIFICITY_VALUES:
        data["specificity"] = "unclear"
    if data.get("causal_link_strength") not in CAUSAL_LINK_VALUES:
        data["causal_link_strength"] = "unclear"

    data["neutral"] = derived_neutral(data)
    data["coder_id"] = "llm_v1"
    data["review_status"] = "unreviewed"
    data["annotation_notes"] = ""
    data["label_schema_version"] = SCHEMA_VERSION
    return data


def process_row(row, model, retries=3):
    last_err = None
    for attempt in range(retries):
        try:
            labels = label_passage(row, model)
            row.update(labels)
            return row, None
        except Exception as e:  # noqa: BLE001
            last_err = e
    return row, last_err


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", default="derived/annotation_template.csv")
    ap.add_argument("--output", default="derived/annotation_llm.csv")
    ap.add_argument("--limit", type=int, default=None)
    ap.add_argument("--workers", type=int, default=6)
    ap.add_argument("--model", default="claude-sonnet-5")
    args = ap.parse_args()

    with open(args.input, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        global FIELDNAMES
        FIELDNAMES = reader.fieldnames
        rows = list(reader)

    if args.limit:
        rows = rows[: args.limit]

    total = len(rows)
    done = 0
    errors = 0

    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = {pool.submit(process_row, row, args.model): row for row in rows}
        with open(args.output, "w", newline="", encoding="utf-8") as out:
            writer = csv.DictWriter(out, fieldnames=FIELDNAMES)
            writer.writeheader()
            for fut in as_completed(futures):
                row, err = fut.result()
                writer.writerow(row)
                done += 1
                if err:
                    errors += 1
                    with _print_lock:
                        print(f"[{done}/{total}] ERROR passage_id={row.get('passage_id')}: {err}", file=sys.stderr)
                elif done % 25 == 0 or done == total:
                    with _print_lock:
                        print(f"[{done}/{total}] labeled ({errors} errors so far)")

    print(f"Done. {done - errors}/{total} labeled, {errors} errors. Wrote {args.output}")


if __name__ == "__main__":
    main()
