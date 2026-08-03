"""Construct-validity check: does FinBERT sentiment polarity -- the proxy this
paper's entire Stage 2/3 sentiment-distance methodology relies on -- actually
track something meaningful relative to a human(-style) judgment of what kind
of AI/layoffs claim a sentence is making?

Stage 1 was abandoned as the paper's primary method (Prof. Schloetzer felt
hand-labeling baked in the researcher's own judgment about what counts as
"AI-washing" language), but export/labeling_dataset.csv was kept as a planned
secondary validation set: ~1,226 sentences from IBM/Oracle/Salesforce/Dell,
meant to be hand-labeled into 4 categories -- genuine automation claim / vague
AI buzzword / efficiency framing / demand-decline framing.

IMPORTANT CAVEAT ON THE LABELS THEMSELVES: labeling_dataset.csv's own `label`
column turned out to be blank on every row (confirmed via git history -- it
was never touched after the initial commit, so the Stage-1 hand-labeling pass
was apparently never actually done or saved). No independently-collected
human labels exist anywhere in this repo or the connected Drive. Rather than
skip this validation, the user asked for a best-effort labeling pass done
directly (not by a second, independent human, and explicitly without looping
back to the professor for label adjudication). The labels used here
(export/labeling_dataset_llm_labeled.csv) are therefore LLM-generated
single-pass labels against a fixed, disclosed rubric (see that file's header
and the accompanying report) -- NOT independently verified hand labels. That
is itself a limitation on how much this validation exercise can prove: it
checks whether FinBERT tone tracks a defensible, consistent reading of these
categories, not whether it tracks independent human judgment.

This script is read-only relative to every existing pipeline file and result:
it does not modify labeling_dataset.csv, any export/*_results.csv, or any
production script. It reuses sentiment_distance.py's FinBERT loading and
extract_ai_sentiment.py's per-sentence batched scorer directly rather than
reimplementing either.

Run:
    python validate_finbert_against_labels.py
"""
import csv
import os
from collections import defaultdict

import numpy as np
from scipy import stats

import config
import extract_ai_sentiment as ais
import sentiment_distance as sd

LABELED_PATH = os.path.join(config.EXPORT_DIR, "labeling_dataset_llm_labeled.csv")

LABEL_NAMES = {
    "G": "genuine automation claim",
    "V": "vague AI buzzword",
    "E": "efficiency framing",
    "D": "demand-decline framing",
    "O": "other / not applicable",
}
LABEL_ORDER = ["G", "V", "E", "D", "O"]

ALPHA = 0.05


def load_labeled_rows():
    with open(LABELED_PATH, newline="", encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))
    for r in rows:
        if r["label"] not in LABEL_NAMES:
            raise ValueError(f"Unexpected label {r['label']!r} on sentence_id {r['sentence_id']}")
    return rows


def score_all(rows, tokenizer, model, device, label_index):
    sentences = [r["sentence"] for r in rows]
    scores = ais.score_sentences(sentences, tokenizer, model, device, label_index)
    for r, s in zip(rows, scores):
        r["finbert_tone"] = s
    return rows


def describe(values):
    values = np.asarray(values, dtype=float)
    return {
        "n": len(values), "mean": values.mean(), "std": values.std(ddof=1) if len(values) > 1 else float("nan"),
        "min": values.min(), "q1": np.percentile(values, 25), "median": np.percentile(values, 50),
        "q3": np.percentile(values, 75), "max": values.max(),
    }


def print_distribution_table(by_label):
    print("\n=== Per-category FinBERT tone distribution ===")
    header = (f"{'Category':<28}{'n':>6}{'mean':>9}{'std':>9}{'min':>8}"
              f"{'Q1':>8}{'median':>8}{'Q3':>8}{'max':>8}")
    print(header)
    print("-" * len(header))
    for code in LABEL_ORDER:
        vals = by_label.get(code, [])
        if not vals:
            print(f"{LABEL_NAMES[code]:<28}{0:>6}   (no sentences)")
            continue
        d = describe(vals)
        print(f"{LABEL_NAMES[code]:<28}{d['n']:>6}{d['mean']:>+9.4f}{d['std']:>9.4f}"
              f"{d['min']:>+8.4f}{d['q1']:>+8.4f}{d['median']:>+8.4f}{d['q3']:>+8.4f}{d['max']:>+8.4f}")


def normality_check(by_label):
    print("\n=== Normality check (Shapiro-Wilk) per category, to pick ANOVA vs. Kruskal-Wallis ===")
    all_normal = True
    for code in LABEL_ORDER:
        vals = by_label.get(code, [])
        if len(vals) < 3:
            print(f"  {LABEL_NAMES[code]:<28}n={len(vals)} -- too few for a normality test")
            continue
        stat, p = stats.shapiro(vals)
        verdict = "normal-ish" if p >= ALPHA else "NOT normal"
        if p < ALPHA:
            all_normal = False
        print(f"  {LABEL_NAMES[code]:<28}n={len(vals):<5}W={stat:.3f}  p={p:.4f}  -> {verdict}")
    return all_normal


