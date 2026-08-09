"""Firm-characteristic grouping tests over the within-document AI-risk
severity metric (ai_vs_other_risk_factors.py's output).

TWO SEPARATE GROUPING VARIABLES, deliberately kept side by side
-----------------------------------------------------------------
These are different questions about a firm, not two names for one thing, so
they are reported as two independent analyses and neither supersedes the
other. Four companies (Microsoft, NVIDIA, AMD, UnitedHealth) are members of
both schemes; that dual membership is expected and is not a labeling
conflict to be resolved by picking one.

  (1) AI centrality -- does the company SELL AI?
      Prof. Schloetzer's original stretch goal (c). Unchanged from the
      earlier 10-company run so its published numbers stay reproducible.
        AI-core:       Oracle, Salesforce, Microsoft, AMD, NVIDIA
        AI-peripheral: IBM, Dell, Verizon, Amex, UnitedHealth

  (2) AI stack role -- does the company BUILD the AI stack, or USE AI
      internally for productivity? Schloetzer's later framing, after
      Wall Street/Goldman Sachs' AI productivity taxonomy.
        AI Infrastructure:  Alphabet, Amazon, Apple, Meta, Microsoft,
                            NVIDIA, Tesla, Broadcom, AMD
                            (9 of his 10 -- TSMC files 20-F as a foreign
                            private issuer, which this pipeline can't read)
        AI Power Adopters:  Walmart, JPMorgan, Eli Lilly, Deere, Accenture,
                            S&P Global, Intuit, ServiceNow, UnitedHealth,
                            Uber

Companies in neither scheme-2 group (IBM, Oracle, Dell, Salesforce, Verizon,
Amex) simply aren't part of Schloetzer's 20-firm list and are excluded from
that comparison only.

Two kinds of exclusion, kept strictly distinct
----------------------------------------------
  - NO USABLE AI DATA: the company's 10-Ks contain too little AI risk-factor
    language to measure (no filing reaches MIN_AI_SENTENCES). Detected from
    the data rather than hardcoded. These are dropped from group means
    instead of being zero-filled, since "we can't measure it" is not the
    same as "the tone is neutral". Verification predicted Apple and Walmart;
    only APPLE actually turned out to be unusable. Walmart's Item 1A was
    being mis-extracted, and once edgar.extract_sections() was fixed its
    filings carry 2/5/10 AI sentences, so it is measured normally now.
  - KNOWN EXTRACTION BUG: this category is now EMPTY.
    ai_vs_other_risk_factors.KNOWN_EXTRACTION_BUG is an empty dict because the
    underlying defect (Accenture's page-header anchoring failure, Deere's
    2014-2018 table-of-contents truncation, Walmart's cross-reference
    mis-anchoring) was fixed in edgar.extract_sections() rather than
    suppressed. All of those filings DO reach this script now and are scored
    like any other. The machinery is kept for any future filer whose text is
    a parsing artifact: a parsing defect is a data problem, never a company
    characteristic.

Sensitivity to individual firm removal (NOT "robustness")
---------------------------------------------------------
It drops one company at a time from whichever group it belongs to and re-runs
the between-group tests, so a result that hinges entirely on one company can't
pass unnoticed (a real risk at these group sizes).

RENAMED from "leave-one-out robustness" after Prof. Schloetzer's critique.
This check is NOT independent robustness evidence and must not be reported as
if it were: every fold re-runs the SAME filing-level unclustered test on
94-98% of the SAME data, so the folds are near-perfectly correlated with each
other and all inherit the same inflated n. A FRAGILE/SENSITIVE verdict is
genuinely informative (one firm carries the result); an
INSENSITIVE verdict is weak positive evidence at best.

The test that actually addresses independence is the FIRM-LEVEL PERMUTATION
TEST in permutation_test.py, which collapses each firm to one value before
reshuffling group labels. Its verdict differs sharply from the filing-level
one here: GROUPING 1 survives (exact p=0.032) while GROUPING 2 (p=0.73) and
GROUPING 3 (p=0.11) do not. Read that script's output alongside this one.

Reuses significance_tests.py's helpers rather than reimplementing any test.
Read-only: no CSVs are modified.

Run:
    python firm_characteristics_test.py
"""
import csv
import os
from collections import defaultdict

