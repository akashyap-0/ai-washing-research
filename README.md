# AI, Workforce, and Corporate Framing Research Pipeline

This repository builds a reproducible company-period dataset for studying how
public companies describe AI adoption, productivity, and workforce effects in
SEC filings--and whether those disclosures are associated with later changes
in employment and financial performance.

The central comparison is a matched 8-K/10-K framing gap. The same versioned
classifier and aggregation formula are applied to every ticker:

```text
filing data
    -> matched company-periods
    -> normalized, section-aware passages
    -> human annotation
    -> multi-label FinBERT classifier
    -> company-period 8-K and 10-K scores
    -> 8-K minus 10-K framing gaps
    -> financial panel
    -> fixed-effect and robustness tests
```

The complete definitions, hypotheses, annotation rules, model design,
statistical specifications, and reviewer safeguards are in
[`RESEARCH_PIPELINE.md`](RESEARCH_PIPELINE.md). Existing study results and
their caveats are documented in [`RESULTS_PACKET.md`](RESULTS_PACKET.md).

## Research questions

The pipeline is designed to test whether:

- disclosed AI adoption predicts subsequent employee or productivity changes;
- explicit AI work-replacement language predicts layoffs, headcount reduction,
  or restructuring;
- firms describe AI more opportunistically in 8-K earnings materials than in
  their legally exposed 10-K disclosures;
- a larger 8-K/10-K framing gap predicts later workforce or financial outcomes;
- those relationships differ between AI-infrastructure suppliers and AI
  adopters.

This is an observational design. Results should be described as associations,
predictions, or temporal patterns unless a separate causal identification
strategy is added.

## Current filing coverage

The collector uses public SEC EDGAR endpoints directly. It supports:

| Form | Material collected |
|---|---|
| 10-K | Item 1 Business, Item 1A Risk Factors, Item 7 MD&A, Item 8 Financial Statements and Notes |
| 8-K | Items 2.02, 2.05, 7.01, and 8.01, plus relevant EX-99 earnings and prepared-remarks exhibits |
| 10-Q | Item 1A Risk Factors; retained for the legacy workflow but not part of the primary matched design |

New EDGAR collection runs retain ticker, CIK, accession number, filing date,
SEC report-period end, form, section, source URL, and retrieval time. Existing
rows can be enriched with newly available metadata without replacing their
original text.

The current checked-in exports mainly reflect the earlier Item 1A, Item 7, and
EX-99 collection. Rerun collection to populate the expanded section coverage.

## Primary passage labels

Labels are multi-label because one passage may describe both productivity and
workforce reduction:

- `ai_opportunity`
- `ai_risk`
- `ai_efficiency`
- `ai_workforce_reduction`
- `ai_adoption`
- `ai_worker_augmentation`
- `generic_ai_marketing`
- `explicit_ai_job_link`

`neutral` is derived only when every substantive label is false. Annotations
also record actuality, specificity, and causal-link strength. Merely mentioning
AI and layoffs in the same passage does not qualify as an explicit AI/job link.

The versioned schema is defined in [`label_schema.py`](label_schema.py).

## Statistical measurement

For company `i`, reporting period `t`, and label `k`, the primary form score is
the mean classifier probability across eligible passages:

```text
form_score(i,t,k) = mean P(label k | passage j)
```

The directional framing gap is:

```text
framing_gap(i,t,k) = 8-K score(i,t,k) - 10-K score(i,t,k)
```

Opportunity, risk, efficiency, and workforce-reduction gaps remain separate;
the pipeline does not hide them inside an arbitrary composite index. Supporting
measures include positive-passage share, positive-word share, evidence count,
and eligible text volume.

Financial associations are estimated using firm and time controls, normally:

```text
outcome(i,t+1) = beta * text_measure(i,t)
               + controls(i,t)
               + firm fixed effects
               + industry-by-year fixed effects
               + error(i,t)
```

Standard errors are clustered by firm. Infrastructure/adopter status is used
as an interaction with the changing text measure, not as an unadjusted group
comparison.

