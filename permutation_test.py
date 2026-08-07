"""Firm-level permutation test for the between-group comparisons over the
within-document AI-risk severity measure.

WHY THIS EXISTS
---------------
Prof. Schloetzer questioned whether the between-group p-values in
firm_characteristics_test.py are computed on genuinely independent
observations. Phase-1 diagnostics settled what the unit of observation is and
what the actual problem is:

  - The unit is NOT a sentence or a passage. It is one 10-K filing
    (= one firm-year). ai_vs_other_risk_factors.py averages every AI sentence
    in a filing to a single ai_tone and every non-AI sentence to a single
    other_tone, so 59,056 sentences collapse into 150 filing-level rows with
    exactly one row per (ticker, filing_date). No test anywhere treats a
    sentence as an observation.

  - The problem is one level up: firm_characteristics_test.between_group_test()
    pools FILING-level values into two flat lists and runs Welch's t-test and
    Mann-Whitney on them with no clustering by firm. Firms contribute between
    1 and 11 filings each, and filings within a firm are highly dependent:

        lag-1 within-firm autocorrelation of within_doc_distance
            r = +0.663 (p = 4.5e-13, 93 within-firm pairs)
        one-way random-effects ICC = 0.478, mean cluster size 4.83
            -> design effect 2.83 -> effective n ~= 41, not 118
        10 of 118 scored filings carry a byte-identical ai_tone to another
            filing from the same firm (the same AI risk sentence recycled
            verbatim: Broadcom x4, Deere x3, UnitedHealth x3, Oracle x2, Uber
            x2), so those are duplicate observations rather than repeat
            measurements. Near-identical cases (Tesla 2021-2024) don't even
            show up in that count.

    Pooling filings therefore overstates the independent sample size and makes
    the filing-level p-values anticonservative.

WHAT THIS TEST DOES
-------------------
Permutes at the FIRM level, which is the level at which the grouping variable
actually varies. Each firm is first collapsed to a single value (the mean of
its own filings' within_doc_distance), so:

  - every firm counts once regardless of how many filings it has, removing the
    Oracle-has-11-filings / JPMorgan-has-1 imbalance;
  - within-firm dependence becomes irrelevant, because nothing within a firm
    is ever compared against anything else;
  - the null being tested is exactly the substantive one -- "the group label is
    unrelated to a firm's AI-risk severity" -- rather than the much stronger
    and clearly false "all 118 filings are exchangeable".

Group sizes are held fixed at their observed values; only the assignment of
labels to firms is reshuffled. The empirical p-value is the share of
permutations whose |mean difference| is >= the observed |mean difference|,
using the (r + 1) / (n + 1) convention so the p-value can never be exactly 0
(a permutation test cannot distinguish "impossible" from "rarer than 1 in
n_perm").

The observed statistic is also reported at the filing level for comparison, so
the gap between the two is visible rather than implied.

Note on power: at firm level the group sizes are small (8 vs 10 for stack
role, 5 vs 5 for centrality). With 5 vs 5 there are only C(10,5) = 252
distinct label assignments, so the smallest attainable two-sided p-value is
about 2/252 ~= 0.008 no matter how large the effect is. That floor is reported
explicitly, since it is a property of the design and not of the data. Where
the number of distinct assignments is small enough, the EXACT test over all
assignments is run instead of sampling, and it is labeled as exact.

This script writes one new CSV (permutation_test_results.csv) and modifies
nothing that already exists.

Run:
    python permutation_test.py
"""
import csv
import itertools
import math
import os
from collections import defaultdict

import numpy as np
from scipy import stats

import config
import extract_ai_sentiment as ais
import firm_characteristics_test as fct
import significance_tests as sigt

OUTPUT_PATH = os.path.join(config.EXPORT_DIR, "permutation_test_results.csv")

N_PERM = 10_000
# Below this many distinct label assignments, enumerate all of them (exact
# test) instead of sampling. C(18,8) = 43758 is comfortably enumerable.
EXACT_MAX_ASSIGNMENTS = 200_000
SEED = 20260807  # fixed so the reported p-values are reproducible


