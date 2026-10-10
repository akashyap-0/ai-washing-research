# Earnings-call study: frozen scope (Gate 1)

Status: **frozen 2026-10-06, pending approval.** Changing anything below needs a written
reason in this file and a re-run of `python earnings_call_scope.py`. The rules are encoded in
[earnings_call_scope.py](earnings_call_scope.py), and the per-call record is
[earnings_calls/coverage_manifest.csv](earnings_calls/coverage_manifest.csv).

## 1. Universe

The seven Mag 7 firms only: Alphabet (GOOGL), Amazon (AMZN), Apple (AAPL), Meta (META),
Microsoft (MSFT), Nvidia (NVDA), Tesla (TSLA). Adding firms, including any S&P 500
expansion, is out of scope until Gate 10 is approved.

## 2. Study window and cutoff

- **Window:** calendar Q4 2021 through calendar Q2 2026, which is 19 calendar quarters.
- **Common cutoff:** Q2 2026, the last quarter all seven firms have reported. Calls for
  calendar Q3 2026 or later stay out of the main analysis even if they exist.
- **Expected calls:** 7 firms × 19 quarters = **133**, made up of 105 calls already in the repo
  plus 28 historical calls (Q4 2021 – Q3 2022). `python earnings_call_scope.py --check`
  checks this count and stops if it is not 133.

