# This Project, Explained Simply

This guide describes what is actually in this folder today. It separates the **current, saved results** from the more ambitious research system that the code is designed to become. That distinction matters: the project is not yet a completed test of whether AI caused layoffs or whether companies falsely blamed layoffs on AI.

## 1. The one-paragraph version

This project collects public company filings from the U.S. Securities and Exchange Commission (SEC), finds sentences that mention AI, and asks how positive or negative that AI language sounds. The completed analysis compares (1) AI-related risk sentences in a company's annual report with that same report's other risk sentences, and (2) AI language in an 8-K earnings release with AI language in the related 10-K risk section. It uses **FinBERT**, a language model trained to label financial text as positive, neutral, or negative, to turn each sentence into a simple tone score. The headline saved finding is that, on average, AI-related risk sentences sound a little less negative than the other risks in the same annual report. A larger planned system would instead have humans label the *meaning* of passages (for example, AI opportunity, AI risk, or AI replacing workers), train a custom classifier, join those text scores to employment and financial data, and test whether earlier language is associated with later layoffs. That planned system is only partly built and has not produced the final kinds of results it promises.

## 2. The pipeline as a story

Here is the intended journey from an SEC filing to a research result. “SEC” means the U.S. government agency that requires public companies to disclose financial information. A **filing** is a document a company submits to that agency.

1. **Choose companies.** `extract_ai_sentiment.py` contains the approved list of 25 stock tickers (short stock-market codes such as `MSFT` for Microsoft). `firm_characteristics_test.py` also puts some firms into pre-set comparison groups.

2. **Download filings from EDGAR.** **EDGAR** is the SEC's public filing database. `main.py` coordinates collection; `edgar.py` finds a ticker's SEC identifier, downloads filings, and tries to locate useful sections; `normalize.py` puts the text into a common format; and `storage.py` avoids duplicate records and saves CSV and JSON files in `export/`.

3. **Pull out the relevant parts.** A **10-K** is a company's detailed annual report; its Item 1A section lists risks. An **8-K** is a shorter event report, often including an earnings release; an **EX-99** is an attached exhibit, such as that release. The current saved tone analysis mainly uses 10-K Item 1A risk factors and 8-K earnings-release material. The collector can also collect 10-Q quarterly reports, business descriptions, management discussion, and financial-statement sections, but those are not the main completed analysis.

4. **Match 8-Ks to annual-report windows.** `sentiment_distance.py` and the newer `build_passage_dataset.py` try to connect each 8-K to the relevant 10-K period for the same company. This is necessary because several 8-Ks can belong to one annual-report cycle. The current tone scripts use filing dates as a rough fiscal-year window; the newer design is stricter about keeping a real period ID.

5. **Find AI text.** `extract_ai_sentiment.py` splits text into sentences and uses a keyword rule for terms such as “artificial intelligence,” “machine learning,” and “generative AI.” It deliberately rejects hits where words like “automatic” do not actually mean AI. `ai_vs_other_risk_factors.py` divides each Item 1A into AI-related and non-AI sentences.

6. **Score tone in the completed analysis.** `sentiment_distance.py` loads stock FinBERT and estimates positive, neutral, and negative probabilities for each sentence. A **probability** is a model's 0-to-1 confidence-like number, not proof. The scripts calculate **net tone = probability of positive minus probability of negative**. Higher means more positive-sounding; lower means more negative-sounding.

7. **Make the two current comparison measures.** `ai_vs_other_risk_factors.py` computes `within_doc_distance`: average AI-sentence tone minus average other-risk-sentence tone within one 10-K. `extract_ai_sentiment.py` computes `sentiment_distance`: average AI tone in a matched 8-K minus average AI tone in its 10-K. Neither measure tells us whether a company truly used AI, replaced workers, or caused layoffs; it measures wording tone.

8. **Check uncertainty and group differences.** `significance_tests.py`, `significance_tests_collapsed.py`, `firm_characteristics_test.py`, `permutation_test.py`, and `sensitivity_unflagged_filings.py` summarize the saved results. A **statistical test** is a calculation asking whether a pattern could easily arise from random variation. The better group test here collapses repeated filings to one value per firm and then uses a permutation test, meaning it tries every possible reassignment of firms to the two groups.

9. **Build richer text measures.** `risk_factor_composition.py` has run on real data. It measures how much of Item 1A is AI-related, where AI risks appear, how numeric they are, and how similar the language is from one year to the next.

