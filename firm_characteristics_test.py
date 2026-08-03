"""Prof. Schloetzer's stretch goal (c): does a firm characteristic -- how
central AI is to the company's current growth narrative -- predict how
severely it frames AI-specific risk relative to its own other risk factors?

With the original 4 companies (IBM, Oracle, Dell, Salesforce) there was only
n=4 to look at, not enough for any real test, just a qualitative read. This
script reuses that same read but applies it to the expanded roster (10
companies after adding Microsoft, AMD, NVIDIA, Verizon, Amex, UnitedHealth),
using the AI-core / AI-peripheral split decided *before* looking at results
(see the company-selection writeup): companies chosen because AI is central
to their current growth narrative vs. companies chosen because it's a minor,
secondary theme.

    AI-core:       Oracle, Salesforce, Microsoft, AMD, NVIDIA
    AI-peripheral: IBM, Dell, Verizon, Amex, UnitedHealth

This doesn't modify or reimplement any scoring/threshold logic. It loads
export/ai_vs_other_risk_factors_results.csv (ai_vs_other_risk_factors.py's
output, unchanged) and reuses significance_tests.py's existing
one_sample_ttest/wilcoxon_test/print_between_company_block helpers verbatim,
just applied to this new two-group split instead of per-company or IBM-vs-
Oracle. Also reuses ai_sentiment_distance_results.csv (collapsed to one row
per unique 10-K, exactly like significance_tests_collapsed.py already does)
for the same two-group comparison on the 8-K-vs-10-K distance metric.

Run:
    python firm_characteristics_test.py
"""
import csv
import os
from collections import defaultdict

import numpy as np
from scipy import stats

import config
import significance_tests as sigt
import significance_tests_collapsed as sigc

WITHIN_DOC_PATH = os.path.join(config.EXPORT_DIR, "ai_vs_other_risk_factors_results.csv")

AI_CORE = {"Oracle", "Salesforce", "Microsoft", "AMD", "NVIDIA"}
AI_PERIPHERAL = {"IBM", "Dell", "Verizon", "Amex", "UnitedHealth"}

TICKER_SHORT = {
    "IBM": "IBM", "ORCL": "Oracle", "DELL": "Dell", "CRM": "Salesforce",
    "MSFT": "Microsoft", "AMD": "AMD", "NVDA": "NVIDIA",
    "VZ": "Verizon", "AXP": "Amex", "UNH": "UnitedHealth",
}


def group_of(company_short):
    if company_short in AI_CORE:
        return "AI-core"
    if company_short in AI_PERIPHERAL:
        return "AI-peripheral"
    return None


def load_within_doc_rows():
    with open(WITHIN_DOC_PATH, newline="", encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))
    out = []
    for r in rows:
        if r["within_doc_distance"] == "":
            continue
        company_short = TICKER_SHORT.get(r["ticker"], r["ticker"])
        grp = group_of(company_short)
        if grp is None:
            continue
        out.append({
            "company_short": company_short,
            "group": grp,
            "within_doc_distance": float(r["within_doc_distance"]),
            "flag": r["flag"],
        })
    return out


def print_group_table(rows, metric_label, groups_dict):
    print(f"\n=== {metric_label}: per-company + per-group ===")
    header = f"{'Company':<14}{'group':<15}{'n':>4}{'mean':>10}"
    print(header)
    print("-" * len(header))
    for company, values in groups_dict.items():
        grp = group_of(company) or "?"
        n = len(values)
        mean = f"{np.mean(values):+.4f}" if n else "--"
        print(f"{company:<14}{grp:<15}{n:>4}{mean:>10}")


