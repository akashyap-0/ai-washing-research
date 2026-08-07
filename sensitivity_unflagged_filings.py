"""Sensitivity of every within-document severity result to dropping
thin-evidence filings.

WHY (RESULTS_PACKET.md OPEN ITEM #3)
------------------------------------
ai_vs_other_risk_factors.py flags a filing LOW_SENTENCE_COUNT when either its
AI subset or its non-AI subset has fewer than MIN_AI_SENTENCES (5) sentences.
A flagged filing's ai_tone is an average over 1-4 sentences, so one unusually
positive or negative sentence moves it freely.

That is not an evenly spread problem. It is concentrated in the companies the
paper leans on hardest:

    Oracle    8 of 11 scored filings flagged (7 of them at exactly 1 sentence)
    IBM       5 of  7
    Tesla     5 of  8
    Broadcom  4 of  6   (all four at exactly 1 sentence, the SAME sentence)
    Deere     4 of  6

Phase-3 work sharpened the concern: several of those single-sentence filings
are not about AI at all. Their only keyword match is an `automat*` form --
"automatic extension", "automation" -- with no AI/ML term anywhere. So for
those filings the measure is averaging one sentence that was mis-selected.

This script answers the question the packet flagged as available but unrun:
does anything change if the thin filings are dropped instead of caveated?

WHAT IT RUNS
------------
Three progressively stricter samples, each through the same tests, with no
change to any threshold, grouping, or method:

  FULL        every scored filing                          (as published)
  UNFLAGGED   drop LOW_SENTENCE_COUNT filings              (>=5 AI sentences
                                                            and >=5 other)
  UNFLAGGED+  also drop filings whose only AI keyword match is `automat*`

For each sample: the pooled one-sample test of within_doc_distance against 0,
per-company means for the companies whose exposure prompted the question, and
every between-group comparison at BOTH the filing level (as originally
published) and the firm level via the exact permutation test in
permutation_test.py.

Reading the output: the interesting question is not whether p-values move --
dropping half of Oracle's filings obviously moves them -- but whether any
VERDICT flips, and whether the surviving estimates stay in the same direction
and rough magnitude. A conclusion that only holds on thin filings is not a
conclusion.

Read-only. Writes one new CSV and modifies nothing that already exists.

Run:
    python sensitivity_unflagged_filings.py
"""
import csv
import os
from collections import defaultdict

import numpy as np

import config
import extract_ai_sentiment as ais
import firm_characteristics_test as fct
import permutation_test as pt
import significance_tests as sigt

OUTPUT_PATH = os.path.join(config.EXPORT_DIR,
                           "sensitivity_unflagged_filings.csv")
PANEL_PATH = os.path.join(config.EXPORT_DIR,
                          "risk_factor_composition_panel.csv")

# Companies whose thin-evidence exposure is what prompted OPEN ITEM #3.
FOCUS = ["Oracle", "IBM", "Tesla", "Broadcom", "Deere", "UnitedHealth", "Amex"]


def load_rows():
    """Scored within-doc rows, each tagged with its flag and whether Phase 3
    judged its AI keyword matches to be `automat*`-only."""
    automat_only = set()
    if os.path.exists(PANEL_PATH):
        with open(PANEL_PATH, newline="", encoding="utf-8-sig") as f:
            for r in csv.DictReader(f):
                if r["ai_match_automat_only"] == "yes":
                    automat_only.add((r["ticker"], r["filing_date"]))
    else:
        print(f"[warn] {PANEL_PATH} not found -- the UNFLAGGED+ sample cannot "
              f"be built. Run risk_factor_composition.py first.")

    rows = []
    with open(fct.WITHIN_DOC_PATH, newline="", encoding="utf-8-sig") as f:
        for r in csv.DictReader(f):
            if r["within_doc_distance"] == "":
                continue
            key = (r["ticker"], r["filing_date"])
            rows.append({
                "company": fct.TICKER_SHORT.get(r["ticker"], r["ticker"]),
                "ticker": r["ticker"],
                "filing_date": r["filing_date"],
                "n_ai_sentences": int(r["n_ai_sentences"]),
                "within_doc_distance": float(r["within_doc_distance"]),
                "flag": r["flag"],
                "automat_only": key in automat_only,
            })
    return rows, bool(automat_only)