10. **The planned next stage, not a completed result.** `build_passage_dataset.py` creates short passages, `label_schema.py` defines human labels, `finbert_multilabel.py` can train a custom multi-label model, `aggregate_company_period.py` can build company-period text scores, `merge_financial_panel.py` can join financial outcomes, and `run_panel_experiments.py` can run the planned regressions. A **regression** is a method for estimating how one measured thing relates to another while holding selected other measured things constant. No trained custom model, complete financial panel, or final regression output exists.

## 3. Tour of the important files

### The maps and explanations

| File | What it does |
|---|---|
| `README.md` | A setup and design overview. It describes the aspirational full workflow as well as the repository layout. |
| `RESEARCH_PIPELINE.md` | The detailed blueprint for the future 20-step study. Treat it as the plan, not proof that every step happened. |
| `STATUS.md` | The best written map of what was complete when it was written; it correctly warns that the reported measure differs from the planned measure. Some claims that `derived/` did not exist are now outdated because that folder is present. |
| `RESULTS_PACKET.md` | A detailed draft results memo. Its main current numbers agree with the saved CSVs inspected here, but it says it was written before some later fixes and should not override the CSVs. |
| `9.17.26 current standing.md` and `INTRO_REFERENCE.md` | Working notes and background/reference material, not final evidence. |
| `ANNOTATION_CODEBOOK.md` and `annotation_prompt.md` | Instructions for labeling a passage's meaning. The codebook is generated from `label_schema.py`; the prompt describes blinded machine-labeling rules. |

### Collection and storage

| File(s) | What they do |
|---|---|
| `config.py` | Reads settings such as the SEC contact header, output folder, optional search key, and optional Google Drive credentials. |
| `main.py` | The main collector command: loops through firms and forms and asks the other collection modules to do the work. |
| `edgar.py` | Talks to SEC EDGAR, finds filing lists and documents, converts HTML to text, and uses imperfect rules to find filing sections. **HTML** is the webpage-style formatting inside many filings. |
| `normalize.py`, `storage.py` | Turn collected material into consistent rows and save the export files without duplicates. |
| `edgar_coverage_audit.py`, `edgar_backfill_10k.py` | Check whether the project missed annual filings and fill historical 10-K gaps. These support the present corpus but are not analysis scripts. |
| `challenger.py`, `serper_search.py`, `gdrive.py` | Optional helpers: collect public Challenger layoff-report material, search for earnings-call links/snippets, and upload exports to Google Drive. They are not the source of the headline results. |

### The analysis that has real saved output

| File(s) | What they do |
|---|---|
| `extract_ai_sentiment.py` | Finds AI sentences, matches 8-Ks and 10-Ks, scores sentence tone, and produces the 8-K minus 10-K distance file. |
| `sentiment_distance.py` | Shared matching and FinBERT-scoring machinery, including long-text handling. |
| `ai_vs_other_risk_factors.py` | Produces the main within-10-K measure: AI risk tone minus other-risk tone. |
| `risk_factor_composition.py` | Produces the 282-row firm-year composition panel and readable AI-risk passage files. |
| `significance_tests.py`, `significance_tests_collapsed.py` | Test whether the 8-K/10-K tone gap is above zero, including a correction for repeatedly matching many 8-Ks to one 10-K. |
| `firm_characteristics_test.py`, `firm_characteristics_robustness.py` | Compare pre-set company groups and do “remove one company” sensitivity checks. |
| `permutation_test.py` | The strongest available group-comparison script because it makes each firm count once. |
| `sensitivity_unflagged_filings.py` | Repeats results after excluding filings with fewer than five AI sentences or fewer than five other-risk sentences. |
| `analyze_ai_sentiment_results.py`, `oracle_ai_risk_sentences.py`, `spotcheck_excluded_sentences.py`, `spotcheck_8k_ai_gap.py` | Read-only summaries and spot-check tools for understanding or auditing results. |

### The newer, partly prepared workflow

