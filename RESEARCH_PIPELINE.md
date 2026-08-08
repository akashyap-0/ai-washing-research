# AI, Workforce, and Corporate Framing Research Pipeline

## Purpose

This repository builds a reproducible company-period panel for studying whether
corporate AI adoption and AI-related workforce claims are associated with later
employment, layoffs, and operating performance. It also measures whether a
company frames the same topic differently in promotional 8-K exhibits and its
legally exposed 10-K.

The project is observational. Unless a separate identification strategy is
added, results must be described as associations, predictions, or temporal
patterns--not proof that AI caused a layoff or productivity change.

## Primary research questions

1. Does increased disclosed AI adoption predict subsequent employee growth or
   revenue per employee?
2. Does explicit AI work-replacement language predict subsequent headcount
   reductions, layoffs, restructuring charges, or lower labor intensity?
3. Is AI described more opportunistically or efficiently in 8-K earnings
   materials than in the matched 10-K?
4. Is that 8-K/10-K framing gap associated with subsequent outcomes?
5. Does the relationship differ between AI-infrastructure suppliers and AI
   adopters?

The last question is a moderation question, not a simple comparison of group
averages. Infrastructure firms differ systematically from adopters in
industry, growth, R&D, capital intensity, and baseline labor intensity.

## Unit of observation and timing

The final analytical unit is `company_id x fiscal_period_end`. CIK is the
permanent company identifier. Ticker and company name are descriptive fields.

Every 8-K is assigned to a 10-K reporting window. Until SEC `reportDate` is
available, the window is identified by its anchor 10-K accession or filing
date and is deliberately called `period_id`, not fiscal year. New collection
runs must retain `period_end` from SEC submissions so this can be replaced by
the actual fiscal year without guessing from the filing date.

Text measured in period t is normally related to outcomes in t+1. Same-period
models are descriptive because the financial outcome may predate publication
of the filing.

## Source universe

The initial universe is the intersection of companies and reporting windows
with both usable 10-K text and relevant 8-K exhibits. A later production run
should begin from a predeclared company/year manifest rather than from whatever
files happen to download successfully.

Included filing material:

- 10-K Item 1 Business
- Human Capital within Item 1
- Item 1A Risk Factors
- Item 7 MD&A
- relevant Item 8 restructuring, severance, and employee-cost notes
- 8-K Item 2.02, Item 2.05, Item 7.01, and Item 8.01 material
- relevant EX-99 earnings, prepared-remarks, and restructuring exhibits

The current exports contain Item 1A, Item 7, and EX-99 material. Broader section
coverage is an acquisition milestone, not something silently assumed to exist.

## Data layers

The pipeline is append-only across these conceptual layers:

1. `raw`: original SEC HTML, exhibits, submission metadata, URL, retrieval
   timestamp, and SHA-256 hash.
2. `sections`: extracted text with section boundaries, extraction method,
   parser version, and quality flags.
3. `passages`: normalized, section-bounded chunks with stable IDs and full
   provenance.
4. `annotations`: human labels, coder identity, rubric version, review status,
   and adjudication.
5. `predictions`: model version, probabilities, thresholds, and binary labels
   for every passage.
6. `company_period_scores`: deterministic aggregates by company, reporting
   period, form, and label.
7. `analysis_panel`: text measures merged with versioned financial outcomes.

Raw files are never overwritten. Derived data must state the parser, label
schema, and model versions that produced it.

## Passage construction

Normalization removes markup artifacts, repeated whitespace, and obvious page
noise while preserving headings, numbers, units, and substantive prose.
Passages never cross section or filing boundaries. The initial target is
roughly 80-220 words, with one-sentence overlap only when a long paragraph must
be split. A passage is retained when it contains an AI/automation term or a
workforce/productivity term. The retrieval reason is recorded so keyword
selection can be audited.

Keyword filtering creates a candidate corpus; it does not define a substantive
label. In particular, `automatic renewal` and similar uses are candidates that
the classifier should reject as unrelated.

## Annotation schema

Labels are multi-label. For example, a passage may describe both efficiency
and workforce reduction. `neutral` is derived only when no substantive label
is present; it is not a mutually exclusive fifth topic forced onto mixed text.

### Primary labels reported by form

- `ai_opportunity`: AI is presented as a commercial, strategic, growth, or
  capability opportunity. Generic praise without evidence may still be an
  opportunity-framing label but is separately marked as generic marketing.
- `ai_risk`: AI creates competitive, operational, regulatory, security,
  implementation, financial, or workforce risk for the company.
- `ai_efficiency`: AI is claimed or expected to increase output, speed,
  quality, capacity, or reduce operating cost.
- `ai_workforce_reduction`: AI or automation explicitly or strongly
  implicitly lowers labor demand, hiring, headcount, roles, or human work.

### Guardrail labels

- `ai_adoption`: AI has been deployed or is actively used. Planned exploration
  alone does not qualify.
- `ai_worker_augmentation`: AI helps employees perform work while employees
  remain part of the described process.
- `generic_ai_marketing`: positive AI language without operational evidence,
  scale, realized use, or a concrete mechanism.
- `explicit_ai_job_link`: the passage directly connects AI/automation to a
  layoff, headcount reduction, reduced hiring, or role elimination.
- `neutral`: derived when every substantive label is false.

Each annotation also records actuality (`realized`, `ongoing`, `planned`,
`hypothetical`, `unclear`), specificity (`quantified`,
`specific_unquantified`, `vague`), and causal-link strength (`explicit`,
`strongly_implied`, `co_occurring_only`, `none`). Co-occurrence of AI and a
layoff is not an explicit AI/job link.