import numpy as np
from scipy import stats

import ai_vs_other_risk_factors as avo
import config
import extract_ai_sentiment as ais
import significance_tests as sigt
import significance_tests_collapsed as sigc

WITHIN_DOC_PATH = os.path.join(
    config.EXPORT_DIR, "ai_vs_other_risk_factors_results.csv")

TICKER_SHORT = {
    "IBM": "IBM", "ORCL": "Oracle", "DELL": "Dell", "CRM": "Salesforce",
    "MSFT": "Microsoft", "AMD": "AMD", "NVDA": "NVIDIA",
    "VZ": "Verizon", "AXP": "Amex", "UNH": "UnitedHealth",
    "GOOGL": "Alphabet", "AMZN": "Amazon", "AAPL": "Apple", "META": "Meta",
    "TSLA": "Tesla", "AVGO": "Broadcom", "ACN": "Accenture", "WMT": "Walmart",
    "JPM": "JPMorgan", "LLY": "EliLilly", "DE": "Deere", "SPGI": "S&PGlobal",
    "INTU": "Intuit", "NOW": "ServiceNow", "UBER": "Uber",
}

# Grouping variable 1: does the company sell AI? (unchanged from prior run)
AI_CENTRALITY = {
    "AI-core": {"Oracle", "Salesforce", "Microsoft", "AMD", "NVIDIA"},
    "AI-peripheral": {"IBM", "Dell", "Verizon", "Amex", "UnitedHealth"},
}

# Grouping variable 2: does the company build the AI stack, or use AI?
AI_STACK_ROLE = {
    "AI Infrastructure": {"Alphabet", "Amazon", "Apple", "Meta", "Microsoft",
                          "NVIDIA", "Tesla", "Broadcom", "AMD"},
    "AI Power Adopters": {"Walmart", "JPMorgan", "EliLilly", "Deere",
                          "Accenture", "S&PGlobal", "Intuit", "ServiceNow",
                          "UnitedHealth", "Uber"},
}

GROUPINGS = [
    ("GROUPING 1 -- AI centrality (does the company SELL AI?)", AI_CENTRALITY),
    ("GROUPING 2 -- AI stack role (BUILD the stack vs. USE AI internally?)",
     AI_STACK_ROLE),
]

# ---------------------------------------------------------------------------
# POST-HOC grouping 3: splitting Schloetzer's "AI Infrastructure" group in two
# ---------------------------------------------------------------------------
# THIS IS A POST-HOC, DATA-MOTIVATED HYPOTHESIS. It exists only because
# GROUPING 2 lost significance in 15 of its 18 single-firm-removal folds, and
# per-company numbers suggested Infrastructure was not behaving as one
# population. It was NOT specified in advance, so it does not carry the same
# evidentiary weight as GROUPING 1 (which was pre-specified and does survive
# the firm-level permutation test at exact p=0.032), and every printout below
# repeats that caveat on purpose.
#
# HOW THIS SPLIT ACTUALLY FARES, so the filing-level p-values below aren't read
# alone: at the FIRM level it does NOT reach significance (exact permutation
# p=0.114, and p=0.200 with Tesla dropped). The effect size stays large
# (Cohen's d=+1.57) and the mean difference barely moves, so this is
# UNDERPOWERED rather than refuted -- 4 firms vs. 4 firms admits only 70
# distinct label assignments, which puts a hard floor of p=0.029 on any
# two-sided test of it. Treat it as suggestive and needing more firms, not as
# tested-and-failed. See permutation_test.py.
#
# Membership is fixed by business-model logic BEFORE running the test, not by
# whichever arrangement maximizes significance:
#
#   Hyperscaler/Platform -- cloud/software/platform businesses that sell AI
#     as a service or an embedded product feature, with software-like gross
#     margins and revenue that scales without unit manufacturing:
#       Alphabet, Amazon, Meta, Microsoft
#
#   Semiconductor/Hardware -- companies whose AI exposure runs through chip
#     design, manufacturing, or physical hardware production, with
#     capital-intensive margin structures tied to unit output:
#       NVIDIA, AMD, Broadcom, Tesla
#
# Sanity check that this split is not reverse-engineered from the results:
# it places AMD (+0.299, one of the most opportunity-framed companies in the
# whole dataset) in the "hardware" group and Microsoft (+0.090, near zero) in
# the "platform" group. Both assignments work AGAINST the hypothesized
# difference. A split chosen to maximize significance would have done the
# opposite.
#
# TESLA IS FLAGGED AS AMBIGUOUS -- see TESLA_AMBIGUITY_NOTE below. Because of
# that, the comparison is reported twice: once with Tesla included (following
# the business-model logic above) and once with Tesla dropped entirely, as a
# sensitivity check. Apple would arguably belong in Semiconductor/Hardware on
# this logic (it designs its own A-/M-series silicon), but it has no usable
# AI data at all (max 4 AI sentences in any filing) so it cannot enter either
# group regardless.
AI_INFRA_SUBSPLIT = {
    "Hyperscaler/Platform": {"Alphabet", "Amazon", "Meta", "Microsoft"},
    "Semiconductor/Hardware": {"NVIDIA", "AMD", "Broadcom", "Tesla"},
}