| File(s) | What they do |
|---|---|
| `build_passage_dataset.py` | Creates 20–220-word passages, candidate filters, matched periods, samples for annotation, and quality checks. Contrary to older `STATUS.md` text, it has now produced files in `derived/`. |
| `label_schema.py` | Defines eight labels and rules for valid annotations. A **multi-label** system lets one passage have more than one label. |
| `llm_annotate.py` | An older one-pass language-model labeling helper; it is not human annotation and its metadata handling is criticized in `annotation_prompt.md`. |
| `finbert_multilabel.py` | Code to fine-tune a new FinBERT model on adjudicated labels and score passages. **Fine-tune** means further training a general model on task-specific examples. No saved trained model exists. |
| `aggregate_company_period.py` | Would average passage predictions by company, time period, and form, then calculate separate 8-K minus 10-K gaps for each meaning label. |
| `merge_financial_panel.py`, `run_panel_experiments.py` | Would join the text results to financial/labor outcomes and run planned statistical models. Their needed input panel is absent. |
| `schemas/financial_panel_template.csv`, `schemas/company_role_template.csv` | Blank column templates showing what outside financial data and firm-role classifications would be needed. |
| `validate_finbert_against_labels.py` | Checks the stock FinBERT tone score against the older LLM labels; it finds the tone score does not distinguish a genuine automation claim from a vague one. |

### Data, tests, and housekeeping

`export/` contains raw extracted text plus the saved result tables. `derived/` contains newer passages and annotation work. `blind_annotation/` contains the sampling, two-machine-coder workflow, labels, and unfinished items. `output/risk_factor_text/` contains readable extracts produced by the composition script; `export/backup_pre_rerun/` is an older snapshot and should not be used for current numbers. `tests/test_pipeline.py` tests pieces of the planned workflow; passing tests do not mean the full research pipeline has run. `requirements.txt` lists the software libraries the code expects.

## 4. REAL vs. NOT REAL

### Real: code that has run and produced saved output

* SEC-derived source exports exist: 822 10-K section rows, 1,032 8-K rows, 99 10-Q rows, and 46 earnings-call-snippet rows in `export/`. A row is a collected section or exhibit, so it is not always a whole filing.
* The present 10-K Item 1A analysis exists: `export/ai_vs_other_risk_factors_results.csv` has 282 filing rows; 115 have both AI and non-AI sentences and therefore a usable within-document tone difference.
* The present 8-K/10-K comparison exists: `export/ai_sentiment_distance_results.csv` has 665 matched-pair rows, 287 with a computed tone distance. Because multiple 8-Ks can share a 10-K, the saved results correctly also collapse these to 75 unique 10-Ks.
* The composition panel exists: `export/risk_factor_composition_panel.csv` has 282 firm-year rows and 47 columns.
* Passage-building has now run: `derived/clean_passages.csv` has 8,990 candidate passages (5,267 from 10-Ks and 3,723 from 8-Ks), across 23 firms represented in both forms and 128 matched periods. This directly contradicts the older `STATUS.md` sentence saying `derived/` did not exist and passage construction was code-only.
* Blinded machine-label output exists: `derived/annotation_master_sample_llm_blind.csv` has 241 rows. It is real output, but it is not a human gold standard.

### Written but not yet a real completed analysis

* The custom eight-label FinBERT training code exists, but no `models/` folder or trained custom model exists.
* The code for passage-level scoring, aggregation, financial merging, firm/time controls, and planned outcomes exists, but the inputs and outputs for that complete chain do not exist.
* The planned test of whether prior AI wording predicts later employee changes, layoffs, revenue per employee, or restructuring has not been run. There is no acquired financial/labor outcome panel.
* The planned infrastructure-versus-adopter **interaction** test is not run. An interaction test asks whether the text–outcome relationship changes by company type; the saved work instead compares simple group averages.
* Placebo tests, which are deliberately irrelevant checks meant to catch a misleading method, have not been run.

### Planned or incomplete annotation work

* The old `export/labeling_dataset.csv` has 1,226 sentences and all 1,226 `label` cells are blank. It is not a completed hand-labeling dataset.
* `export/labeling_dataset_llm_labeled.csv` has the same 1,226 rows with all labels filled, but they are single-pass AI labels, not human labels and not a verified gold standard.
* The newer blinded sample was intended to be 255 passages. `blind_annotation/STATUS.md` says 241 were completed, 11 still need adjudication, and 3 never started. The present 241-row file marks every row `unreviewed`, even though its companion notes describe two blinded machine coders and machine adjudication on disagreements. No human coding, independent human second coding, or human agreement statistic exists.

## 5. The actual results so far

### First, what these results do and do not say

