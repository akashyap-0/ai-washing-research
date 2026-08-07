# RESULTS PACKET — AI-Washing in Corporate Layoffs

**Reference document for writing the Results section. Not paper text.**

Every figure below was pulled fresh from the live CSVs and read-only script outputs on
the date this file was generated — not from memory or prior summaries. Sources are named
per section so any number can be re-verified.

**Data sources**
- `export/ai_vs_other_risk_factors_results.csv` — within-document severity (Stage 3b)
- `export/ai_sentiment_distance_results.csv` — 8-K vs. 10-K distance (Stage 3a)
- `export/ai_washing_10-K.csv`, `export/ai_washing_8-K.csv` — raw extracted filing sections
- `export/labeling_dataset_llm_labeled.csv` — validation labels (see Section F caveat)
- Read-only scripts: `significance_tests.py`, `significance_tests_collapsed.py`,
  `firm_characteristics_test.py`, `validate_finbert_against_labels.py`

---

## SECTION A — Headline Finding: AI-Centrality (AI-core vs. AI-peripheral)

**Construct.** Does the company *sell* AI? This was Prof. Schloetzer's original stretch
goal (c) — whether firm characteristics explain cross-sectional variation in how severely
a company frames AI risk. Group membership was fixed a priori.

**Metric.** `within_doc_distance` = mean FinBERT net tone of AI-related Item 1A sentences
minus mean net tone of that same filing's non-AI Item 1A sentences. One observation per
10-K filing. Positive = AI risk framed *less* severely than the company's other risks
("opportunity-framed"). Negative = framed as or more severely ("existential-framed").

**Groups (fixed a priori, unchanged across every re-run):**

| Group | Companies (n=5 each) |
|---|---|
| AI-core | Oracle, Salesforce, Microsoft, AMD, NVIDIA |
| AI-peripheral | IBM, Dell, Verizon, American Express, UnitedHealth |

**Result**

| Group | n filings | mean |
|---|---|---|
| AI-core | 31 | **−0.0260** |
| AI-peripheral | 27 | **+0.3036** |

- Mean difference (core − peripheral): **−0.3297**
- Welch's t-test: **p = 0.0000**
- Mann-Whitney U: **p = 0.0001**

**Leave-one-out robustness — all 10 folds** (drop one company, re-test):

| Dropped | Welch p | Mann-Whitney p | Both still significant? |
|---|---|---|---|
| AMD | 0.0000 | 0.0000 | yes |
| Amex | 0.0000 | 0.0001 | yes |
| Dell | 0.0000 | 0.0000 | yes |
| IBM | 0.0001 | 0.0005 | yes |
| Microsoft | 0.0001 | 0.0004 | yes |
| NVIDIA | 0.0003 | 0.0010 | yes |
| Oracle | 0.0013 | 0.0015 | yes |
| Salesforce | 0.0000 | 0.0001 | yes |
| UnitedHealth | 0.0002 | 0.0007 | yes |
| Verizon | 0.0001 | 0.0005 | yes |

Welch p range **0.0000–0.0013**; Mann-Whitney p range **0.0000–0.0015**.
**Verdict: ROBUST** — significant on both tests in every fold. Weakest fold is dropping
Oracle (p=0.0013), still comfortably significant.

**Pooled sample context.** Pooled n across all companies = **118 scored 10-K filings**
from **24 companies** (26 companies pulled; Palantir excluded, Apple has no usable AI
data — see Section G). The 58 filings in this comparison are the subset belonging to
the ten AI-core/AI-peripheral companies.

**Writing note.** This finding is *arithmetically independent* of the extraction-bug fix
described in Section G: none of the three corrected companies (Accenture, Deere, Walmart)
belongs to either group, so the numbers are byte-identical before and after that
correction. Worth stating — it means the headline result was never contaminated.

---

## SECTION B — 8-K vs. 10-K AI-Sentence Distance (Stage 3a)

**Source:** `export/ai_sentiment_distance_results.csv`; `significance_tests.py`,
`significance_tests_collapsed.py`

**Construct.** Within a company, compare FinBERT net tone of AI-related sentences in
promotional 8-K earnings releases against AI-related sentences in the matched 10-K's Item
1A Risk Factors. A large positive distance = the company talks about AI far more
optimistically in the press release than in the legally-exposed annual report.

**Pooled result (all pairs, uncollapsed):** 665 pair rows, **287 with a computable
distance**.
- Mean 10-K AI-sentence net tone: **−0.2840** (84% of pairs net-negative)
- Mean 8-K AI-sentence net tone: **+0.4528** (5% of pairs net-negative)
- Mean distance (8-K − 10-K): **+0.7368**

**Pseudo-replication correction (methodologically important — describe this accurately).**
The fiscal-year pairing matches many 8-Ks to the same 10-K, so a single 10-K's tone value
is repeated across every 8-K matched to it. Treating those as independent inflates n and
shrinks p-values. Collapsing to **one row per unique 10-K** (averaging that 10-K's matched
8-K distances) reduces **287 pairs → 75 unique 10-Ks** (mean 3.8 8-Ks per 10-K; IBM is the
extreme at 8.0).

