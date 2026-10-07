# Data dictionary: earnings_calls_canonical/

All files are UTF-8 CSV with a header row and `\n` line endings. Flags are `0`/`1`. Text
fields are never trimmed or edited beyond the filter's documented normalization (README §Rules).

## Shared fields

| Field | Type | Meaning |
|---|---|---|
| `call_id` | str | `<company>_<period_label>`; one per call |
| `company` | str | `alphabet`, `amazon`, `apple`, `meta`, `microsoft`, `nvidia`, `tesla` |
| `ticker` | str | GOOGL, AMZN, AAPL, META, MSFT, NVDA, TSLA |
| `period_label` | str | Exactly the raw file's label: fiscal `FYyy_Qn` (Microsoft, Apple, Nvidia) or calendar `YYYY_Qn` |
| `calendar_year`, `calendar_quarter` | int | Calendar quarter assigned by the majority-of-months rule (EARNINGS_CALL_SCOPE.md §3). Supplemental only |
| `fiscal_or_calendar_label` | str | Human-readable fiscal label with fiscal-year-end note |
| `call_date` | date / blank | ISO date stated in the file (metadata, title line, or "as of today, <date>"). Blank when not stated, and never inferred |
| `call_date_source` | str | `file_metadata`, `transcript_text`, `not_stated_in_source_file` |
| `source_file` | str | Repo-relative raw transcript path |
| `source_url` | str / blank | URL from the raw file's metadata. Blank for Nvidia FY26 Q1 – FY27 Q2 (the metadata says "q4cdn PDF" with no URL) |
| `source_type` | str | `official_ir_transcript_pdf`, `official_ir_transcript_html`, `official_ir_transcript_docx`, `official_ir_pdf_factset_callstreet`, `third_party_transcript_motley_fool`, `youtube_auto_captions`, `machine_transcript_whisper_of_official_ir_audio` |
| `unit_type` | str | `sentence` (Punkt), `caption_sentence` (Punkt on punctuated captions), `caption_segment` (one unpunctuated ~30 s caption line, **not a sentence**), `whisper_unit` (sentence-like Whisper unit) |
| `section` | str | `prepared_remarks` or `qa` |
| `speaker` | str | Speaker label as the filter produced it. `Speaker not labeled` for caption/Whisper files. `Operator`. Names kept as printed (variants are not merged) |
| `speaker_role` | str | Rule from the label: `operator`; `unlabeled`; `unknown` (Fool "Unknown speaker"); `analyst` (descriptor says Analyst or is a firm); `company_representative` (descriptor has a title word: CEO, CFO, Chief, Officer, President, VP, Director, Head, Investor Relations, …); `unresolved` (bare name, no descriptor) |
| `speaker_attribution_warning` | str / blank | Non-blank when the unit follows a `NAME, Firm:` label the parser did not recognise inside the same turn, so `speaker` is probably the previous speaker. Only Microsoft and Alphabet formats are checked |
| `extraction_version` | str | `filter_earnings_calls.py@sha256:<12 hex>/canonical-v1` |

## earnings_call_sentences.csv (measurement unit)

| Field | Type | Meaning |
|---|---|---|
| `sentence_id` | str | `<call_id>_u<NNNN>_<sha256(text_verbatim)[:10]>`; unique, deterministic |
| `parser_format` | str | Filter parser used: `meta`, `msft`, `factset`, `fool`, `alphabet`, `captions` |
| `section_method` | str | How the Q&A start was found: `explicit_section_header`, `first_operator_turn_after_management`, `transition_phrase_heuristic`, `not_detected_all_prepared` |
| `turn_order_in_call` | int | 1-based speaker-turn index in the parsed call |
| `sentence_order_in_call` | int | 1-based position among **all** parsed units of the call (AI or not). Gaps are non-AI units |
| `sentence_order_in_section` | int | 1-based position among all parsed units of its section |
| `text_verbatim` | str | Unit text |
| `word_count` | int | Whitespace tokens |
| `trigger_terms` | str | All filter term groups matched, `; `-separated, in filter order |
| `core_terms` / `weak_terms` | str | `trigger_terms` split into core and weak groups |
| `is_uncertain` | 0/1 | Only weak terms matched (filter `⚑ uncertain`) |
| `is_safe_harbor` | 0/1 | Forward-looking-statement language (filter `⚑ uncertain: safe-harbor`) |
| `is_context_dependent` | 0/1 | Starts with an anaphoric word (filter `⚑ context-dependent`) |
| `is_long` | 0/1 | Over 150 words |
| `call_parse_flags` | str | The filter's file-level flags for the call (no speakers, unpunctuated captions, out-of-range counts, …) |
| `in_committed_filter_output` | str | `yes`: same (section, text) is in the committed `*_ai.md`; `no`: not there (stale committed output); `no_committed_file` |