# ---------------------------------------------------------------------------
# Firm-level collapse
# ---------------------------------------------------------------------------

def firm_level_values(rows, grouping, exclude=()):
    """Collapse filings to one value per firm.

    Returns {label: {firm: mean_within_doc_distance}} plus a per-firm record of
    how many filings went into each mean, so the collapse is auditable.
    """
    per_firm = defaultdict(list)
    for r in rows:
        c = r["company"]
        if c in exclude:
            continue
        if fct.group_of(c, grouping) is None:
            continue
        per_firm[c].append(r["within_doc_distance"])

    by_label = defaultdict(dict)
    counts = {}
    for firm, vals in per_firm.items():
        by_label[fct.group_of(firm, grouping)][firm] = float(np.mean(vals))
        counts[firm] = len(vals)
    return dict(by_label), counts


# ---------------------------------------------------------------------------
# The permutation test itself
# ---------------------------------------------------------------------------

def permutation_test(group_a_vals, group_b_vals, n_perm=N_PERM, seed=SEED):
    """Two-sided permutation test on the difference in means.

    Reshuffles which firms carry which label, holding group sizes fixed.
    Enumerates every assignment when that is cheap enough (exact test),
    otherwise samples `n_perm` random assignments.
    """
    a = np.asarray(group_a_vals, dtype=float)
    b = np.asarray(group_b_vals, dtype=float)
    na, nb = len(a), len(b)
    pooled = np.concatenate([a, b])
    observed = a.mean() - b.mean()

    n_assign = math.comb(na + nb, na)
    exact = n_assign <= EXACT_MAX_ASSIGNMENTS

    diffs = []
    if exact:
        idx = np.arange(na + nb)
        for combo in itertools.combinations(idx, na):
            mask = np.zeros(na + nb, dtype=bool)
            mask[list(combo)] = True
            diffs.append(pooled[mask].mean() - pooled[~mask].mean())
        diffs = np.asarray(diffs)
        n_used = len(diffs)
    else:
        rng = np.random.default_rng(seed)
        diffs = np.empty(n_perm)
        for i in range(n_perm):
            perm = rng.permutation(pooled)
            diffs[i] = perm[:na].mean() - perm[na:].mean()
        n_used = n_perm

    n_extreme = int(np.sum(np.abs(diffs) >= abs(observed) - 1e-12))
    if exact:
        # Every assignment is enumerated, including the observed one, so the
        # count is already the exact tail probability.
        p = n_extreme / n_used
    else:
        # (r + 1) / (n + 1): the observed assignment is itself one valid
        # arrangement under the null, so a sampled p-value is never 0.
        p = (n_extreme + 1) / (n_used + 1)

    # Smallest two-sided p this design can attain, given only n_assign
    # distinct label assignments exist.
    p_floor = 2.0 / n_assign if exact else 1.0 / (n_used + 1)

    return {
        "observed_diff": float(observed),
        "n_a": na, "n_b": nb,
        "mean_a": float(a.mean()), "mean_b": float(b.mean()),
        "n_assignments": n_assign,
        "exact": exact,
        "n_used": n_used,
        "n_extreme": n_extreme,
        "p": p,
        "p_floor": p_floor,
        "perm_diff_sd": float(np.std(diffs, ddof=1)),
        "perm_diff_range": (float(diffs.min()), float(diffs.max())),
    }


def filing_level_tests(rows, grouping, exclude=()):
    """The existing filing-level Welch / Mann-Whitney numbers, recomputed here
    so the two levels sit side by side in one table."""
    return fct.between_group_test(rows, grouping, exclude_companies=exclude)


