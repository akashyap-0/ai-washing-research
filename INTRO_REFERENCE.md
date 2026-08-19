# INTRO REFERENCE — Background/Methodology Material for the Introduction

**Purpose:** a single consolidated reference for writing the paper's Introduction/
Background section, built only from facts that are stable regardless of how the
annotation pass, panel regressions, or Prof. Schloetzer's next round of feedback
turn out. This is not a results summary — no headline p-value, effect size, or
significance verdict from the current tests appears anywhere below. Where a
number could still shift, it has been left out and flagged in the "excluded as
possibly still in flux" list at the end.

Compiled 2026-08-19 from `RESEARCH_PIPELINE.md`, `STATUS.md`, `RESULTS_PACKET.md`,
`ANNOTATION_CODEBOOK.md`, `README.md`, and the docstrings/comments of `challenger.py`,
`extract_ai_sentiment.py`, `ai_vs_other_risk_factors.py`, `sentiment_distance.py`,
`validate_finbert_against_labels.py`, `edgar_backfill_10k.py`, and `label_schema.py`.
Two facts (the Oracle citation and the raw corpus counts) were re-verified directly
against the live `export/*.csv` files rather than taken from a prior summary.

---

## 1. Research motivation and framing

**Core research question.** The project studies whether corporate AI adoption and
AI-related workforce claims are associated with later employment, layoffs, and
operating performance — and, separately, whether a company frames the same AI
topic differently in a promotional 8-K earnings release than in its legally
exposed 10-K. Per `RESEARCH_PIPELINE.md`, the design is explicitly observational:
absent a separate identification strategy, results must be reported as
associations or temporal patterns, not as evidence that AI *caused* a layoff or
productivity change.

