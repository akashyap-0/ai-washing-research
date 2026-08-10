# STATUS — where the code actually is against the 20-step design

Read this before touching anything.

`RESEARCH_PIPELINE.md` describes the target architecture. What is in this repo
is a **partial, ad-hoc implementation of it**, built to answer a specific set
of questions from Prof. Schloetzer, not a build-out of the 20 steps in order.
The two documents disagree, and `RESEARCH_PIPELINE.md` is the aspiration.
This file is the ground truth about what runs today.

The single most important thing to understand: **the measure the paper
currently reports is not the measure the design calls for.** The design calls
for a fine-tuned multi-label classifier (`ai_opportunity`, `ai_risk`,
`ai_efficiency`, `ai_workforce_reduction`) scoring passages, aggregated to
company-periods, merged with financials, and run through lagged panel
regressions. What exists is off-the-shelf **FinBERT 3-class sentiment
polarity** applied to sentences, differenced within a document
(`within_doc_distance = ai_tone - other_tone`), compared across firm groups.
Steps 7-9 and 14-19 are the missing middle, and nothing downstream of step 13
has real data behind it.

Status key: **DONE** = implemented and run on real data · **PARTIAL** =
implemented but incomplete, or implemented differently than designed ·
**CODE-ONLY** = code exists, never run on real data / no inputs ·
**NOT STARTED** = no implementation.

---

## The 20 steps

| # | Step | Status | Where |
|---|------|--------|-------|
| 1 | Company universe | **PARTIAL** | `extract_ai_sentiment.APPROVED_TICKERS` (25 tickers), groupings in `firm_characteristics_test.py` |
| 2 | EDGAR collection | **DONE** (10-K); PARTIAL elsewhere | `edgar.py`, `main.py`, `storage.py`, `edgar_coverage_audit.py`, `edgar_backfill_10k.py` |
| 3 | Normalization | **PARTIAL** | `normalize.py`, `edgar.extract_sections`, `risk_factor_composition.strip_page_noise` |
| 4 | Period matching | **PARTIAL** | `build_passage_dataset.py` (`period_id`), `risk_factor_composition.period_from_doc` |
| 5 | Passage construction | **CODE-ONLY** | `build_passage_dataset.py` |
| 6 | Candidate filtering | **DONE** | `extract_ai_sentiment.AI_KEYWORD_PATTERN` + `is_ai_related`; `build_passage_dataset.py` (broader net) |
| 7 | Human annotation | **NOT STARTED** | `label_schema.py` (schema only); `export/labeling_dataset.csv` is **empty of labels** |
| 8 | Annotation review | **NOT STARTED** | — |
| 9 | FinBERT training | **CODE-ONLY** | `finbert_multilabel.py` — no trained model exists |
| 10 | Scoring | **PARTIAL** (different measure) | `ai_vs_other_risk_factors.py`, `extract_ai_sentiment.py`, `sentiment_distance.py` |
| 11 | Aggregation | **PARTIAL** (different measure) | `permutation_test.firm_level_values`; designed version in `aggregate_company_period.py` is CODE-ONLY |
| 12 | Framing gaps | **PARTIAL** (1 scalar, not 4 labels) | `extract_ai_sentiment.py` (`sentiment_distance` = 8-K minus 10-K) |
| 13 | Composition measures | **DONE** | `risk_factor_composition.py` → `export/risk_factor_composition_panel.csv` |
| 14 | Financial merge | **CODE-ONLY** (no data) | `merge_financial_panel.py`, `schemas/financial_panel_template.csv` |
| 15 | Company-year panel | **PARTIAL** (text only) | `export/risk_factor_composition_panel.csv` |
| 16 | Primary tests | **NOT STARTED** as designed | `run_panel_experiments.py` is CODE-ONLY; what runs is `significance_tests*.py`, `firm_characteristics_test.py`, `permutation_test.py` |
| 17 | Infra/Adopter interaction | **NOT STARTED** as an interaction | tested today as an unadjusted group mean difference (GROUPING 2) |
| 18 | Robustness battery | **PARTIAL** | `firm_characteristics_robustness.py`, `permutation_test.py`, `sensitivity_unflagged_filings.py` |
| 19 | Placebo tests | **NOT STARTED** | only the firm-label permutation in `permutation_test.py` |
| 20 | Final output | **PARTIAL** | `RESULTS_PACKET.md`, `RESEARCH_PIPELINE.md`, this file |

