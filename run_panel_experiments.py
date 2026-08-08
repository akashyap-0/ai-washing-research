"""Run prespecified descriptive, fixed-effect, interaction, and placebo tests.

This script expects a merged panel with `ticker`, `fiscal_year`, numeric
predictors/outcomes, and optional `industry` and `ai_business_role`. Outcomes
should normally be next-period variables constructed in the financial panel.
It writes one tidy row per predictor/outcome/specification and applies a
Benjamini-Hochberg false-discovery correction within each specification.
"""

import argparse
import json
import os


def split_names(value):
    return [item.strip() for item in value.split(",") if item.strip()]


def benjamini_hochberg(pvalues):
    """Return monotone BH-adjusted p-values in original order."""
    import numpy as np

    values = np.asarray(pvalues, dtype=float)
    order = np.argsort(values)
    adjusted = np.empty(len(values))
    running = 1.0
    for reverse_rank, index in enumerate(order[::-1], start=1):
        rank = len(values) - reverse_rank + 1
        running = min(running, values[index] * len(values) / rank)
        adjusted[index] = running
    return adjusted.tolist()


def fit_ols(data, outcome, predictor, controls, formula_suffix, specification,
            coefficient_term=None, extra_required=()):
    import statsmodels.formula.api as smf

    terms = [predictor] + controls
    formula = f"{outcome} ~ " + " + ".join(terms)
    if formula_suffix:
        formula += " + " + formula_suffix
    coefficient_term = coefficient_term or predictor
    columns = [outcome, predictor, "ticker", *extra_required] + controls
    used = data.dropna(subset=list(dict.fromkeys(columns))).copy()
    if len(used) < max(20, len(terms) + 5) or used["ticker"].nunique() < 5:
        return None
    result = smf.ols(formula, data=used).fit(
        cov_type="cluster", cov_kwds={"groups": used["ticker"]})
    if coefficient_term not in result.params:
        return None
    return {
        "outcome": outcome,
        "predictor": predictor,
        "specification": specification,
        "n": int(result.nobs),
        "firms": int(used["ticker"].nunique()),
        "coefficient": float(result.params[coefficient_term]),
        "std_error_clustered": float(result.bse[coefficient_term]),
        "p_value": float(result.pvalues[coefficient_term]),
        "r_squared": float(result.rsquared),
    }


def run(data, outcomes, predictors, controls):
    from scipy import stats

    results = []
    for outcome in outcomes:
        for predictor in predictors:
            pair = data[[outcome, predictor]].dropna()
            if len(pair) >= 5:
                pearson = stats.pearsonr(pair[predictor], pair[outcome])
                spearman = stats.spearmanr(pair[predictor], pair[outcome])
                results.extend([
                    {"outcome": outcome, "predictor": predictor,
                     "specification": "pearson", "n": len(pair),
                     "firms": data.loc[pair.index, "ticker"].nunique(),
                     "coefficient": float(pearson.statistic),
                     "std_error_clustered": None, "p_value": float(pearson.pvalue),
                     "r_squared": None},
                    {"outcome": outcome, "predictor": predictor,
                     "specification": "spearman", "n": len(pair),
                     "firms": data.loc[pair.index, "ticker"].nunique(),
                     "coefficient": float(spearman.statistic),
                     "std_error_clustered": None, "p_value": float(spearman.pvalue),
                     "r_squared": None},
                ])

            specifications = [
                ("year_fe", "C(fiscal_year)"),
                ("firm_year_fe", "C(ticker) + C(fiscal_year)"),
            ]
            if "industry" in data.columns:
                specifications.append(("firm_industry_year_fe",
                                       "C(ticker) + C(industry):C(fiscal_year)"))
            for name, suffix in specifications:
                fitted = fit_ols(data, outcome, predictor, controls, suffix, name)
                if fitted:
                    results.append(fitted)

            # Moderation is meaningful only if both roles are present.
            if "ai_business_role" in data.columns:
                data = data.copy()
                data["infrastructure"] = (
                    data["ai_business_role"].str.lower() == "infrastructure").astype(int)
                interaction = f"{predictor}:infrastructure"
                fitted = fit_ols(
                    data, outcome, predictor, controls,
                    f"{predictor} * infrastructure + C(ticker) + C(fiscal_year)",
                    "firm_year_fe_role_interaction", coefficient_term=interaction,
                    extra_required=("infrastructure",))
                if fitted:
                    results.append(fitted)

    by_specification = {}
    for index, result in enumerate(results):
        by_specification.setdefault(result["specification"], []).append(index)
    for indices in by_specification.values():
        adjusted = benjamini_hochberg([results[index]["p_value"] for index in indices])
        for index, value in zip(indices, adjusted):
            results[index]["p_value_bh"] = value
    return results


def main(argv=None):
    import pandas as pd

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--panel", default="derived/analysis_panel.csv")
    parser.add_argument("--outcomes", required=True,
                        help="comma-separated next-period financial outcomes")
    parser.add_argument("--predictors", required=True,
                        help="comma-separated text scores or framing gaps")
    parser.add_argument("--controls", default="",
                        help="comma-separated prespecified numeric controls")
    parser.add_argument("--output", default="derived/panel_experiments.csv")
    parser.add_argument("--metadata-output", default="derived/panel_experiments.json")
    args = parser.parse_args(argv)

    data = pd.read_csv(args.panel)
    outcomes, predictors, controls = map(
        split_names, (args.outcomes, args.predictors, args.controls))
    required = {"ticker", "fiscal_year", *outcomes, *predictors, *controls}
    missing = required - set(data.columns)
    if missing:
        raise ValueError(f"Panel is missing required columns: {sorted(missing)}")
    results = run(data, outcomes, predictors, controls)
    if not results:
        raise ValueError("No estimable tests; check sample size and missing values")

    os.makedirs(os.path.dirname(args.output) or ".", exist_ok=True)
    pd.DataFrame(results).to_csv(args.output, index=False)
    metadata = {
        "panel": args.panel,
        "outcomes": outcomes,
        "predictors": predictors,
        "controls": controls,
        "tests": len(results),
        "notes": [
            "All OLS standard errors are clustered by firm.",
            "BH correction is applied within specification across requested tests.",
            "Associations are not causal estimates.",
        ],
    }
    with open(args.metadata_output, "w", encoding="utf-8") as handle:
        json.dump(metadata, handle, indent=2, sort_keys=True)
    print(f"Wrote {len(results):,} test rows -> {args.output}")


if __name__ == "__main__":
    main()