TESLA_AMBIGUITY_NOTE = [
    "TESLA CLASSIFICATION IS AMBIGUOUS -- flagged deliberately, not resolved",
    "by its score. Tesla fits the 'Semiconductor/Hardware' definition on",
    "capital intensity, physical manufacturing, and in-house inference-chip",
    "design (FSD computer, Dojo). But it is NOT a semiconductor vendor: it",
    "sells no chips to third parties, and its AI exposure is better described",
    "as APPLYING AI to a manufactured product -- which is closer to the 'AI",
    "Power Adopter' concept than to 'AI Infrastructure' at all. Tesla is the",
    "weakest conceptual fit of the nine companies in Schloetzer's",
    "Infrastructure list. It is kept in the main test because the",
    "business-model logic above admits it, and the Tesla-excluded sensitivity",
    "check below exists precisely so its ambiguity cannot drive the verdict.",
]

POSTHOC_BANNER = [
    "*** POST-HOC / EXPLORATORY -- NOT A PRE-REGISTERED COMPARISON ***",
    "This split was motivated by inspecting GROUPING 2's per-company results",
    "after the fact. Any p-value below is therefore optimistically biased by",
    "the fact that the hypothesis was chosen with the data already visible.",
    "Do NOT report this at the same confidence level as GROUPING 1.",
]

# 8-K promotional-gap metric: only these newly-added companies have real AI
# content in their earnings press releases (verified by sampling before the
# pull). Everything else in the 15-company expansion has ~zero, so no
# group-level promotional-gap comparison is computed for scheme 2 at all.
EIGHTK_USABLE_NEW = ["Amazon", "Alphabet", "S&PGlobal"]


def group_of(company, grouping):
    for label, members in grouping.items():
        if company in members:
            return label
    return None


def load_within_doc_rows():
    """Return (rows, unusable_companies, best_n_ai). A company is 'unusable'
    when none of its filings reach MIN_AI_SENTENCES AI sentences -- too little
    AI language to measure, so it's reported but kept out of group means.
    best_n_ai maps company -> the largest AI-sentence count in any one of its
    filings, so callers can print why a company was ruled unusable.

    Callers must unpack all three values; firm_characteristics_robustness.py
    and this module's own main() both do."""
    with open(WITHIN_DOC_PATH, newline="", encoding="utf-8-sig") as f:
        raw = list(csv.DictReader(f))

    best_n_ai = defaultdict(int)
    for r in raw:
        company = TICKER_SHORT.get(r["ticker"], r["ticker"])
        best_n_ai[company] = max(best_n_ai[company], int(r["n_ai_sentences"]))
    unusable = {c for c, n in best_n_ai.items() if n < ais.MIN_AI_SENTENCES}

    rows = []
    for r in raw:
        if r["within_doc_distance"] == "":
            continue
        rows.append({
            "company": TICKER_SHORT.get(r["ticker"], r["ticker"]),
            "filing_date": r["filing_date"],
            "n_ai_sentences": int(r["n_ai_sentences"]),
            "within_doc_distance": float(r["within_doc_distance"]),
            "flag": r["flag"],
        })
    return rows, unusable, best_n_ai