---

## Step detail

**1. Company universe — PARTIAL.**
25 tickers hardcoded in `extract_ai_sentiment.APPROVED_TICKERS`, with short
names in `firm_characteristics_test.TICKER_SHORT` and three grouping variables
(`AI_CENTRALITY`, `AI_STACK_ROLE`, `AI_INFRA_SUBSPLIT`) in the same module.
Missing vs. design: it is a Python set, not a versioned company/period
manifest keyed on CIK, and it has no period dimension — the sample is
"whatever filings downloaded successfully", which `RESEARCH_PIPELINE.md`
explicitly says a production run must not do. TSMC and SAP are absent because
they file 20-F, not 10-K (documented at `extract_ai_sentiment.py:85`).

**2. EDGAR collection — DONE for 10-K, PARTIAL elsewhere.**
`edgar.py` handles ticker→CIK, filing lists, document fetch, and heuristic
section extraction; `main.py` orchestrates; `storage.Dataset` dedups on a
content-derived `doc_id` and writes `export/ai_washing_{form}.{csv,json}`.
`edgar.all_filings()` walks the older submission shards, not just the inlined
`filings.recent` block that `recent_filings()` reads (which silently truncates
history for high-volume filers).
`edgar_coverage_audit.py` reports EDGAR availability vs. what was pulled;
`edgar_backfill_10k.py` pulls the gap for the ten AI-centrality firms.
Missing vs. design layer 1: raw HTML is cached under `cache/filing_html` but
is not content-hashed, and no parser version is recorded.

**3. Normalization — PARTIAL.**
`normalize.py` maps pulled text into the storage schema.
`edgar.extract_sections` is heuristic and known-fragile;
`ai_vs_other_risk_factors.KNOWN_EXTRACTION_BUG` exists precisely because it
mis-parses specific filings, which are excluded and reported separately from
substantive exclusions. `risk_factor_composition.strip_page_noise` removes
running headers/page numbers. Missing: the design's layer-2 contract (per-row
extraction method, parser version, quality flags) exists only inside the
composition panel (`heading_method`, `position_flag`), not repo-wide.

**4. Period matching — PARTIAL, and the weakest link in the current design.**
`period_end` is retained from SEC submissions and
`risk_factor_composition.period_from_doc`/`submissions_meta` recover report
dates, but **the analysis scripts key on `filing_date`, not fiscal period.**
`build_passage_dataset.py` builds `period_id = TICKER:anchor_10k_filing_date`
and deliberately refuses to infer fiscal year from filing year — the severity
scripts have not been brought up to that standard. Anything doing year-over-year
comparison (`yoy_tfidf_cosine`, `yoy_shingle_jaccard`) inherits this.

**5. Passage construction — CODE-ONLY.**
`build_passage_dataset.py` implements section-bounded 80-220 word chunking with
stable IDs and provenance, and writes `derived/clean_passages.csv`,
`annotation_template.csv`, `passage_qa.json`. **`derived/` does not exist** —
this has never been run to a retained output. It is the entry point for steps
5-11 and is the correct place to start that work.

**6. Candidate filtering — DONE.**
Two deliberately different layers:
- `build_passage_dataset.py` uses a **broad** net (AI + automation + workforce
  + restructuring + productivity) to create annotation candidates.
- `extract_ai_sentiment.AI_KEYWORD_PATTERN` is the **narrow** AI-only pattern
  driving every severity/composition measure that is actually reported.

