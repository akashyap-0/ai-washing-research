# Gate 4 validation report: canonical earnings-call corpus

| | |
|---|---|
| Report version | gate4-v1, 2026-10-06 |
| Corpus | 116 present calls of 133 expected (Mag 7, Q4 2021 – Q2 2026) |
| Extraction | `filter_earnings_calls.py@sha256:<12>/canonical-v2` (see `gate4_validation.json → extraction_version`) |
| Machine-readable results | [gate4_validation.json](gate4_validation.json) |
| Reproduce | `python build_earnings_call_canonical.py` then `python earnings_calls_canonical/gate4_validate.py` |

**What this is.** Mechanical checks **run by code**. No human has validated any row. "Pass"
below means a coded check passed, not that a person confirmed the data. The AI filter's
precision and recall have **not** been validated: no new hand review was done here, and the
150-row review sheet (§9) is blank.

**This is the only validation report for the 116-call canonical corpus.** Legacy results in
`earnings_calls_ai_only/_validation.json` and in the Validation section of
`earnings_calls_ai_only/FILTER_METHOD.md` describe earlier corpus states and **must not be
quoted** as describing this corpus (§8).

## Summary

| Check | Result |
|---|---|
| 1. Scope coverage | 133 expected, 116 present, 17 missing (9 awaiting a source decision, 8 unavailable) |
| 2. Source/output coverage | Pass. All 116 raw files have sentence and passage rows. No extra, stray or duplicate source files |
| 3. Field completeness | Pass. 0 missing required values. Blanks only where the source gives nothing (call_date 3,106 rows, source_url 1,038), and no fabricated values (every date re-derived from the file, every URL found in the file's metadata) |
| 4. IDs and reproducibility | Pass. 0 duplicate sentence, passage or borderline IDs. 0 orphaned anchors. Clean rebuild into an empty directory byte-identical for all 5 generated files |
| 5. Verbatim | Pass for all 9,884 canonical sentences and 2,413 borderline rows. 1 failure among 54,350 parsed units (a non-AI unit, explained below) |
| 6. Sections and speakers | 0 unknown-section rows. 176 AI speaker errors corrected. 46 unresolved, 802 unverified, 1,858 from unlabelled sources. **New defect found:** misplaced labels in 2 Gate 2 acquisitions (quarantined) |
| 7. Flags | uncertain 2,566; context-dependent 585; long 1; safe-harbor 0; borderline automation/robotics 456; borderline infrastructure 1,957 |
| 8. Unit comparability | 80 sentence calls, 14 punctuated-caption calls, 15 Whisper calls, 7 caption-segment calls. Not directly comparable |
| B3. Filter reconciliation | 105 calls in both. 93.4% of canonical core-term units overlap Tanush's passages, and 96.7% of his passages contain a canonical unit. Canonical is primary; Tanush's passages are audit only |
| B5. Review sample | 150 rows, seed 20261006, judgment columns blank |

## Part A: labeling passages (Gate 3 corrective finish)

Note on the brief: the previous passage file did have context for every row (9,884 of
9,884), but its rule (≤2 before, ≤1 after, same section) crossed speaker turns in 637
passages. The new rule fixes that.

**Rule `ctx-v2-same-turn-pm1`:** the anchor plus the immediately previous and next parsed
unit **of the same speaker turn** (same speaker, section and call). It never crosses a speaker
change, the prepared/Q&A boundary or the transcript boundary. With no neighbour, the passage
is the anchor alone.

| `context_speaker_continuity` | Passages | Meaning |
|---|---:|---|
| `same_labelled_speaker_turn` | 7,215 | genuine same-speaker context |
| `same_turn_unlabelled_source_speaker_unverified` | 1,858 | caption/Whisper files: the whole section is one unlabelled turn, so a speaker change inside it cannot be detected |
| `same_turn_meta_label_loss_risk` | 733 | original-corpus Meta Q&A (see §6) |
| `same_turn_raw_label_misplacement_risk` | 69 | `meta_2022_Q2`, `meta_2022_Q3` (see §6) |
| `anchor_only_no_same_turn_neighbour` | 9 | anchor is a one-unit turn |

The passages contain 29,271 context IDs. All AI and borderline context IDs resolve to rows in
the sentence and borderline files. The 9,280 non-AI context units are not stored as rows; their
text is in the passage and their IDs follow the same formula. Sentence rows remain the
measurement unit, and any passage label maps back via `anchor_sentence_id`.

**Change versus the previous sentence file** (`git HEAD`, canonical-v1):

- same 9,884 rows;
- 1 ID replaced (label text removed: `alphabet_2022_Q3_u0436_8c6a59d3e5` →
  `alphabet_2022_Q3_u0436_398e6c3edd`, in the audit);
- `text_verbatim` unchanged on every common ID;
- changed columns: `speaker` and `speaker_role` (175 common rows plus the 1 replaced),
  `turn_order_in_call` (660, renumbered by turn splits), `extraction_version` (all rows);
- removed column: `speaker_attribution_warning`;
- added columns: `speaker_status`, `speaker_status_reason`, `speaker_correction_rule`.

## 1. Scope coverage

| Status | Calls |
|---|---|
| Present (116) | 105 original + 11 acquired in Gate 2 |
| Awaiting human source decision (9) | alphabet 2021_Q4; amazon 2021_Q4, 2022_Q1, 2022_Q2, 2022_Q3; tesla 2021_Q4, 2022_Q1, 2022_Q2, 2022_Q3 |
| Unavailable public source (8) | apple FY22_Q1, FY22_Q2, FY22_Q3, FY22_Q4; nvidia FY22_Q4, FY23_Q1, FY23_Q2, FY23_Q3 |

All 17 missing calls fall in Q4 2021 – Q3 2022. Reasons are in `earnings_calls/ACQUISITION_LOG.md`.

## 2. Source / output coverage

116 raw files on disk, all in the expected set. No case-insensitive duplicate stems. Every
present call has sentence rows, passage rows and a call-units row. No output call lies outside
the present set. No call has zero AI rows.

## 3. Field completeness

All 37 sentence fields were checked. Every required field has 0 missing values.

| Field | Blank rows | Why |
|---|---:|---|
| `call_date` | 3,106 | date not stated in the source file; never inferred |
| `source_url` | 1,038 | Nvidia FY26 Q1 – FY27 Q2 metadata gives no URL |
| `speaker_status_reason`, `speaker_correction_rule`, `core_terms`, `weak_terms`, `call_parse_flags` | by design | blank when not applicable |

To check that nothing was fabricated, every stored `call_date` was re-derived from its own
raw file. All 116 matched, and every stored `source_url` occurs in that file's metadata.

## 4. IDs and reproducibility

Duplicate sentence, passage and borderline IDs: 0, 0, 0. Orphaned anchors: 0. Sentences
without a passage: 0. IDs not matching the formula: 0.

**Clean rebuild:** `build_earnings_call_canonical.py --out <new empty temp dir>`, then a byte
comparison with `earnings_calls_canonical/`. All 5 files were identical and the IDs were
identical and in the same order. Outputs embed no timestamps, temp paths or git HEAD.
Separate builds under `PYTHONHASHSEED` = 1, 2 and 3 were also identical.

Disclosure: one earlier Gate 4 run in this session reported `build_validation.json` as not
byte-identical (the 4 CSVs were identical). Six later attempts did not reproduce it: the final
full run, an isolated re-run, three hash seeds, and a manual rebuild. It most likely compared
against a file from an earlier build, but this is not proven.

## 5. Verbatim / source checks (code, not human)

- **Tier 1:** the unit, with whitespace collapsed, is a substring of the raw body after the
  documented normalization (HTML entities decoded, `[mm:ss]` timestamps and caption tags
  removed, whitespace collapsed).
- **Tier 2:** if tier 1 fails, the filter's `verbatim_found`, which also allows the filter's
  deleted noise (page numbers, FactSet headers, hyphen wraps) between words.

| Rows | Checked | Tier 1 | Tier 2 only | Failures |
|---|---:|---:|---:|---:|
| Canonical AI sentences | 9,884 | 9,739 | 145 | **0** |
| Borderline rows | 2,413 | 2,391 | 22 | 0 |
| All parsed units (incl. non-AI) | 54,350 | 53,954 | 395 | **1** |

The one failure is `meta_2022_Q3_u0233_38f63447fd`, a non-AI unit: "first 34 of 39 words
found contiguous; break before 'rationalize our real estate'". The raw file has a misplaced
`Operator:` label inside this sentence (§6). The words are correct, but the label sits
between them.

## 6. Sections and speakers

**Sections.** AI rows: prepared remarks 4,981, Q&A 4,903, unknown 0. No call has only one
section. No labelled call has only one speaker. 36 calls have a single speaker only because
the source has no labels (15 Amazon, 13 Apple, 7 Tesla, Nvidia FY24 Q4).

**Speaker corrections (B1).** Both rules use only text in the same raw transcript:

| Rule | Units changed | Confidence |
|---|---:|---|
| `msft_name_comma_firm_label`: raw `KEITH WEISS, Morgan Stanley:` starts that speaker's turn | 973 | high (explicit label) |
| `alphabet_name_comma_firm_label`: raw `Brian Nowak, Morgan Stanley:` (Alphabet 2022 Q1–Q3) | 255 | high |
| `same_transcript_name_propagation`: bare `Keith Weiss` → `Keith Weiss, Morgan Stanley` when the same transcript gives exactly one such label | 169 | medium |

That is 1,397 units in total: **176 AI rows corrected**, which covers all 175 rows previously
flagged plus 1. All 41 distinct label strings were checked and all are analyst labels. After
correction, 0 unrecognised `NAME, Firm:` labels remain. Typical fixes: `Brett Iversen` (IR host)
→ the analyst actually asking, e.g. `Keith Weiss, Morgan Stanley`, `Karl Keirstead, UBS`.

**Speaker status of the 9,884 AI rows:**

| Status | Rows |
|---|---:|
| resolved | 6,999 |
| resolved_corrected | 176 |
| operator | 3 |
| unresolved_bare_name | 37 |
| unknown_speaker_in_source | 9 |
| unverified_meta_label_loss_risk | 733 |
| unverified_raw_label_misplacement | 69 |
| unlabeled_source | 1,858 |

- Resolved total: 7,178. Unresolved: 46 (37 bare names plus 9 "Unknown speaker" rows).
- The 37 bare names cannot be resolved from the transcripts: Tesla `Elon Musk` (21) and
  `Martin Viecha` (9) in files that never give them a title, and Meta `David Wehner` (3),
  `Javier Olivan`, `Eric Sheridan`, `Brian Nowak`, `Kenneth Gawrelski` (1 each).
- `speaker_attribution_audit.csv` has 4,103 rows: 1,397 corrected units (176 AI) plus every
  AI row not resolved, each with a reason.

**Meta label loss (unresolved by design).** Original-corpus Meta raw files can lack inline Q&A
labels. Gate 2 proved this for `meta_2022_Q4` against the official PDF, and the loss cannot be
detected row by row from the raw text. Per this task, no outside source was used, so all 733 Q&A
AI rows of the 15 original Meta calls are marked `unverified_meta_label_loss_risk` and left
unchanged.

**New defect: label misplacement in two Gate 2 acquisitions.** Comparing each acquired PDF
file with `pdftotext -raw` of its cached official original (label plus next 4 words):

| Call | Labels (PDF -raw / raw file) | In PDF, not in file | In file, not in PDF |
|---|---|---:|---:|
| meta_2022_Q2 | 39 / 38 | 16 | 15 |
| meta_2022_Q3 | 34 / 33 | 14 | 13 |
| meta_2021_Q4, meta_2022_Q1, alphabet_2022_Q1–Q3 | identical | 0 | 0 |

The Gate 2 `pdftotext -layout` extraction moved some inline labels to the wrong lines. For
example, a stray `Operator:` turns part of the CFO's answer into the Operator's, and
`Justin Post:` lands inside the CFO's text. The text is complete and the prepared/Q&A
boundary is correct, but speakers in these two calls are not reliable. Raw text may not be
changed in Gate 4, so all 69 labelled AI rows there are quarantined as
`unverified_raw_label_misplacement`. **Gate 2's "0 corrupted" was wrong** (erratum:
`earnings_calls/ACQUISITION_LOG_GATE4_ERRATUM.md`). The fix needs approval: re-extract both
files with `pdftotext -raw` from the cached PDFs, then rebuild.