Collapsed pooled: n=75, mean **+0.7425**, t-test **p=0.000**, Wilcoxon **p=0.000**.

**Per-company, collapsed to unique 10-Ks:**

| Company | unique 10-Ks | mean distance | t-test p | Wilcoxon p | Verdict |
|---|---|---|---|---|---|
| Oracle | 9 | +0.9314 | 0.001 | 0.004 | **significant (both)** |
| Broadcom | 6 | +1.0859 | 0.000 | 0.031 | **significant (both)** |
| NVIDIA | 6 | +1.0281 | 0.000 | 0.031 | **significant (both)** |
| Tesla | 8 | +0.8595 | 0.001 | 0.008 | **significant (both)** |
| Microsoft | 6 | +0.7508 | 0.001 | 0.031 | **significant (both)** |
| IBM | 7 | +0.4906 | 0.017 | 0.031 | **significant (both)** |
| Intuit | 4 | +1.0352 | 0.005 | 0.125 | t only |
| S&P Global | 3 | +0.8089 | 0.020 | 0.250 | t only |
| Amazon | 5 | +0.4949 | 0.001 | 0.062 | t only |
| UnitedHealth | 2 | +0.7365 | 0.190 | 0.500 | underpowered |
| Salesforce | 2 | +0.6668 | 0.162 | 0.500 | underpowered |
| Alphabet | 2 | +0.6027 | 0.146 | 0.500 | underpowered |
| AMD | 3 | +0.5103 | 0.180 | 0.250 | underpowered |
| Uber | 2 | +0.5149 | 0.050 | 0.500 | underpowered |
| Deere | 3 | +0.3535 | 0.489 | 1.000 | underpowered |
| Dell | 4 | +0.2182 | 0.325 | 0.375 | underpowered |
| Verizon / Apple / Walmart | 1 each | — | n<2 | n<2 | not testable |
| Amex / Meta / Accenture / JPMorgan / Eli Lilly / ServiceNow | 0 | — | — | — | no computable pairs |
| **ALL (pooled)** | **75** | **+0.7425** | **0.000** | **0.000** | **significant** |

**Individually significant on both tests (the defensible per-company claims):** Oracle,
Broadcom, NVIDIA, Tesla, Microsoft, IBM.
**Underpowered / not individually significant:** Dell, AMD, Salesforce, Alphabet,
UnitedHealth, Deere, Uber, plus everything with n≤1.

**Before/after collapsing — which verdicts changed** (this is the honest robustness story):

| Company | n before → after | t-test before → after | Wilcoxon before → after |
|---|---|---|---|
| IBM | 56 → 7 | SIG → SIG | SIG → SIG |
| Oracle | 33 → 9 | SIG → SIG | SIG → SIG |
| Microsoft | 19 → 6 | SIG → SIG | SIG → SIG |
| NVIDIA | 26 → 6 | SIG → SIG | SIG → SIG |
| Tesla | 19 → 8 | SIG → SIG | SIG → SIG |
| Broadcom | 44 → 6 | SIG → SIG | SIG → SIG |
| **Salesforce** | 5 → 2 | **SIG → n.s.** | n.s. → n.s. |
| **AMD** | 7 → 3 | **SIG → n.s.** | **SIG → n.s.** |
| **Amazon** | 25 → 5 | SIG → SIG | **SIG → n.s.** |
| **S&P Global** | 9 → 3 | SIG → SIG | **SIG → n.s.** |
| **Intuit** | 16 → 4 | SIG → SIG | **SIG → n.s.** |
| **Walmart** | 6 → 1 | **SIG → not testable** | **SIG → not testable** |
| Dell | 5 → 4 | n.s. → n.s. | n.s. → n.s. |
| ALL pooled | 287 → 75 | SIG → SIG | SIG → SIG |

**Also dropped by the correction:** the IBM-vs-Oracle pairwise difference was significant
uncollapsed (p<0.001) but **not** significant collapsed (Welch p=0.070, Mann-Whitney
p=0.114). That cross-company claim should not be made.

---

## SECTION C — Within-Document AI-Risk vs. Other-Risk Severity (Stage 3b)

**Source:** `export/ai_vs_other_risk_factors_results.csv`

**Construct.** Prof. Schloetzer's second suggestion: within a *single* 10-K, does the
AI-related risk language read more or less severe than that same document's other risk
language? Positive = AI framed as an opportunity-type risk; negative = existential-type.

**Sample growth and the pooled result** (this is the key methodological arc — the effect
appears only once the sample is large enough):

| Stage | pooled n (10-K filings) | mean | t-test p | Wilcoxon p |
|---|---|---|---|---|
| Original 4-company sample | 25 | — | **0.56 (null)** | — |
| 10-company expansion | 58 | +0.1275 | 0.004 | 0.000 |
| 24-company expansion | 113 | +0.0826 | 0.007 | 0.001 |
| **Current (post extraction-fix)** | **118** | **+0.0831** | **0.005** | **0.001** |

Current pooled: mean AI tone **−0.2438**, mean other-risk tone **−0.3269**, distance
**+0.0831**, 95% CI **[+0.0260, +0.1403]**.