`extract_ai_sentiment.is_ai_related()` is the predicate every "is this AI
content?" decision now goes through. It excludes text whose only keyword hit
is an `automat*` form ("automatic extension", "automatically") with no real
AI/ML/generative-AI term co-occurring in the same sentence or subsection.
This is an **extraction-time exclusion**, not a downstream flag: such
sentences fall into the non-AI subset, and a filing left below
`MIN_AI_SENTENCES` drops out of the scored sample by the existing threshold.
`risk_factor_composition.check_automat_only_excluded()` asserts this held.
Call `is_ai_related(text)` — never `AI_KEYWORD_PATTERN.search(text)` — for any
new AI/non-AI decision.

**7. Human annotation — NOT STARTED. Do not let the file names mislead you.**
`label_schema.py` (v1.0.0) defines the multi-label schema, actuality,
specificity, and causal-link fields. But:
- `export/labeling_dataset.csv` has 1,226 sentences and its `label` column is
  **blank on all 1,226 rows** — the Stage-1 hand-labeling pass was never done.
- `export/labeling_dataset_llm_labeled.csv` has all 1,226 labels filled, but
  they are **single-pass LLM labels against a fixed rubric, not human labels**
  (see the header of `validate_finbert_against_labels.py`). They may be used
  for rubric development or weak supervision. They must never be described as
  human validation, and they are not a gold set.

No second coder, no adjudication, no Cohen's kappa, no audit trail.

**8. Annotation review — NOT STARTED.** Nothing to review yet.

**9. FinBERT training — CODE-ONLY.**
`finbert_multilabel.py` implements the designed classifier: sigmoid multi-label
head replacing FinBERT's sentiment head, company-level train/val/test split,
and it refuses unadjudicated labels. **No model has ever been trained**
(`models/` is gitignored and absent), because step 7 has not happened.

What is actually used today is a completely different thing: the stock
three-class `ProsusAI/finbert` **sentiment** head, loaded by
`sentiment_distance.load_finbert`, reduced to a net tone (positive minus
negative) per sentence. `validate_finbert_against_labels.py` checks its
construct validity against the LLM labels and finds it **cannot separate a
genuine automation claim from a vague one** (d = -0.022, p = 0.77) — it
separates promotional from hedged language, which is not the same construct.
That limitation applies to every number the paper currently reports.

**10. Scoring — PARTIAL, and a different measure than designed.**
Running today:
- `ai_vs_other_risk_factors.py` — splits each 10-K Item 1A into AI and non-AI
  sentences, FinBERT-scores both, writes `within_doc_distance` per filing to
  `export/ai_vs_other_risk_factors_results.csv`. This is the paper's headline
  measure.
- `extract_ai_sentiment.py` — the 8-K vs. 10-K AI sentiment comparison.
- `sentiment_distance.py` — document-level chunked scoring used by the above.

`finbert_multilabel.predict` exists but has no model to load.

**11. Aggregation — PARTIAL, different measure.**
The design's deterministic company-period aggregation is
`aggregate_company_period.py`, which reads `derived/passage_predictions.csv`
(does not exist) — CODE-ONLY. What actually aggregates today is
`permutation_test.firm_level_values`, collapsing each firm to the mean of its
filings before group comparison. That collapse is the thing that makes the
firm-level tests honest about non-independence (lag-1 within-firm
autocorrelation +0.66, ICC 0.48, effective n far below filing count).

**12. Framing gaps — PARTIAL.**
`extract_ai_sentiment.py` computes one scalar gap (`sentiment_distance` =
8-K AI tone minus 10-K AI tone), tested in `significance_tests.py` /
`significance_tests_collapsed.py`. The design's four separate per-label gaps
(`framing_gap_k` for opportunity / risk / efficiency / workforce reduction)
require steps 9-11 and do **not** exist. The design also warns the four signs
must not be collapsed into one index — the current single scalar is exactly
that collapse, and should be described as such.

