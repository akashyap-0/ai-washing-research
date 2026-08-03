"""Robustness check on firm_characteristics_test.py's AI-core vs. AI-peripheral
result: is it a genuine 5-vs-5 group effect, or mostly Oracle and NVIDIA (the
two companies whose own within-doc distance was individually negative)
being described as a group effect?

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
    """Return {'within_doc': rows, 'sentiment_distance': rows}, each row a
    dict with at least company_short and the metric value, exactly as
    firm_characteristics_test.py loads them."""
    within_doc_rows = fct.load_within_doc_rows()

    uncollapsed = sigt.load_usable_rows()
    for r in uncollapsed:
        r["company_short"] = fct.TICKER_SHORT.get(r["ticker"], r["ticker"])
    collapsed = sigc.collapse_by_tenk(uncollapsed)
    for r in collapsed:
        r["group"] = fct.group_of(r["company_short"])

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

    full_core = set(fct.AI_CORE)
    periph = set(fct.AI_PERIPHERAL)
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
        header = (f"  {'Dropped':<14}{'n core':>8}{'mean core':>12}{'mean diff':>12}"
                  f"{'Cohen d':>10}{'t-test p':>11}{'MWU p':>9}{'verdict (t / MWU)':>20}")
        print(header)
        print("  " + "-" * (len(header) - 2))

        periph_vals = values_for(rows, metric_key, periph)
        for dropped in sorted(full_core):
            kept = full_core - {dropped}
            core_vals = values_for(rows, metric_key, kept)
            res = run_test(core_vals, periph_vals)
            if res is None:
                print(f"  {dropped:<14}{'--':>8}{'--':>12}{'--':>12}{'--':>10}{'--':>11}{'--':>9}{'n/a':>20}")
                continue
            verdict = f"{sigt.sig_label(res['t_p']).split()[0]} / {sigt.sig_label(res['u_p']).split()[0]}"
            print(f"  {dropped:<14}{res['n_core']:>8}{res['mean_core']:>+12.4f}"
                  f"{res['mean_diff']:>+12.4f}{res['d']:>+10.3f}"
                  f"{res['t_p']:>11.4f}{res['u_p']:>9.4f}{verdict:>20}")

        # also show the full, unreduced 5-company baseline for reference
        core_vals_full = values_for(rows, metric_key, full_core)
        res_full = run_test(core_vals_full, periph_vals)
        if res_full:
            verdict = f"{sigt.sig_label(res_full['t_p']).split()[0]} / {sigt.sig_label(res_full['u_p']).split()[0]}"
            print(f"  {'(none, full 5)':<14}{res_full['n_core']:>8}{res_full['mean_core']:>+12.4f}"
                  f"{res_full['mean_diff']:>+12.4f}{res_full['d']:>+10.3f}"
                  f"{res_full['t_p']:>11.4f}{res_full['u_p']:>9.4f}{verdict:>20}")

    print("\n" + "=" * 88)
    print("Done. See conversation for the plain-language read on whether this is a")
    print("distributed group effect or a two-company (Oracle/NVIDIA) effect.")
    print("=" * 88)


if __name__ == "__main__":
    main()
