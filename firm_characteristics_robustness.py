"""Sensitivity of firm_characteristics_test.py's AI-core vs. AI-peripheral
result to individual firm removal: is it a genuine 5-vs-5 group effect, or
mostly Oracle and NVIDIA (the two companies whose own within-doc distance was
individually negative) being described as a group effect?

NOT INDEPENDENT ROBUSTNESS EVIDENCE -- renamed from "Robustness check" after
Prof. Schloetzer's critique, and kept consistent with the same relabeling in
firm_characteristics_test.py. Every fold here re-runs the same FILING-level
unclustered Welch/Mann-Whitney test on 80-100% of the same data, so the folds
are near-perfectly correlated with each other and all inherit the same
inflated n: 118 filings from 25 firms are treated as 118 independent
observations, when the lag-1 within-firm autocorrelation is +0.66 and the ICC
is 0.48 (effective n ~= 41). Repeating a biased test does not remove the bias.

The test that DOES address independence is the firm-level permutation test in
permutation_test.py, which collapses each firm to one value before reshuffling
group labels. It agrees with this script's verdict for AI centrality (exact
p = 0.032, and 0.032 again after dropping keyword false positives), and
disagrees sharply for the other groupings. Read that script's output alongside
this one.

Also note this script's leave-one-out is deliberately ONE-SIDED: it drops only
AI-core members and holds the AI-peripheral side fixed, because the question it
was written to answer is specifically "is this an Oracle/NVIDIA artifact?".
firm_characteristics_test.py runs the two-sided version over both groups.

Read-only diagnostic: does not modify export/ai_vs_other_risk_factors_results.csv,
export/ai_sentiment_distance_results.csv, or the AI-core/AI-peripheral group
definition itself (that classification -- Oracle, Salesforce, Microsoft, AMD,
NVIDIA vs. IBM, Dell, Verizon, Amex, UnitedHealth -- was decided a priori in
firm_characteristics_test.py and stays fixed here; this script only changes
which rows get pooled into the "AI-core" side of the comparison, never the
peripheral side, never the underlying per-company data).

Reuses firm_characteristics_test.py's data loading (load_within_doc_rows,
the same sigt/sigc collapse for sentiment_distance) and the same
Welch's t-test / Mann-Whitney U pairing already used there -- no new
statistical method, just re-pooling with companies held out.

Run:
    python firm_characteristics_robustness.py
"""
import numpy as np
from scipy import stats

import firm_characteristics_test as fct
import significance_tests as sigt
import significance_tests_collapsed as sigc

METRICS = {}


def load_metrics():
    """Return (within_doc_rows, collapsed_sentiment_distance_rows), each row a
    dict with at least company_short and the metric value, exactly as
    firm_characteristics_test.py loads them.

    Note on the three call sites below that changed when
    firm_characteristics_test.py was extended to hold several grouping
    variables side by side:
      - load_within_doc_rows() now returns (rows, unusable, best_n_ai)
        rather than just rows;
      - its rows key the company as "company", not "company_short";
      - group_of() now takes the grouping to look in as a second argument,
        since AI-centrality is no longer the only scheme.
    """
    within_doc_rows, unusable, _ = fct.load_within_doc_rows()
    # Companies with too little AI language to measure are dropped rather than
    # zero-filled, matching firm_characteristics_test.py. None of them are in
    # the AI-core/AI-peripheral groups today, but filtering here keeps the two
    # scripts from silently diverging if that changes.
    within_doc_rows = [dict(r, company_short=r["company"])
                       for r in within_doc_rows
                       if r["company"] not in unusable]

    uncollapsed = sigt.load_usable_rows()
    for r in uncollapsed:
        r["company_short"] = fct.TICKER_SHORT.get(r["ticker"], r["ticker"])
    collapsed = sigc.collapse_by_tenk(uncollapsed)
    for r in collapsed:
        r["group"] = fct.group_of(r["company_short"], fct.AI_CENTRALITY)

    return within_doc_rows, collapsed


def cohens_d(a, b):
    a, b = np.asarray(a, dtype=float), np.asarray(b, dtype=float)
    na, nb = len(a), len(b)
    if na < 2 or nb < 2:
        return float("nan")
    pooled_var = ((na - 1) * np.var(a, ddof=1) + (nb - 1) * np.var(b, ddof=1)) / (na + nb - 2)
    pooled_std = np.sqrt(pooled_var)
    if pooled_std == 0:
        return float("nan")
    return (np.mean(a) - np.mean(b)) / pooled_std


def run_test(core_vals, periph_vals):
    if len(core_vals) < 2 or len(periph_vals) < 2:
        return None
    t_stat, p_t = stats.ttest_ind(core_vals, periph_vals, equal_var=False)
    u_stat, p_u = stats.mannwhitneyu(core_vals, periph_vals, alternative="two-sided")
    return {
        "n_core": len(core_vals), "n_periph": len(periph_vals),
        "mean_core": np.mean(core_vals), "mean_periph": np.mean(periph_vals),
        "mean_diff": np.mean(core_vals) - np.mean(periph_vals),
        "t_p": p_t, "u_p": p_u, "d": cohens_d(core_vals, periph_vals),
    }


