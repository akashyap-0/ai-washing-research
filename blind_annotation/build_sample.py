"""Stratified, deterministic sample of annotation_template.csv for blinded LLM labeling.

Up to PER_COMPANY passages per ticker, allocated across (form, section) strata
proportionally (largest-remainder), seeded shuffle within each stratum so the
pick is deterministic and not order-biased. Writes:
  - blinded/<passage_id>.txt   : bare passage text ONLY (what the labeler sees)
  - sample_manifest.json       : list of {id, path} for the workflow
  - sample_rows.csv            : full provenance rows of the sample (for merge)
"""
import csv, json, math, os, random, sys
from collections import defaultdict

REPO = r"c:\Users\advik\Downloads\gtown_research"
OUT = os.path.dirname(os.path.abspath(__file__))
PER_COMPANY = 12
SEED = 20260901

with open(os.path.join(REPO, "derived", "annotation_template.csv"),
          newline="", encoding="utf-8-sig") as f:
    reader = csv.DictReader(f)
    fieldnames = reader.fieldnames
    rows = list(reader)

by_company = defaultdict(list)
for r in rows:
    by_company[r["ticker"]].append(r)

rng = random.Random(SEED)
sample = []
for ticker in sorted(by_company):
    crows = by_company[ticker]
    if len(crows) <= PER_COMPANY:
        sample.extend(crows)
        continue
    strata = defaultdict(list)
    for r in crows:
        strata[(r["form"], r["section"])].append(r)
    # proportional allocation, largest remainder, min 1 per non-empty stratum
    keys = sorted(strata)
    quotas = {k: len(strata[k]) * PER_COMPANY / len(crows) for k in keys}
    alloc = {k: max(1, math.floor(quotas[k])) for k in keys}
    # trim/grow to exactly PER_COMPANY
    while sum(alloc.values()) > PER_COMPANY:
        k = max((k for k in keys if alloc[k] > 1),
                key=lambda k: alloc[k] - quotas[k])
        alloc[k] -= 1
    rem = sorted(keys, key=lambda k: quotas[k] - alloc[k], reverse=True)
    i = 0
    while sum(alloc.values()) < PER_COMPANY:
        k = rem[i % len(rem)]
        if alloc[k] < len(strata[k]):
            alloc[k] += 1
        i += 1
    for k in keys:
        pool = sorted(strata[k], key=lambda r: r["content_sha256"])
        rng.shuffle(pool)
        sample.extend(pool[: alloc[k]])

# sanity: unique ids
ids = [r["passage_id"] for r in sample]
assert len(ids) == len(set(ids)), "duplicate passage ids in sample"

blind_dir = os.path.join(OUT, "blinded")
os.makedirs(blind_dir, exist_ok=True)
manifest = []
for r in sample:
    p = os.path.join(blind_dir, r["passage_id"] + ".txt")
    with open(p, "w", encoding="utf-8") as f:
        f.write(r["text"])
    manifest.append({"id": r["passage_id"], "path": p})

with open(os.path.join(OUT, "sample_manifest.json"), "w", encoding="utf-8") as f:
    json.dump(manifest, f)

with open(os.path.join(OUT, "sample_rows.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=fieldnames)
    w.writeheader()
    w.writerows(sample)

from collections import Counter
print(f"sampled {len(sample)} passages from {len(by_company)} companies")
for t in sorted(by_company):
    n = sum(1 for r in sample if r["ticker"] == t)
    forms = Counter((r["form"], r["section"]) for r in sample if r["ticker"] == t)
    print(f"  {t:6s} {n:3d}  " + "; ".join(f"{f}/{s.split()[0]}:{c}" for (f, s), c in sorted(forms.items())))