## Setup

Python 3.10 or newer is recommended.

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
```

SEC requests require a descriptive user agent containing a real contact email:

```bash
export SEC_USER_AGENT="Your Name research your-email@example.com"
```

Optional configuration:

```bash
export EXPORT_DIR="./export"
export SERPER_API_KEY="your-key"                 # optional URL/snippet lookup
export GDRIVE_CREDENTIALS_PATH="credentials.json" # optional Drive upload
export GDRIVE_TOKEN_PATH="token.json"
```

Secrets, OAuth tokens, generated datasets, and trained models are ignored by
Git.

## Quick start

### 1. Download or refresh SEC data

From the repository root:

```bash
source .venv/bin/activate
export SEC_USER_AGENT="Your Name research your-email@example.com"

python3 main.py \
  --companies IBM,ORCL,DELL,CRM,MSFT,AMD,NVDA,VZ,AXP,UNH,GOOGL,AMZN,AAPL,META,TSLA,AVGO,ACN,WMT,JPM,LLY,DE,SPGI,INTU,NOW,UBER \
  --forms 10-K,8-K \
  --no-serper \
  --no-drive-upload
```

The collector deduplicates by source type, company, URL, and section. A rerun
adds new documents and fills blank metadata without overwriting existing text.

### 2. Build the matched passage corpus

```bash
python3 build_passage_dataset.py
```

This command:

- applies the predeclared ticker universe;
- excludes unapproved exploratory Palantir data;
- matches 8-Ks to 10-K reporting windows;
- keeps the same company-period universe;
- normalizes text and creates 20-220-word section-bounded passages;
- retrieves broad AI, automation, workforce, restructuring, and productivity
  candidates;
- writes an annotation sample and QA report.

Generated outputs:

```text
derived/clean_passages.csv
derived/annotation_template.csv
derived/passage_qa.json
```

The current build from checked-in exports contains 9,581 candidate passages,
23 companies, and 128 matched reporting windows. Regenerating after a fresh
EDGAR pull may change those counts.

### 3. Annotate and validate passages

Fill the label fields in a copy of `derived/annotation_template.csv`. Training
requires adjudicated labels from at least five companies.

```bash
python3 finbert_multilabel.py validate \
  --annotations path/to/adjudicated_annotations.csv
```

The validator rejects blank labels, inconsistent `neutral` values, duplicate
passage IDs, and unadjudicated rows. The existing LLM-generated legacy labels
are not treated as human validation.

### 4. Fine-tune and evaluate FinBERT

```bash
python3 finbert_multilabel.py train \
  --annotations path/to/adjudicated_annotations.csv \
  --output-dir models/finbert-ai-workforce-v1
```

Training replaces FinBERT's original sentiment head with a sigmoid multi-label
classifier. Data are split by company to reduce leakage from repeated filing
boilerplate. The model directory records:

- train, validation, and held-out companies;
- random seed and base model;
- validation-selected threshold for each label;
- held-out precision, recall, F1, and average precision;
- label-schema version and training history.

### 5. Score every passage

```bash
python3 finbert_multilabel.py score \
  --passages derived/clean_passages.csv \
  --model-dir models/finbert-ai-workforce-v1 \
  --output derived/passage_predictions.csv
```

### 6. Aggregate company-period scores and framing gaps

```bash
python3 aggregate_company_period.py \
  --predictions derived/passage_predictions.csv \
  --output derived/company_period_text_scores.csv
```

### 7. Merge structured financial data

The expected fields are shown in
[`schemas/financial_panel_template.csv`](schemas/financial_panel_template.csv).
Company-role classification fields are shown in
[`schemas/company_role_template.csv`](schemas/company_role_template.csv).

The current merge requires a unique `period_id`. It deliberately refuses to
guess a fiscal year from a 10-K filing year.

```bash
python3 merge_financial_panel.py \
  --text-scores derived/company_period_text_scores.csv \
  --financials path/to/financial_panel.csv \
  --output derived/analysis_panel.csv