The completed results measure **tone**, not truth. “Positive” here means that FinBERT judged wording as more positive than negative; it does not mean a statement is accurate, beneficial, or deceptive. The results do not connect a particular layoff to AI and do not show that a company was “AI washing.” **AI washing** is the idea that a company may use AI language to create a favorable story or excuse; the current output can only be early evidence about language patterns.

### A. AI risk language versus other risk language in the same 10-K

This is the strongest current result. Each usable 10-K has a `within_doc_distance` score: mean tone of AI-related Item 1A sentences minus mean tone of all other Item 1A risk sentences. A positive number means AI risks sounded less negative than the firm's other risks.

| Sample | What was compared | Result |
|---|---|---|
| Full scored sample | 115 usable 10-Ks | Mean difference **+0.1060**: AI-risk wording was less negative on average. The CSV-based tests report p = **0.0005** (t test) and **0.0002** (rank test). |
| Stricter “unflagged” sample | 77 filings with at least 5 AI and 5 other-risk sentences | Mean difference **+0.1322**; both saved p-values round to **0.0000**. |

A **p-value** is the probability of seeing a pattern at least this strong if there really were no average difference under the test's assumptions. Very small p-values look impressive, but these filing-level tests treat repeated annual filings from the same company as more independent than they really are. The results memo estimates an effective sample closer to 43 than 115, so the direction and size are more trustworthy than the exact p-value. Still, the result becoming larger in the stricter sample is encouraging.

### B. AI-core versus AI-peripheral firms

This comparison asks whether companies that are more central to selling AI sound different from firms more peripheral to AI. The groups were fixed as five firms each: AI-core = Oracle, Salesforce, Microsoft, AMD, NVIDIA; AI-peripheral = IBM, Dell, Verizon, American Express, UnitedHealth.

| Unit counted once | AI-core | AI-peripheral | Difference (core minus peripheral) |
|---|---:|---:|---:|
| 5 firms each, averaging each firm's filings first | +0.0669 | +0.3726 | **−0.3057** |

The exact firm-level permutation p-value is **0.0238** (6 of all 252 possible label assignments were at least as extreme). That is evidence of a difference in this small, pre-set sample. But it is fragile: after the stricter five-sentence rule, the difference remains negative (−0.1711) but its exact p-value becomes **0.1270**, not conventionally significant. The safe description is: *the full sample shows a sizeable difference, but it weakens and loses statistical significance when thin-evidence filings are excluded.* Do not present it as a settled headline.

### C. AI infrastructure firms versus AI “power adopters”

This is the professor's Infrastructure vs. Adopters comparison. Infrastructure firms are suppliers/builders of AI technology; adopters are firms mainly using AI in their own operations. The firm-level averages are **+0.0890** for 8 infrastructure firms and **+0.0676** for 10 adopters, a tiny difference of **+0.0214**. The exact permutation p-value is **0.8603**.

Plain English: this saved analysis found no evidence that the two groups differ on the current tone measure. This is a null result, meaning a result that does not show a detectable difference; it is not proof that the groups are identical. It also is not the better planned interaction test.

### D. 8-K earnings materials versus 10-K risks

For matched company periods, the project compares AI tone in an 8-K earnings release with AI tone in the related 10-K risk factors. On the 287 computable pair rows, the average gap is **+0.7368**. After correctly collapsing repeated 8-Ks to 75 unique 10-Ks, the average is **+0.7425**. In plain English, the AI language in earnings materials was much more positive than the AI language in annual-report risk sections.

This is a real and unsurprising document-type difference, but it is not by itself proof of dishonesty: earnings releases are designed to discuss performance and investor-facing news, while Item 1A is legally required to describe risks. The more defensible claim is “the language differs strongly by document purpose,” not “companies are lying.”

### E. Composition and recycling results

The saved composition panel covers **282 firm-years, 25 firms, fiscal years 2014–2026**. Its median AI word share is 0 under either measurement method, which means at least half of Item 1A filings in this sample contain no detected AI risk text. Among filings with AI text, the saved summary says the median first AI-risk position is **8.5%** of the way through the risk-factor list and the median average position is **35%**, suggesting AI material is often raised early but distributed across the list. The median year-to-year TF-IDF cosine is **0.970** and median five-word-phrase overlap is **0.517**. **TF-IDF cosine** is a 0-to-1 similarity score based on weighted word use; **five-word-phrase overlap** checks whether exact runs of five words repeat. Together, these numbers suggest companies often reuse the same vocabulary but rewrite some exact phrases.

## 6. The data

### Companies and exclusions

