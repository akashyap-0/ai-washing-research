"""Standalone significance testing over export/ai_sentiment_distance_results.csv
(the output of extract_ai_sentiment.py). Doesn't modify or re-run the pipeline
-- reads the 99 rows with a non-blank sentiment_distance and asks whether the
raw means already reported (IBM +0.48, Oracle +0.86, Dell +0.24,
Salesforce +0.70) are statistically distinguishable from zero, and from each
other, or could just be noise given how few pairs some companies have.

Tests run:
  1. One-sample t-test (sentiment_distance vs. 0), per company + pooled, with
     95% CI on the mean.
  2. Wilcoxon signed-rank test (nonparametric equivalent), per company +
     pooled -- the small-n companies (n<15) should be read from this, not
     the t-test, since the t-test's normality assumption is shaky with only
     5 data points.
  3. Independent two-sample t-test + Mann-Whitney U, IBM vs. Oracle
     sentiment_distance (the two companies with enough n to compare).
  4. One-sample t-test + Wilcoxon (ai_sentiment_10k vs. 0) and
     (ai_sentiment_8k vs. 0), per company -- is the 10-K side actually
     significantly negative and the 8-K side actually significantly
     positive, standalone, not just their difference.

Console output only, no new CSV.

Run:
    python significance_tests.py
"""
import csv
import os

import numpy as np
from scipy import stats

import config

RESULTS_PATH = os.path.join(config.EXPORT_DIR, "ai_sentiment_distance_results.csv")

TICKER_TO_NAME = {
    "IBM": "IBM", "ORCL": "Oracle", "DELL": "Dell", "CRM": "Salesforce",
    "MSFT": "Microsoft", "AMD": "AMD", "NVDA": "NVIDIA",
    "VZ": "Verizon", "AXP": "Amex", "UNH": "UnitedHealth",
}
COMPANY_ORDER = ["IBM", "Oracle", "Dell", "Salesforce",
                 "Microsoft", "AMD", "NVIDIA", "Verizon", "Amex", "UnitedHealth"]

ALPHA = 0.05
SMALL_N_CUTOFF = 15  # below this, flag the t-test's normality assumption as questionable


def load_usable_rows():
    with open(RESULTS_PATH, newline="", encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))
    usable = []
    for r in rows:
        if r["sentiment_distance"] == "":
            continue
        r["company_short"] = TICKER_TO_NAME.get(r["ticker"], r["ticker"])
        r["sentiment_distance"] = float(r["sentiment_distance"])
        r["ai_sentiment_10k"] = float(r["ai_sentiment_10k"])
        r["ai_sentiment_8k"] = float(r["ai_sentiment_8k"])
        usable.append(r)
    return usable


def sig_label(p):
    return f"significant at .05" if p < ALPHA else "not significant"


def one_sample_ttest(values):
    values = np.asarray(values, dtype=float)
    n = len(values)
    mean = values.mean()
    t_stat, p_val = stats.ttest_1samp(values, 0.0)
    if n > 1:
        sem = stats.sem(values)
        ci = stats.t.interval(0.95, df=n - 1, loc=mean, scale=sem)
    else:
        ci = (float("nan"), float("nan"))
    return {"n": n, "mean": mean, "t": t_stat, "p": p_val, "ci_low": ci[0], "ci_high": ci[1]}


def wilcoxon_test(values):
    values = np.asarray(values, dtype=float)
    nonzero = values[values != 0]
    if len(nonzero) < 1:
        return {"n": len(values), "stat": float("nan"), "p": float("nan"), "note": "all values zero"}
    try:
        stat, p_val = stats.wilcoxon(values)
        return {"n": len(values), "stat": stat, "p": p_val, "note": ""}
    except ValueError as e:
        return {"n": len(values), "stat": float("nan"), "p": float("nan"), "note": str(e)}