**Full per-company table** (all 25 companies with ≥1 scored filing; sorted by mean.
"flagged" = filings where the AI or non-AI subset had <5 sentences, i.e. low-confidence):

| Company | AI-centrality grp | Stack-role grp | n | flagged | mean | t-test p | Wilcoxon p |
|---|---|---|---|---|---|---|---|
| Verizon | AI-peripheral | — | 3 | 1 | +0.3983 | **0.007** | 0.250 |
| IBM | AI-peripheral | — | 7 | 5 | +0.3654 | **0.031** | **0.016** |
| UnitedHealth | AI-peripheral | Adopter | 6 | 3 | +0.3537 | **0.006** | **0.031** |
| Alphabet | — | Infrastructure | 3 | 0 | +0.3412 | **0.011** | 0.250 |
| Deere | — | Adopter | 6 | 4 | +0.3362 | **0.005** | **0.031** |
| ServiceNow | — | Adopter | 4 | 0 | +0.3231 | **0.019** | 0.125 |
| AMD | AI-core | Infrastructure | 4 | 1 | +0.2986 | **0.002** | 0.125 |
| Meta | — | Infrastructure | 2 | 0 | +0.2707 | 0.067 | 0.500 |
| Amazon | — | Infrastructure | 5 | 2 | +0.2682 | **0.001** | 0.062 |
| Amex | AI-peripheral | — | 7 | 4 | +0.2133 | **0.018** | **0.016** |
| Dell | AI-peripheral | — | 4 | 1 | +0.2078 | 0.222 | 0.125 |
| Intuit | — | Adopter | 4 | 0 | +0.1481 | 0.398 | 0.625 |
| Salesforce | AI-core | — | 3 | 0 | +0.1444 | **0.026** | 0.250 |
| Microsoft | AI-core | Infrastructure | 7 | 0 | +0.0896 | **0.031** | **0.031** |
| Walmart | — | Adopter | 3 | 1 | +0.0778 | 0.620 | 1.000 |
| Apple *(no usable AI data)* | — | Infrastructure | 2 | 2 | +0.0488 | 0.562 | 1.000 |
| S&P Global | — | Adopter | 4 | 0 | +0.0373 | 0.479 | 0.625 |
| Accenture | — | Adopter | 3 | 0 | +0.0209 | 0.740 | 0.750 |
| Uber | — | Adopter | 6 | 0 | +0.0197 | 0.606 | 0.438 |
| NVIDIA | AI-core | Infrastructure | 6 | 1 | −0.0754 | 0.462 | 1.000 |
| Eli Lilly | — | Adopter | 3 | 0 | −0.0818 | 0.387 | 0.500 |
| JPMorgan | — | Adopter | 1 | 0 | −0.1931 | n<2 | n<2 |
| Oracle | AI-core | — | 11 | 8 | −0.2371 | 0.065 | 0.102 |
| Tesla | — | Infrastructure | 8 | 5 | −0.3155 | **0.043** | 0.055 |
| Broadcom | — | Infrastructure | 6 | 4 | −0.3481 | **0.004** | **0.031** |
| **ALL pooled** | | | **118** | | **+0.0831** | **0.005** | **0.001** |

**Individually significant on both tests:** IBM, UnitedHealth, Deere, Amex, Microsoft,
Broadcom (Broadcom in the *negative* direction).

**Caveat to state in the paper:** Oracle's mean (−0.2371) rests on 11 filings of which
**8 are flagged** low-confidence — 8 of its filings (2016–2023) contain only a single AI
sentence in Item 1A. Its apparent "existential framing" is heavily driven by
single-sentence subsets. Same caution applies to IBM (5 of 7 flagged) and Tesla (5 of 8).

---

## SECTION D — Alternative Hypotheses Tested and Not Supported

Frame this section as: *we tested two further groupings and neither was supported.*

### D.1 — AI Infrastructure vs. AI Power Adopters (Prof. Schloetzer's specific request)

**Construct.** Does the company *build* the AI stack, or *use* AI internally for
productivity? Per the Wall Street / Goldman Sachs AI-productivity taxonomy.

| Group | Members |
|---|---|
| AI Infrastructure (8 scored) | Alphabet, Amazon, Meta, Microsoft, NVIDIA, Tesla, Broadcom, AMD — *Apple excluded, no usable AI data* |
| AI Power Adopters (10 scored) | Walmart, JPMorgan, Eli Lilly, Deere, Accenture, S&P Global, Intuit, ServiceNow, UnitedHealth, Uber |

TSMC was in Schloetzer's original Infrastructure list of 10 but **cannot be included**: it
files 20-F as a foreign private issuer, which this pipeline does not support (same reason
SAP was dropped earlier).

**Result**

| Group | n filings | mean |
|---|---|---|
| AI Infrastructure | 41 | −0.0082 |
| AI Power Adopters | 40 | +0.1537 |

- Mean difference: **−0.1619**
- Welch's t-test: **p = 0.0109** (significant)
- Mann-Whitney U: **p = 0.1225** (**not** significant)
- Leave-one-out: **FRAGILE — 16 of 18 folds lose significance.** Only dropping AMD,
  Alphabet, or Amazon leaves it significant on both tests. Welch p range 0.0032–0.1454;
  Mann-Whitney p range 0.0325–0.5991.