def samples(rows):
    full = rows
    unflagged = [r for r in rows if not r["flag"]]
    strict = [r for r in unflagged if not r["automat_only"]]
    return [
        ("FULL (as published)", full),
        (f"UNFLAGGED (>={ais.MIN_AI_SENTENCES} AI and >="
         f"{ais.MIN_AI_SENTENCES} other sentences)", unflagged),
        ("UNFLAGGED+ (also drops automat*-only keyword matches)", strict),
    ]


def pooled_block(named_samples):
    print("\n" + "=" * 78)
    print("POOLED within_doc_distance vs. 0")
    print("=" * 78)
    print("Caveat carried forward from Phase 1: these pooled tests treat every")
    print("filing as independent. They are anticonservative at every sample")
    print("size below (ICC 0.48, effective n ~= 41 on the full sample). They")
    print("are shown because they are what the packet currently reports.")
    hdr = (f"{'sample':<52}{'n':>5}{'mean':>10}{'t p':>9}{'W p':>9}"
           f"{'verdict':>10}")
    print(hdr)
    print("-" * len(hdr))
    out = []
    for label, rs in named_samples:
        vals = [r["within_doc_distance"] for r in rs]
        if len(vals) < 2:
            print(f"{label:<52}{len(vals):>5}{'--':>10}")
            continue
        t = sigt.one_sample_ttest(vals)
        w = sigt.wilcoxon_test(vals)
        w_p = float("nan") if w["note"] else w["p"]
        both = t["p"] < sigt.ALPHA and (np.isnan(w_p) or w_p < sigt.ALPHA)
        print(f"{label:<52}{len(vals):>5}{t['mean']:>+10.4f}{t['p']:>9.4f}"
              f"{w_p:>9.4f}{('SIG' if both else 'n.s.'):>10}")
        out.append({"analysis": "pooled_vs_0", "sample": label,
                    "n": len(vals), "mean": round(t["mean"], 4),
                    "p_a": round(t["p"], 4), "p_b": round(w_p, 4),
                    "verdict": "SIG" if both else "n.s."})
    return out


def per_company_block(named_samples):
    print("\n" + "=" * 78)
    print("PER-COMPANY means -- the companies OPEN ITEM #3 named")
    print("=" * 78)
    hdr = f"{'company':<14}" + "".join(
        f"{lbl.split(' ')[0]:>22}" for lbl, _ in named_samples)
    print(hdr)
    print("-" * len(hdr))
    out = []
    for c in FOCUS:
        cells = []
        for label, rs in named_samples:
            vals = [r["within_doc_distance"] for r in rs if r["company"] == c]
            cells.append(f"{np.mean(vals):+.4f} (n={len(vals)})" if vals
                         else "-- (n=0)")
            out.append({"analysis": "per_company", "sample": label,
                        "company": c, "n": len(vals),
                        "mean": round(float(np.mean(vals)), 4) if vals else ""})
        print(f"{c:<14}" + "".join(f"{x:>22}" for x in cells))
    print("\n  A company dropping to n=0 means every one of its scored filings")
    print("  was thin. That is a finding about the company's disclosure, not a")
    print("  defect: it had no filing with 5+ AI sentences.")
    return out