def firm_level_parametric(a, b):
    """Welch + Mann-Whitney on the FIRM-level values, for reference. These are
    not the headline -- the permutation p-value is -- but they show how much of
    the filing-level significance was coming from the inflated n rather than
    from the effect."""
    if len(a) < 2 or len(b) < 2:
        return None
    _, t_p = stats.ttest_ind(a, b, equal_var=False)
    _, u_p = stats.mannwhitneyu(a, b, alternative="two-sided")
    # Hedges-corrected Cohen's d
    na, nb = len(a), len(b)
    s = math.sqrt(((na - 1) * np.var(a, ddof=1) + (nb - 1) * np.var(b, ddof=1))
                  / (na + nb - 2))
    d = (np.mean(a) - np.mean(b)) / s if s > 0 else float("nan")
    return {"t_p": t_p, "u_p": u_p, "d": float(d)}


# ---------------------------------------------------------------------------
# Reporting
# ---------------------------------------------------------------------------

def verdict(p):
    return "SIGNIFICANT" if p < sigt.ALPHA else "not significant"


def run_comparison(title, rows, grouping, unusable, extra_exclude=frozenset(),
                   note=None):
    exclude = set(unusable) | set(extra_exclude)
    labels = list(grouping.keys())
    la, lb = labels

    print("\n" + "=" * 78)
    print(title)
    print("=" * 78)
    if note:
        for line in note:
            print("  " + line)
        print("-" * 78)

    by_label, counts = firm_level_values(rows, grouping, exclude=exclude)
    if la not in by_label or lb not in by_label:
        print("  Not enough data in one or both groups.")
        return None

    firms_a = sorted(by_label[la])
    firms_b = sorted(by_label[lb])
    a = [by_label[la][f] for f in firms_a]
    b = [by_label[lb][f] for f in firms_b]

    print(f"\n  FIRM-LEVEL COLLAPSE (each firm = mean of its own filings)")
    print(f"  {'firm':<14}{'group':<24}{'n filings':>10}{'firm mean':>12}")
    print("  " + "-" * 60)
    for f in firms_a:
        print(f"  {f:<14}{la:<24}{counts[f]:>10}{by_label[la][f]:>+12.4f}")
    for f in firms_b:
        print(f"  {f:<14}{lb:<24}{counts[f]:>10}{by_label[lb][f]:>+12.4f}")
    if exclude:
        print(f"  excluded: {', '.join(sorted(exclude))}")

    n_filings_a = sum(counts[f] for f in firms_a)
    n_filings_b = sum(counts[f] for f in firms_b)

    perm = permutation_test(a, b)
    filing = filing_level_tests(rows, grouping, exclude=exclude)
    firm_par = firm_level_parametric(a, b)

    print(f"\n  {'':<26}{la:>24}{lb:>24}")
    print(f"  {'firms':<26}{len(a):>24}{len(b):>24}")
    print(f"  {'filings behind those firms':<26}{n_filings_a:>24}"
          f"{n_filings_b:>24}")
    print(f"  {'FIRM-level mean':<26}{np.mean(a):>+24.4f}{np.mean(b):>+24.4f}")
    if filing:
        print(f"  {'FILING-level mean':<26}{filing['mean_a']:>+24.4f}"
              f"{filing['mean_b']:>+24.4f}")

    print(f"\n  Mean difference ({la} minus {lb}):")
    print(f"    at firm level:   {perm['observed_diff']:+.4f}")
    if filing:
        print(f"    at filing level: {filing['diff']:+.4f}")

    print(f"\n  {'TEST':<44}{'p':>10}{'verdict':>18}")
    print("  " + "-" * 72)
    if filing:
        print(f"  {'Welch t (FILING level, n=' + str(filing['n_a']) + '+'
                 + str(filing['n_b']) + ', unclustered)':<44}"
              f"{filing['t_p']:>10.4f}{verdict(filing['t_p']):>18}")
        print(f"  {'Mann-Whitney U (FILING level, unclustered)':<44}"
              f"{filing['u_p']:>10.4f}{verdict(filing['u_p']):>18}")
    if firm_par:
        print(f"  {'Welch t (FIRM level, n=' + str(len(a)) + '+'
                 + str(len(b)) + ')':<44}"
              f"{firm_par['t_p']:>10.4f}{verdict(firm_par['t_p']):>18}")
        print(f"  {'Mann-Whitney U (FIRM level)':<44}"
              f"{firm_par['u_p']:>10.4f}{verdict(firm_par['u_p']):>18}")
    kind = "EXACT, all assignments" if perm["exact"] else f"{perm['n_used']:,} draws"
    print(f"  {'>> PERMUTATION (FIRM level, ' + kind + ')':<44}"
          f"{perm['p']:>10.4f}{verdict(perm['p']):>18}")

    print(f"\n  Permutation detail:")
    print(f"    distinct label assignments possible: "
          f"{perm['n_assignments']:,}")
    print(f"    assignments evaluated:               {perm['n_used']:,}"
          f"{'  (exhaustive -> exact p)' if perm['exact'] else '  (random sample)'}")
    print(f"    assignments with |diff| >= observed: {perm['n_extreme']:,}")
    print(f"    null distribution of diff: sd={perm['perm_diff_sd']:.4f}, "
          f"range [{perm['perm_diff_range'][0]:+.4f}, "
          f"{perm['perm_diff_range'][1]:+.4f}]")
    print(f"    smallest p this design can reach:    {perm['p_floor']:.3g}"
          f"   <- design floor, not a data property")
    if firm_par:
        print(f"    firm-level Cohen's d: {firm_par['d']:+.3f}")

    if filing and filing["t_p"] < sigt.ALPHA and perm["p"] >= sigt.ALPHA:
        print(f"\n    >> The filing-level test is significant and the "
              f"firm-level permutation test is NOT.")
        print(f"       The filing-level result was relying on treating "
              f"{n_filings_a + n_filings_b} dependent")
        print(f"       filings as independent observations.")
    elif perm["p"] < sigt.ALPHA:
        print(f"\n    >> Survives permutation at the firm level: the group "
              f"label carries")
        print(f"       information beyond what reshuffling {len(a) + len(b)} "
              f"firms produces by chance.")

    return {
        "comparison": title.split(" -- ")[0].strip(),
        "group_a": la, "group_b": lb,
        "n_firms_a": len(a), "n_firms_b": len(b),
        "n_filings_a": n_filings_a, "n_filings_b": n_filings_b,
        "firm_mean_a": round(float(np.mean(a)), 4),
        "firm_mean_b": round(float(np.mean(b)), 4),
        "firm_diff": round(perm["observed_diff"], 4),
        "filing_mean_a": round(filing["mean_a"], 4) if filing else "",
        "filing_mean_b": round(filing["mean_b"], 4) if filing else "",
        "filing_diff": round(filing["diff"], 4) if filing else "",
        "filing_welch_p": round(filing["t_p"], 4) if filing else "",
        "filing_mwu_p": round(filing["u_p"], 4) if filing else "",
        "firm_welch_p": round(firm_par["t_p"], 4) if firm_par else "",
        "firm_mwu_p": round(firm_par["u_p"], 4) if firm_par else "",
        "firm_cohens_d": round(firm_par["d"], 3) if firm_par else "",
        "perm_p": round(perm["p"], 4),
        "perm_exact": perm["exact"],
        "perm_n_assignments": perm["n_assignments"],
        "perm_n_evaluated": perm["n_used"],
        # more decimals than the p-values: with 43,758 assignments the floor is
        # 4.6e-05, which rounds to a misleading 0.0000 at 4 dp
        "perm_p_design_floor": f"{perm['p_floor']:.3g}",
        "excluded": "; ".join(sorted(exclude)),
    }