**Why it failed — three independent reasons:**

1. **The two tests disagree at baseline.** Significant parametrically, not
   non-parametrically. With group distributions this dispersed, the nonparametric result
   is the more trustworthy one.
2. **Leave-one-out collapse.** 16/18 folds fail. A result that survives only 2 of 18
   single-company deletions is not a group effect.
3. **Counterevidence from the best-qualified test cases.** After the extraction bug was
   fixed (Section G), Accenture and Walmart entered this comparison with real data for the
   first time — and both landed near zero (**Accenture +0.0209**, **Walmart +0.0778**)
   against an Adopters mean of +0.172, *diluting* the group toward Infrastructure. Adding
   them moved Welch p from 0.0065 → 0.0109, Mann-Whitney from 0.0746 → 0.1225, and
   leave-one-out failures from 8/16 → 16/18. Accenture is a consulting firm whose entire
   business is deploying technology for clients — arguably the purest "Power Adopter" in
   the set — and it frames AI risk essentially identically to its other risks. That is
   evidence against the grouping's premise, from its strongest theoretical case.

**Internal coherence.** Neither group is internally coherent. Infrastructure spans
Alphabet +0.341 to Broadcom −0.348, with members individually significant in *opposite
directions*. Adopters spans UnitedHealth +0.354 to JPMorgan −0.193.

### D.2 — Hyperscaler/Platform vs. Semiconductor/Hardware (POST-HOC)

**Flag this as post-hoc every time it is mentioned.** It was generated by inspecting D.1's
per-company results after the fact, so its p-values are optimistically biased by an
unquantifiable amount. It was *not* specified in advance.

| Group | Members |
|---|---|
| Hyperscaler/Platform | Alphabet, Amazon, Meta, Microsoft |
| Semiconductor/Hardware | NVIDIA, AMD, Broadcom, Tesla |

Membership was fixed by business-model logic (software-like margins and AI-as-a-service vs.
capital-intensive chip design/hardware production) *before* running the test. Evidence it
was not reverse-engineered: it places **AMD (+0.299, strongly opportunity-framed) in the
"severe" hardware group** and **Microsoft (+0.090, near zero) in the "opportunity" platform
group** — both assignments work against the hypothesis.

**Main result (Tesla included)**

| Group | n filings | mean |
|---|---|---|
| Hyperscaler/Platform | 17 | +0.2079 |
| Semiconductor/Hardware | 24 | −0.1613 |

- Mean difference: **+0.3691**
- Welch's t-test **p = 0.0000**; Mann-Whitney **p = 0.0005**
- Leave-one-out: **ROBUST**, all 8 folds significant on both tests (Welch 0.0000–0.0026;
  MWU 0.0000–0.0079)

**Sensitivity: Tesla removed** (its classification is genuinely ambiguous — it fits on
capital intensity and in-house inference silicon, but sells no chips to third parties, and
its AI exposure is really *applying* AI to a manufactured product, which is closer to an
Adopter; it is the weakest conceptual fit of the nine Infrastructure firms):

| Group | n filings | mean |
|---|---|---|
| Hyperscaler/Platform | 17 | +0.2079 |
| Semiconductor/Hardware (3 firms) | 16 | −0.0842 |

- Mean difference **+0.2920**; Welch **p = 0.0022**; Mann-Whitney **p = 0.0052**
- Leave-one-out: **FRAGILE — 2 of 7 folds fail.** Dropping **Broadcom** → Welch 0.1566 /
  MWU 0.1833; dropping **NVIDIA** → MWU 0.0747.

**Why it is not proposable as a replacement framing:** (a) post-hoc; (b) its robustness is
contingent on retaining Tesla, the member with the weakest justification — remove it and
the effect becomes fragile; (c) AMD is a within-group counterexample, a semiconductor firm
that frames AI risk *less* severely than its other risks, significantly so (p=0.002).

**Recommended framing:** a hypothesis worth testing on an expanded semiconductor/hardware
sample (Intel, Micron, Qualcomm, Texas Instruments, Applied Materials, Lam Research), not
a finding. Note Intel currently fails extraction entirely (see Section G).

---

## SECTION E — Oracle Case Study

All text below pulled verbatim from `export/ai_washing_10-K.csv` on the date of this file.

### E.1 — The citable admission

**Citation**
- Company: ORACLE CORP (ORCL)
- Filing: FY2026 Form 10-K, Item 1A Risk Factors
- Filing date: **2026-06-22**
- `doc_id`: **b5db10277712ffd2**
- URL: https://www.sec.gov/Archives/edgar/data/1341439/000119312526277521/orcl-20260531.htm
- Section length: 114,836 characters; located at character offset 36,059

**The sentence (verbatim):**

> In addition, the adoption and deployment of AI technologies across our operations have
> resulted, and may continue to result, in reductions to our workforce.

**Surrounding paragraph (verbatim, for context):**