def omnibus_tests(by_label):
    groups = [by_label[c] for c in LABEL_ORDER if by_label.get(c)]
    labels_present = [c for c in LABEL_ORDER if by_label.get(c)]
    print(f"\n=== Omnibus test across categories: {[LABEL_NAMES[c] for c in labels_present]} ===")
    f_stat, p_anova = stats.f_oneway(*groups)
    print(f"  One-way ANOVA:      F={f_stat:.3f}  p={p_anova:.4f}")
    h_stat, p_kw = stats.kruskal(*groups)
    print(f"  Kruskal-Wallis:     H={h_stat:.3f}  p={p_kw:.4f}")
    return p_anova, p_kw


def pairwise(by_label, code_a, code_b, label_a=None, label_b=None):
    a, b = by_label.get(code_a, []), by_label.get(code_b, [])
    label_a = label_a or LABEL_NAMES[code_a]
    label_b = label_b or LABEL_NAMES[code_b]
    print(f"\n-- {label_a} (n={len(a)}) vs. {label_b} (n={len(b)}) --")
    if len(a) < 2 or len(b) < 2:
        print("  Not enough data in one or both groups for a test.")
        return
    t_stat, p_t = stats.ttest_ind(a, b, equal_var=False)
    u_stat, p_u = stats.mannwhitneyu(a, b, alternative="two-sided")
    mean_diff = np.mean(a) - np.mean(b)
    pooled_std = np.sqrt((np.var(a, ddof=1) * (len(a) - 1) + np.var(b, ddof=1) * (len(b) - 1)) / (len(a) + len(b) - 2))
    d = mean_diff / pooled_std if pooled_std > 0 else float("nan")
    print(f"  mean {label_a}: {np.mean(a):+.4f}   mean {label_b}: {np.mean(b):+.4f}   diff: {mean_diff:+.4f}   Cohen's d: {d:+.3f}")
    print(f"  Welch t-test: t={t_stat:.3f}  p={p_t:.4f}   Mann-Whitney U: U={u_stat:.1f}  p={p_u:.4f}")
    sig = "SIGNIFICANT" if min(p_t, p_u) < ALPHA else "not significant"
    print(f"  -> {sig} at alpha=0.05 (using the more conservative of the two p-values)")


def print_examples(rows, n_per_category=5):
    print("\n=== Example sentences per category (first n, with FinBERT tone) ===")
    by_label_rows = defaultdict(list)
    for r in rows:
        by_label_rows[r["label"]].append(r)
    for code in LABEL_ORDER:
        examples = by_label_rows.get(code, [])[:n_per_category]
        print(f"\n-- {LABEL_NAMES[code]} (showing {len(examples)} of {len(by_label_rows.get(code, []))}) --")
        for r in examples:
            sent = r["sentence"]
            trunc = sent if len(sent) <= 200 else sent[:200].rstrip() + "..."
            print(f"  [{r['finbert_tone']:+.4f}] ({r['company'][:20]}) {trunc}")


def main():
    print("Loading labeled dataset...")
    rows = load_labeled_rows()
    print(f"Loaded {len(rows)} labeled sentences.")

    print("\nLoading FinBERT (ProsusAI/finbert)...")
    tokenizer, model, device, label_index = sd.load_finbert()
    print(f"Scoring all {len(rows)} sentences on {device}...")
    rows = score_all(rows, tokenizer, model, device, label_index)

    by_label = defaultdict(list)
    for r in rows:
        by_label[r["label"]].append(r["finbert_tone"])

    print_distribution_table(by_label)

    all_normal = normality_check(by_label)
    print(f"\n  -> {'Using ANOVA as primary (normal-ish per group)' if all_normal else 'Using Kruskal-Wallis as primary (non-normal in at least one group)'}, reporting both regardless.")

    p_anova, p_kw = omnibus_tests(by_label)
    primary_p = p_anova if all_normal else p_kw
    omnibus_sig = primary_p < ALPHA

    if omnibus_sig:
        print(f"\nOmnibus test is significant (p={primary_p:.4f} < {ALPHA}) -- running pairwise comparisons "
              f"between every pair of categories with n>=2:")
        present = [c for c in LABEL_ORDER if len(by_label.get(c, [])) >= 2]
        for i in range(len(present)):
            for j in range(i + 1, len(present)):
                pairwise(by_label, present[i], present[j])
    else:
        print(f"\nOmnibus test is NOT significant (p={primary_p:.4f} >= {ALPHA}) -- categories are not "
              f"reliably distinguishable by FinBERT tone as a group. Still running the two specific "
              f"comparisons the paper cares about most, since a non-significant omnibus doesn't rule out "
              f"a real difference between a specific pair (and the paper's key questions are about "
              f"specific pairs, not the overall omnibus):")

    print("\n" + "=" * 78)
    print("KEY QUESTION 1: genuine automation claim vs. vague AI buzzword")
    print("(both nominally AI-positive -- does FinBERT tone distinguish substantive")
    print(" AI claims from generic AI marketing language, or do both just read as positive?)")
    print("=" * 78)
    pairwise(by_label, "G", "V")

    print("\n" + "=" * 78)
    print("KEY QUESTION 2: efficiency framing vs. demand-decline framing")
    print("(the two competing explanations for layoffs at the heart of this paper's puzzle)")
    print("=" * 78)
    pairwise(by_label, "E", "D")

    print_examples(rows, n_per_category=5)

    print("\n" + "=" * 78)
    print("Done. See conversation for the full honest read on construct validity.")
    print("=" * 78)


if __name__ == "__main__":
    main()