The raw 10-K export contains 26 tickers:

`AAPL, ACN, AMD, AMZN, AVGO, AXP, CRM, DE, DELL, GOOGL, IBM, INTU, JPM, LLY, META, MSFT, NOW, NVDA, ORCL, PLTR, SPGI, TSLA, UBER, UNH, VZ, WMT`.

The approved analysis universe is the same list **except PLTR (Palantir)**, so it has 25 companies. `STATUS.md` says Palantir is unapproved exploratory data and should not enter results. TSMC and SAP are not included because they file a different annual-report form, the 20-F, which this workflow does not support.

Apple needs a careful note. It is in the raw data and has two scored 2024–2025 rows, but only 2 and 4 AI sentences, respectively, both marked low sentence count. It is excluded from the pre-set group comparisons rather than treated as a meaningful “zero-AI” firm. This is more precise than the outdated shorthand “Apple has no usable AI data.”

### Dates and before/after ChatGPT

ChatGPT became publicly available on November 30, 2022. Using each file's `filing_date`—not a guessed fiscal year—the current saved files show:

| Data item | Before 2022-11-30 | On/after 2022-11-30 | Total | Date span |
|---|---:|---:|---:|---|
| Raw 10-K section rows | 634 | 188 | 822 | 2006-02-24 to 2026-07-29 |
| Item 1A risk-factor rows | 194 | 94 | 288 | same raw 10-K period |
| 10-K result rows | 192 | 90 | 282 | 2006-02-27 to 2026-07-29 |
| Usable AI-versus-other-risk tone rows | 31 | 84 | 115 | same result period |
| Raw 8-K rows | 582 | 450 | 1,032 | 2015-01-07 to 2026-07-30 |

The current data can support a **descriptive** question such as “did detected AI risk disclosure become more common after ChatGPT?” There are both pre- and post-November-2022 filings, and the contrast is large: only 31 of 192 pre-ChatGPT 10-K result rows contain scoreable AI text, versus 84 of 90 post-ChatGPT rows. But it cannot yet support a clean causal claim that ChatGPT caused the change. Reasons: the sample is not a pre-registered balanced company-by-year panel, extraction quality changes over time, the relevant current measure is tone rather than a validated AI-risk label, and filing dates are only a proxy for fiscal periods. A next analysis should explicitly count AI disclosure per firm-year, plot it over time, check the raw text manually, and make clear it is a before/after description rather than proof of cause.

## 7. The labeling and annotation files

**Annotation** means a person or model reads text and applies pre-defined tags. A **gold standard** is a carefully checked set of human answers used to judge or train a model.

| File/location | What it is | Who filled it | Status |
|---|---|---|---|
| `export/labeling_dataset.csv` | 1,226 sentence rows with a `label` column | No one | All 1,226 labels are blank. |
| `export/labeling_dataset_llm_labeled.csv` | Same 1,226 sentences, with labels | An AI language model in one pass | All labels filled, but not human-validated. Useful for exploration only. |
| `label_schema.py` / `ANNOTATION_CODEBOOK.md` | The rules for the future labels | Written specification, not row-level labels | Defines opportunity, risk, efficiency, workforce reduction, adoption, worker augmentation, generic marketing, and explicit AI/job link. |
| `derived/annotation_template.csv` | Newer sample ready for annotation | The passage-building script | 1,200 rows. |
| `blind_annotation/` | Protocol, sample manifest, labels, and unfinished tasks | Two blinded AI coders plus an AI adjudicator, according to its status note | Intended sample 255; 241 merged machine-labeled rows; 14 still open (11 adjudication-only, 3 not started). |
| `derived/annotation_master_sample_llm_blind.csv` | The merged newer machine-label output | Machine-only; `coder_id` says `llm_blind:claude-fable-5:prompt-1.0.0+risk_type` | 241 rows, all marked `unreviewed`; no human gold set. |

The key methodological point: neither LLM label file can be described as human annotation. The planned model is wisely written to require **adjudicated** training rows; adjudication means an explicit final decision after independent coders disagree. That human step has not happened.

## 8. Known problems, weak spots, and limitations

1. **The paper question and current measure are not the same.** “AI washing” around layoffs needs evidence about AI claims, workforce changes, and whether the connection is real. The current results mostly measure positive-minus-negative wording in risk language.