```

### 8. Run panel experiments

Example:

```bash
python3 run_panel_experiments.py \
  --panel derived/analysis_panel.csv \
  --outcomes next_employee_growth,next_revenue_per_employee_growth \
  --predictors gap_ai_opportunity_mean_probability,gap_ai_workforce_reduction_mean_probability \
  --controls log_total_assets,revenue_growth,profitability,rd_intensity,capital_intensity
```

The experiment runner produces Pearson and Spearman diagnostics, year fixed
effects, firm/year fixed effects, industry-by-year specifications when
available, infrastructure-role interactions, firm-clustered standard errors,
and Benjamini-Hochberg-adjusted p-values.

## Tests

Run the local test suite with:

```bash
python3 -m unittest discover -s tests -v
python3 -m compileall -q . -x '/\.git/'
```

Tests cover passage matching and chunking, label consistency, sample-universe
protection, safe metadata enrichment, aggregation, framing-gap direction,
financial merge validation, multiple-testing correction, and fixed-effect
experiment execution.

## Repository layout

```text
RESEARCH_PIPELINE.md           full research and statistical specification
RESULTS_PACKET.md              legacy/current results with methodological caveats
main.py                        SEC/source collection orchestration
edgar.py                       SEC submissions, filings, sections, and exhibits
normalize.py                   normalized document schema
storage.py                     deduplication and CSV/JSON export
build_passage_dataset.py       matched filtering, normalization, chunking, and QA
label_schema.py                versioned multi-label annotation schema
finbert_multilabel.py          validation, training, evaluation, and scoring
aggregate_company_period.py    form scores and 8-K/10-K framing gaps
merge_financial_panel.py       strict text/financial company-period merge
run_panel_experiments.py       panel, interaction, and multiple-testing analysis
schemas/                       financial and company-role input templates
tests/                         pipeline regression tests
export/                        checked-in source and legacy result datasets
derived/                       generated passages, predictions, and panels (ignored)
models/                        trained model artifacts (ignored)
```

## Current limitations

- `edgar.recent_filings()` currently reads the SEC submissions `filings.recent`
  arrays but does not yet follow older `filings.files` archives. Complete long
  historical coverage requires that pagination step.
- Filing section boundaries are heuristic because SEC HTML varies by filer and
  year. Extraction quality must be manually audited on a stratified sample.
- Human Capital is currently contained within Item 1 rather than reliably
  separated as its own subsection.
- The collector exports normalized text but does not yet preserve an immutable
  local copy of every original HTML file and retrieval manifest.
- The checked-in annotation labels are single-pass LLM labels, not independent
  human validation. The new classifier must use adjudicated annotations.
- Labor cost and employee definitions are inconsistent across issuers.
- Disclosure measures what firms say, not necessarily what they do.
- Revenue per employee is affected by pricing, acquisitions, divestitures,
  outsourcing, and product mix; it is not direct physical productivity.
- RAG and vector search may support retrieval and audits, but they are not used
  to generate the quantitative outcome panel.

## Copyright and access boundaries

SEC filings and Challenger's public reports are public sources. The repository
does not scrape full paywalled earnings-call transcripts from providers such as
Motley Fool or Seeking Alpha. Optional Serper integration stores only search
URLs and short search-result snippets. Earnings-release and prepared-remarks
text should come from public SEC 8-K exhibits whenever possible.



New Pipeline:

1. COMPANY UNIVERSE
   25 approved tickers
   Same companies and reporting periods
        ↓
2. SEC EDGAR COLLECTION
   10-K:
   • Item 1 Business
   • Item 1A Risk Factors
   • Item 7 MD&A
   • Item 8 Financial Notes

   8-K:
   • Items 2.02, 2.05, 7.01, 8.01
   • EX-99 earnings releases
   • Prepared remarks
        ↓
3. DOCUMENT NORMALIZATION
   • Remove HTML artifacts
   • Remove page headers and page numbers
   • Preserve sections, numbers, and source metadata
   • Store CIK, ticker, accession, dates, section, and URL
        ↓
4. MATCH COMPANY PERIODS
   • Match each 8-K to its covering 10-K period
   • Exclude unmatched periods
   • Apply the same rules to every ticker
        ↓
5. PASSAGE CONSTRUCTION
   • Split text within section boundaries
   • Keep passages between 20 and 220 words
   • Generate stable passage IDs
   • Record source and retrieval reason
        ↓
6. CANDIDATE FILTERING
   Retain passages related to:
   • AI and machine learning
   • Automation
   • Employees and workforce
   • Layoffs and restructuring
   • Productivity and efficiency
        ↓
7. HUMAN ANNOTATION
   Multi-label categories:
   • AI opportunity
   • AI risk
   • AI efficiency
   • AI workforce reduction
   • AI adoption
   • Worker augmentation
   • Generic AI marketing
   • Explicit AI and job-loss connection
   • Neutral when no substantive label applies

   Additional attributes:
   • Realized, ongoing, planned, or hypothetical
   • Quantified, specific, or vague
   • Explicit, implied, or co-occurring causal link
        ↓
8. ANNOTATION REVIEW
   • Two independent coders for evaluation data
   • Resolve disagreements
   • Mark final rows as adjudicated
   • Measure coder agreement
        ↓
9. FINBERT TRAINING
   • Multi-label classifier
   • Split data by company
   • Select thresholds using validation companies
   • Test on completely held-out companies
   • Report precision, recall, F1, and average precision
        ↓
10. SCORE EVERY PASSAGE
    Output one probability and binary prediction per label
        ↓
11. AGGREGATE BY COMPANY, PERIOD, AND FORM
    For each 8-K and 10-K calculate:
    • Mean label probability
    • Positive passage share
    • Positive word share
    • Number of positive passages
    • Eligible passage and word counts
        ↓
12. CALCULATE FRAMING GAPS
    For each label:

    framing gap = 8-K score minus 10-K score

    Separate gaps for:
    • Opportunity
    • Risk
    • Efficiency
    • Workforce reduction
        ↓
13. BUILD COMPOSITION MEASURES
    • AI share of Item 1A
    • Position of AI risk factors
    • Quantitative specificity
    • Year-to-year text similarity
    • Recycled boilerplate
    • New versus repeated AI language
        ↓
14. MERGE FINANCIAL DATA
    • Revenue
    • Profit
    • Operating margin
    • Employee count
    • Employee growth
    • Revenue per employee
    • Operating expenses
    • Labor costs when available
    • Layoffs
    • Restructuring charges
    • Assets, R&D, and capital intensity
        ↓
15. BUILD COMPANY-YEAR PANEL
    One row per company and fiscal year
        ↓
16. PRIMARY STATISTICAL TESTS
    Test whether text scores and framing gaps predict:
    • Next-year employee growth
    • Next-year layoffs
    • Next-year restructuring
    • Next-year revenue per employee
    • Next-year margins and expenses

    Include:
    • Firm fixed effects
    • Industry-by-year fixed effects
    • Firm-clustered standard errors
    • Financial controls
        ↓
17. INFRASTRUCTURE VS. ADOPTER TEST
    Test whether the relationship differs by firm role:

    AI score × infrastructure indicator

    Do not rely on an unadjusted comparison of group averages
        ↓
18. ROBUSTNESS TESTS
    • Alternative score definitions
    • Minimum evidence thresholds
    • Keyword false-positive exclusion
    • Recycled-text exclusion
    • Leave-one-firm-out sensitivity
    • Firm-level permutation tests
    • Threshold sensitivity
    • Exclude semiconductor firms
    • Exclude mega-cap technology firms
    • Multiple-testing correction
        ↓
19. PLACEBO TESTS
    • Future text predicting past outcomes
    • Generic AI marketing versus substantive adoption
    • AI adoption without workforce language
    • Non-AI filing length predicting outcomes
        ↓
20. FINAL OUTPUT
    Test the AI cover-story hypothesis:

    Do companies that promote AI more heavily in 8-Ks than in 10-Ks
    subsequently experience worse workforce or financial outcomes? 
