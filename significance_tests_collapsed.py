"""Fixes a non-independence problem in significance_tests.py: that script
treated all 99 usable 8-K/10-K pairs as independent observations, but the
fiscal-year pairing in extract_ai_sentiment.py/sentiment_distance.py matches
many 8-Ks to the same 10-K (e.g. one IBM 10-K's ai_sentiment_10k value is
repeated verbatim across every 8-K matched to it). That inflates n and can
make p-values look smaller (more "significant") than the actual amount of
independent information supports.

This script collapses to one row per unique 10-K (keyed on 10k_doc_id,
averaging sentiment_distance/ai_sentiment_10k/ai_sentiment_8k across that
10-K's matched 8-Ks) and reruns the identical battery of tests from
significance_tests.py on both the original and collapsed data, so the two
can be compared directly. Reuses significance_tests.py's data loading and
test helper functions rather than reimplementing them -- only the
collapsing step and the before/after comparison table are new.

Doesn't modify significance_tests.py, extract_ai_sentiment.py, or
analyze_ai_sentiment_results.py.

Run:
    python significance_tests_collapsed.py
"""
from collections import defaultdict

import numpy as np
from scipy import stats

import significance_tests as sigt

METRICS = ["sentiment_distance", "ai_sentiment_10k", "ai_sentiment_8k"]


def collapse_by_tenk(rows):
    """One row per unique 10-K (10k_doc_id), averaging the three metrics
    across all 8-Ks matched to it."""
    by_tenk = defaultdict(list)
    for r in rows:
        by_tenk[r["10k_doc_id"]].append(r)

    collapsed = []
    for doc_id, group in by_tenk.items():
        collapsed.append({
            "10k_doc_id": doc_id,
            "company_short": group[0]["company_short"],
            "n_8ks": len(group),
            "sentiment_distance": float(np.mean([g["sentiment_distance"] for g in group])),
            "ai_sentiment_10k": float(np.mean([g["ai_sentiment_10k"] for g in group])),
            "ai_sentiment_8k": float(np.mean([g["ai_sentiment_8k"] for g in group])),
        })
    return collapsed


def print_collapse_counts(uncollapsed, collapsed):
    print("=== Collapse summary: pairs -> unique 10-Ks, per company ===")
    header = f"{'Company':<12}{'orig pairs':>12}{'unique 10-Ks':>14}{'avg 8-Ks/10-K':>16}"
    print(header)
    print("-" * len(header))
    for c in sigt.COMPANY_ORDER:
        n_orig = sum(1 for r in uncollapsed if r["company_short"] == c)
        c_rows = [r for r in collapsed if r["company_short"] == c]
        n_collapsed = len(c_rows)
        avg_8k = n_orig / n_collapsed if n_collapsed else float("nan")
        print(f"{c:<12}{n_orig:>12}{n_collapsed:>14}{avg_8k:>16.1f}")
    print(f"{'ALL':<12}{len(uncollapsed):>12}{len(collapsed):>14}"
          f"{len(uncollapsed) / len(collapsed):>16.1f}")


def metric_groups(rows, metric):
    groups = [(c, [r[metric] for r in rows if r["company_short"] == c]) for c in sigt.COMPANY_ORDER]
    groups.append(("ALL (pooled)", [r[metric] for r in rows]))
    return groups


def gather_verdicts(rows, metric):
    """label -> (t_p, w_p) for every company + pooled, for the before/after table."""
    out = {}
    for label, values in metric_groups(rows, metric):
        if len(values) < 2:
            out[label] = (None, None)
            continue
        t_res = sigt.one_sample_ttest(values)
        w_res = sigt.wilcoxon_test(values)
        out[label] = (t_res["p"], w_res["p"] if not w_res["note"] else None)
    return out


def verdict_str(p):
    if p is None:
        return "n/a"
    return "SIG" if p < sigt.ALPHA else "n.s."