def per_company_stats(rows):
    """company -> dict(n, mean, t_p, w_p, n_flagged)."""
    by_company = defaultdict(list)
    flagged = defaultdict(int)
    for r in rows:
        by_company[r["company"]].append(r["within_doc_distance"])
        flagged[r["company"]] += bool(r["flag"])
    out = {}
    for company, vals in by_company.items():
        entry = {"n": len(vals), "mean": float(np.mean(vals)),
                 "n_flagged": flagged[company], "t_p": None, "w_p": None}
        if len(vals) >= 2:
            entry["t_p"] = sigt.one_sample_ttest(vals)["p"]
            w = sigt.wilcoxon_test(vals)
            entry["w_p"] = None if w["note"] else w["p"]
        out[company] = entry
    return out


def verdict(p):
    if p is None:
        return "--"
    return f"{p:.3f} {'SIG' if p < sigt.ALPHA else 'n.s.'}"


def print_per_company(rows, unusable, best_n_ai):
    stats_by_company = per_company_stats(rows)
    print("\n=== Per-company within-document severity "
          "(ai_tone minus other_tone) ===")
    print("positive = AI risk framed LESS severely than the company's other "
          "risk factors")
    print("negative = AI risk framed AS or MORE severely than its other risks")
    header = (f"{'Company':<14}{'grp1':<15}{'grp2':<20}{'n':>3}{'flagged':>9}"
              f"{'mean':>10}{'t-test':>14}{'Wilcoxon':>14}")
    print(header)
    print("-" * len(header))
    for company in sorted(stats_by_company, key=lambda c: -stats_by_company[c]["mean"]):
        s = stats_by_company[company]
        g1 = group_of(company, AI_CENTRALITY) or "-"
        g2 = group_of(company, AI_STACK_ROLE) or "-"
        note = "  << NO USABLE AI DATA" if company in unusable else ""
        print(f"{company:<14}{g1:<15}{g2:<20}{s['n']:>3}{s['n_flagged']:>9}"
              f"{s['mean']:>+10.4f}{verdict(s['t_p']):>14}"
              f"{verdict(s['w_p']):>14}{note}")

    if unusable:
        print(f"\n  Companies with NO USABLE AI DATA (max AI sentences in any "
              f"one filing < {ais.MIN_AI_SENTENCES}) -- excluded from all "
              f"group means below, NOT zero-filled:")
        for c in sorted(unusable):
            print(f"    {c:<14} max AI sentences in a single filing = "
                  f"{best_n_ai[c]}")


def between_group_test(rows, grouping, exclude_companies=(), drop_company=None):
    """Welch t-test + Mann-Whitney between the grouping's two groups."""
    labels = list(grouping.keys())
    vals = {lab: [] for lab in labels}
    for r in rows:
        c = r["company"]
        if c in exclude_companies or c == drop_company:
            continue
        lab = group_of(c, grouping)
        if lab is not None:
            vals[lab].append(r["within_doc_distance"])
    a, b = vals[labels[0]], vals[labels[1]]
    if len(a) < 2 or len(b) < 2:
        return None
    _, t_p = stats.ttest_ind(a, b, equal_var=False)
    _, u_p = stats.mannwhitneyu(a, b, alternative="two-sided")
    return {
        "labels": labels,
        "n_a": len(a), "n_b": len(b),
        "mean_a": float(np.mean(a)), "mean_b": float(np.mean(b)),
        "diff": float(np.mean(a) - np.mean(b)),
        "t_p": t_p, "u_p": u_p,
    }