2. **Stock FinBERT is not trained for this exact question.** It recognizes financial positivity/negativity, not whether a sentence makes a real AI automation claim. The repository's own validation script reports it cannot separate genuine automation claims from vague ones using the available LLM labels.

3. **No human labels yet.** Machine labels are not a gold standard. Without independent human coding and an agreement check, the custom classifier cannot be credibly trained or evaluated.

4. **No outcome data.** There is no saved, linked panel of employee counts, layoffs, restructuring charges, labor cost, or later productivity. So the project does not test whether language predicts real workforce outcomes.

5. **Repeated observations create fake confidence.** A company appears in multiple years. Treating its filings as completely independent can make p-values too small. The firm-level permutation test fixes this for group comparisons, but the pooled within-document test still has this limitation.

6. **Thin evidence can change conclusions.** Some filing scores rest on only one or a few AI sentences. Requiring at least five AI and five non-AI sentences strengthens the pooled result but removes significance from the AI-core/peripheral comparison and reverses Oracle's own mean from −0.1558 to +0.0616.

7. **Different documents have different jobs.** An 8-K earnings release and a 10-K risk section are supposed to sound different. A positive 8-K-minus-10-K gap may reflect normal legal and communication conventions, not manipulation.

8. **Extraction is heuristic.** A heuristic is a practical rule of thumb, not a guarantee. SEC HTML differs across companies and years, and section headings can be parsed incorrectly. The repository documents prior extraction bugs and applies exclusions, but manual auditing remains necessary.

9. **Period matching is imperfect in the current output.** The saved severity scripts use filing dates rather than a fully verified fiscal period. That can be wrong for companies with unusual fiscal years.

10. **The sample is limited and selectively constructed.** It is 25 large firms with successful collection, not all public companies. Foreign private issuers on 20-Fs are excluded. Results may not generalize.

11. **Old documentation is stale.** `STATUS.md` accurately explains many limitations but says `derived/` was absent; it is now present. `README.md` gives an older 9,581 passage count, while the actual `derived/passage_qa.json` says 8,990 after 591 exclusions. Use actual output files for numbers.

12. **Association is not causation.** An **association** means two things move together; **causation** means one made the other happen. Even the planned regression stage would need stronger design choices before claiming cause.

## 9. If the professor asks...

1. **“What is your main result?”**  
   In 115 usable 10-Ks, AI-related Item 1A risk sentences were on average less negative than the other risks in the same filing: +0.1060 on the FinBERT tone-difference scale. The effect becomes +0.1322 after excluding thin-evidence filings.

2. **“Does this prove AI washing?”**  
   No. It shows a wording pattern, not whether companies used AI as a false layoff explanation. The data needed to test layoffs and later employment outcomes are not yet merged.

3. **“Why compare 8-Ks and 10-Ks?”**  
   They are two official company communication settings: earnings materials often tell a performance story, while Item 1A must state risks. The +0.7425 collapsed average gap shows they use very different AI tone, but that difference can be normal rather than deceptive.

4. **“What does FinBERT actually do?”**  
   It estimates whether each financial sentence sounds positive, neutral, or negative. It does not fact-check the sentence and does not directly recognize layoffs, AI adoption, or causal claims.

5. **“Why aren't you using the custom AI/workforce labels in the headline results?”**  
   The code exists, but the required human, reviewed labels and trained custom model do not. The saved headline output uses stock three-class FinBERT tone instead.

6. **“Are the labels human labels?”**  
   No. The old 1,226-row hand-label template is blank; the filled version and the 241-row blinded sample are machine labels. Human independent coding and adjudication are still needed.

7. **“What happened to the AI-core versus AI-peripheral result?”**  
   In the full sample it has an exact firm-level permutation p-value of 0.0238 and a −0.3057 difference. With a stricter minimum-evidence rule, the sign remains negative but p becomes 0.1270, so it is a qualified, not settled, finding.

8. **“Do infrastructure firms differ from AI adopters?”**  
   Not on the current tone score. The firm-level difference is only +0.0214 and the exact p-value is 0.8603. The stronger planned interaction-based version has not been run because the financial panel is missing.

9. **“Can you study ChatGPT's effect on AI disclosure?”**  
   The filings span before and after November 30, 2022, so you can describe a sharp rise in scoreable AI text: 31 usable pre-date 10-K rows versus 84 post-date rows. But that is not causal proof; it needs a careful firm-year time analysis and manual validation.