def print_leave_one_out_relabel():
    """Per Schloetzer's critique: leave-one-out is retained but must not be
    read as independent robustness evidence."""
    print("\n" + "=" * 78)
    print("NOTE ON THE EXISTING LEAVE-ONE-OUT RESULTS")
    print("=" * 78)
    for line in LOO_RELABEL:
        print("  " + line)


LOO_RELABEL = [
    "The leave-one-out table printed by firm_characteristics_test.py is",
    "RELABELED as: 'SENSITIVITY TO INDIVIDUAL FIRM REMOVAL'.",
    "",
    "It is NOT independent robustness evidence, and should not be reported as",
    "if it were, for three reasons:",
    "",
    "  1. Every fold reuses the same filings and the same two group",
    "     definitions. The 18 folds are ~18 recomputations of one statistic on",
    "     94-98% of one dataset, so they are almost perfectly correlated with",
    "     each other and with the full-sample result. Passing all of them is",
    "     close to a restatement of the full-sample p-value, not a second",
    "     independent confirmation of it.",
    "",
    "  2. Each fold still runs the FILING-level unclustered test, so every",
    "     fold inherits the same inflated n and the same anticonservative",
    "     p-value. Repeating a biased test 18 times does not remove the bias.",
    "",
    "  3. It answers only 'does one firm drive this?'. It cannot answer 'is",
    "     this bigger than chance label assignment?' -- which is what the",
    "     permutation test above answers.",
    "",
    "What leave-one-out IS good for is exactly what its new name says:",
    "detecting single-firm dependence. A FRAGILE verdict there is still",
    "informative (it means one firm carries the result); a ROBUST verdict",
    "there is weak positive evidence at best.",
]