> **Our periodic workforce restructurings and reorganizations can be disruptive.**
> We have an existing restructuring plan in place under which we have made, and will
> continue to make, adjustments to our workforce in response to management changes,
> product changes, performance issues, changes in strategies, acquisitions and other
> internal and external considerations. We may initiate new restructuring plans in the
> future. In addition, the adoption and deployment of AI technologies across our
> operations have resulted, and may continue to result, in reductions to our workforce.
>
> These types of restructurings have resulted, and may in the future result, in increased
> restructuring costs and reduced productivity. These types of restructurings may also
> lead to shortages of sufficiently skilled employees in certain roles, loss of valuable
> institutional knowledge and damage to employee morale and retention.

**Analytical points supported by the raw text:**
- The admission uses the past perfect — "**have resulted**" — so it is a statement of
  completed fact, not purely forward-looking risk boilerplate.
- It is **hedged and buried**: it appears as the *final sentence* of a generic
  restructuring paragraph, appended to a list of conventional causes (management changes,
  product changes, performance issues, strategy changes, acquisitions). It is **not** given
  its own risk-factor heading.
- The risk factor's own heading frames the topic as ordinary periodic restructuring, not
  as AI-driven workforce displacement.

### E.2 — 2020 vs. 2026 before/after contrast

Oracle's Item 1A AI-sentence count rose from **1 → 25** between FY2020 and FY2026
(same keyword filter, same extraction, both verified in this run).

**FY2020 — the complete AI risk disclosure (all of it, one sentence):**
- Filing date **2020-06-22**; `doc_id` **923d2c6a00b872e9**
- URL: https://www.sec.gov/Archives/edgar/data/1341439/000156459020030125/orcl-10k_20200531.htm

> Machine learning and artificial intelligence are increasingly driving innovations in
> technology but if they fail to operate as anticipated or our other products do not
> perform as promised, our business and reputation may be harmed .

*(The trailing space before the period is in the source text as extracted.)*

**FY2026 — 25 AI sentences spanning materially new risk categories.** Representative
verbatim examples of categories that did not exist in 2020:

- *Workforce:* "In addition, the adoption and deployment of AI technologies across our
  operations have resulted, and may continue to result, in reductions to our workforce."
- *EU AI Act / regulation:* "Additionally, obligations under the EU AI Act have gone into
  effect and will continue to be implemented in phases through 2030, and other
  jurisdictions have passed or are considering similarly focused legislation."
- *Bias / model quality:* "The data used to develop or operate AI systems may be overly
  broad, incomplete, or include biased or inaccurate information, which could result in
  outputs that are offensive, unlawful, inaccurate or otherwise harmful."
- *Cybersecurity:* "The increasing use of AI technologies may also introduce or accelerate
  existing cybersecurity and operational risks."
- *Energy/datacenter constraint:* "We have faced, and may continue to face, challenges
  with securing reliable and cost-effective power sources for our data center energy
  demands, which are constrained globally due to the significant increase in demand for
  and limited availability of energy to power AI compute."
- *Reskilling:* "In addition, implementation of AI tools may require new skills and
  capabilities, and we may not be successful in reskilling current employees."

**The contrast to draw:** in 2020 Oracle's entire AI risk disclosure was a single generic
clause about products failing to work as advertised. By 2026 it is a multi-paragraph risk
block covering workforce reduction, regulation, bias, cybersecurity, energy supply, and
talent — including a concrete admission that AI has already cut headcount.

---

## SECTION F — Methodology Validation (FinBERT vs. Labels)

**Source:** `validate_finbert_against_labels.py` (read-only), run fresh for this packet;
labels in `export/labeling_dataset_llm_labeled.csv`

### ⚠️ F.0 — LABEL PROVENANCE: MUST BE DISCLOSED IN THE METHODS SECTION

**The validation labels are LLM-generated, not human-labeled.** This is not a detail to
gloss over. Verified facts:

- `export/labeling_dataset.csv` contains **1,226 sentences** and its `label` column is
  **blank on all 1,226 rows** (confirmed directly: 0 non-blank labels). The Stage-1
  hand-labeling pass was never completed or saved.
- No independently-collected human labels exist anywhere in the repo.
- `export/labeling_dataset_llm_labeled.csv` holds **1,226 single-pass LLM-generated labels**
  against a fixed disclosed rubric — **not** independently verified human labels, not
  double-coded, and with no professor adjudication.
- Sentence sources: IBM 784, Oracle 238, Salesforce 183, Dell 21.
- Label distribution: vague AI buzzword 507, other/NA 344, genuine automation claim 262,
  efficiency framing 109, demand-decline framing **4**.

**What this limits.** The exercise tests whether FinBERT tone tracks *a defensible,
internally consistent reading* of these categories — **not** whether it tracks independent
human judgment. Any claim of "validated against human labels" would be inaccurate. See
OPEN ITEMS #1.

### F.1 — Per-category FinBERT tone distribution

| Category | n | mean | std | median |
|---|---|---|---|---|
| genuine automation claim | 262 | +0.5939 | 0.3280 | +0.7014 |
| vague AI buzzword | 507 | +0.6011 | 0.3321 | +0.7441 |
| efficiency framing | 109 | −0.0005 | 0.7174 | +0.0073 |
| demand-decline framing | 4 | −0.1108 | 0.9833 | −0.1555 |
| other / not applicable | 344 | −0.0539 | 0.5230 | +0.0041 |