def values_for(rows, metric_key, company_set):
    return [r[metric_key] for r in rows if r["company_short"] in company_set]


def print_result(label, res):
    if res is None:
        print(f"  {label}: not enough data for a test")
        return
    print(f"  {label}")
    print(f"    n (core, periph)      = {res['n_core']}, {res['n_periph']}")
    print(f"    mean core / periph    = {res['mean_core']:+.4f} / {res['mean_periph']:+.4f}")
    print(f"    mean diff (core-periph) = {res['mean_diff']:+.4f}   Cohen's d = {res['d']:+.3f}")
    print(f"    Welch t-test p = {res['t_p']:.4f} ({sigt.sig_label(res['t_p'])})")
    print(f"    Mann-Whitney p = {res['u_p']:.4f} ({sigt.sig_label(res['u_p'])})")


def main():
    within_doc_rows, sd_rows = load_metrics()

    full_core = set(fct.AI_CENTRALITY["AI-core"])
    periph = set(fct.AI_CENTRALITY["AI-peripheral"])
    reduced_core = full_core - {"Oracle", "NVIDIA"}

    print("=" * 88)
    print("1. Oracle + NVIDIA excluded from AI-core (AI-core reduced to Microsoft, AMD, Salesforce)")
    print(f"   AI-core (reduced): {sorted(reduced_core)}")
    print(f"   AI-peripheral (unchanged): {sorted(periph)}")
    print("=" * 88)

    print("\n-- within_doc_distance (ai_tone minus other_tone) --")
    core_vals = values_for(within_doc_rows, "within_doc_distance", reduced_core)
    periph_vals = values_for(within_doc_rows, "within_doc_distance", periph)
    print_result("AI-core (reduced) vs. AI-peripheral", run_test(core_vals, periph_vals))

    print("\n-- sentiment_distance (collapsed, one row per unique 10-K) --")
    core_vals2 = values_for(sd_rows, "sentiment_distance", reduced_core)
    periph_vals2 = values_for(sd_rows, "sentiment_distance", periph)
    print_result("AI-core (reduced) vs. AI-peripheral", run_test(core_vals2, periph_vals2))

    print("\n" + "=" * 88)
    print("2. Leave-one-out: drop exactly one AI-core company at a time, re-test vs. the")
    print("   full, unchanged AI-peripheral group. AI-peripheral membership never changes.")
    print("=" * 88)

    for metric_label, rows, metric_key in [
        ("within_doc_distance", within_doc_rows, "within_doc_distance"),
        ("sentiment_distance (collapsed)", sd_rows, "sentiment_distance"),
    ]:
        print(f"\n-- {metric_label} --")
        # 27 wide, not 20: "significant / significant" is 25 characters and was
        # overflowing into the MWU p-value column.
        header = (f"  {'Dropped':<14}{'n core':>8}{'mean core':>12}{'mean diff':>12}"
                  f"{'Cohen d':>10}{'t-test p':>11}{'MWU p':>9}"
                  f"{'verdict (t / MWU)':>27}")
        print(header)
        print("  " + "-" * (len(header) - 2))

        periph_vals = values_for(rows, metric_key, periph)
        for dropped in sorted(full_core):
            kept = full_core - {dropped}
            core_vals = values_for(rows, metric_key, kept)
            res = run_test(core_vals, periph_vals)
            if res is None:
                print(f"  {dropped:<14}{'--':>8}{'--':>12}{'--':>12}{'--':>10}{'--':>11}{'--':>9}{'n/a':>27}")
                continue
            verdict = f"{sigt.sig_label(res['t_p']).split()[0]} / {sigt.sig_label(res['u_p']).split()[0]}"
            print(f"  {dropped:<14}{res['n_core']:>8}{res['mean_core']:>+12.4f}"
                  f"{res['mean_diff']:>+12.4f}{res['d']:>+10.3f}"
                  f"{res['t_p']:>11.4f}{res['u_p']:>9.4f}{verdict:>27}")

        # also show the full, unreduced 5-company baseline for reference
        core_vals_full = values_for(rows, metric_key, full_core)
        res_full = run_test(core_vals_full, periph_vals)
        if res_full:
            verdict = f"{sigt.sig_label(res_full['t_p']).split()[0]} / {sigt.sig_label(res_full['u_p']).split()[0]}"
            print(f"  {'(none, full 5)':<14}{res_full['n_core']:>8}{res_full['mean_core']:>+12.4f}"
                  f"{res_full['mean_diff']:>+12.4f}{res_full['d']:>+10.3f}"
                  f"{res_full['t_p']:>11.4f}{res_full['u_p']:>9.4f}{verdict:>27}")

    print("\n" + "=" * 88)
    print("Done. See conversation for the plain-language read on whether this is a")
    print("distributed group effect or a two-company (Oracle/NVIDIA) effect.")
    print("=" * 88)


if __name__ == "__main__":
    main()