## 7. Filter flags

| | Alphabet | Amazon | Apple | Meta | Microsoft | Nvidia | Tesla | All |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| uncertain | 234 | 233 | 17 | 310 | 295 | 921 | 556 | 2,566 |
| context-dependent | 123 | 80 | 11 | 78 | 87 | 150 | 56 | 585 |
| long | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 1 |
| borderline automation/robotics | 23 | 71 | 0 | 33 | 19 | 25 | 285 | 456 |
| borderline infrastructure | 268 | 178 | 53 | 405 | 362 | 585 | 106 | 1,957 |

Safe-harbor: 0. Counts by source type are in `gate4_validation.json → 7_flags`.

## 8. Unit comparability

| Unit type | AI rows | All units | Calls |
|---|---:|---:|---:|
| `sentence` (Punkt) | 8,026 | 39,991 | 80 |
| `caption_sentence` (punctuated YouTube captions) | 774 | 7,017 | 14 |
| `whisper_unit` (Amazon, sentence-like) | 974 | 6,547 | 15 |
| `caption_segment` (unpunctuated, ~30 s) | 110 | 795 | 7 |

The caption-segment calls are Apple FY23 Q2, FY23 Q4, FY24 Q1, FY24 Q2, FY24 Q3, FY25 Q1 and
Tesla 2023 Q1. **Caption segments are not sentences, and counts or shares built on them are
not directly comparable to true-sentence counts.** The same applies, to a lesser degree, to
Whisper units. They must be reported separately or adjusted by a documented method, and
never pooled silently.