Shapiro-Wilk: non-normal in 4 of 5 categories (all p=0.0000 except demand-decline,
p=0.0663, n=4) → **Kruskal-Wallis is primary**, both reported.

Omnibus: one-way ANOVA **F=152.214, p=0.0000**; Kruskal-Wallis **H=369.662, p=0.0000**.

### F.2 — What the validation CONFIRMED

FinBERT cleanly separates **promotional AI language from hedged/neutral language**, with
large effect sizes:

| Comparison | mean diff | Cohen's d | Welch p | MWU p |
|---|---|---|---|---|
| genuine automation vs. efficiency framing | +0.5944 | **+1.248** | 0.0000 | 0.0000 |
| vague buzzword vs. efficiency framing | +0.6017 | **+1.413** | 0.0000 | 0.0000 |
| genuine automation vs. other/NA | +0.6477 | **+1.442** | 0.0000 | 0.0000 |
| vague buzzword vs. other/NA | +0.6550 | **+1.560** | 0.0000 | 0.0000 |

This is the construct the paper's Stage 3 method actually relies on — the promotional-vs-
hedged axis — and it holds with d > 1.2 in every test.

### F.3 — What the validation did NOT confirm

**Key Question 1 — genuine automation claim vs. vague AI buzzword: NOT distinguishable.**

- means +0.5939 vs. +0.6011, difference **−0.0073**, Cohen's d **−0.022**
- Welch t **p = 0.7721**; Mann-Whitney **p = 0.6520**

FinBERT cannot tell a substantive AI capability claim from generic AI marketing language —
both simply read as positive. **This is a direct limitation on the AI-washing construct**:
the method detects *that* a company is talking about AI optimistically, not *whether the
optimism is substantiated*. State this explicitly as a limitation.

**Key Question 2 — efficiency framing vs. demand-decline framing: NOT distinguishable.**

- means −0.0005 vs. −0.1108, difference +0.1102, Cohen's d +0.152
- Welch t **p = 0.8380**; Mann-Whitney **p = 0.4236**
- **n=4 for demand-decline** — this comparison is severely underpowered and should be
  reported as inconclusive-by-sample-size rather than as evidence of no difference.

These are the two competing explanations for layoffs at the heart of the paper's puzzle, and
sentiment polarity does not separate them.

---

## SECTION G — Data & Pipeline Summary

### G.1 — Final company roster

**26 companies pulled.** Per-company sample sizes (from the live CSVs):

| Ticker | Company | 10-K Item 1A filings | 8-K filings | within-doc scored | flagged | max AI sentences |
|---|---|---|---|---|---|---|
| IBM | IBM | 7 | 73 | 7 | 5 | 10 |
| ORCL | Oracle | 11 | 60 | 11 | 8 | 25 |
| DELL | Dell | 4 | 10 | 4 | 1 | 21 |
| CRM | Salesforce | 3 | 6 | 3 | 0 | 43 |
| MSFT | Microsoft | 7 | 48 | 7 | 0 | 65 |
| AMD | AMD | 9 | 12 | 4 | 1 | 41 |
| NVDA | NVIDIA | 6 | 27 | 6 | 1 | 49 |
| VZ | Verizon | 3 | 16 | 3 | 1 | 9 |
| AXP | American Express | 7 | 16 | 7 | 4 | 23 |
| UNH | UnitedHealth | 6 | 8 | 6 | 3 | 12 |
| GOOGL | Alphabet | 3 | 5 | 3 | 0 | 39 |
| AMZN | Amazon | 6 | 33 | 5 | 2 | 11 |
| AAPL | Apple | 11 | 32 | 2 | 2 | **4** |
| META | Meta | 2 | 0 | 2 | 0 | 45 |
| TSLA | Tesla | 8 | 67 | 8 | 5 | 9 |
| AVGO | Broadcom | 8 | 69 | 6 | 4 | 19 |
| ACN | Accenture | 3 | 0 | 3 | 0 | 27 |
| WMT | Walmart | 3 | 19 | 3 | 1 | 10 |
| JPM | JPMorgan | 1 | 7 | 1 | 0 | 8 |
| LLY | Eli Lilly | 5 | 2 | 3 | 0 | 18 |
| DE | Deere | 12 | 81 | 6 | 4 | 10 |
| SPGI | S&P Global | 9 | 79 | 4 | 0 | 29 |
| INTU | Intuit | 6 | 28 | 4 | 0 | 28 |
| NOW | ServiceNow | 4 | 1 | 4 | 0 | 24 |
| UBER | Uber | 6 | 15 | 6 | 0 | 18 |
| PLTR | Palantir | 6 | 27 | **0 (excluded)** | — | — |

### G.2 — Exclusions, with reasons

