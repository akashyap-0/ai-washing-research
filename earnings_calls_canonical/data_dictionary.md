# Data dictionary: earnings_calls_canonical/ (canonical-v2, gate4-v1)

All files are UTF-8 CSV with a header row and `\n` line endings. Flags are `0`/`1`. Text is
never edited beyond the filter's documented normalization and the Gate 4 label removal
described in README.

**Sentence rows are the primary measurement unit.** Passages are annotation inputs only, and
any label put on a passage must be mapped back to its `anchor_sentence_id`.

## Shared fields

| Field | Type | Meaning |
|---|---|---|
| `call_id` | str | `<company>_<period_label>` |
| `company` / `ticker` | str | alphabet GOOGL, amazon AMZN, apple AAPL, meta META, microsoft MSFT, nvidia NVDA, tesla TSLA |
| `period_label` | str | Exactly the raw file's label: fiscal `FYyy_Qn` (Microsoft, Apple, Nvidia) or calendar `YYYY_Qn` |
| `calendar_year`, `calendar_quarter` | int | Majority-of-months calendar assignment (EARNINGS_CALL_SCOPE.md §3). Supplemental only |
| `fiscal_or_calendar_label` | str | Readable fiscal label with fiscal-year-end note |
| `call_date` | date / blank | ISO date stated in the file. Blank if not stated, and never inferred |
| `call_date_source` | str | `file_metadata`, `transcript_text`, `not_stated_in_source_file` |
| `source_file` | str | Repo-relative raw transcript path |
| `source_url` | str / blank | URL from the raw file's metadata. Blank for Nvidia FY26 Q1 – FY27 Q2 (none given) |
| `source_type` | str | `official_ir_transcript_pdf`, `official_ir_transcript_html`, `official_ir_transcript_docx`, `official_ir_pdf_factset_callstreet`, `third_party_transcript_motley_fool`, `youtube_auto_captions`, `machine_transcript_whisper_of_official_ir_audio` |
| `unit_type` | str | `sentence`; `caption_sentence` (Punkt on punctuated captions); `caption_segment` (one unpunctuated ~30 s caption line, **not a sentence**); `whisper_unit` (sentence-like Whisper unit) |
| `section` | str | `prepared_remarks` or `qa` |
| `speaker` | str | Speaker as parsed, after the Gate 4 corrections. `Speaker not labeled` in caption and Whisper files |
| `speaker_role` | str | Rule from the label: `operator`, `unlabeled`, `unknown`, `analyst` (descriptor says Analyst or is a firm), `company_representative` (descriptor has a title word), `unresolved` (bare name) |
| `speaker_status` | str | `resolved`, `resolved_corrected`, `operator`, `unresolved_bare_name`, `unknown_speaker_in_source`, `unverified_meta_label_loss_risk`, `unverified_raw_label_misplacement`, `unlabeled_source` (see README) |
| `extraction_version` | str | `filter_earnings_calls.py@sha256:<12 hex>/canonical-v2` |

## earnings_call_sentences.csv

| Field | Meaning |
|---|---|
| `sentence_id` | `<call_id>_u<NNNN>_<sha256(text_verbatim)[:10]>`; unique and deterministic |
| `parser_format` | `meta`, `msft`, `factset`, `fool`, `alphabet`, `captions` |
| `section_method` | `explicit_section_header`, `first_operator_turn_after_management`, `transition_phrase_heuristic`, `not_detected_all_prepared` |
| `speaker_status_reason` | Why the status is not `resolved` (blank when resolved or operator) |
| `speaker_correction_rule` | `msft_name_comma_firm_label`, `alphabet_name_comma_firm_label`, `same_transcript_name_propagation`, or blank |
| `turn_order_in_call` | 1-based turn index after the Gate 4 turn splits |
| `sentence_order_in_call` | 1-based position among **all** parsed units of the call |
| `sentence_order_in_section` | 1-based position among all units of its section |
| `text_verbatim` | Unit text |
| `word_count` | Whitespace tokens |
| `trigger_terms`, `core_terms`, `weak_terms` | Filter term groups matched (`; `-separated) |
| `is_uncertain` | Weak term only (filter `⚑ uncertain`) |
| `is_safe_harbor` | Forward-looking-statement language |
| `is_context_dependent` | Starts with an anaphoric word |
| `is_long` | Over 150 words |
| `call_parse_flags` | The filter's file-level flags |
| `in_committed_filter_output` | `yes` / `no` / `no_committed_file`: the filter's own (pre-correction) unit is in the committed `*_ai.md` |