def print_grouping_analysis(title, rows, grouping, unusable,
                            banner=None, extra_exclude=frozenset()):
    """`banner` prints a prominent caveat block (used to mark the post-hoc
    test). `extra_exclude` drops named companies on top of the unusable set
    (used for the Tesla-excluded sensitivity run)."""
    print("\n" + "=" * 78)
    print(title)
    print("=" * 78)
    if banner:
        for line in banner:
            print("  " + line)
        print("-" * 78)
    if extra_exclude:
        print(f"  SENSITIVITY RUN -- additionally excluded by business-model "
              f"ambiguity: {', '.join(sorted(extra_exclude))}")
    # Three exclusion reasons, kept visually distinct so none reads as
    # another: measured-but-too-little-AI-language, zero-rows-from-a-known
    # parsing bug, and deliberately-dropped-for-ambiguity (sensitivity only).
    unusable = set(unusable)
    extra_exclude = set(extra_exclude)
    all_excluded = unusable | extra_exclude
    present = {r["company"] for r in rows}
    for lab, members in grouping.items():
        included = sorted(m for m in members
                          if m not in all_excluded and m in present)
        no_data = sorted(m for m in members if m not in present)
        dropped = sorted(m for m in members if m in unusable and m in present)
        ambiguous = sorted(m for m in members
                           if m in extra_exclude and m in present)
        print(f"  {lab}:")
        print(f"     included ({len(included)}): {', '.join(included)}")
        if dropped:
            print(f"     EXCLUDED, no usable AI data ({len(dropped)}): "
                  f"{', '.join(dropped)}")
        if no_data:
            print(f"     EXCLUDED, zero scored filings -- known extraction "
                  f"bug ({len(no_data)}): {', '.join(no_data)}")
        if ambiguous:
            print(f"     EXCLUDED for this sensitivity run only, ambiguous "
                  f"business model ({len(ambiguous)}): {', '.join(ambiguous)}")

    unusable = all_excluded
    res = between_group_test(rows, grouping, exclude_companies=unusable)
    if res is None:
        print("\n  Not enough data in one or both groups for a between-group test.")
        return
    la, lb = res["labels"]
    print(f"\n  {la:<20} n={res['n_a']:>3} filings, mean={res['mean_a']:+.4f}")
    print(f"  {lb:<20} n={res['n_b']:>3} filings, mean={res['mean_b']:+.4f}")
    print(f"  Mean difference ({la} minus {lb}): {res['diff']:+.4f}")
    print(f"  Welch's t-test:      p={res['t_p']:.4f}  -> {sigt.sig_label(res['t_p'])}")
    print(f"  Mann-Whitney U test: p={res['u_p']:.4f}  -> {sigt.sig_label(res['u_p'])}")

    # Sensitivity to individual firm removal (see module docstring).
    # DELIBERATELY NOT CALLED "ROBUSTNESS": see LOO_CAVEAT.
    members = sorted((grouping[la] | grouping[lb]) - set(unusable))
    present = {r["company"] for r in rows}
    members = [m for m in members if m in present]
    print(f"\n  SENSITIVITY TO INDIVIDUAL FIRM REMOVAL (drop each company, "
          f"re-test; {len(members)} companies):")
    print(f"    NOT independent robustness evidence -- every fold re-runs the "
          f"same\n    filing-level unclustered test on 94-98% of the same "
          f"data. See\n    permutation_test.py for the firm-level test that "
          f"does address independence.")
    print(f"    {'dropped':<14}{'Welch p':>12}{'MWU p':>12}{'both still SIG?':>18}")
    print("    " + "-" * 56)
    t_ps, u_ps, all_hold = [], [], True
    for m in members:
        r2 = between_group_test(rows, grouping,
                                exclude_companies=unusable, drop_company=m)
        if r2 is None:
            print(f"    {m:<14}{'--':>12}{'--':>12}{'insufficient n':>18}")
            all_hold = False
            continue
        holds = r2["t_p"] < sigt.ALPHA and r2["u_p"] < sigt.ALPHA
        all_hold = all_hold and holds
        t_ps.append(r2["t_p"]); u_ps.append(r2["u_p"])
        print(f"    {m:<14}{r2['t_p']:>12.4f}{r2['u_p']:>12.4f}"
              f"{('yes' if holds else 'NO'):>18}")
    if t_ps:
        print(f"\n    Welch p range: {min(t_ps):.4f} - {max(t_ps):.4f}   "
              f"MWU p range: {min(u_ps):.4f} - {max(u_ps):.4f}")
        if all_hold:
            summary = ("INSENSITIVE to single-firm removal: significant on "
                       "both tests in every fold.\n       (This is weak "
                       "positive evidence only -- see the caveat above.)")
        else:
            summary = ("SENSITIVE to single-firm removal: at least one fold "
                       "loses significance\n       (see NO rows above). This "
                       "is informative -- one firm carries the result.")
        print(f"    -> {summary}")


