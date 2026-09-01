"""Merge blinded workflow labels onto sampled provenance rows -> final CSV.

Reads labels either from labels.json (the workflow's return value, saved by the
orchestrator) or, as a fallback, reconstructs finals from the workflow
journal.jsonl (adjudicator result wins; else agreement merge of the two coders).

Output columns are identical to derived/annotation_template.csv. Every row is
checked with label_schema.validate_annotation before writing.
"""
import csv, json, os, sys
from collections import Counter

SCRATCH = os.path.dirname(os.path.abspath(__file__))
REPO = r"c:\Users\advik\Downloads\gtown_research"
sys.path.insert(0, REPO)
from label_schema import (MODEL_LABELS, SCHEMA_VERSION, derived_neutral,
                          validate_annotation)

OUT_CSV = os.path.join(REPO, "derived", "annotation_master_sample_llm_blind.csv")
CODER_ID = "llm_blind:claude-fable-5:prompt-1.0.0+risk_type"
COMPARE_FIELDS = list(MODEL_LABELS) + [
    "risk_type", "risk_type_secondary", "actuality", "specificity",
    "causal_link_strength"]


def from_labels_json(path):
    data = json.load(open(path, encoding="utf-8"))
    return {r["id"]: r for r in data["results"] if r.get("labels")}


def from_journal(path):
    """Reconstruct finals from journal.jsonl agent returns."""
    per_id = {}
    for line in open(path, encoding="utf-8"):
        line = line.strip()
        if not line:
            continue
        rec = json.loads(line)
        label = rec.get("label") or ""
        if ":" not in label:
            continue
        tag, pid = label.split(":", 1)
        if tag not in ("coderA", "coderB", "retryA", "retryB", "adjudicate"):
            continue
        val = rec.get("result")
        if isinstance(val, dict) and "ai_opportunity" in val:
            per_id.setdefault(pid, {})[tag] = val
    finals = {}
    for pid, runs in per_id.items():
        def clean(l):
            if l and l.get("risk_type_secondary") == l.get("risk_type"):
                l["risk_type_secondary"] = ""
            return l
        if "adjudicate" in runs:
            disputes = []
            a = clean(runs.get("coderA") or runs.get("retryA"))
            b = clean(runs.get("coderB") or runs.get("retryB"))
            if a and b:
                disputes = [f for f in COMPARE_FIELDS if a[f] != b[f]]
            finals[pid] = {"id": pid, "status": "adjudicated",
                           "labels": clean(runs["adjudicate"]),
                           "agreed": False, "disputes": disputes}
        else:
            cands = [clean(runs[t]) for t in
                     ("coderA", "coderB", "retryA", "retryB") if runs.get(t)]
            if not cands:
                continue
            a = cands[0]
            if len(cands) >= 2:
                b = cands[1]
                ev = a["evidence"] if a["evidence"].strip() else b["evidence"]
                merged = dict(a)
                merged["evidence"] = ev
                finals[pid] = {"id": pid, "status": "agreed", "labels": merged,
                               "agreed": True, "disputes": []}
            else:
                finals[pid] = {"id": pid, "status": "single_pass", "labels": a,
                               "agreed": None, "disputes": []}
    return finals


def main():
    labels_json = os.path.join(SCRATCH, "labels.json")
    journal = sys.argv[1] if len(sys.argv) > 1 else None
    if os.path.exists(labels_json):
        finals = from_labels_json(labels_json)
        src = "labels.json"
    elif journal and os.path.exists(journal):
        finals = from_journal(journal)
        src = "journal"
    else:
        sys.exit("no labels.json and no journal path given")

    with open(os.path.join(SCRATCH, "sample_rows.csv"), newline="",
              encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        rows = list(reader)

    out_rows, problems, missing = [], [], []
    status_counter = Counter()
    for row in rows:
        pid = row["passage_id"]
        rec = finals.get(pid)
        if not rec or not rec.get("labels"):
            missing.append(pid)
            continue
        lab = rec["labels"]
        status_counter[rec["status"]] += 1
        for k in MODEL_LABELS:
            row[k] = str(int(lab[k]))
        row["neutral"] = str(derived_neutral(lab))
        row["risk_type"] = lab["risk_type"]
        row["risk_type_secondary"] = lab.get("risk_type_secondary", "")
        row["actuality"] = lab["actuality"]
        row["specificity"] = lab["specificity"]
        row["causal_link_strength"] = lab["causal_link_strength"]
        row["coder_id"] = CODER_ID
        row["review_status"] = "unreviewed"
        note = 'evidence="' + lab.get("evidence", "").replace('"', "'") + '"'
        if rec["status"] == "agreed":
            note += " | coders: 2/2 agreed on all fields"
        elif rec["status"] == "adjudicated":
            note += (" | coders disagreed on " +
                     (", ".join(rec.get("disputes") or []) or "evidence rule") +
                     "; blinded adjudicator decided")
        else:
            note += " | " + rec["status"]
        row["annotation_notes"] = note
        row["label_schema_version"] = SCHEMA_VERSION
        errs = validate_annotation(row)
        if errs:
            problems.append((pid, errs))
        out_rows.append(row)

    with open(OUT_CSV, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(out_rows)

    print(f"source: {src}")
    print(f"wrote {len(out_rows)} rows -> {OUT_CSV}")
    print("status:", dict(status_counter))
    if missing:
        print(f"MISSING labels for {len(missing)} passages:", missing)
    if problems:
        print(f"VALIDATION problems in {len(problems)} rows:")
        for pid, errs in problems[:20]:
            print(" ", pid, errs)
    else:
        print("all rows pass validate_annotation()")

    # summary stats for reporting
    n = len(out_rows)
    print("\nlabel prevalence:")
    for k in MODEL_LABELS + ("neutral",):
        c = sum(int(r[k]) for r in out_rows)
        print(f"  {k:26s} {c:4d}  ({100*c/n:.1f}%)")
    for field in ("risk_type", "actuality", "specificity",
                  "causal_link_strength"):
        print(f"\n{field}:")
        for v, c in Counter(r[field] for r in out_rows).most_common():
            print(f"  {v:26s} {c:4d}")
    agree = status_counter.get("agreed", 0)
    adj = status_counter.get("adjudicated", 0)
    if agree + adj:
        print(f"\ncoder agreement: {agree}/{agree+adj} "
              f"({100*agree/(agree+adj):.1f}%) passages identical across all "
              f"13 fields; {adj} adjudicated")
    comp = Counter(r["ticker"] for r in out_rows)
    print(f"\ncompanies covered: {len(comp)}")


if __name__ == "__main__":
    main()