Main earnings call only. Separate follow-up calls (for example Meta's "Follow Up Call"),
investor days and conferences are excluded.

## 3. Period labels and calendar mapping

`period_label` is the label in the raw file name. It is **kept exactly as given and never
rewritten**: fiscal for Microsoft, Apple and Nvidia (`FY22_Q2`), calendar for the others
(`2021_Q4`). The `calendar_year` and `calendar_quarter` fields are extra fields used only
for pooling across firms. They do not replace the fiscal label.

Each fiscal quarter is assigned to the calendar quarter that holds most of its months:

| Firm | Fiscal year end | Rule | Window (first → last) |
|---|---|---|---|
| Alphabet, Amazon, Meta, Tesla | Dec 31 | same as the calendar | `2021_Q4` → `2026_Q2` |
| Microsoft | Jun 30 | FY Q1 = CY(FY−1) Q3, Q2 = CY(FY−1) Q4, Q3 = CY(FY) Q1, Q4 = CY(FY) Q2 | `FY22_Q2` → `FY26_Q4` |
| Apple | last Saturday of Sep | FY Q1 (≈Oct–Dec) = CY(FY−1) Q4, Q2 = CY(FY) Q1, Q3 = CY(FY) Q2, Q4 = CY(FY) Q3 | `FY22_Q1` → `FY26_Q3` |
| Nvidia | last Sunday of Jan | FY Qn = CY(FY−1) Qn (e.g. FY23 Q4 ≈ Nov 2022–Jan 2023 → 2022 Q4) | `FY22_Q4` → `FY27_Q2` |

The Nvidia rule needs approval (see §9). Nvidia's quarters run about one month behind the
calendar, so "2022 Q4" for Nvidia includes January 2023. The teammate passage filter
(`earnings_calls/filter_ai_passages.py:cal_quarter`) uses the same assignment, although
its docstring says "ends in", which is not accurate for Nvidia.

`expected_call_window` in the manifest runs from 14 to 60 days after the approximate
fiscal-quarter end. It is a derived planning range, not a fact from any source. `call_date`
is filled only when the file itself states the date (metadata, a transcript title line, or
the spoken "as of today, <date>"), or for absent calls, when the company IR event listing
gives one. Otherwise it is left blank, and the date is never inferred.

## 4. Unit of analysis

- **Measurement unit:** an AI-relevant transcript unit, meaning one row of
  `earnings_calls_canonical/earnings_call_sentences.csv` (Gate 3).
- In punctuated text a unit is a sentence (nltk Punkt with the filter's abbreviation list).
  In unpunctuated YouTube captions a unit is a ~30 s **caption segment**, and in Whisper
  transcripts it is a **sentence-like Whisper unit**. Every row carries `unit_type`.
  **Caption segments are not sentences.** Counts and shares built on them are not comparable
  to sentence-based calls and must be reported separately or excluded, never pooled silently.
- **Context passages** (`earnings_call_labeling_passages.csv`) are built from the sentence
  rows only to help later human annotation. They never replace the sentence unit and are
  never counted.

## 5. Primary and secondary sources

| Role | Source | Rule |
|---|---|---|
| Primary (source of truth) | Sentence-level filter: `filter_earnings_calls.py` → `earnings_calls_ai_only/` | The canonical dataset re-runs this exact filter code, read-only, on the current raw files (Gate 3) |
| Secondary / audit only | Teammate passage filter: `earnings_calls/filter_ai_passages.py` → `earnings_calls/ai_passages.csv` (3,335 passages) | Used only for comparison in Gate 4. Never merged with, appended to, or substituted for the primary data |

The two are different analytical units. The passage file uses a narrower term list, ±1
sentence of context, merged windows, a different sentence splitter, and different section and
speaker heuristics. Any reconciliation rule needs to be written down and approved in Gate 4
before the two are combined.

## 6. Denominator

- **Primary denominator:** all valid parsed call units in a firm-quarter. This is the filter's
  `total` for the call: every unit kept after removing known non-call text (metadata block,
  title/cover block, page numbers, running headers, disclaimers, Motley Fool roster and ads,
  pre-call livestream chatter, caption tags and timestamps). Operator lines are part of the
  call and count.
- **Section denominators:** units in prepared remarks and units in Q&A, kept separately.
- **Numerators and denominators are always kept as counts** (`earnings_call_call_units.csv`),
  never only as shares.
- Borderline automation/robotics and infrastructure-only units are part of the denominator and
  are **not** in the AI numerator. They go to a separate review file.

## 7. Sections

Prepared remarks and Q&A are separate measures throughout. A pooled whole-call figure may be
reported in addition, never instead. The method that found the Q&A start (explicit header,
first operator turn after management spoke, or a transition-phrase heuristic) is stored per
row as `section_method`.

## 8. What may not be claimed

- No claim about margins, layoffs, headcount, productivity, efficiency gains or any causal
  effect of AI is allowed until the outcome data and validated models from later gates exist.
  Even then, claims stay descriptive unless a causal design is approved.
- No AI mentions in a call does not mean the firm has not adopted AI.
- No semantic labels (opportunity, risk, efficiency, workforce reduction) exist yet. Existing
  SEC-filing labels and LLM annotations are not earnings-call gold labels.
- The sentence filter has not been fully validated. Its own records conflict (see the Gate 3
  report and Gate 4), so it must not be described as validated.

## 9. Scope limitations

1. **Source quality is uneven across firms.** Official IR text: Alphabet, Meta, Microsoft, and
   Nvidia FY26 Q1+ (FactSet CallStreet PDFs hosted by NVIDIA IR). Third-party Motley Fool:
   Nvidia FY23 Q4 – FY25 Q4 except FY24 Q4, Tesla 2022 Q4 and 2023 Q2 – 2024 Q4, and Apple FY23 Q1
   and FY24 Q4. YouTube auto-captions: 13 Apple calls, 7 Tesla calls, Nvidia FY24 Q4. Whisper
   machine transcripts of official IR audio: all 15 Amazon calls.
2. **No speaker labels** in any caption or Whisper file (`Speaker not labeled`), so role-based
   measures cannot be computed for Amazon, most Apple calls, Tesla caption calls, or Nvidia FY24 Q4.
3. **Unpunctuated caption files** (Apple FY23 Q2, FY23 Q4, FY24 Q1, FY24 Q2, FY24 Q3, FY25 Q1;
   Tesla 2023 Q1) use caption segments as units, so their counts are not comparable to the rest.
4. **Machine transcripts garble names and numbers.** Those errors are kept and never corrected.
5. **Known speaker-attribution gaps.** The Microsoft and Alphabet parsers do not recognise
   `NAME, Firm:` analyst labels, so an analyst's first question can be attributed to the
   previous speaker. Affected rows carry `speaker_attribution_warning`. In some committed Meta
   files, inline Q&A labels were lost during the original PDF extraction, which cannot be
   detected row by row.
6. **The historical window is incomplete.** 17 of the 28 Q4 2021 – Q3 2022 calls are not in
   the corpus (see `earnings_calls/ACQUISITION_LOG.md`). Any figure covering Q4 2021 – Q3 2022
   must show which firms are present in each quarter.
7. **Apple and Amazon are audio-only calls**, so they cannot be used for later video analysis.

## 10. Items that need approval

- The Nvidia and Apple calendar assignment (§3).
- Whether to accept non-company sources for the 9 calls awaiting a decision and the 8
  unavailable calls (see the acquisition log).
- Including the 11 newly acquired calls in the canonical dataset, even though the committed
  `earnings_calls_ai_only/` outputs (which this task did not modify) do not cover them.

**Approved 2026-10-10 (Advik):**

- **The 17 pre-2023 calls from non-company sources** (`earnings_calls_pre2022_extra/`) are included.
  Reason: they give pre-ChatGPT (Q4 2021 – Q3 2022) coverage for every firm except Amazon, whose
  added calls are Whisper units and not sentence-comparable. Every call stays flagged by
  `source_type` and `unit_type`.
- **The Nvidia and Apple fiscal-to-calendar assignment in §3.** Reason: each fiscal quarter goes to
  the calendar quarter holding most of its months. Nvidia's quarters run about one month behind the
  calendar quarter they are assigned to, and this lag is disclosed wherever Nvidia is pooled by quarter.