## earnings_call_labeling_passages.csv (annotation context only)

Same metadata and flags as the anchor sentence, plus:

| Field | Meaning |
|---|---|
| `passage_id` | `P_` + `anchor_sentence_id` |
| `anchor_sentence_id` | The measurement unit the passage belongs to (1:1) |
| `anchor_speaker`, `anchor_speaker_role`, `anchor_sentence_order_in_call` | Anchor's speaker, role and order |
| `context_rule` | Text of the rule: ≤2 preceding and ≤1 following contiguous units, same call and section |
| `context_before_orders`, `context_after_orders` | Space-separated `sentence_order_in_call` values of the context units (these may be non-AI units, so they are not in the sentence file) |
| `context_crosses_speaker_turn` | 1 if any context unit is from another turn |
| `context_speakers` | Distinct speakers in the passage, in order, ` \| `-separated |
| `context_before_text`, `anchor_text`, `context_after_text` | The three parts, verbatim |
| `passage_text` | The three parts joined with single spaces |
| `passage_word_count` | Whitespace tokens of `passage_text` |
| `passage_role` | Always `annotation_context_only; measurement unit is anchor_sentence_id` |

## earnings_call_borderline_review.csv

Units the filter put in its Borderline sections. They contain no AI term and are **not** AI
candidates.

| Field | Meaning |
|---|---|
| `borderline_id` | Same rule as `sentence_id` with `_b` |
| `borderline_type` | `automation_robotics_no_ai_term` (automat*, robot*, Optimus, humanoid*) or `infrastructure_no_ai_term` (GPU, data center, capex, compute, server, accelerator, infrastructure, …) |
| `matched_terms` | Lower-cased matched words |
| `review_route` | `gate5_human_uncertainty_review` |

## earnings_call_call_units.csv (denominators)

| Field | Meaning |
|---|---|
| `source_sha256` | SHA-256 of the raw file as read |
| `acquisition_status` | `already_present` or `acquired` (Gate 2) |
| `unit_type` | Unit types present in the call |
| `units_comparable_to_sentences` | 1 if every unit is `sentence` or every unit is `caption_sentence`; 0 for Whisper and unpunctuated-caption calls |
| `total_units`, `total_units_prepared`, `total_units_qa` | **Primary denominators**: all parsed call units after noise removal |
| `ai_units`, `ai_units_prepared`, `ai_units_qa` | AI candidate counts (= rows in the sentence file) |
| `ai_uncertain`, `ai_context_dependent`, `ai_safe_harbor`, `ai_long` | Flag counts among AI units |
| `borderline_automation`, `borderline_infrastructure` | Borderline counts (in the denominator, not the AI numerator) |
| `speaker_attribution_warning_units` | Units of any kind with a speaker-attribution warning |
| `committed_filter_output` | `present` / `absent` committed `*_ai.md` |
| `committed_drift` | `match`, `differs`, `no_committed_file` (AI units, rebuilt vs committed) |

## build_validation.json

`counts`; breakdowns `by_company`, `by_calendar_quarter`, `by_company_period`, `by_section`,
`by_source_type`, `by_unit_type`, `by_speaker_role`, `by_section_method`; `flag_counts`;
`integrity` (duplicate IDs, missing required fields, allowed blanks with reasons, passage-anchor
check, verbatim check); `source_file_to_output_coverage`; `committed_output_drift`;
`missing_or_unavailable_periods`; `manifest_counts`; `reproducibility` (git HEAD, Python and
nltk versions, script and per-source SHA-256, ID and context rules); `output_sha256`.
