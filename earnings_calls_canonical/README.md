# Canonical earnings-call dataset (canonical-v2)

Sentence-level dataset of AI-relevant language in Mag 7 earnings calls, Q4 2021 – Q2 2026
(scope: [EARNINGS_CALL_SCOPE.md](../EARNINGS_CALL_SCOPE.md)).

- **No semantic labels** (opportunity, risk, efficiency, workforce reduction) exist yet.
- **No human validation has been done.** All checks in `build_validation.json` and
  `gate4_validation.json` were run by code. The current validation report is
  [GATE4_VALIDATION_REPORT.md](GATE4_VALIDATION_REPORT.md). The legacy records in
  `earnings_calls_ai_only/` must not be quoted as describing this corpus.

## Reproduce

```
python build_earnings_call_canonical.py                  # the 4 CSVs + build_validation.json
python earnings_calls_canonical/gate4_validate.py        # Gate 4 checks, audit, comparison, review sample
python build_earnings_call_canonical.py --verify         # optional: two in-memory builds, byte-compared
```

This needs local Python 3 and nltk (Punkt data on disk) and makes no network calls.
`gate4_validate.py` also reads git history and, for one check, the cached official PDFs in
`cache/earnings_call_sources/` (gitignored and local). Outputs contain no timestamps, so a
rebuild into an empty directory is byte-identical.

## What the rows are

**Extraction version** `filter_earnings_calls.py@sha256:<12>/canonical-v2`. The builder
imports the sentence filter's parser, splitter and classifier and re-runs them on the
current raw files. This is a **distinct current extraction**. It is **not** the committed
`earnings_calls_ai_only/*.md` output: 103 committed calls match it, 2 differ because their
raw files changed after the filter ran (`apple_FY23_Q1`, `apple_FY24_Q4`), and 11 calls
acquired in Gate 2 have no committed output. Each row records `in_committed_filter_output`.

On top of the filter, canonical-v2 applies two **speaker corrections** and nothing else.
Every change is listed in `speaker_attribution_audit.csv`:

1. **Microsoft and Alphabet formats.** A raw `NAME, Firm:` label that the filter's parser
   left inside a turn now starts that speaker's turn, and the label text is removed (as the
   parser does for labels it recognises). This made 1,228 unit changes, 212 of which are
   label-text removals.
2. **Same-transcript name propagation.** A bare name takes the firm the same transcript gives
   it elsewhere, but only when exactly one labelled speaker matches. This made 169 unit
   changes.

Unit count (54,350), AI rows (9,884) and classification are unchanged. One AI row's ID
changed, because its text lost the label (`alphabet_2022_Q3_u0436_8c6a59d3e5` →
`alphabet_2022_Q3_u0436_398e6c3edd`). `turn_order_in_call` shifts in calls where turns were
split.

## Files

| File | Rows | One row per | Use |
|---|---:|---|---|
| `earnings_call_sentences.csv` | 9,884 | AI candidate unit | **Primary measurement unit** |
| `earnings_call_labeling_passages.csv` | 9,884 | AI candidate unit with same-turn context | **Annotation input only** |
| `earnings_call_borderline_review.csv` | 2,413 | automation/robotics (456) or infrastructure-only (1,957) unit with no AI term | Gate 5 review route. Not AI candidates |
| `earnings_call_call_units.csv` | 116 | present call | Denominators and counts |
| `build_validation.json` | — | — | Build integrity |
| `gate4_validation.json` | — | — | Gate 4 mechanical validation (current) |
| `speaker_attribution_audit.csv` | — | changed or unresolved speaker assignment | Gate 4 B1 audit |
| `filter_comparison.csv` | 133 | company-period | Canonical vs. Tanush's passage filter |
| `manual_review_sample.csv` | 150 | sampled anchor sentence | Blank human-review sheet (seed 20261006) |

Field definitions: [data_dictionary.md](data_dictionary.md).

## Sentences, passages and labels

- **Sentence rows are the measurement unit.** Counts, shares and any later time series are
  built from `earnings_call_sentences.csv` and the denominators in `earnings_call_call_units.csv`.
- **Passages are annotation inputs only.** Rule `ctx-v2-same-turn-pm1`: the anchor plus the
  immediately previous and next unit **of the same speaker turn** (same speaker, same section,
  same call). A passage never crosses a speaker change, the prepared-remarks/Q&A boundary or
  the transcript boundary. With no same-turn neighbour, the passage is the anchor alone (9 cases).
- **Labels applied to a passage belong to its `anchor_sentence_id`** and must be mapped back
  to that sentence row. Passages overlap and must never be counted.
- `context_speaker_continuity` says how far the "same speaker" claim can be trusted:
  `same_labelled_speaker_turn` (7,215); `same_turn_unlabelled_source_speaker_unverified`
  (1,858; caption and Whisper files have no speaker labels, so a speaker change inside the
  section cannot be detected); `same_turn_meta_label_loss_risk` (733);
  `same_turn_raw_label_misplacement_risk` (69); `anchor_only_no_same_turn_neighbour` (9).

## Speaker status (AI rows)

| `speaker_status` | Rows | Meaning |
|---|---:|---|
| `resolved` | 6,999 | Speaker label with title or firm, from the raw text |
| `resolved_corrected` | 176 | Fixed in Gate 4 from a raw-text label |
| `operator` | 3 | Operator |
| `unresolved_bare_name` | 37 | The transcript never gives a title or firm for the name. Nothing is inferred |
| `unknown_speaker_in_source` | 9 | The source itself says "Unknown speaker" |
| `unverified_meta_label_loss_risk` | 733 | Q&A rows of original-corpus Meta files: the raw text can lack inline labels (proved for `meta_2022_Q4`). Not changed |
| `unverified_raw_label_misplacement` | 69 | `meta_2022_Q2`, `meta_2022_Q3`: the Gate 2 PDF extraction (`pdftotext -layout`) misplaced inline labels. All speakers in these two calls are quarantined until the raw files are re-extracted (needs approval). Sections are unaffected |
| `unlabeled_source` | 1,858 | Caption and Whisper files: `Speaker not labeled` |

Exact counts: `gate4_validation.json → 6_section_speaker`.

## Other rules

- `text_verbatim` is the unit's source text after the filter's documented normalization only.
  All 9,884 rows are found in their raw file (gate4 §5).
- `sentence_id = <company>_<period_label>_u<order>_<sha256(text)[:10]>`. Passage ID = `P2_` +
  anchor ID. Borderline ID uses `_b`, and the borderline file also gives the `unit_id` (`_u`).
- `call_date` and `source_url` are blank when the raw file does not state them (3,106 and
  1,038 rows). They are never inferred.
- `unit_type` separates `sentence`, `caption_sentence`, `caption_segment` (unpunctuated ~30 s
  caption lines, 7 calls) and `whisper_unit` (Amazon). Caption segments and Whisper units are
  **not** comparable to sentence counts.