## earnings_call_labeling_passages.csv (annotation input only)

| Field | Meaning |
|---|---|
| `passage_id` | `P2_` + `anchor_sentence_id` |
| `anchor_sentence_id` | The sentence row the passage, and any label on it, belongs to (1:1) |
| `context_rule_version` | `ctx-v2-same-turn-pm1` |
| `context_sentence_ids` | Unit IDs in passage order (previous, anchor, next). AI units are in the sentence file, borderline units in `earnings_call_borderline_review.csv` (`unit_id`). Other non-AI units are not stored as rows, but their IDs follow the same formula |
| `context_unit_kinds` | `ai`, `borderline_automation`, `borderline_infrastructure` or `non_ai`, per ID |
| `n_units` | 1–3 |
| `text` | The passage: units joined with single spaces, verbatim |
| `context_word_count` | Whitespace tokens of `text` (anchor plus context) |
| `context_before_text`, `anchor_text`, `context_after_text` | The parts, verbatim |
| `context_speaker_continuity` | `same_labelled_speaker_turn`, `same_turn_unlabelled_source_speaker_unverified`, `same_turn_meta_label_loss_risk`, `same_turn_raw_label_misplacement_risk`, `anchor_only_no_same_turn_neighbour` |
| `anchor_*`, flags, `trigger_terms` | Copied from the anchor sentence row |
| `passage_role` | `annotation_input_only; map labels back to anchor_sentence_id` |

## earnings_call_borderline_review.csv

| Field | Meaning |
|---|---|
| `borderline_id` | Sentence-ID formula with `_b` |
| `unit_id` | The same unit's `_u` ID (as used in `context_sentence_ids`) |
| `borderline_type` | `automation_robotics_no_ai_term` or `infrastructure_no_ai_term` |
| `matched_terms` | Lower-cased matched words |
| `review_route` | `gate5_human_uncertainty_review` |

## earnings_call_call_units.csv

| Field | Meaning |
|---|---|
| `source_sha256` | SHA-256 of the raw file as read |
| `acquisition_status` | `already_present` or `acquired` |
| `units_comparable_to_sentences` | 1 only if every unit is `sentence`, or every unit is `caption_sentence` |
| `total_units`, `total_units_prepared`, `total_units_qa` | **Primary denominators** (all parsed units) |
| `ai_units*`, `ai_uncertain`, `ai_context_dependent`, `ai_safe_harbor`, `ai_long` | Numerators and flag counts |
| `borderline_automation`, `borderline_infrastructure` | In the denominator, not the AI numerator |
| `units_speaker_corrected`, `units_text_changed_by_correction` | Gate 4 corrections in this call |
| `ai_units_speaker_unresolved`, `ai_units_speaker_unverified` | AI rows with `unresolved_bare_name` / any `unverified_*` status |
| `committed_filter_output`, `committed_drift` | Committed `*_ai.md` present, and `match` / `differs` / `no_committed_file` |

## speaker_attribution_audit.csv

One row per unit (any kind) whose speaker changed, plus one per AI row whose speaker is not
resolved.

| Field | Meaning |
|---|---|
| `sentence_id`, `old_sentence_id`, `id_changed` | Current and pre-correction unit ID |
| `unit_kind`, `in_sentence_file` | `ai` / `auto` / `infra` / `out`; 1 if the row is in the sentence file |
| `old_speaker`, `new_speaker`, `old_role`, `new_role` | Before and after |
| `audit_status` | `corrected`, `unresolved`, `unverified`, `unresolved_source_has_no_labels` |
| `parsing_rule`, `confidence` | Rule applied; `high` (explicit raw label), `medium` (same-transcript propagation), `n/a` |
| `source_text_evidence` | Raw label text, or the propagation evidence |
| `reason` | Why it was changed or left unresolved |

## filter_comparison.csv

One row for each of the 133 company-periods. The method is in `overlap_method`. Canonical is
the primary measurement source and Tanush's passages are audit/context only; they are never
merged.

## manual_review_sample.csv

150 anchor sentences, seed 20261006, stratified by company × section × core/uncertain (5
each), with time-spread draws and a 10-row caption-segment top-up. It shows source text,
location, flags, speaker, section and passage. The `reviewer_*` and `q_*` columns are
**blank** and are mechanical questions only (about AI? text, speaker, section, unit boundary
correct?). There are no substantive labels.