## Annotation protocol

The gold set is stratified by form, section, firm type, company, period,
keyword family, and likely class. At least two coders independently label the
evaluation subset. Disagreements are adjudicated and retained in the audit
trail. Report label prevalence, raw agreement, and label-specific Cohen's
kappa.

Train/validation/test splitting is by company, not random passage, to prevent
near-identical company boilerplate from appearing on both sides. The existing
single-pass LLM labels may be used for rubric development or weak supervision,
but never described as human validation.

## Model

FinBERT is fine-tuned as a multi-label sequence classifier using sigmoid output
and binary cross-entropy. This differs from applying its original three-class
sentiment head. Thresholds are selected per label on the validation companies
and frozen before evaluating the held-out companies.

Report per-label precision, recall, F1, average precision, and calibration.
The rare `explicit_ai_job_link` label prioritizes precision and is always
accompanied by a human-readable evidence audit.

Sentence-transformer embeddings and vector search are auxiliary tools for
label selection, semantic retrieval, duplicate detection, and qualitative
evidence review. RAG is not used to generate the quantitative panel.

## Aggregation

For company i, reporting period t, form f, and label k, save:

- mean predicted probability across eligible passages
- share of passages above the frozen threshold
- number of distinct positive passages after overlap deduplication
- positive words divided by eligible words
- eligible passage and word counts
- share of evidence that is realized, quantified, or explicit

Primary comparisons use normalized shares or mean probabilities rather than
raw counts, which otherwise reward longer filings.

For each label k:

`framing_gap_k = score_8K_k - score_10K_k`

Positive opportunity or efficiency gaps mean the 8-K is more promotional.
Positive risk or workforce-reduction gaps mean the 8-K emphasizes those topics
more, so signs must not be collapsed into a single index without a prespecified
formula. The primary analysis reports the four gaps separately.

## Financial variables

Required join fields are CIK and fiscal period end. Every input variable must
have source, units, currency, and fiscal-period definitions.

- `revenue`: annual revenue
- `profit`: net income and, separately, operating income
- `operating_margin`: operating income / revenue
- `employees`: consistently defined year-end employee count
- `employee_growth`: log(employees_t / employees_t-1)
- `revenue_per_employee`: revenue / average employees where possible
- `revenue_per_employee_growth`: log change in revenue per employee
- `operating_expenses`: consistently defined annual operating expense
- `labor_cost`: personnel expense where separately disclosed; expected to be
  missing for many US issuers
- `layoffs_announced` and `layoffs_completed`: kept separate
- `restructuring_charges`: severance/exit/reorganization expense
- controls: log assets, revenue growth, profitability, R&D intensity, capital
  intensity, acquisition/divestiture flags, industry, and prior outcome

Revenue per employee is a proxy, not direct physical productivity. It changes
with prices, product mix, acquisitions, divestitures, and outsourcing.

## Primary statistical design

For outcome Y:

`Y(i,t+1) = beta * text_score(i,t) + controls(i,t) + firm_FE + industry_year_FE + error(i,t)`

Standard errors are clustered by firm. Infrastructure/adopter status is not
used as an unadjusted treatment. Its primary use is the interaction:

`text_score(i,t) * infrastructure(i)`

The infrastructure main effect is absorbed by firm fixed effects when the
classification does not change over time.

## Prespecified tests

### Primary

1. AI workforce-reduction score -> next-period employee growth.
2. Explicit AI/job link -> next-period layoffs or restructuring intensity.
3. AI efficiency score -> next-period revenue-per-employee growth.
4. Each 8-K/10-K framing gap -> the corresponding next-period outcome.
5. Each relationship interacted with infrastructure/adopter role.

### Robustness

- same-period versus one-period-lagged outcomes
- firm and industry-year fixed effects
- firm-clustered standard errors
- winsorized and unwinsorized outcomes
- probability, prevalence, and explicit-evidence score definitions
- exclude passages supported only by `automat*`
- exclude recycled passages or include novelty as a control
- minimum-evidence thresholds
- leave-one-firm-out estimates
- exclude semiconductor firms and mega-cap technology firms
- matched infrastructure/adopter samples
- company-held-out model evaluation
- threshold sensitivity
- correction for multiple outcomes using Benjamini-Hochberg

### Falsification and diagnostic tests

- future text predicting past outcomes (lead/placebo test)
- non-AI text length predicting outcomes
- generic AI marketing versus explicit implementation
- AI adoption without workforce language versus explicit replacement
- randomized group-label permutation at firm level where applicable
- pre-trend/event-time plots around first substantive AI adoption disclosure

## Reviewer-facing limitations

- Disclosure is not behavior; silence is not proof of no adoption.
- Reverse causality remains possible: layoffs can prompt AI framing.
- Infrastructure/adopter comparisons are confounded without within-firm and
  industry-time controls.
- Employee and labor-cost reporting is inconsistent across companies.
- Acquisitions, divestitures, and outsourcing affect headcount productivity.
- Classification error must be propagated through threshold and validation
  sensitivity checks.
- RAG answers and single-pass LLM labels are not reproducible outcome measures.

## Build order

1. Freeze company/period universe and financial merge contract.
2. Build filing manifest and retain SEC report-period metadata.
3. Save immutable HTML and extract the expanded section set.
4. Build and manually QA the passage corpus.
5. Produce and adjudicate the gold annotation set.
6. Fine-tune and evaluate the multi-label classifier by held-out company.
7. Score all passages and deterministically aggregate company-period measures.
8. Merge financial outcomes and run the prespecified tests.
9. Freeze artifacts, environment, random seeds, and a results packet.