def group_block(named_samples, unusable):
    print("\n" + "=" * 78)
    print("BETWEEN-GROUP COMPARISONS at both levels")
    print("=" * 78)
    out = []
    groupings = [
        ("GROUPING 1 -- AI centrality (pre-specified)", fct.AI_CENTRALITY),
        ("GROUPING 2 -- AI stack role", fct.AI_STACK_ROLE),
        ("GROUPING 3 -- Hyperscaler vs. Semi (POST-HOC)",
         fct.AI_INFRA_SUBSPLIT),
    ]
    for title, grouping in groupings:
        print(f"\n{title}")
        hdr = (f"  {'sample':<52}{'firms':>7}{'filings':>9}{'diff':>9}"
               f"{'Welch':>8}{'MWU':>8}{'PERM':>8}{'perm verdict':>14}")
        print(hdr)
        print("  " + "-" * (len(hdr) - 2))
        for label, rs in named_samples:
            filing = fct.between_group_test(rs, grouping,
                                            exclude_companies=unusable)
            by_label, counts = pt.firm_level_values(rs, grouping,
                                                    exclude=unusable)
            labs = list(grouping.keys())
            if (filing is None or labs[0] not in by_label
                    or labs[1] not in by_label
                    or len(by_label[labs[0]]) < 2 or len(by_label[labs[1]]) < 2):
                print(f"  {label:<52}{'insufficient n for a test':>55}")
                continue
            a = list(by_label[labs[0]].values())
            b = list(by_label[labs[1]].values())
            perm = pt.permutation_test(a, b)
            nf = filing["n_a"] + filing["n_b"]
            print(f"  {label:<52}{len(a)}v{len(b):<5}{nf:>9}"
                  f"{perm['observed_diff']:>+9.4f}{filing['t_p']:>8.4f}"
                  f"{filing['u_p']:>8.4f}{perm['p']:>8.4f}"
                  f"{('SIG' if perm['p'] < sigt.ALPHA else 'n.s.'):>14}")
            out.append({
                "analysis": title.split(" --")[0], "sample": label,
                "n_firms_a": len(a), "n_firms_b": len(b), "n_filings": nf,
                "firm_diff": round(perm["observed_diff"], 4),
                "filing_welch_p": round(filing["t_p"], 4),
                "filing_mwu_p": round(filing["u_p"], 4),
                "perm_p": round(perm["p"], 4),
                "perm_exact": perm["exact"],
                "verdict": "SIG" if perm["p"] < sigt.ALPHA else "n.s.",
            })
    return out


def main():
    if not os.path.exists(fct.WITHIN_DOC_PATH):
        print(f"[error] {fct.WITHIN_DOC_PATH} not found.")
        return
    rows, have_panel = load_rows()
    _, unusable, _ = fct.load_within_doc_rows()

    named = samples(rows)
    print("=" * 78)
    print("SENSITIVITY TO THIN-EVIDENCE FILINGS  (RESULTS_PACKET OPEN ITEM #3)")
    print("=" * 78)
    for label, rs in named:
        n_firms = len({r["company"] for r in rs})
        print(f"  {label:<52}{len(rs):>4} filings, {n_firms:>2} firms")
    if not have_panel:
        print("\n  [note] UNFLAGGED+ equals UNFLAGGED because the Phase-3 panel "
              "was unavailable.")

    dropped = defaultdict(lambda: [0, 0])
    for r in rows:
        if r["flag"]:
            dropped[r["company"]][0] += 1
        if r["automat_only"]:
            dropped[r["company"]][1] += 1
    print(f"\n  {'company':<14}{'thin':>6}{'automat*-only':>15}{'of scored':>11}")
    print("  " + "-" * 44)
    for c in sorted(dropped):
        tot = sum(1 for r in rows if r["company"] == c)
        print(f"  {c:<14}{dropped[c][0]:>6}{dropped[c][1]:>15}{tot:>11}")

    results = []
    results += pooled_block(named)
    results += per_company_block(named)
    results += group_block(named, unusable)

    fields = sorted({k for r in results for k in r})
    fields = (["analysis", "sample"]
              + [f for f in fields if f not in ("analysis", "sample")])
    os.makedirs(config.EXPORT_DIR, exist_ok=True)
    with open(OUTPUT_PATH, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for r in results:
            w.writerow(r)
    print(f"\nWritten to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