## B3. Filter reconciliation (canonical vs. Tanush's `ai_passages.csv`)

There is no row-level merge: the two files use different analytical units. Per-call results
are in [filter_comparison.csv](filter_comparison.csv) (133 rows).

**Method.** Lowercase, and turn every non-alphanumeric run into one space.
- *Shingle overlap* (primary): a canonical unit overlaps if ≥50% of its word 6-grams occur in
  that call's Tanush passages. A passage overlaps if some canonical unit has ≥50% of its
  6-grams in it.
- *Strict containment* is also reported. It understates overlap, because Tanush's passages
  can start mid-unit (Whisper line splits) and his cleaner deletes digit-only lines (losing
  numbers in Alphabet's one-word-per-line PDFs).

**Coverage.**
- 105 calls are in both sources.
- 11 calls are only in canonical: the Gate 2 acquisitions, made after his filter ran on
  2026-10-01.
- 0 calls are only in Tanush's file.
- 17 calls are in neither (absent from the repo).

**Pooled over the 105 shared calls:**

| | Overlapping | Share |
|---|---|---:|
| Canonical AI units → Tanush (shingle) | 7,339 / 9,669 | 75.9% |
| … strict containment | 7,063 / 9,669 | 73.0% |
| … core-term units | 6,665 / 7,133 | **93.4%** |
| … uncertain (weak-term) units | 674 / 2,536 | 26.6% |
| Tanush passages → canonical unit | 3,226 / 3,335 | **96.7%** |

Interpretation (mechanical):

- Most non-overlap is by design. Tanush's passages exclude weak terms (FSD, inference,
  chip names, bare "model", agents), which canonical keeps as `is_uncertain`.