def print_eightk_partial():
    """8-K promotional-gap: report ONLY the newly-added companies that have
    real AI content in earnings releases, explicitly as partial/exploratory.
    No group-level comparison is computed -- the data is far too thin."""
    print("\n" + "=" * 78)
    print("8-K PROMOTIONAL-GAP METRIC -- PARTIAL / EXPLORATORY ONLY")
    print("=" * 78)
    print("Verification before the pull found that outside AI-vendor tech firms,")
    print("earnings press releases contain almost no AI prose. Of the 15 newly")
    print("added companies, only these have usable AI-8-K content, so NO")
    print("Infrastructure-vs-Adopters promotional-gap group mean is computed.")

    try:
        uncollapsed = sigt.load_usable_rows()
    except FileNotFoundError:
        print("\n  [skip] ai_sentiment_distance_results.csv not found.")
        return
    for r in uncollapsed:
        r["company_short"] = TICKER_SHORT.get(r["ticker"], r["ticker"])
    collapsed = sigc.collapse_by_tenk(uncollapsed)

    by_company = defaultdict(list)
    for r in collapsed:
        by_company[r["company_short"]].append(r["sentiment_distance"])

    print(f"\n  {'Company':<14}{'unique 10-Ks':>14}{'mean 8-K-minus-10-K':>22}"
          f"{'stack role':>22}")
    print("  " + "-" * 70)
    for c in EIGHTK_USABLE_NEW:
        vals = by_company.get(c, [])
        role = group_of(c, AI_STACK_ROLE) or "-"
        if not vals:
            print(f"  {c:<14}{0:>14}{'no usable pairs':>22}{role:>22}")
            continue
        print(f"  {c:<14}{len(vals):>14}{np.mean(vals):>+22.4f}{role:>22}")
    print("\n  Interpretation: descriptive only. n is 1-3 filings per company,")
    print("  spans only one group-pair, and cannot support a group-level test.")


def main():
    if not os.path.exists(WITHIN_DOC_PATH):
        print(f"[error] {WITHIN_DOC_PATH} not found. "
              f"Run ai_vs_other_risk_factors.py first.")
        return

    rows, unusable, best_n_ai = load_within_doc_rows()
    companies = {r["company"] for r in rows}
    print(f"Loaded {len(rows)} scored 10-K filings across {len(companies)} "
          f"companies from {WITHIN_DOC_PATH}.")
    # Print what is actually true rather than a hardcoded sentence: the
    # extraction-bug suppression list is empty now that the defect was fixed in
    # edgar.extract_sections(), so Accenture and Deere 2014-2018 DO reach this
    # script. Deriving this from the live dict means it can't go stale again.
    if avo.KNOWN_EXTRACTION_BUG:
        print(f"(Filings suppressed upstream for a known extraction bug: "
              f"{', '.join(sorted(avo.KNOWN_EXTRACTION_BUG))} -- see "
              f"ai_vs_other_risk_factors.py.)")
    else:
        print("(No filings are suppressed for extraction bugs: the underlying "
              "defect was\n fixed in edgar.extract_sections(), so Accenture, "
              "Deere 2014-2018, and Walmart\n are extracted correctly and "
              "scored like any other filing.)")

    print_per_company(rows, unusable, best_n_ai)
    for title, grouping in GROUPINGS:
        print_grouping_analysis(title, rows, grouping, unusable)

    # Post-hoc grouping 3, reported twice: as specified, then with the
    # ambiguous company (Tesla) dropped. Banner repeats on both so neither
    # can be quoted out of context as a pre-registered result.
    print("\n\n" + "#" * 78)
    print("#  EVERYTHING BELOW THIS LINE IS POST-HOC AND EXPLORATORY")
    print("#" * 78)
    print()
    for line in TESLA_AMBIGUITY_NOTE:
        print("  " + line)

    print_grouping_analysis(
        "GROUPING 3 (POST-HOC) -- splitting 'AI Infrastructure': "
        "Hyperscaler/Platform vs. Semiconductor/Hardware",
        rows, AI_INFRA_SUBSPLIT, unusable, banner=POSTHOC_BANNER)

    print_grouping_analysis(
        "GROUPING 3-S (POST-HOC, SENSITIVITY) -- same split, Tesla removed "
        "for business-model ambiguity",
        rows, AI_INFRA_SUBSPLIT, unusable,
        banner=POSTHOC_BANNER, extra_exclude={"Tesla"})

    print_eightk_partial()


if __name__ == "__main__":
    main()