def main():
    if not os.path.exists(fct.WITHIN_DOC_PATH):
        print(f"[error] {fct.WITHIN_DOC_PATH} not found. "
              f"Run ai_vs_other_risk_factors.py first.")
        return

    rows, unusable, best_n_ai = fct.load_within_doc_rows()
    firms = {r["company"] for r in rows}
    print("=" * 78)
    print("FIRM-LEVEL PERMUTATION TESTS")
    print("=" * 78)
    print(f"Source: {fct.WITHIN_DOC_PATH}")
    print(f"{len(rows)} scored filings across {len(firms)} firms.")
    print(f"Permutation: {N_PERM:,} random label assignments, or exhaustive "
          f"enumeration when\n<= {EXACT_MAX_ASSIGNMENTS:,} assignments exist "
          f"(then the p-value is exact). Seed {SEED}.")
    print(f"Firms with no usable AI data (max AI sentences < "
          f"{ais.MIN_AI_SENTENCES}) are excluded,\nnot zero-filled: "
          f"{', '.join(sorted(unusable)) or 'none'}")

    out = []
    r = run_comparison(
        "GROUPING 1 -- AI centrality (does the company SELL AI?)",
        rows, fct.AI_CENTRALITY, unusable,
        note=["Pre-specified comparison (Schloetzer's original stretch goal c).",
              "This is the headline result the permutation test is meant to "
              "stress."])
    if r:
        out.append(r)

    r = run_comparison(
        "GROUPING 2 -- AI stack role (BUILD the stack vs. USE AI internally?)",
        rows, fct.AI_STACK_ROLE, unusable,
        note=["Schloetzer has redirected this comparison away from a single",
              "severity scalar and toward composition (see the Phase-3 panel).",
              "The severity test is reported here for completeness and because",
              "the firm-level p-value is what the redirect should be judged",
              "against."])
    if r:
        out.append(r)

    print("\n\n" + "#" * 78)
    print("#  POST-HOC AND EXPLORATORY BELOW THIS LINE")
    print("#" * 78)
    r = run_comparison(
        "GROUPING 3 (POST-HOC) -- Hyperscaler/Platform vs. "
        "Semiconductor/Hardware",
        rows, fct.AI_INFRA_SUBSPLIT, unusable,
        note=fct.POSTHOC_BANNER)
    if r:
        out.append(r)

    r = run_comparison(
        "GROUPING 3-S (POST-HOC, SENSITIVITY) -- same split, Tesla removed",
        rows, fct.AI_INFRA_SUBSPLIT, unusable, extra_exclude={"Tesla"},
        note=fct.POSTHOC_BANNER)
    if r:
        out.append(r)

    print_leave_one_out_relabel()

    os.makedirs(config.EXPORT_DIR, exist_ok=True)
    with open(OUTPUT_PATH, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=list(out[0].keys()))
        w.writeheader()
        for row in out:
            w.writerow(row)
    print(f"\nWritten to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