10. **“What should we do next?”**  
   First, finish a real human-labeled, double-coded passage set and adjudicate disagreements. Then train and evaluate the custom multi-label model. Separately acquire/assemble a documented company-period labor and financial panel before testing whether text predicts later outcomes.

## 10. Glossary

| Term | Plain-English meaning |
|---|---|
| 8-K | A short SEC report announcing a major event; this project often uses its earnings-release attachment. |
| 10-K | A detailed annual report that U.S. public companies file with the SEC. |
| 10-Q | A quarterly SEC report. |
| 20-F | The annual-report form used by many foreign companies instead of a 10-K. |
| Adjudication | Making one final label after independent coders disagree. |
| AI washing | The concern that companies may exaggerate or strategically invoke AI to make an action, such as layoffs, sound better; it is the topic being investigated, not something this project has proven. |
| Annual report | A yearly report about a public company's business, finances, and risks; here, usually a 10-K. |
| Association | A pattern where two measured things are related, without proving one caused the other. |
| Causal claim | A claim that one thing made another happen. |
| Classifier | A computer model that sorts text into categories. |
| Company-period panel | A table with one row for each company and time period, allowing comparisons over time. |
| Confidence interval | A range of values that gives a sense of the uncertainty around an estimate. |
| CSV | A plain-text spreadsheet file where columns are separated by commas. |
| EDGAR | The SEC's public online filing database. |
| Effective sample size | The smaller number of genuinely independent pieces of information after accounting for repeated similar observations. |
| EX-99 | An exhibit attached to an SEC filing, often an earnings release or prepared remarks. |
| FinBERT | A language model adapted to financial text that assigns positive, neutral, and negative probabilities. |
| Fine-tuning | Further training an existing model on examples for a specific task. |
| Fiscal year | A company's accounting year, which may not match January through December. |
| Fixed effects | A regression technique that compares a company mainly with itself over time, helping account for stable company differences. |
| Gold standard | Carefully checked human labels used as the best available answer key. |
| Heuristic | A practical rule of thumb that often works but can make mistakes. |
| HTML | The formatting code used to structure webpages and many SEC filing documents. |
| ICC (intraclass correlation) | A number showing how similar repeated measurements from the same group, such as the same firm, are. |
| Infrastructure firm | In this project, a company classified as building or supplying important AI technology rather than mainly using it internally. |
| Interaction test | A test asking whether a relationship differs between groups. |
| Item 1A Risk Factors | The 10-K section where a company describes important risks to its business. |
| JSON | A structured text-file format used for data and settings. |
| Label | A tag assigned to text, such as “AI risk” or “AI opportunity.” |
| Language model | A computer system trained on text that can estimate, classify, or generate language. |
| Multi-label | A labeling setup where one passage can receive several tags at once. |
| Net tone | Positive probability minus negative probability; a higher score means more positive-sounding language. |
| Null result | A result that does not show a detectable difference; it does not prove there is no difference. |
| Outcome | The result a study wants to explain or predict, such as later employee growth or layoffs. |
| p-value | A test's estimate of how surprising a result would be if there were truly no pattern, given the test's assumptions. |
| Passage | A short block of text, longer than a sentence but shorter than a whole document. |
| Permutation test | A test that repeatedly rearranges group labels—in this case, exactly all possible arrangements—to see how unusual the observed difference is. |
| Placebo test | A deliberately irrelevant or backwards-looking check used to reveal a misleading research method. |
| Probability | A model's 0-to-1 estimate, not direct proof that a statement is true. |
| Pseudo-replication | Treating repeated observations from the same firm or source as if they were completely independent. |
| Regression | A statistical method for estimating how one measured variable relates to another while including selected other variables. |
| Risk factor | A stated possibility that could harm a company, usually listed in Item 1A. |
| SEC | The U.S. Securities and Exchange Commission, the government agency that oversees public-company disclosure. |
| Sensitivity analysis | Repeating an analysis after a reasonable change, such as dropping low-information filings, to see whether the conclusion changes. |
| Statistical significance | A conventional label for a small p-value; it is not the same thing as importance, truth, or causation. |
| TF-IDF cosine | A 0-to-1 text-similarity score based on which words appear and how distinctive they are. |
| Tone | How positive or negative a sentence sounds to the model. |
| Unflagged sample | Here, filings with at least five AI sentences and at least five other-risk sentences, reducing thin-evidence cases. |
| Within-document distance | In this project, AI-risk tone minus other-risk tone inside the same 10-K. |