| Entity | Status | Reason |
|---|---|---|
| **TSMC** | Never pulled | Files **20-F** as a foreign private issuer; pipeline handles 10-K filers only. Same reason SAP was dropped. Reduces Schloetzer's Infrastructure group from 10 firms to 9. |
| **Palantir** | Pulled, **excluded from all analysis** | Present in the export files from an earlier unrelated bulk commit; never on any approved company list. Enforced by `APPROVED_TICKERS` in `extract_ai_sentiment.py`. |
| **Apple** | Scored, **excluded from group means** | Genuinely has almost no AI risk-factor language: max **4** AI sentences in any single filing, across 11 filings, below the 5-sentence reliability floor. Not a bug — dropped rather than zero-filled, since "cannot measure" ≠ "neutral tone". |
| **Intel** | Not in dataset | Item 1A extraction fails on all 7 filings for a structural reason: Intel never labels its risk-factors section "Item 1A" — it uses a Form 10-K cross-reference index mapping items to page ranges. Relevant if the semiconductor sample is ever expanded. |

**Two Palantir claims to correct if they appear in any earlier draft:** (1) Palantir has
**no** encoding corruption — 0 instances of U+FFFD in both the fresh fetch and the stored
CSV; the character in question is U+2019, an ordinary curly apostrophe. (2) Its Item 1A
"swallowing" Item 1B/2/3 is **not** Palantir-specific — `_ITEM_PATTERNS` contains no
Item 1B/2/3 boundary patterns, so Item 1A runs to Item 7 for *every* company.

### G.3 — Extraction-bug correction (describe in Methods or a data-quality footnote)

`edgar.py`'s `extract_sections()` had **four independent defects**, all diagnosed and fixed:

1. **Running page headers.** Filers repeating the section title at the top of every page
   produced many line-anchored matches; the old max-gap selection rule picked one of those
   instead of the real heading, yielding fragments starting mid-sentence.
2. **Too-tight separator tolerance.** Only 8 non-alphanumeric characters were allowed
   between item number and title; Deere's headings span table cells with 17–50 characters
   of non-breaking spaces, so the real heading never matched at all.
3. **Line-anchored cross-references.** A wrapped quotation such as `…see "Item 1A. Risk
   Factors" under…` can place the quote at the start of a line, indistinguishable from a
   heading.
4. **Same-item running headers treated as boundaries**, truncating sections to one page.

