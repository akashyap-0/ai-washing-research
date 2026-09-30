"""Finish the 14 open passages from the blinded annotation run.

Reads the authoritative CODEBOOK and LABEL_SCHEMA out of workflow_script.js so
the prompt text for this batch is byte-identical to the one used for the other
241 passages. Blinding is preserved: the model sees bare passage text only.

- 11 passages need adjudication (both coder label sets already in remaining_work.json)
- 3 passages were never coded (two independent blinded coders, then adjudicate if they differ)

Appends finals to labels.json. Run merge_labels.py afterwards to rebuild the CSV.
"""
import csv
import json
import re
import sys

import anthropic

MODEL = "claude-sonnet-5"
PROMPT_VERSION = "prompt-1.0.0+risk_type"

RISK_TYPES = ["demand", "competition", "export_controls", "implementation",
              "displacement", "governance", "other", "not_a_risk", "unclear"]
BIN_FIELDS = ["ai_opportunity", "ai_risk", "ai_efficiency", "ai_workforce_reduction",
              "ai_adoption", "ai_worker_augmentation", "generic_ai_marketing",
              "explicit_ai_job_link"]
ENUMS = {
    "risk_type": RISK_TYPES,
    "risk_type_secondary": RISK_TYPES + [""],
    "actuality": ["realized", "ongoing", "planned", "hypothetical", "unclear"],
    "specificity": ["quantified", "specific_unquantified", "vague", "unclear"],
    "causal_link_strength": ["explicit", "strongly_implied", "co_occurring_only", "none", "unclear"],
}
FIELDS = BIN_FIELDS + list(ENUMS)

TOOL = {
    "name": "StructuredOutput",
    "description": "Return the label set for the passage.",
    "input_schema": {
        "type": "object",
        "additionalProperties": False,
        "required": FIELDS + ["evidence"],
        "properties": {
            **{f: {"type": "integer", "enum": [0, 1]} for f in BIN_FIELDS},
            **{f: {"type": "string", "enum": v} for f, v in ENUMS.items()},
            "evidence": {"type": "string", "maxLength": 400},
        },
    },
}

client = anthropic.Anthropic()


def load_codebook():
    """Extract the verbatim CODEBOOK string array from workflow_script.js."""
    src = open("blind_annotation/workflow_script.js", encoding="utf-8").read()
    start = src.index("const CODEBOOK = [")
    end = src.index("const BIN =", start)
    block = src[start:end]
    lines = re.findall(r"^'(.*)',?$", block[block.index("["):], re.M)
    return "\n".join(l.replace("\\'", "'").replace("\\n", "\n") for l in lines)


CODEBOOK = load_codebook()


def call(prompt):
    resp = client.messages.create(
        model=MODEL,
        max_tokens=1000,
        tools=[TOOL],
        tool_choice={"type": "tool", "name": "StructuredOutput"},
        messages=[{"role": "user", "content": prompt}],
    )
    for block in resp.content:
        if block.type == "tool_use":
            out = dict(block.input)
            if out.get("risk_type_secondary") == out.get("risk_type"):
                out["risk_type_secondary"] = ""
            return out
    raise RuntimeError("no structured output returned")


def code_prompt(text):
    return (
        f"{CODEBOOK}\n\n---\n\nThe passage to label:\n\n{text}\n\n"
        "Return your labels with a single StructuredOutput call. Judge only the "
        "passage text above. This labeling is blinded; do not speculate about its source."
    )


def adjudicate_prompt(text, a, b, disputes):
    return (
        f"{CODEBOOK}\n\n---\n\nThe passage to label:\n\n{text}\n\n"
        "Two annotators independently applied this codebook to the passage."
        + (f" They disagree on: {', '.join(disputes)}." if disputes else "")
        + f"\nAnnotator A returned: {json.dumps(a)}"
        + f"\nAnnotator B returned: {json.dumps(b)}"
        + "\n\nYou are the adjudicator. Decide EVERY field yourself, strictly per the "
        "codebook, from the passage alone. The annotators' outputs identify where "
        "judgment is contested; they are not authority, and you may also correct a "
        "field they agree on if it plainly violates the codebook. Do not split "
        "differences. Return the complete final label set with a single "
        "StructuredOutput call. This labeling is blinded."
    )


def main():
    texts = {}
    with open("blind_annotation/sample_rows.csv", newline="", encoding="utf-8-sig") as f:
        for row in csv.DictReader(f):
            texts[row["passage_id"]] = row["text"]

    remaining = json.load(open("blind_annotation/remaining_work.json"))
    doc = json.load(open("blind_annotation/labels.json"))
    labels = doc["results"] if isinstance(doc, dict) else doc
    existing = {e["id"] for e in labels}
    print(f"labels.json currently holds {len(existing)} finalized passages")

    finals = []
    for entry in remaining:
        pid = entry["id"]
        text = texts.get(pid)
        if not text:
            print(f"  {pid}: NO TEXT FOUND in sample_rows.csv", file=sys.stderr)
            continue

        if entry["why"] == "needs adjudication":
            final = call(adjudicate_prompt(text, entry["coderA"], entry["coderB"],
                                           entry.get("disputes") or []))
            status, agreed = "adjudicated", False
            disputes = entry.get("disputes") or []
        else:
            a = call(code_prompt(text))
            b = call(code_prompt(text))
            disputes = [f for f in FIELDS if a.get(f) != b.get(f)]
            if disputes:
                final = call(adjudicate_prompt(text, a, b, disputes))
                status, agreed = "adjudicated", False
            else:
                final, status, agreed = a, "agreed", True

        if final["explicit_ai_job_link"] == 1 and not final.get("evidence", "").strip():
            print(f"  {pid}: WARNING explicit_ai_job_link=1 with empty evidence", file=sys.stderr)

        finals.append({"id": pid, "status": status, "labels": final,
                       "agreed": agreed, "disputes": disputes})
        print(f"  {pid}: {status}" + (f" (disputed: {', '.join(disputes)})" if disputes else ""))

    already = {e["id"] for e in finals} & existing
    if already:
        print(f"WARNING: {len(already)} ids already in labels.json, not re-adding", file=sys.stderr)
        finals = [e for e in finals if e["id"] not in existing]

    labels.extend(finals)
    with open("blind_annotation/labels.json", "w", encoding="utf-8") as f:
        json.dump(doc if isinstance(doc, dict) else labels, f, indent=2)

    print(f"\nFinalized {len(finals)} passages. labels.json now holds {len(labels)}.")
    print("Next: python blind_annotation/merge_labels.py")


if __name__ == "__main__":
    main()
