# Canonical earnings-call dataset (Gate 3)

Structured, sentence-level dataset of AI-relevant language in Mag 7 earnings calls,
Q4 2021 – Q2 2026 (scope: [EARNINGS_CALL_SCOPE.md](../EARNINGS_CALL_SCOPE.md)).
**No semantic labels** (opportunity, risk, efficiency, workforce reduction) exist here yet.
**The AI filter is not validated.** `build_validation.json` reports build-integrity checks
only. Recall and precision are Gate 4.

## Reproduce

```
python build_earnings_call_canonical.py            # writes every file in this folder except README/data_dictionary
python build_earnings_call_canonical.py --verify   # builds twice in memory, checks byte-identical, writes nothing
```

The build needs local Python 3 and nltk (Punkt data on disk). It makes no network calls. It
reads `earnings_calls/*/*.md` and the committed `earnings_calls_ai_only/*/*_ai.md` (for the
drift report only) and writes nothing outside this folder. It was tested by deleting every
output and rebuilding: the result was byte-identical (SHA-256 of each output is in
`build_validation.json → output_sha256`).

## Where the rows come from

The source of truth is the sentence-level filter `filter_earnings_calls.py`. The builder
imports its parser, Punkt sentence splitter and `classify()`, and re-runs them read-only on
the **current** raw transcripts. For every call it checks that its units are identical to
`filter_earnings_calls.process_file()` and stops if they are not. The committed
`earnings_calls_ai_only/` outputs are **not** the input, because they are out of date:

| Committed output vs. today's raw file | Calls | Why |
|---|---:|---|
| Identical AI units | 103 | Nvidia and Tesla Fool files lost trailing ads on 2026-10-01, but the filter already ignored that text |
| Differs | 2 | `apple_FY23_Q1`, `apple_FY24_Q4`: raw file replaced on 2026-10-01 (commit 6e03fcb) after the filter ran on 2026-09-30 (captions → Motley Fool, and a different Fool text) |
| No committed output | 11 | Calls acquired in Gate 2 (Alphabet 2022 Q1–Q3, Meta 2021 Q4 – 2022 Q3, Microsoft FY22 Q2 – FY23 Q1) |

Every sentence row has `in_committed_filter_output` (`yes` / `no` / `no_committed_file`), so
committed-only analyses stay possible.

## Files

| File | Rows | One row per | Use |
|---|---:|---|---|
| `earnings_call_sentences.csv` | 9,884 | AI candidate unit | **Measurement unit / source of truth** |
| `earnings_call_labeling_passages.csv` | 9,884 | AI candidate unit, with bounded context | Annotation display only. Never counted |
| `earnings_call_borderline_review.csv` | 2,413 | automation/robotics (456) or infrastructure-only (1,957) unit with no AI term | Gate 5 human review. **Not** AI candidates |
| `earnings_call_call_units.csv` | 116 | present call | Denominators (all parsed units, by section) and numerators as counts |
| `build_validation.json` | — | — | Counts, integrity checks, coverage, drift, hashes |

Field definitions: [data_dictionary.md](data_dictionary.md).

## Coverage

133 expected calls, 116 present and processed, and 17 absent (9 awaiting a human source
decision, 8 with no public company source). All are listed in `build_validation.json →
missing_or_unavailable_periods` and in `earnings_calls/coverage_manifest.csv`. Q4 2021 – Q3 2022
has only Alphabet (Q1–Q3 2022), Meta and Microsoft, so cross-firm figures for those quarters
are not comparable to later ones.

AI rows by company: Alphabet 1,806 · Amazon 974 · Apple 319 · Meta 1,570 · Microsoft 1,750 ·
Nvidia 2,519 · Tesla 946. By section: prepared remarks 4,981, Q&A 4,903. All parsed units
(the denominator base): 54,350.

## Rules applied

- **Verbatim text.** `text_verbatim` is the filter's unit text: source text with only the
  filter's documented changes (line re-flow, hyphen-wrap joins, removal of page numbers,
  headers, timestamps and caption tags, HTML-entity decoding). Transcription errors are kept.
  All 9,884 rows pass the filter's own `verbatim_found` check against the raw file.
- **Stable IDs.** `sentence_id = <company>_<period_label>_u<order in call, 4 digits>_<sha256(text)[:10]>`.
  The ID changes only if the raw file or the filter changes. Passage ID = `P_` + anchor ID.
  Borderline ID uses `_b` in place of `_u`.
- **Flags kept as they are.** `is_uncertain` (weak term only), `is_safe_harbor`,
  `is_context_dependent`, `is_long`. No row is dropped for having a flag.
- **Units are not all sentences.** `unit_type` is `sentence`, `caption_sentence` (punctuated
  YouTube captions), `caption_segment` (unpunctuated captions, ~30 s; 7 calls) or `whisper_unit`
  (Amazon). `units_comparable_to_sentences = 0` marks calls whose counts must not be pooled with
  sentence-based calls without a stated adjustment.
- **Speakers are never guessed.** Caption and Whisper rows carry the filter's fallback
  `Speaker not labeled`. `speaker_role` is assigned by rule from the label text, and bare
  names stay `unresolved`. `speaker_attribution_warning` marks 175 AI rows (all in Microsoft
  calls and Alphabet 2022 Q1–Q3) that come after a `NAME, Firm:` label the parser did not
  recognise, so the listed speaker is probably wrong. Sections are not affected.
- **Borderline material** (automation/robotics without an AI term, which includes most Tesla
  Optimus content, and infrastructure-only such as GPU / data center / capex) is in a separate
  file with `review_route = gate5_human_uncertainty_review`.

## Passages (for later annotation only)

Each AI unit gets one passage: up to **2 preceding and 1 following** parsed units of the same
call, the **same section**, contiguous in call order. It may cross a speaker turn
(`context_crosses_speaker_turn = 1`) but never the prepared-remarks / Q&A boundary. Passages
overlap, so they must never be counted or used as a denominator. Annotations made on a passage
apply to its `anchor_sentence_id`.

## Known issues for Gate 4

1. The filter's own records disagree with each other. `FILTER_METHOD.md` reports "48,555 checked, 0
   failures" for verbatim, 0 false-positive `ai` tokens and 2,536 uncertain. The committed
   `_validation.json` reports 45,293 checked, 8 failures (Tesla Fool "Unknown speaker" seams),
   4 false positives, 2,419 uncertain, and Amazon coverage of 8 source files. It was run while
   Amazon had 8 of 15 files. Neither record describes the current corpus.
2. The speaker-attribution gaps described above, and missing inline labels in committed Meta
   raw text.
3. The precision spot-check in `FILTER_METHOD.md` (40 sentences) is too small to call the
   filter validated.