Fix approach: select the earliest candidate followed by real lowercase prose
(`MIN_PROSE_WORDS = 8`) rather than by a character-count floor — necessary because a TOC
line and a legitimately one-sentence section are the same length (Accenture's TOC line is
followed by 325 characters, IBM's genuine one-sentence Item 7 by 211). Cross-reference
tails are dropped; section end is the next *different* item heading.

**Regression-checked:** re-extracted all filings and diffed against the prior output —
**267 sections byte-identical**, with every Item 1A change confined to the four
known-broken companies. No previously-correct Item 1A section changed.

**Recovered filings:**

| Company | Before | After |
|---|---|---|
| Accenture (3 filings) | 11.6K / 19.4K / 20.7K chars, garbled | **92.8K / 106.1K / 108.4K**, clean heading |
| Deere 2014–2018 (5 filings) | 379–415 chars (TOC stubs) | **38.9K–46.6K** |
| Walmart (3 filings) | ~48K but starting mid-sentence | **99.4K / 104.5K / 108.3K** |

**Conclusions the fix overturned or corrected:**
- **Walmart's "essentially no AI risk language" was wrong** — an artifact of broken
  extraction. Real counts are **2, 5, 10** AI sentences (was 0, 0, 1). It now enters the
  Adopters group.
- **Accenture had no usable data at all** (0/3) purely because of the bug. It now has
  **13, 26, 27** AI sentences, all clearing the reliability floor.
- **Deere's recovered 2014–2018 filings contain zero AI sentences** — historically
  expected for pre-2019 10-Ks. Deere's scored n therefore stays at 6, not 12; the
  recovered filings are real but analytically empty.

### G.4 — Sample sizes at each stage

| Stage | Unit | n |
|---|---|---|
| Companies pulled | company | 26 |
| Companies with usable scored data | company | 24 (excl. Palantir, Apple) |
| 10-K Item 1A sections extracted | filing-section | 150 rows in results file |
| Within-document scored filings (Stage 3b) | 10-K filing | **118** |
| 8-K/10-K pairs constructed | pair | 665 |
| Pairs with computable distance (Stage 3a) | pair | 287 |
| Unique 10-Ks after pseudo-replication collapse | 10-K filing | **75** |
| Validation sentences | sentence | 1,226 (LLM-labeled) |

### G.5 — Methodology paragraph (adapt for Methods section)

> Filings were collected directly from the SEC EDGAR full-text and submissions APIs for 26
> large-cap U.S. issuers, restricted to 10-K filers (foreign private issuers filing 20-F,
> such as TSMC and SAP, are outside the pipeline's scope). For each 10-K, the Item 1A Risk
> Factors section was located heuristically by matching line-anchored item headings and
> validated by requiring substantive prose to follow the match, a check introduced after
> four distinct extraction defects were identified and corrected. For each 8-K, EX-99
> earnings-release and prepared-remarks exhibits were extracted, with filer-specific naming
> conventions accommodated (e.g. NVIDIA's `q4fy26pr.htm`, UnitedHealth's
> `earningsrelease…htm`). Each 8-K was matched to the 10-K covering the same fiscal year
> using the interval between consecutive 10-K filing dates as a fiscal-year proxy; 8-Ks
> filed after a company's most recent 10-K were left unmatched rather than assigned. Within
> each document, sentences were segmented with NLTK Punkt, bounded to 6–60 words, and
> filtered to those matching an AI-specific keyword pattern (AI, artificial intelligence,
> generative AI, machine learning, deep learning, neural networks, LLMs, automation,
> cognitive computing, plus the branded terms Agentforce, watsonx, and Watson). Each
> matched sentence was scored individually with FinBERT (ProsusAI/finbert) and reduced to a
> net-tone scalar, P(positive) − P(negative), the FinBERT analogue of a Loughran-McDonald
> net-tone measure. Two distance measures were computed: a between-document measure (mean
> 8-K AI-sentence tone minus mean 10-K AI-sentence tone) and a within-document measure
> (mean AI-related Item 1A sentence tone minus mean non-AI Item 1A sentence tone). Subsets
> with fewer than five qualifying sentences were flagged as low-confidence. Because the
> fiscal-year pairing matches multiple 8-Ks to a single 10-K, all between-document
> significance tests are reported both uncollapsed and collapsed to one observation per
> unique 10-K; the collapsed figures are the ones we rely on. Significance is assessed with
> both a parametric test (one-sample or Welch's t) and its nonparametric analogue (Wilcoxon
> signed-rank or Mann-Whitney U), with the nonparametric result preferred at small n, and
> group-level comparisons additionally subjected to a leave-one-out check in which each
> company is dropped in turn.

---

## OPEN ITEMS — decisions needed before this goes in the paper

1. **⚠️ Label-provenance disclosure to Prof. Schloetzer (highest priority).** The Section F
   validation rests on **LLM-generated labels**, because the original hand-labeling pass was
   never completed (all 1,226 `label` cells are blank). The repo documents this honestly,
   but Schloetzer may believe human labels exist. He needs to be told before the validation
   is cited, and the Methods section must say "LLM-generated single-pass labels against a
   fixed rubric," never "hand-labeled" or "human-validated." **Decision:** disclose to him
   now, or drop Section F from the paper and cite the method without construct validation?

2. **Does the post-hoc hyperscaler/semiconductor split get mentioned at all?** Options:
   (a) omit entirely; (b) one sentence in Limitations/Future Work flagged as post-hoc and
   Tesla-dependent; (c) a short subsection under alternative hypotheses. Recommend (b) — it
   is not robust enough for more, but it is the most concrete future-work direction, and it
   is the honest explanation for *why* D.1 failed.

3. **How to report Oracle's flagged filings.** Oracle's −0.2371 mean rests on 11 filings of
   which 8 have only a single AI sentence. Options: report as-is with a caveat; report a
   sensitivity restricted to unflagged filings; or drop the per-company Oracle claim and
   rely only on the case study. Same question applies to IBM (5/7 flagged) and Tesla (5/8).
   **No sensitivity analysis restricted to unflagged filings has been run yet** — flagging
   as an available robustness check, not a completed one.

4. **Whether to fold the recovered Deere 2014–2018 filings into any time-trend analysis.**
   They contain zero AI sentences, which is itself a meaningful baseline observation
   (pre-2019 filings simply did not discuss AI) but contributes nothing to tone measures.
   If the paper makes a "growth of AI disclosure over time" argument, these are useful; if
   not, they are inert.

5. **⚠️ `firm_characteristics_robustness.py` is currently broken — and I broke it.** When I
   rewrote `firm_characteristics_test.py` to hold two grouping variables, `group_of()`
   gained a required second argument, and this script still calls it with one. It now
   crashes with `TypeError: group_of() missing 1 required positional argument: 'grouping'`.
   It is a read-only diagnostic, so no data or result was corrupted, but its Oracle/NVIDIA
   hold-out analysis is unavailable until a one-line fix. I did not repair it because this
   task was scoped read-only. **Decision:** want it fixed?

6. **Correction to a claim I made earlier in our conversation.** I previously told you the
   leave-one-out robustness check "did not previously exist" in the codebase. **That was
   wrong.** `firm_characteristics_robustness.py` already contained a leave-one-out check for
   the AI-core/peripheral comparison. It differs from the one now in
   `firm_characteristics_test.py` — the pre-existing version drops only AI-core companies
   and holds the peripheral group fixed, whereas the newer one drops companies from both
   groups — so the two are complementary rather than duplicative. But your original framing
   that such a check already existed was correct, and mine was not.

7. **Stage 2 (whole-document sentiment distance) is not in this packet.**
   `export/sentiment_distance_results.csv` still exists from the abandoned approach, along
   with the confound that all 145 10-K scores were negative regardless of company. Decide
   whether Stage 2 appears in the paper as methodological narrative (why Stage 3 was
   necessary) or is omitted entirely.

8. **Item 7 MD&A sections are no longer extracted for some filers** (Deere 2019–2025,
   Tesla 2019–2020) because their genuine Item 7 is a ~180-character
   incorporation-by-reference stub that falls below the prose threshold. No active analysis
   uses Item 7, so no result is affected — but if the paper ever cites MD&A text, this
   matters.