def print_one_sample_block(title, groups):
    """groups: list of (label, values) -- e.g. per-company + pooled."""
    print(f"\n=== {title} ===")
    header = (f"{'Group':<14}{'n':>4}{'mean':>10}{'t-stat':>10}{'p (t)':>9}"
              f"{'95% CI':>22}{'t-test verdict':>20}")
    print(header)
    print("-" * len(header))
    for label, values in groups:
        n = len(values)
        if n < 2:
            print(f"{label:<14}{n:>4}{'--':>10}{'--':>10}{'--':>9}{'--':>22}{'n<2, skipped':>20}")
            continue
        res = one_sample_ttest(values)
        ci_str = f"[{res['ci_low']:+.4f}, {res['ci_high']:+.4f}]"
        flag = " (n<15)" if n < SMALL_N_CUTOFF else ""
        print(f"{label + flag:<14}{n:>4}{res['mean']:>+10.4f}{res['t']:>10.3f}"
              f"{res['p']:>9.3f}{ci_str:>22}{sig_label(res['p']):>20}")

    print(f"\n  Wilcoxon signed-rank (nonparametric, vs. 0):")
    header2 = f"  {'Group':<14}{'n':>4}{'W-stat':>10}{'p (W)':>9}{'verdict':>20}"
    print(header2)
    print("  " + "-" * (len(header2) - 2))
    for label, values in groups:
        n = len(values)
        wres = wilcoxon_test(values)
        if wres["note"]:
            print(f"  {label:<14}{n:>4}{'--':>10}{'--':>9}{wres['note']:>20}")
            continue
        print(f"  {label:<14}{n:>4}{wres['stat']:>10.3f}{wres['p']:>9.3f}{sig_label(wres['p']):>20}")


def print_between_company_block(ibm_dist, oracle_dist):
    print(f"\n=== 3. IBM vs. Oracle: sentiment_distance, independent samples ===")
    t_stat, p_val = stats.ttest_ind(ibm_dist, oracle_dist, equal_var=False)  # Welch's, unequal n
    u_stat, p_val_u = stats.mannwhitneyu(ibm_dist, oracle_dist, alternative="two-sided")

    print(f"  IBM:    n={len(ibm_dist)}, mean={np.mean(ibm_dist):+.4f}")
    print(f"  Oracle: n={len(oracle_dist)}, mean={np.mean(oracle_dist):+.4f}")
    print(f"  Mean difference (IBM - Oracle): {np.mean(ibm_dist) - np.mean(oracle_dist):+.4f}")
    print(f"\n  Welch's t-test:      t={t_stat:.3f}  p={p_val:.3f}  -> {sig_label(p_val)}")
    print(f"  Mann-Whitney U test: U={u_stat:.3f}  p={p_val_u:.3f}  -> {sig_label(p_val_u)}")


def main():
    if not os.path.exists(RESULTS_PATH):
        print(f"[error] {RESULTS_PATH} not found. Run extract_ai_sentiment.py first.")
        return

    rows = load_usable_rows()
    print(f"Loaded {len(rows)} usable rows (non-blank sentiment_distance) from {RESULTS_PATH}.")

    by_company = {c: [r for r in rows if r["company_short"] == c] for c in COMPANY_ORDER}

    # 1 & 2: one-sample tests on sentiment_distance, per company + pooled
    dist_groups = [(c, [r["sentiment_distance"] for r in by_company[c]]) for c in COMPANY_ORDER]
    dist_groups.append(("ALL (pooled)", [r["sentiment_distance"] for r in rows]))
    print_one_sample_block(
        "1/2. sentiment_distance vs. 0 (8-K minus 10-K AI-sentence tone)", dist_groups)

    # 3: IBM vs Oracle, independent samples
    print_between_company_block(
        [r["sentiment_distance"] for r in by_company["IBM"]],
        [r["sentiment_distance"] for r in by_company["Oracle"]],
    )

    # 4: one-sample tests on ai_sentiment_10k and ai_sentiment_8k separately, per company
    tenk_groups = [(c, [r["ai_sentiment_10k"] for r in by_company[c]]) for c in COMPANY_ORDER]
    print_one_sample_block(
        "4a. ai_sentiment_10k vs. 0 (is the 10-K AI-language actually net-negative?)",
        tenk_groups)

    eightk_groups = [(c, [r["ai_sentiment_8k"] for r in by_company[c]]) for c in COMPANY_ORDER]
    print_one_sample_block(
        "4b. ai_sentiment_8k vs. 0 (is the 8-K AI-language actually net-positive?)",
        eightk_groups)

    print(f"\n(n<{SMALL_N_CUTOFF} flagged above -- t-test normality assumption is "
          f"questionable at that sample size; prefer the Wilcoxon result there.)")


if __name__ == "__main__":
    main()