- The 468 core units with no Tanush counterpart come from three sources:
  - terms only canonical treats as core (named products such as TPU, Nova, Claude, NIM;
    model phrases; training/inference compute; superintelligence; x.ai): 150 + 76 + 64 + 35 + 19 trigger hits;
  - text-processing differences for plain "AI" (103);
  - Amazon Whisper boundaries (94 of the 468 are Amazon).

  These breakdowns were computed ad hoc with the same overlap rule.
- The 109 Tanush passages with no canonical unit are candidate recall checks for Gate 5.
  Examples include `vertex`, `bedrock`, `gemini`, `large language model` and `gen ai` hits
  whose text differs from canonical segmentation. Up to 40 are listed in
  `gate4_validation.json → B3_filter_comparison.examples_tanush_passages_without_canonical_unit`.
- 34 calls have shingle overlap under 70%, mostly Nvidia FY25–FY27 and Meta 2025–26, where
  weak-term rows are numerous.

**Roles.**
- The **canonical sentence dataset is the primary measurement source**: it preserves
  sentence order, flags, the prepared/Q&A split, stable IDs and denominators.
- **Tanush's passages are an auxiliary audit/context source only.** They must not replace or
  be merged with canonical rows.

## B4. Legacy validation reconciliation

The legacy files were not edited.