**13. Composition measures — DONE.**
`risk_factor_composition.py` builds `export/risk_factor_composition_panel.csv`
(one row per firm-year) plus human-readable passages in
`output/risk_factor_text/*.md`. Measures: AI share of Item 1A by two
denominators (3b), ordinal position of AI risk factors raw and normalized
(3c), numeric-token density and two year-over-year recycling measures (3d),
plus SIC/industry and an EDGAR-derived size proxy. Subsection boundaries come
from HTML emphasis runs with paragraph and sentence-window fallbacks;
`heading_method` records which was used, and ordinal position is not
comparable across methods. Deliberately **not** combined into a composite
index.

**14. Financial merge — CODE-ONLY, no data.**
`merge_financial_panel.py` validates a financial file against the text scores
on `period_id` and refuses to infer fiscal year.
`schemas/financial_panel_template.csv` is the contract to fill.
**No financial data has been acquired.** Revenue/assets appear in the
composition panel as a size proxy from EDGAR company facts only — that is not
the outcome data the design needs (employees, employee growth, revenue per
employee, restructuring charges, layoffs). Market cap cannot be built from
EDGAR alone (no share price).

**15. Company-year panel — PARTIAL (text only).**
`export/risk_factor_composition_panel.csv` is a genuine firm-year panel of
text measures. The `analysis_panel` the design means — text measures joined to
versioned financial outcomes — does not exist and cannot until step 14.

**16. Primary tests — NOT STARTED as designed.**
`run_panel_experiments.py` implements OLS, fixed effects, firm-clustered
errors, interactions, and Benjamini-Hochberg correction, reading
`derived/analysis_panel.csv` — which does not exist. CODE-ONLY.

What runs today are **group-difference tests, not the prespecified lagged
regressions**: `significance_tests.py` (one-sample t / Wilcoxon),
`significance_tests_collapsed.py`, `firm_characteristics_test.py` (per-company
and between-group), `permutation_test.py` (exact firm-level permutation).
None of them test `Y(i,t+1) = beta * text_score(i,t) + controls + FE`.

**17. Infrastructure/Adopter interaction — NOT STARTED as an interaction.**
`RESEARCH_PIPELINE.md` is explicit that infrastructure/adopter status must
enter as an interaction with firm and industry-year fixed effects, not as an
unadjusted group comparison, because the two groups differ systematically in
industry, growth, R&D, and capital intensity. Today it is tested as exactly
the unadjusted comparison the design rules out (GROUPING 2 in
`permutation_test.py`), and at the firm level that comparison is null.
`run_panel_experiments.py` accepts an `ai_business_role` column for the
correct specification once a panel exists.

**18. Robustness battery — PARTIAL.**
Implemented: leave-one-firm-out (`firm_characteristics_test.py`,
`firm_characteristics_robustness.py` — note both are relabeled *sensitivity to
individual firm removal*, **not** independent robustness evidence, because
every fold re-runs the same filing-level unclustered test on 80-100% of the
same data); exact firm-level label permutation (`permutation_test.py`);
minimum-evidence threshold sensitivity (`sensitivity_unflagged_filings.py`);
the post-hoc Tesla-removed sensitivity. The design's "exclude passages
supported only by `automat*`" is now moot — it happens at extraction (step 6).

Not implemented: winsorization, same-period vs. lagged comparison, FE
specifications, BH correction across outcomes, matched infrastructure/adopter
samples, classifier threshold sensitivity, company-held-out model evaluation.

**19. Placebo tests — NOT STARTED.**
No lead/placebo test (future text predicting past outcomes), no non-AI text
length control, no pre-trend/event-time plots. All of these need a panel with
financial outcomes. The firm-label permutation in `permutation_test.py` is the
only randomization-based check that exists.