**Schloetzer's framing, in his own or the project's closest-to-verbatim words.**
No single quotation of Prof. Schloetzer appears in quotation marks anywhere in the
repo. The most direct paraphrase on record, from the header of `sentiment_distance.py`
(written by the student describing the advisor's actual feedback):

> "my advisor's feedback was that hand-scoring sentences for 'AI-washing' bakes in
> my own judgment about which words count as hype, and a reviewer could easily push
> back on that."

This is the documented origin of the pivot away from hand-labeling (see Section 3).
Two later, more specific research directions are attributed to him directly in code
comments (not quoted, but consistently described across multiple files):

- His "original stretch goal (c)": does AI *centrality* — whether a company sells
  AI — explain cross-sectional variation in how severely a company frames AI risk
  in its own 10-K? (`firm_characteristics_test.py:12-14`, `RESULTS_PACKET.md` Section A)
- His "second suggestion": within a single 10-K, does AI-related risk language read
  as an "opportunity-type risk" ("we might fall behind competitors") or an
  "existential" one ("our core business is threatened")? He is recorded as having
  guessed IBM might read as the former and Salesforce the latter, explicitly
  flagged by him as speculation, not a finding (`ai_vs_other_risk_factors.py:5-8`).
- A later reframing (per the Wall Street/Goldman Sachs AI-productivity taxonomy):
  does the company *build* the AI stack (Infrastructure) or *use* AI internally for
  productivity (Power Adopter)? (`firm_characteristics_test.py:18-20`)
- A 2026-08-07 request to add a risk-type taxonomy (`demand`, `competition`,
  `export_controls`, etc.) to test whether Infrastructure and Power Adopter firms
  differ in *kind* rather than *degree* of AI risk framing (`label_schema.py:34-37`).

**The empirical puzzle this responds to.** The project's stated public-facing
starting point is Challenger, Gray & Christmas's job-cuts reporting: `challenger.py`
exists specifically to pull "the source of the AI-attribution layoff statistics
cited in the paper's background" from Challenger's public blog
(`challengergray.com/blog/category/job-cuts-report/`). Challenger's reports have
publicly attributed some announced layoffs to AI/automation, with that attribution
appearing concentrated in technology-sector announcements. That public narrative —
that AI is a stated driver of tech-sector job cuts — is the puzzle motivating the
question this project actually tests: what do the *companies' own* SEC disclosures
say about AI and workforce effects, and does their legally exposed framing (10-K)
match their promotional framing (8-K)? **Note for whoever drafts this paragraph:**
Challenger's own report data is not stored or versioned anywhere in this repo —
`challenger.py` is a live scraper with no corresponding export file — so any specific
figure (a percentage, a count, a specific month) cited from Challenger's reporting
must be sourced and verified directly from Challenger's site at drafting time, not
pulled from this repository.

---

## 2. Data sources and provenance

**Filing forms used, and why.**

- **10-K Item 1A "Risk Factors"** — the primary text source. It is the company's
  own legally exposed disclosure of risk, drafted under liability exposure by
  counsel, which is precisely why it is useful as a check against promotional
  framing: it is structurally hedged and cautious regardless of subject matter
  (see Section 3, Stage 2 discussion).
- **Matched 8-K earnings releases / prepared-remarks exhibits (EX-99)** — the
  promotional counterpart. 8-Ks are filed close to a stock-moving earnings event
  and are written to be read positively; comparing the same company's tone across
  the two filing types isolates promotional framing without requiring any
  researcher judgment about which individual words count as "hype"
  (`sentiment_distance.py:5-13`).
- Also collected, per `RESEARCH_PIPELINE.md`'s source universe: 10-K Item 1
  Business (including Human Capital), Item 7 MD&A, and relevant Item 8
  restructuring/severance notes; 8-K Items 2.02, 2.05, 7.01, and 8.01. The current
  exports mainly reflect Item 1A, Item 7, and EX-99 material — broader section
  coverage is a stated acquisition milestone, not something assumed to already
  exist.

**The company universe — approved roster as of 2026-08-19.** 25 tickers are
hardcoded in `extract_ai_sentiment.APPROVED_TICKERS`:

| Ticker | Company | Ticker | Company | Ticker | Company |
|---|---|---|---|---|---|
| IBM | IBM | GOOGL | Alphabet | ACN | Accenture |
| ORCL | Oracle | AMZN | Amazon | WMT | Walmart |
| DELL | Dell | AAPL | Apple | JPM | JPMorgan |
| CRM | Salesforce | META | Meta | LLY | Eli Lilly |
| MSFT | Microsoft | TSLA | Tesla | DE | Deere |
| AMD | AMD | AVGO | Broadcom | SPGI | S&P Global |
| NVDA | NVIDIA | | | INTU | Intuit |
| VZ | Verizon | | | NOW | ServiceNow |
| AXP | American Express | | | UBER | Uber |
| UNH | UnitedHealth | | | | |

**Documented, non-bug reasons a company is excluded, as of this date:**

- **TSMC and SAP** are absent because both file **Form 20-F** as foreign private
  issuers, and this pipeline only handles 10-K filers. This is explicitly the same
  reason for both (`extract_ai_sentiment.py:85-87`). TSMC was the 10th firm in
  Schloetzer's original AI-Infrastructure list.
- **Apple** has been confirmed to have genuinely near-zero AI risk-factor language
  — at most 4 AI-related sentences in any single filing across 11 filings scored,
  below the pipeline's 5-sentence reliability floor. This has been verified as a
  fact about Apple's disclosure, **not an extraction bug**: it is dropped from
  group-mean comparisons rather than zero-filled, on the reasoning that "cannot
  measure" is not the same claim as "neutral tone" (`STATUS.md`, `RESULTS_PACKET.md`
  Section G.2).