def main():
    print("=" * 78)
    print("Firm-characteristics stretch goal: AI-core vs. AI-peripheral")
    print("(grouping decided a priori from each company's public business model,")
    print(" before looking at any results -- see the company-selection writeup)")
    print(f"  AI-core:       {sorted(AI_CORE)}")
    print(f"  AI-peripheral: {sorted(AI_PERIPHERAL)}")
    print("=" * 78)

    # --- 1. within_doc_distance (AI-risk severity vs. other risks) ---
    rows = load_within_doc_rows()
    by_company = defaultdict(list)
    for r in rows:
        by_company[r["company_short"]].append(r["within_doc_distance"])
    print_group_table(rows, "within_doc_distance (ai_tone minus other_tone)", by_company)

    core_vals = [r["within_doc_distance"] for r in rows if r["group"] == "AI-core"]
    periph_vals = [r["within_doc_distance"] for r in rows if r["group"] == "AI-peripheral"]

    print(f"\n  AI-core:       n={len(core_vals)}, mean={np.mean(core_vals):+.4f}" if core_vals else "\n  AI-core: n=0")
    print(f"  AI-peripheral: n={len(periph_vals)}, mean={np.mean(periph_vals):+.4f}" if periph_vals else "  AI-peripheral: n=0")

    if len(core_vals) >= 2 and len(periph_vals) >= 2:
        t_stat, p_val = stats.ttest_ind(core_vals, periph_vals, equal_var=False)
        u_stat, p_val_u = stats.mannwhitneyu(core_vals, periph_vals, alternative="two-sided")
        print(f"\n  Mean difference (AI-core minus AI-peripheral): "
              f"{np.mean(core_vals) - np.mean(periph_vals):+.4f}")
        print(f"  Welch's t-test:      t={t_stat:.3f}  p={p_val:.3f}  -> {sigt.sig_label(p_val)}")
        print(f"  Mann-Whitney U test: U={u_stat:.3f}  p={p_val_u:.3f}  -> {sigt.sig_label(p_val_u)}")
    else:
        print("\n  Not enough data in one or both groups for a between-group test.")

    # --- 2. sentiment_distance (8-K vs 10-K), collapsed to one row per unique 10-K ---
    print("\n" + "=" * 78)
    print("Same comparison on sentiment_distance (8-K vs. 10-K AI-sentence tone),")
    print("collapsed to one row per unique 10-K (same collapse as")
    print("significance_tests_collapsed.py, to avoid the pseudo-replication problem)")
    print("=" * 78)

    uncollapsed = sigt.load_usable_rows()
    for r in uncollapsed:
        r["company_short"] = TICKER_SHORT.get(r["ticker"], r["ticker"])
    collapsed = sigc.collapse_by_tenk(uncollapsed)

    by_company2 = defaultdict(list)
    for r in collapsed:
        by_company2[r["company_short"]].append(r["sentiment_distance"])
    print_group_table(collapsed, "sentiment_distance (collapsed, one row per unique 10-K)", by_company2)

    core_vals2 = [r["sentiment_distance"] for r in collapsed if group_of(r["company_short"]) == "AI-core"]
    periph_vals2 = [r["sentiment_distance"] for r in collapsed if group_of(r["company_short"]) == "AI-peripheral"]

    print(f"\n  AI-core:       n={len(core_vals2)}, mean={np.mean(core_vals2):+.4f}" if core_vals2 else "\n  AI-core: n=0")
    print(f"  AI-peripheral: n={len(periph_vals2)}, mean={np.mean(periph_vals2):+.4f}" if periph_vals2 else "  AI-peripheral: n=0")

    if len(core_vals2) >= 2 and len(periph_vals2) >= 2:
        t_stat, p_val = stats.ttest_ind(core_vals2, periph_vals2, equal_var=False)
        u_stat, p_val_u = stats.mannwhitneyu(core_vals2, periph_vals2, alternative="two-sided")
        print(f"\n  Mean difference (AI-core minus AI-peripheral): "
              f"{np.mean(core_vals2) - np.mean(periph_vals2):+.4f}")
        print(f"  Welch's t-test:      t={t_stat:.3f}  p={p_val:.3f}  -> {sigt.sig_label(p_val)}")
        print(f"  Mann-Whitney U test: U={u_stat:.3f}  p={p_val_u:.3f}  -> {sigt.sig_label(p_val_u)}")
    else:
        print("\n  Not enough data in one or both groups for a between-group test.")


if __name__ == "__main__":
    main()