**20. Final output — PARTIAL.**
`RESULTS_PACKET.md` is the current results packet and carries the open items.
**It is out of date as of the `automat*` extraction fix and the historical
10-K backfill**: its filing counts and p-values were computed before both, so
every number in it needs re-checking against the current
`export/*.csv` before it is quoted. Reconciling it is a reporting decision,
not a code change, and has deliberately been left to a human.
`RESEARCH_PIPELINE.md` is the design. This file is the state map. There is no
frozen artifact/environment manifest; the permutation seed (20260807) is
hardcoded in `permutation_test.py` and is the only pinned randomness.

---

## Supporting code not on the 20-step path

| File | Purpose |
|------|---------|
| `spotcheck_excluded_sentences.py` | Diagnostic: sentences a wider net catches that `AI_KEYWORD_PATTERN` misses. Monkeypatches the pattern to match-anything to reuse the sentence splitter — see the note in `is_ai_related` about why that path must short-circuit. |
| `spotcheck_8k_ai_gap.py` | Same idea for 8-K text. |
| `oracle_ai_risk_sentences.py` | Dumps Oracle's matched AI risk sentences for reading. |
| `analyze_ai_sentiment_results.py` | Descriptive summary of the 8-K/10-K results. |
| `validate_finbert_against_labels.py` | Construct-validity check of FinBERT polarity against the LLM labels. Read its header before citing any FinBERT number. |
| `challenger.py`, `serper_search.py` | Challenger Gray layoff reports; earnings-call URL lookup (snippets only, for copyright). |
| `gdrive.py` | Optional export upload. |
| `tests/test_pipeline.py` | Unit tests for the step 5-16 modules (chunking, aggregation, merge validation, BH). Tests the CODE-ONLY path, so it passes without proving anything about the reported results. |

## Current data state (as of the `automat*` fix + historical backfill)

| Artifact | Count |
|---|---|
| `export/ai_washing_10-K.csv` documents | 822 (was 300) |
| 10-Ks with a usable Item 1A | 282 (was 150) |
| Filings with scoreable AI data (`within_doc_distance`) | 115 |
| Of those, surviving the thin-evidence filter (`>=5` AI **and** `>=5` other sentences) | 77 |
| Firms | 25 (Apple has no usable AI data and is excluded, not zero-filled) |

The gap between 282 and 115 is the real story of this corpus: most Item 1A
sections, especially 2006-2016, contain no AI risk-factor language at all.
Backfilling 136 historical 10-Ks added only 10 scoreable filings. That is a
finding about disclosure history, not a collection failure.

Annual reports older than roughly calendar 2006 cannot contribute at all:
Item 1A Risk Factors only became a required 10-K item for fiscal years ending
on or after 2005-12-01, so there is no section to extract. `edgar_backfill_10k.py`
draws that line explicitly (`ITEM_1A_ERA_START`) and reports the pre-Item-1A
count per company rather than skipping silently.

## Environment

Python venv at `C:\venv_gtown`. `SEC_USER_AGENT` must be set (name + email) for
anything touching EDGAR — `edgar_coverage_audit.py`, `edgar_backfill_10k.py`,
and `risk_factor_composition.py` all need it. `cache/` (~700 MB of filing HTML
and company facts), `output/`, `derived/`, `models/`, and `credentials.json`
are gitignored.

Order to re-run after any change to extraction or the corpus:

```
python ai_vs_other_risk_factors.py     # slow: FinBERT over every Item 1A sentence
python risk_factor_composition.py      # needs SEC_USER_AGENT
python permutation_test.py
python sensitivity_unflagged_filings.py
```

## If you are picking this up cold

The highest-value next step is **not** more statistics on the current measure.
It is step 5 → 7: run `build_passage_dataset.py` to produce
`derived/clean_passages.csv` and the annotation template, then get real human
labels with a second coder and adjudication. Steps 9-13 are largely written and
waiting on that. Steps 14-19 are waiting on financial data acquisition, which
is a data-purchasing decision, not a coding task.

Do not build stubs for the unstarted steps. An empty stub reads as progress.