- **Palantir** was never on any approved company list. It is present in the raw
  export CSVs only because an earlier, unrelated bulk commit ("fixing distance
  logic", 2026-07-27) bundled in a larger exploratory pull that was never trimmed
  back out. It is enforced-excluded via `APPROVED_TICKERS`
  (`extract_ai_sentiment.py:72-80`).
- **Intel** is not in the dataset because its Item 1A extraction fails structurally
  on all filings pulled to date: Intel never labels its risk-factors section
  "Item 1A" in a form this pipeline's heading matcher recognizes — it uses a
  cross-reference index mapping items to page ranges instead. This is relevant if
  the semiconductor sample is ever expanded (`RESULTS_PACKET.md` Section G.2).

**This roster is explicitly not final.** `STATUS.md` frames company universe as
"PARTIAL" against the target design — it is a Python set, not a versioned
company/period manifest, and it has no period dimension. A second annotation pass
or further input from Prof. Schloetzer could still add companies (e.g., an
expanded semiconductor/hardware sample has already been suggested as a follow-up
in `RESULTS_PACKET.md` Section D.2). Do not describe the 25-ticker roster as
permanently frozen.

**Current raw corpus size (scale, not a results claim).** Verified directly
against the live export files on 2026-08-19:

| File | Rows | Distinct tickers | Filing-date range |
|---|---|---|---|
| `export/ai_washing_10-K.csv` | 822 | 26 (25 approved + Palantir) | 2006-02-24 to 2026-07-29 |
| `export/ai_washing_8-K.csv` | 1,032 | 24 | 2015-01-07 to 2026-07-30 |

Of the 10-K rows, 282 filing-sections have a usable, extractable Item 1A Risk
Factors section (`STATUS.md`). This is a fact about section extractability across
the corpus, not a downstream scoring result.

**Regulatory history fact (stable, citable).** Item 1A "Risk Factors" did not
exist as a required 10-K item until the SEC's 2005 disclosure overhaul, which
applied to fiscal years ending on or after **2005-12-01** (cited in code as
Securities Act Release 33-8591; `edgar_backfill_10k.py:17-19`). Every 10-K for a
fiscal year ending before that date has **no Item 1A section to extract at all** —
not an Item 1A that happens to lack AI content, but no such item in the filing.
This sets a hard floor on how far back any Item 1A-based analysis in this project
can reach, independent of anything about AI disclosure specifically.

---

## 3. Methodology narrative (the evolution — real project history, stable regardless of final numbers)

The project went through three distinct measurement approaches. Each later stage
exists because the previous one had a specific, named methodological problem —
not because it produced an unfavorable result.

**Stage 1 — sentence-level hand-labeling for "AI-washing" language. Abandoned.**
The original plan was to hand-score individual sentences for AI-washing language.
Per the advisor's feedback (quoted above in Section 1), this was abandoned as the
paper's *primary* method because it "bakes in the researcher's own judgment about
what counts as 'AI-washing' language," making it vulnerable to reviewer pushback
(`validate_finbert_against_labels.py:6-8`, `sentiment_distance.py:5-8`). The
associated dataset (`export/labeling_dataset.csv`, ~1,226 sentences from
IBM/Oracle/Salesforce/Dell) was kept as a planned secondary validation set, but the
hand-labeling pass on it was never actually completed — its `label` column is blank
on every row, confirmed via git history (see Section F.0 caveat, carried into
Section 6 below).

**Stage 2 — whole-document sentiment distance (8-K vs. 10-K). Superseded.**
`sentiment_distance.py` implements a whole-document approach: run FinBERT sentiment
over an entire document (10-K Item 1A + Item 7, or the full 8-K text) and take the
net-tone difference between a company's 8-K and its matched 10-K, as a "less
subjective stand-in for hand-labeling AI-washing language." This measure is
superseded, not because of a null result, but because of an identified confound:
10-K Risk Factors sections are drafted by counsel to read structurally negative
regardless of subject matter ("our business may be harmed by...", "we may be
unable to..."), so a whole-document distance score risks measuring "10-Ks are
legally hedged documents" rather than anything specific to AI language
(`extract_ai_sentiment.py:6-13`).

**Stage 3 — AI-specific sentence/passage extraction. Current approach.**
`extract_ai_sentiment.py` and `ai_vs_other_risk_factors.py` restrict the FinBERT
comparison to only the sentences that actually mention AI/ML/automation terms,
isolating the AI-specific signal from the general hedged-legal-document effect.
This is the approach the current pipeline and results packet are built on. Two
parallel comparisons exist at this stage:

- **Between-document (Stage 3a):** AI-sentence tone in a company's 8-K vs. the
  matched 10-K's Item 1A (`extract_ai_sentiment.py`).
- **Within-document (Stage 3b):** AI-related Item 1A sentence tone vs. that same
  filing's *other* (non-AI) Item 1A sentence tone (`ai_vs_other_risk_factors.py`)
  — Schloetzer's "second suggestion" described in Section 1.

**General shape of the current extraction/scoring pipeline** (approach, not
result numbers): each 10-K's Item 1A section is isolated by a heading-matching
extractor; sentences are split with NLTK Punkt and bounded to 6–60 words; sentences
are classified as AI-related or not by a shared, explicit AI-keyword pattern
(`extract_ai_sentiment.AI_KEYWORD_PATTERN`, covering generic terms like "artificial
intelligence," "machine learning," "generative AI," "automat*," plus a small set of
branded terms found by spot-checking to matter for specific filers — Salesforce's
"Agentforce," IBM's "watsonx"/"Watson" — added because the generic pattern alone
was missing real AI-content sentences that use only a product name); each matched
sentence is scored individually with FinBERT (`ProsusAI/finbert`, off-the-shelf
3-class sentiment head) and reduced to a net-tone scalar, P(positive) − P(negative);
scores are compared within a document (AI-sentence tone vs. other-sentence tone)
and across documents (8-K AI-sentence tone vs. matched 10-K AI-sentence tone).
`STATUS.md` is explicit that this off-the-shelf FinBERT-sentiment-polarity approach
is **not** the fine-tuned multi-label classifier (`ai_opportunity`, `ai_risk`,
`ai_efficiency`, `ai_workforce_reduction`) that `RESEARCH_PIPELINE.md` describes as
the target design — that classifier exists in code (`finbert_multilabel.py`) but
has never been trained, because it depends on the human annotation step (Stage
7 of the 20-step design) that has not yet happened.

**Labeling dataset provenance — precise, and not yet corrected to Schloetzer.**
The validation labels used to construct-check FinBERT
(`export/labeling_dataset_llm_labeled.csv`, 1,226 labels covering IBM, Oracle,
Salesforce, and Dell sentences) were generated by **a single LLM pass against a
fixed, disclosed rubric** — they are **not** hand-labeled by a human coder, not
independently verified, not double-coded, and carry no professor adjudication
(`validate_finbert_against_labels.py:13-26`, `STATUS.md` Step 7). This has been
identified in the repo's own documentation as something that **still needs to be
disclosed to Prof. Schloetzer before the validation is cited** — he may currently
believe human labels exist, and the Methods section must describe these as
"LLM-generated single-pass labels against a fixed rubric," never as "hand-labeled"
or "human-validated" (`RESULTS_PACKET.md` OPEN ITEM #1). As of this writing, that
disclosure to Schloetzer has not yet happened.

---

## 4. Validated method limitations (findings about the method itself, independent of any specific result)

These are established properties of the current FinBERT-sentiment-based measure,
verified in `validate_finbert_against_labels.py` against the LLM-generated
validation labels described above. They are limitations of what the *method* can
detect, not specific results that could shift with more data — though the
underlying validation is itself run against the LLM labels (Section 3's
provenance caveat applies to it as well).

- **FinBERT reliably separates promotional/marketing register from
  hedged/legal register.** Sentences independently characterized as "genuine
  automation claim" or "vague AI buzzword" score clearly differently from
  sentences characterized as "efficiency framing" or "other/not applicable" —
  this is the promotional-vs-hedged axis the paper's Stage 3 method actually
  relies on, and the validation script found it holds with a large effect
  across every such comparison.
- **FinBERT cannot distinguish a genuine automation claim from a vague AI
  buzzword.** Both simply read as generically positive to the sentiment model.
  This is a direct limitation on the AI-washing construct itself: the method
  detects *that* a company is talking about AI optimistically, not *whether the
  optimism is substantiated* by a concrete, operational claim.
- **FinBERT cannot distinguish efficiency-framing from demand-decline-framing.**
  These are the two competing explanations for a layoff at the heart of the
  paper's puzzle (AI making work more efficient vs. AI reducing demand for a
  company's output/workers), and sentiment polarity alone does not separate
  them. The validation script flags this comparison as also underpowered by
  sample size on the "demand-decline" side, independent of the direction of
  the effect.

State these as caveats on what the current tone-based measure is and is not
capable of showing — they belong in the Introduction/Methods as a limitation of
the approach, not in the Results section, and they do not depend on which
specific companies or filings end up in the final analysis sample.

---

## 5. The Oracle case study — citation re-verified 2026-08-19

**Verification method:** the citation below was re-checked directly against the
live `export/ai_washing_10-K.csv` (not from memory or a prior summary) by locating
the row with `doc_id = b5db10277712ffd2` and confirming the filing date, URL,
section length, and the exact sentence text at its recorded character offset.
**Result: unchanged.** Every element matches what was previously documented.

**Citation**
- Company: ORACLE CORP (ORCL)
- Filing: FY2026 Form 10-K, Item 1A Risk Factors
- Filing date: **2026-06-22**
- `doc_id`: **b5db10277712ffd2**
- URL: `https://www.sec.gov/Archives/edgar/data/1341439/000119312526277521/orcl-20260531.htm`
- Section length: 114,836 characters; target sentence located at character offset
  36,059 (re-confirmed directly against the current CSV)

**The sentence (verbatim, re-confirmed):**

> In addition, the adoption and deployment of AI technologies across our
> operations have resulted, and may continue to result, in reductions to our
> workforce.

**Surrounding paragraph (verbatim, for context):**

> Our periodic workforce restructurings and reorganizations can be disruptive.
> We have an existing restructuring plan in place under which we have made, and
> will continue to make, adjustments to our workforce in response to management
> changes, product changes, performance issues, changes in strategies,
> acquisitions and other internal and external considerations. We may initiate
> new restructuring plans in the future. In addition, the adoption and
> deployment of AI technologies across our operations have resulted, and may
> continue to result, in reductions to our workforce.
>
> These types of restructurings have resulted, and may in the future result, in
> increased restructuring costs and reduced productivity. These types of
> restructurings may also lead to shortages of sufficiently skilled employees in
> certain roles, loss of valuable institutional knowledge and damage to employee
> morale and retention.

**Points supported directly by the raw text, safe to use in the Introduction:**
- The sentence uses the past perfect — "have resulted" — making it a statement of
  completed fact, not purely forward-looking risk boilerplate.
- It is the final sentence of a generic restructuring paragraph, appended after a
  list of conventional causes (management changes, product changes, performance
  issues, strategy changes, acquisitions), and does not receive its own
  risk-factor heading.

**Scope limit, carried forward from `RESULTS_PACKET.md`:** this quotation is a
verbatim disclosure and its evidentiary value as a documented instance of an
AI-attributed workforce reduction does not depend on any tone statistic. It should
**not**, however, be used to imply that Oracle *systematically* frames AI risk as
existential — that broader claim is a separate, results-dependent question, and is
therefore excluded from this reference document (see the excluded list below).

---

## 6. Literature citations status (inventory only — no new verification performed)

No dedicated bibliography or citations list exists yet anywhere in this repo. The
items below are every citation-like reference found across the repo's docs and
code, plus the unresolved external items the user identified directly. Nothing
below was independently verified in this pass — this is strictly an inventory of
confirmed vs. still-open.

| Citation / reference | Where it appears | Status |
|---|---|---|
| SEC Securities Act Release 33-8591 (2005 disclosure overhaul; basis for the Item 1A regulatory-history fact in Section 2) | `edgar_backfill_10k.py:17-19` | **Pending** — cited in code comments; not independently re-verified against the primary SEC release text in this pass |
| Loughran-McDonald net-tone measure (informal methodological analogue for the FinBERT P(positive)−P(negative) reduction) | `sentiment_distance.py:293`, `RESULTS_PACKET.md` (Methodology paragraph, Section G.5) | **Pending** — referenced informally as an analogue, no full citation (author/year/venue) given anywhere; not yet a real bibliography entry |
| Wall Street / Goldman Sachs AI-productivity taxonomy (basis for the Infrastructure-vs-Power-Adopter grouping) | `firm_characteristics_test.py:18-20`, `RESULTS_PACKET.md` Section D.1 | **Pending** — referenced informally, no specific report or publication cited |
| "Working Draft" ambiguity (NotebookLM-sourced) | External to this repo | **Open** — flagged by the user as unresolved; not found in this repo, cannot be located or checked from repo contents |
| Possible duplicate with Brynjolfsson et al. 2025 (NotebookLM-sourced) | External to this repo | **Open** — flagged by the user as unresolved; no matching citation found anywhere in this repo |
| Possible duplicate with Seele & Schultz 2022 (NotebookLM-sourced) | External to this repo | **Open** — flagged by the user as unresolved; no matching citation found anywhere in this repo |

None of the three NotebookLM-sourced items were investigated further, per
instruction — they are carried forward exactly as open.

---

## Excluded as possibly still in flux

The following were deliberately left out of the sections above because they are
current-analysis-stage numbers that could still shift with the annotation pass,
panel regressions, or further methodological feedback, and therefore do not
belong in Introduction/Background material:

- Any p-value, effect size (Cohen's d), or significance verdict from the
  AI-centrality (core vs. peripheral), Infrastructure-vs-Adopter, or
  Hyperscaler-vs-Semiconductor group comparisons (`RESULTS_PACKET.md` Sections A,
  D, H.3).
- The within-document AI-vs-other-risk severity pooled result and its confidence
  interval (`RESULTS_PACKET.md` Section C).
- The 8-K vs. 10-K distance result, pooled or per-company, collapsed or
  uncollapsed (`RESULTS_PACKET.md` Section B).
- The thin-evidence/`automat*`-exclusion sensitivity results, including the
  specific claim that Oracle's within-document mean "flips sign" once restricted
  to filings with ≥5 AI sentences (`RESULTS_PACKET.md` Section H.6) — this bears
  directly on how the Oracle case study in Section 5 above may ultimately be
  framed in the Results section, but is not included here.
- Specific counts of scored/surviving filings downstream of raw extraction (e.g.,
  "115 scored 10-Ks," "77 filings after the thin-evidence filter") — these are
  outputs of the current measure and threshold choices, not fixed corpus facts.
  Only the raw pull counts and Item-1A-extractable counts are included above in
  Section 2, since those depend only on what SEC EDGAR contains and what the
  extractor can locate, not on any scoring choice.
- The composition-panel descriptive statistics (AI word share, ordinal position,
  specificity, year-over-year recycling medians/quartiles) from
  `RESULTS_PACKET.md` Section H.4.
- The FinBERT validation's specific effect sizes and p-values (Section F.1–F.3 of
  `RESULTS_PACKET.md`) — Section 4 above states the qualitative limitations these
  numbers support, without the numbers themselves.
- Any claim that a specific company (Oracle, Tesla, Broadcom, etc.) systematically
  frames AI risk in a particular direction — this is exactly the kind of
  per-company claim `RESULTS_PACKET.md` itself warns is thin-filing-dependent and
  not yet stable.
- Specific figures from Challenger, Gray & Christmas's public layoff reporting
  (e.g., a percentage of layoffs attributed to AI, a tech-sector concentration
  statistic) — no such figures are stored in this repo; `challenger.py` is a live
  scraper with no corresponding retained export, so any number used in the
  Introduction's empirical-puzzle framing needs to be sourced and verified
  directly from Challenger's site, not from this repository.