| # | Conflict | Explanation | Evidence |
|---|---|---|---|
| 1 | Verbatim: FILTER_METHOD.md "48,555 checked, 0 failures" vs `_validation.json` "45,293 checked, 8 failures" | **Prior validation bug (stale overwrite).** The `_validation.json` committed at c1dd6c6 says exactly 48,555 / 0, matching FILTER_METHOD.md. The next commit, a33883b, replaced it with a file produced in a working copy that had only 8 Amazon files. Re-running the filter at commit 4b47e6a (8 Amazon files) gives 45,394 / 5, close to but not equal to 45,293 / 8, so the committed file comes from an intermediate state that cannot be reproduced exactly. | `gate4_validation.json → B4_legacy` |
| 2 | Amazon "8 source files" vs 15 | Same cause: generated before the Amazon merge (99d4ed2) reached that working copy. All 15 have been present since 2026-09-30. | git history |
| 3 | False-positive `ai` tokens: 0 vs 4 | **Code-version difference.** The 4 are `x.ai` / `Character.ai` / `XAi`, which became core terms in c1dd6c6. The fb184fe json (pre-fix) says 4, c1dd6c6 says 0, and a33883b's stale file says 4 again. The current code on the current corpus gives 0. | same |
| 4 | Uncertain 2,536 vs 2,419; context-dependent 574 vs 531 | **Corpus difference.** 2,419 / 531 counts only 8 Amazon files (the 4b47e6a re-run gives 2,365 / 530). On the current raw files, the current code gives 2,536 uncertain / 573 context-dependent for the 105 original calls (574 → 573 is the 2 Apple raw files replaced on Oct 1), and 2,566 / 585 for all 116. | `current_filter_code_on_current_raw` |
| 5 | Tesla "9 Motley Fool / 6 captions" | **Documentation error.** The split is **8 Motley Fool / 7 YouTube captions**, both now and at a33883b. Motley Fool: 2022 Q4, 2023 Q2 – 2024 Q4. Captions: 2023 Q1, 2025 Q1 – 2026 Q2. | `tesla_source_split` |
| 6 | Committed `earnings_calls_ai_only/` vs current raw | **Corpus changes.** `apple_FY23_Q1` and `apple_FY24_Q4` raw files were replaced on 2026-10-01 (6e03fcb), after the filter ran. 11 calls were acquired later. 103 committed calls still match the current filter run exactly. | `build_validation.json → committed_output_drift` |
| 7 | Legacy verbatim failures (Tesla Fool "Unknown speaker" seams) | Not present with current code: 0 failures over all 49,005 filter units of the 105 original calls. | `current_filter_code_on_current_raw` |

**Still unvalidated, even for the 116 present calls:**

- AI filter precision and recall (only a 40-sentence check exists, in FILTER_METHOD.md, and
  it was not repeated);
- Whisper and caption unit boundaries;
- speaker identity in caption/Whisper files, original Meta Q&A, and `meta_2022_Q2` / `Q3`;
- the Nvidia/Apple calendar mapping (awaiting approval).

**Unvalidated until all 133 calls are available:** anything covering Q4 2021 – Q3 2022 across
firms. Seventeen calls are missing, so the early-window quarters have 3–4 firms rather than 7,
and the 17 future files have not been checked at all.

## B5. Manual review sample

[manual_review_sample.csv](manual_review_sample.csv) has 150 rows, seed **20261006**.

- **Strata:** company × section × core/uncertain (28 strata × 5 = 140), with draws spread
  across time order within each stratum, plus 10 caption-segment rows as a top-up.
- **Coverage:** all 7 companies (Apple 29, Tesla 21, others 20). Prepared 74 / Q&A 76. Core
  79 / uncertain 71. Units: sentence 95, caption sentence 22, Whisper 20, caption segment 13.
  Years 2022–2026.
- **Judgment columns:** `reviewer_id`, `review_date`, `q_is_about_ai`,
  `q_text_matches_source`, `q_speaker_correct`, `q_section_correct`, `q_unit_boundary_ok` and
  `reviewer_notes` are **blank**. No substantive (opportunity, risk, efficiency, workforce)
  labels exist.

## Open items

1. `meta_2022_Q2` and `meta_2022_Q3` speaker labels are misplaced in the raw files
   (quarantined). Re-extraction needs approval.
2. 733 original-Meta Q&A AI rows are unverified (label loss). Fixing them needs an approved
   re-extraction from the official PDFs.
3. 37 bare-name and 9 "Unknown speaker" AI rows are unresolvable from the transcripts.
4. 1,858 AI rows come from sources without speaker labels.
5. AI filter precision and recall are not validated. The review sample is not yet reviewed.
6. 17 calls are missing (decisions pending).
7. Calendar mapping approval for Nvidia and Apple (Gate 1).
8. `earnings_calls/coverage_manifest.csv` and `EARNINGS_CALL_SCOPE.md` §9.5 predate Gate 4
   (they mention 175 speaker warnings and "0 corrupted"). This report and the erratum
   supersede them. Neither was edited, because they are outside Gate 4's allowed areas.