def print_before_after_table(uncollapsed, collapsed):
    print("\n=== 4. Before (uncollapsed pairs) vs. after (collapsed unique 10-Ks) ===")
    n_orig = {c: sum(1 for r in uncollapsed if r["company_short"] == c) for c in sigt.COMPANY_ORDER}
    n_orig["ALL (pooled)"] = len(uncollapsed)
    n_coll = {c: sum(1 for r in collapsed if r["company_short"] == c) for c in sigt.COMPANY_ORDER}
    n_coll["ALL (pooled)"] = len(collapsed)

    for metric in METRICS:
        before = gather_verdicts(uncollapsed, metric)
        after = gather_verdicts(collapsed, metric)
        print(f"\n  -- {metric} vs. 0 --")
        header = (f"  {'Group':<14}{'n (before->after)':>20}"
                  f"{'t-test before':>16}{'t-test after':>15}"
                  f"{'Wilcoxon before':>18}{'Wilcoxon after':>17}")
        print(header)
        print("  " + "-" * (len(header) - 2))
        for label in list(sigt.COMPANY_ORDER) + ["ALL (pooled)"]:
            nb, na = n_orig[label], n_coll[label]
            tb, wb = before[label]
            ta, wa = after[label]
            print(f"  {label:<14}{f'{nb} -> {na}':>20}"
                  f"{verdict_str(tb):>16}{verdict_str(ta):>15}"
                  f"{verdict_str(wb):>18}{verdict_str(wa):>17}")

    # IBM vs Oracle between-company comparison, before/after
    print(f"\n  -- IBM vs. Oracle, sentiment_distance (independent samples) --")
    ibm_before = [r["sentiment_distance"] for r in uncollapsed if r["company_short"] == "IBM"]
    oracle_before = [r["sentiment_distance"] for r in uncollapsed if r["company_short"] == "Oracle"]
    ibm_after = [r["sentiment_distance"] for r in collapsed if r["company_short"] == "IBM"]
    oracle_after = [r["sentiment_distance"] for r in collapsed if r["company_short"] == "Oracle"]

    _, t_p_before = stats.ttest_ind(ibm_before, oracle_before, equal_var=False)
    _, u_p_before = stats.mannwhitneyu(ibm_before, oracle_before, alternative="two-sided")
    _, t_p_after = stats.ttest_ind(ibm_after, oracle_after, equal_var=False)
    _, u_p_after = stats.mannwhitneyu(ibm_after, oracle_after, alternative="two-sided")

    print(f"  {'n (IBM, Oracle) before':<28}{len(ibm_before)}, {len(oracle_before)}")
    print(f"  {'n (IBM, Oracle) after':<28}{len(ibm_after)}, {len(oracle_after)}")
    print(f"  {'Welch t-test':<28}before={verdict_str(t_p_before)} (p={t_p_before:.3f})   "
          f"after={verdict_str(t_p_after)} (p={t_p_after:.3f})")
    print(f"  {'Mann-Whitney U':<28}before={verdict_str(u_p_before)} (p={u_p_before:.3f})   "
          f"after={verdict_str(u_p_after)} (p={u_p_after:.3f})")


def main():
    uncollapsed = sigt.load_usable_rows()
    print(f"Loaded {len(uncollapsed)} usable pairs (non-blank sentiment_distance).\n")

    collapsed = collapse_by_tenk(uncollapsed)
    print_collapse_counts(uncollapsed, collapsed)

    # 3. re-run the same battery of tests on the collapsed data
    dist_groups = metric_groups(collapsed, "sentiment_distance")
    sigt.print_one_sample_block(
        "1/2 (collapsed). sentiment_distance vs. 0, one 10-K = one observation",
        dist_groups)

    print(f"\n=== 3 (collapsed). IBM vs. Oracle: sentiment_distance, independent samples ===")
    ibm_dist = [r["sentiment_distance"] for r in collapsed if r["company_short"] == "IBM"]
    oracle_dist = [r["sentiment_distance"] for r in collapsed if r["company_short"] == "Oracle"]
    sigt.print_between_company_block(ibm_dist, oracle_dist)

    tenk_groups = metric_groups(collapsed, "ai_sentiment_10k")
    sigt.print_one_sample_block(
        "4a (collapsed). ai_sentiment_10k vs. 0", tenk_groups)

    eightk_groups = metric_groups(collapsed, "ai_sentiment_8k")
    sigt.print_one_sample_block(
        "4b (collapsed). ai_sentiment_8k vs. 0", eightk_groups)

    print(f"\n(n<{sigt.SMALL_N_CUTOFF} flagged above -- t-test normality assumption is "
          f"questionable at that sample size; prefer the Wilcoxon result there.)")

    # 4. explicit before/after comparison table
    print_before_after_table(uncollapsed, collapsed)


if __name__ == "__main__":
    main()
