# METHODS_FACTS: verified facts for the Methods section

Reference file for the session drafting the Methods section of the Mag 7 earnings-call study (for Prof. Schloetzer).
It contains facts only, no paper prose. Compiled 2026-10-10 from the working tree at commit `c80f6a6`.

## How to read this file

- **Build used everywhere:** the extended 133-call build: `earnings_calls_canonical_extended/`,
  `analysis_calls/out_extended/`, `figures_calls_extended/`.
- **Status tags.** **[R]** = recomputed for this file from the CSVs or by re-running code. **[F]** = read from a file
  (code or committed output) and checked against the code. **[ND]** = NOT DETERMINABLE FROM REPO.
- **Citation format.** `file:line` or `file:function`. Line numbers refer to the working tree at `c80f6a6`.
- **Out of scope, not covered:** the fine-tuned FinBERT model (`03_finetune_predict.py`, `ft_metrics.json`,
  `ec_passage_labels.csv`, `tenk_item1a_ai_labels.csv`, fig6) and the older 8-K/10-K AI-washing pipeline
  (`RESULTS_PACKET.md`, permutation tests, annotation dataset). The 10-K *input file* `export/ai_washing_10-K.csv`
  is used by the tone comparison, so its contents are described in III.7.
- **Reproduction checks done for this file** (all outputs in a scratch directory; nothing in the repo was overwritten):
  1. The extended canonical dataset was rebuilt from raw transcripts plus the 17 extras. All 4 CSVs and
     `build_validation.json` are **identical** to the committed files, apart from (a) the `"python"` version string in
     `build_validation.json` (3.13.14 here vs 3.14.6 committed) and (b) CRLF line endings in this Windows checkout
     (`core.autocrlf=true`; the index stores LF). **[R]**
  2. `01_timeseries.py` and `04_network.py` were re-run on the extended data. `ai_share_pre_post.csv` is identical.
     `topic_first_appearance.csv` has identical rows; only the order of rows that tie on first quarter differs (unstable
     sort). **[R]**
  3. `02_finbert_tone.py`, `02b_baseline_tone.py` and `05_tone_figures.py` were re-run. Same rows in the same order;
     probabilities differ by at most 5e-6, consistent with a CPU-vs-original-device float difference.
     `tone_summary.csv` agrees to at least 6 decimal places. **[R]**
  4. Figures: see the Figures map.

---

# III. Data

## III.1 Universe, window, call count

| Fact | Value | Source | Status |
|---|---|---|---|
| Firms (7) | Alphabet GOOGL, Amazon AMZN, Apple AAPL, Meta META, Microsoft MSFT, Nvidia NVDA, Tesla TSLA | `earnings_call_scope.py:27-29` (`COMPANIES`, `TICKER`) | [F] |
| Window | Calendar Q4 2021 – calendar Q2 2026, 19 calendar quarters | `earnings_call_scope.py:32-34` | [F] |
| Expected calls | 7 × 19 = **133** | `earnings_call_scope.py:34`, `main()` check | [R] `--check` on the scratch copy: "expected 133 … present 133; files outside window: none" |
| Present calls (extended build) | **133 of 133** (116 in `earnings_calls/` + 17 in `earnings_calls_pre2022_extra/`) | `earnings_call_call_units.csv` (133 rows) | [R] |
| Firm-level coverage | Every firm has 19 calls, one per calendar quarter | `earnings_call_call_units.csv` | [R] |

Caveat: the committed (non-extended) canonical build `earnings_calls_canonical/` has 116 calls. The 17 extras live
outside `earnings_calls/` and are merged only in a scratch copy at build time (see Reproducibility).

## III.1b Per-call list (all 133 calls) [R]

Source: `earnings_calls_canonical_extended/earnings_call_call_units.csv`. `comp` = `units_comparable_to_sentences`
(1 if every unit in the call is `sentence` or `caption_sentence`; `build_earnings_call_canonical.py:502`). `share` =
`ai_units / total_units × 100`. ★ = one of the 17 extra calls.

| Firm | period_label | Calendar | source_type | unit_type | comp | section_method | total_units | ai_units | share % |
|---|---|---|---|---|---|---|---:|---:|---:|
| alphabet | 2021_Q4 ★ | 2021 Q4 | unknown | sentence | 1 | first_operator_turn_after_management | 538 | 34 | 6.3 |
| alphabet | 2022_Q1 | 2022 Q1 | official_ir_transcript_pdf | sentence | 1 | first_operator_turn_after_management | 456 | 12 | 2.6 |
| alphabet | 2022_Q2 | 2022 Q2 | official_ir_transcript_pdf | sentence | 1 | first_operator_turn_after_management | 485 | 24 | 4.9 |
| alphabet | 2022_Q3 | 2022 Q3 | official_ir_transcript_pdf | sentence | 1 | first_operator_turn_after_management | 475 | 22 | 4.6 |
| alphabet | 2022_Q4 | 2022 Q4 | official_ir_transcript_pdf | sentence | 1 | first_operator_turn_after_management | 468 | 76 | 16.2 |
| alphabet | 2023_Q1 | 2023 Q1 | official_ir_transcript_pdf | sentence | 1 | first_operator_turn_after_management | 516 | 79 | 15.3 |
| alphabet | 2023_Q2 | 2023 Q2 | official_ir_transcript_pdf | sentence | 1 | first_operator_turn_after_management | 509 | 95 | 18.7 |
| alphabet | 2023_Q3 | 2023 Q3 | official_ir_transcript_pdf | sentence | 1 | first_operator_turn_after_management | 453 | 83 | 18.3 |
| alphabet | 2023_Q4 | 2023 Q4 | official_ir_transcript_pdf | sentence | 1 | first_operator_turn_after_management | 496 | 96 | 19.4 |
| alphabet | 2024_Q1 | 2024 Q1 | official_ir_transcript_pdf | sentence | 1 | first_operator_turn_after_management | 488 | 87 | 17.8 |
| alphabet | 2024_Q2 | 2024 Q2 | official_ir_transcript_pdf | sentence | 1 | first_operator_turn_after_management | 496 | 109 | 22.0 |
| alphabet | 2024_Q3 | 2024 Q3 | official_ir_transcript_pdf | sentence | 1 | first_operator_turn_after_management | 558 | 129 | 23.1 |
| alphabet | 2024_Q4 | 2024 Q4 | official_ir_transcript_pdf | sentence | 1 | first_operator_turn_after_management | 527 | 127 | 24.1 |
| alphabet | 2025_Q1 | 2025 Q1 | official_ir_transcript_pdf | sentence | 1 | first_operator_turn_after_management | 488 | 107 | 21.9 |
| alphabet | 2025_Q2 | 2025 Q2 | official_ir_transcript_pdf | sentence | 1 | first_operator_turn_after_management | 508 | 126 | 24.8 |
| alphabet | 2025_Q3 | 2025 Q3 | official_ir_transcript_pdf | sentence | 1 | first_operator_turn_after_management | 453 | 141 | 31.1 |
| alphabet | 2025_Q4 | 2025 Q4 | official_ir_transcript_pdf | sentence | 1 | first_operator_turn_after_management | 515 | 158 | 30.7 |
| alphabet | 2026_Q1 | 2026 Q1 | official_ir_transcript_pdf | sentence | 1 | first_operator_turn_after_management | 504 | 161 | 31.9 |
| alphabet | 2026_Q2 | 2026 Q2 | official_ir_transcript_pdf | sentence | 1 | first_operator_turn_after_management | 523 | 174 | 33.3 |
| amazon | 2021_Q4 ★ | 2021 Q4 | machine_transcript_whisper_of_official_ir_audio | whisper_unit | 0 | transition_phrase_heuristic | 381 | 1 | 0.3 |
| amazon | 2022_Q1 ★ | 2022 Q1 | machine_transcript_whisper_of_official_ir_audio | whisper_unit | 0 | transition_phrase_heuristic | 323 | 2 | 0.6 |
| amazon | 2022_Q2 ★ | 2022 Q2 | machine_transcript_whisper_of_official_ir_audio | whisper_unit | 0 | transition_phrase_heuristic | 354 | 0 | 0.0 |
| amazon | 2022_Q3 ★ | 2022 Q3 | machine_transcript_whisper_of_official_ir_audio | whisper_unit | 0 | transition_phrase_heuristic | 320 | 2 | 0.6 |
| amazon | 2022_Q4 | 2022 Q4 | machine_transcript_whisper_of_official_ir_audio | whisper_unit | 0 | transition_phrase_heuristic | 381 | 1 | 0.3 |
| amazon | 2023_Q1 | 2023 Q1 | machine_transcript_whisper_of_official_ir_audio | whisper_unit | 0 | transition_phrase_heuristic | 546 | 38 | 7.0 |
| amazon | 2023_Q2 | 2023 Q2 | machine_transcript_whisper_of_official_ir_audio | whisper_unit | 0 | transition_phrase_heuristic | 364 | 54 | 14.8 |
| amazon | 2023_Q3 | 2023 Q3 | machine_transcript_whisper_of_official_ir_audio | whisper_unit | 0 | transition_phrase_heuristic | 392 | 73 | 18.6 |
| amazon | 2023_Q4 | 2023 Q4 | machine_transcript_whisper_of_official_ir_audio | whisper_unit | 0 | transition_phrase_heuristic | 442 | 50 | 11.3 |
| amazon | 2024_Q1 | 2024 Q1 | machine_transcript_whisper_of_official_ir_audio | whisper_unit | 0 | transition_phrase_heuristic | 457 | 56 | 12.3 |
| amazon | 2024_Q2 | 2024 Q2 | machine_transcript_whisper_of_official_ir_audio | whisper_unit | 0 | transition_phrase_heuristic | 409 | 53 | 13.0 |
| amazon | 2024_Q3 | 2024 Q3 | machine_transcript_whisper_of_official_ir_audio | whisper_unit | 0 | transition_phrase_heuristic | 411 | 58 | 14.1 |
| amazon | 2024_Q4 | 2024 Q4 | machine_transcript_whisper_of_official_ir_audio | whisper_unit | 0 | transition_phrase_heuristic | 384 | 82 | 21.4 |
| amazon | 2025_Q1 | 2025 Q1 | machine_transcript_whisper_of_official_ir_audio | whisper_unit | 0 | transition_phrase_heuristic | 444 | 70 | 15.8 |
| amazon | 2025_Q2 | 2025 Q2 | machine_transcript_whisper_of_official_ir_audio | whisper_unit | 0 | transition_phrase_heuristic | 492 | 80 | 16.3 |
| amazon | 2025_Q3 | 2025 Q3 | machine_transcript_whisper_of_official_ir_audio | whisper_unit | 0 | transition_phrase_heuristic | 451 | 76 | 16.9 |
| amazon | 2025_Q4 | 2025 Q4 | machine_transcript_whisper_of_official_ir_audio | whisper_unit | 0 | transition_phrase_heuristic | 522 | 96 | 18.4 |
| amazon | 2026_Q1 | 2026 Q1 | machine_transcript_whisper_of_official_ir_audio | whisper_unit | 0 | transition_phrase_heuristic | 425 | 100 | 23.5 |
| amazon | 2026_Q2 | 2026 Q2 | machine_transcript_whisper_of_official_ir_audio | whisper_unit | 0 | transition_phrase_heuristic | 427 | 87 | 20.4 |
| apple | FY22_Q1 ★ | 2021 Q4 | third_party_transcript_motley_fool | sentence | 1 | explicit_section_header | 485 | 1 | 0.2 |
| apple | FY22_Q2 ★ | 2022 Q1 | third_party_transcript_motley_fool | sentence | 1 | explicit_section_header | 497 | 0 | 0.0 |
| apple | FY22_Q3 ★ | 2022 Q2 | third_party_transcript_motley_fool | sentence | 1 | explicit_section_header | 435 | 1 | 0.2 |
| apple | FY22_Q4 ★ | 2022 Q3 | third_party_transcript_motley_fool | sentence | 1 | explicit_section_header | 485 | 0 | 0.0 |
| apple | FY23_Q1 | 2022 Q4 | third_party_transcript_motley_fool | sentence | 1 | explicit_section_header | 512 | 2 | 0.4 |
| apple | FY23_Q2 | 2023 Q1 | youtube_auto_captions | caption_segment | 0 | transition_phrase_heuristic | 117 | 4 | 3.4 |
| apple | FY23_Q3 | 2023 Q2 | youtube_auto_captions | caption_sentence | 1 | transition_phrase_heuristic | 469 | 5 | 1.1 |
| apple | FY23_Q4 | 2023 Q3 | youtube_auto_captions | caption_segment | 0 | transition_phrase_heuristic | 116 | 5 | 4.3 |
| apple | FY24_Q1 | 2023 Q4 | youtube_auto_captions | caption_segment | 0 | transition_phrase_heuristic | 110 | 11 | 10.0 |
| apple | FY24_Q2 | 2024 Q1 | youtube_auto_captions | caption_segment | 0 | transition_phrase_heuristic | 111 | 14 | 12.6 |
| apple | FY24_Q3 | 2024 Q2 | youtube_auto_captions | caption_segment | 0 | transition_phrase_heuristic | 113 | 31 | 27.4 |
| apple | FY24_Q4 | 2024 Q3 | third_party_transcript_motley_fool | sentence | 1 | explicit_section_header | 512 | 35 | 6.8 |
| apple | FY25_Q1 | 2024 Q4 | youtube_auto_captions | caption_segment | 0 | transition_phrase_heuristic | 107 | 24 | 22.4 |
| apple | FY25_Q2 | 2025 Q1 | youtube_auto_captions | caption_sentence | 1 | transition_phrase_heuristic | 473 | 31 | 6.6 |
| apple | FY25_Q3 | 2025 Q2 | youtube_auto_captions | caption_sentence | 1 | transition_phrase_heuristic | 480 | 35 | 7.3 |
| apple | FY25_Q4 | 2025 Q3 | youtube_auto_captions | caption_sentence | 1 | transition_phrase_heuristic | 531 | 29 | 5.5 |
| apple | FY26_Q1 | 2025 Q4 | youtube_auto_captions | caption_sentence | 1 | transition_phrase_heuristic | 483 | 28 | 5.8 |
| apple | FY26_Q2 | 2026 Q1 | youtube_auto_captions | caption_sentence | 1 | transition_phrase_heuristic | 530 | 25 | 4.7 |
| apple | FY26_Q3 | 2026 Q2 | youtube_auto_captions | caption_sentence | 1 | transition_phrase_heuristic | 510 | 40 | 7.8 |
| meta | 2021_Q4 | 2021 Q4 | official_ir_transcript_pdf | sentence | 1 | first_operator_turn_after_management | 513 | 12 | 2.3 |
| meta | 2022_Q1 | 2022 Q1 | official_ir_transcript_pdf | sentence | 1 | first_operator_turn_after_management | 517 | 22 | 4.3 |
| meta | 2022_Q2 | 2022 Q2 | official_ir_transcript_pdf | sentence | 1 | first_operator_turn_after_management | 559 | 37 | 6.6 |
| meta | 2022_Q3 | 2022 Q3 | official_ir_transcript_pdf | sentence | 1 | first_operator_turn_after_management | 464 | 32 | 6.9 |
| meta | 2022_Q4 | 2022 Q4 | official_ir_transcript_pdf | sentence | 1 | first_operator_turn_after_management | 509 | 34 | 6.7 |
| meta | 2023_Q1 | 2023 Q1 | official_ir_transcript_pdf | sentence | 1 | first_operator_turn_after_management | 487 | 64 | 13.1 |
| meta | 2023_Q2 | 2023 Q2 | official_ir_transcript_pdf | sentence | 1 | first_operator_turn_after_management | 497 | 75 | 15.1 |
| meta | 2023_Q3 | 2023 Q3 | official_ir_transcript_pdf | sentence | 1 | first_operator_turn_after_management | 471 | 77 | 16.3 |
| meta | 2023_Q4 | 2023 Q4 | official_ir_transcript_pdf | sentence | 1 | first_operator_turn_after_management | 467 | 83 | 17.8 |
| meta | 2024_Q1 | 2024 Q1 | official_ir_transcript_pdf | sentence | 1 | first_operator_turn_after_management | 447 | 119 | 26.6 |
| meta | 2024_Q2 | 2024 Q2 | official_ir_transcript_pdf | sentence | 1 | first_operator_turn_after_management | 468 | 111 | 23.7 |
| meta | 2024_Q3 | 2024 Q3 | official_ir_transcript_pdf | sentence | 1 | first_operator_turn_after_management | 443 | 85 | 19.2 |
| meta | 2024_Q4 | 2024 Q4 | official_ir_transcript_pdf | sentence | 1 | first_operator_turn_after_management | 463 | 94 | 20.3 |
| meta | 2025_Q1 | 2025 Q1 | official_ir_transcript_pdf | sentence | 1 | first_operator_turn_after_management | 455 | 122 | 26.8 |
| meta | 2025_Q2 | 2025 Q2 | official_ir_transcript_pdf | sentence | 1 | first_operator_turn_after_management | 451 | 112 | 24.8 |
| meta | 2025_Q3 | 2025 Q3 | official_ir_transcript_pdf | sentence | 1 | first_operator_turn_after_management | 446 | 101 | 22.6 |
| meta | 2025_Q4 | 2025 Q4 | official_ir_transcript_pdf | sentence | 1 | first_operator_turn_after_management | 477 | 112 | 23.5 |
| meta | 2026_Q1 | 2026 Q1 | official_ir_transcript_pdf | sentence | 1 | first_operator_turn_after_management | 480 | 135 | 28.1 |
| meta | 2026_Q2 | 2026 Q2 | official_ir_transcript_pdf | sentence | 1 | first_operator_turn_after_management | 509 | 143 | 28.1 |
| microsoft | FY22_Q2 | 2021 Q4 | official_ir_transcript_docx | sentence | 1 | transition_phrase_heuristic | 448 | 9 | 2.0 |
| microsoft | FY22_Q3 | 2022 Q1 | official_ir_transcript_docx | sentence | 1 | transition_phrase_heuristic | 453 | 13 | 2.9 |
| microsoft | FY22_Q4 | 2022 Q2 | official_ir_transcript_docx | sentence | 1 | transition_phrase_heuristic | 466 | 9 | 1.9 |
| microsoft | FY23_Q1 | 2022 Q3 | official_ir_transcript_docx | sentence | 1 | transition_phrase_heuristic | 509 | 23 | 4.5 |
| microsoft | FY23_Q2 | 2022 Q4 | official_ir_transcript_html | sentence | 1 | transition_phrase_heuristic | 485 | 49 | 10.1 |
| microsoft | FY23_Q3 | 2023 Q1 | official_ir_transcript_html | sentence | 1 | transition_phrase_heuristic | 464 | 79 | 17.0 |
| microsoft | FY23_Q4 | 2023 Q2 | official_ir_transcript_html | sentence | 1 | transition_phrase_heuristic | 516 | 101 | 19.6 |
| microsoft | FY24_Q1 | 2023 Q3 | official_ir_transcript_html | sentence | 1 | transition_phrase_heuristic | 476 | 90 | 18.9 |
| microsoft | FY24_Q2 | 2023 Q4 | official_ir_transcript_html | sentence | 1 | transition_phrase_heuristic | 522 | 123 | 23.6 |
| microsoft | FY24_Q3 | 2024 Q1 | official_ir_transcript_html | sentence | 1 | transition_phrase_heuristic | 502 | 118 | 23.5 |
| microsoft | FY24_Q4 | 2024 Q2 | official_ir_transcript_html | sentence | 1 | transition_phrase_heuristic | 507 | 94 | 18.5 |
| microsoft | FY25_Q1 | 2024 Q3 | official_ir_transcript_html | sentence | 1 | transition_phrase_heuristic | 524 | 140 | 26.7 |
| microsoft | FY25_Q2 | 2024 Q4 | official_ir_transcript_html | sentence | 1 | transition_phrase_heuristic | 501 | 142 | 28.3 |
| microsoft | FY25_Q3 | 2025 Q1 | official_ir_transcript_html | sentence | 1 | transition_phrase_heuristic | 485 | 116 | 23.9 |
| microsoft | FY25_Q4 | 2025 Q2 | official_ir_transcript_html | sentence | 1 | transition_phrase_heuristic | 454 | 106 | 23.3 |
| microsoft | FY26_Q1 | 2025 Q3 | official_ir_transcript_html | sentence | 1 | transition_phrase_heuristic | 508 | 125 | 24.6 |
| microsoft | FY26_Q2 | 2025 Q4 | official_ir_transcript_html | sentence | 1 | transition_phrase_heuristic | 483 | 137 | 28.4 |
| microsoft | FY26_Q3 | 2026 Q1 | official_ir_transcript_html | sentence | 1 | transition_phrase_heuristic | 506 | 138 | 27.3 |
| microsoft | FY26_Q4 | 2026 Q2 | official_ir_transcript_html | sentence | 1 | transition_phrase_heuristic | 519 | 138 | 26.6 |
| nvidia | FY22_Q4 ★ | 2021 Q4 | third_party_transcript_motley_fool | sentence | 1 | explicit_section_header | 459 | 101 | 22.0 |
| nvidia | FY23_Q1 ★ | 2022 Q1 | third_party_transcript_motley_fool | sentence | 1 | explicit_section_header | 510 | 113 | 22.2 |
| nvidia | FY23_Q2 ★ | 2022 Q2 | third_party_transcript_motley_fool | sentence | 1 | explicit_section_header | 503 | 74 | 14.7 |
| nvidia | FY23_Q3 ★ | 2022 Q3 | third_party_transcript_motley_fool | sentence | 1 | explicit_section_header | 480 | 70 | 14.6 |
| nvidia | FY23_Q4 | 2022 Q4 | third_party_transcript_motley_fool | sentence | 1 | explicit_section_header | 482 | 126 | 26.1 |
| nvidia | FY24_Q1 | 2023 Q1 | third_party_transcript_motley_fool | sentence | 1 | explicit_section_header | 518 | 144 | 27.8 |
| nvidia | FY24_Q2 | 2023 Q2 | third_party_transcript_motley_fool | sentence | 1 | explicit_section_header | 470 | 138 | 29.4 |
| nvidia | FY24_Q3 | 2023 Q3 | third_party_transcript_motley_fool | sentence | 1 | explicit_section_header | 541 | 193 | 35.7 |
| nvidia | FY24_Q4 | 2023 Q4 | youtube_auto_captions | caption_sentence | 1 | transition_phrase_heuristic | 511 | 143 | 28.0 |
| nvidia | FY25_Q1 | 2024 Q1 | third_party_transcript_motley_fool | sentence | 1 | explicit_section_header | 484 | 166 | 34.3 |
| nvidia | FY25_Q2 | 2024 Q2 | third_party_transcript_motley_fool | sentence | 1 | explicit_section_header | 544 | 195 | 35.8 |
| nvidia | FY25_Q3 | 2024 Q3 | third_party_transcript_motley_fool | sentence | 1 | explicit_section_header | 507 | 189 | 37.3 |
| nvidia | FY25_Q4 | 2024 Q4 | third_party_transcript_motley_fool | sentence | 1 | explicit_section_header | 505 | 187 | 37.0 |
| nvidia | FY26_Q1 | 2025 Q1 | official_ir_pdf_factset_callstreet | sentence | 1 | explicit_section_header | 470 | 203 | 43.2 |
| nvidia | FY26_Q2 | 2025 Q2 | official_ir_pdf_factset_callstreet | sentence | 1 | explicit_section_header | 466 | 181 | 38.8 |
| nvidia | FY26_Q3 | 2025 Q3 | official_ir_pdf_factset_callstreet | sentence | 1 | explicit_section_header | 498 | 170 | 34.1 |
| nvidia | FY26_Q4 | 2025 Q4 | official_ir_pdf_factset_callstreet | sentence | 1 | explicit_section_header | 509 | 172 | 33.8 |
| nvidia | FY27_Q1 | 2026 Q1 | official_ir_pdf_factset_callstreet | sentence | 1 | explicit_section_header | 525 | 173 | 33.0 |
| nvidia | FY27_Q2 | 2026 Q2 | official_ir_pdf_factset_callstreet | sentence | 1 | explicit_section_header | 479 | 139 | 29.0 |
| tesla | 2021_Q4 ★ | 2021 Q4 | third_party_transcript_motley_fool | sentence | 1 | transition_phrase_heuristic | 538 | 38 | 7.1 |
| tesla | 2022_Q1 ★ | 2022 Q1 | youtube_auto_captions | caption_segment | 0 | transition_phrase_heuristic | 126 | 13 | 10.3 |
| tesla | 2022_Q2 ★ | 2022 Q2 | third_party_transcript_motley_fool | sentence | 1 | transition_phrase_heuristic | 586 | 26 | 4.4 |
| tesla | 2022_Q3 ★ | 2022 Q3 | third_party_transcript_motley_fool | sentence | 1 | transition_phrase_heuristic | 591 | 22 | 3.7 |
| tesla | 2022_Q4 | 2022 Q4 | third_party_transcript_motley_fool | sentence | 1 | transition_phrase_heuristic | 517 | 37 | 7.2 |
| tesla | 2023_Q1 | 2023 Q1 | youtube_auto_captions | caption_segment | 0 | transition_phrase_heuristic | 121 | 21 | 17.4 |
| tesla | 2023_Q2 | 2023 Q2 | third_party_transcript_motley_fool | sentence | 1 | transition_phrase_heuristic | 590 | 61 | 10.3 |
| tesla | 2023_Q3 | 2023 Q3 | third_party_transcript_motley_fool | sentence | 1 | transition_phrase_heuristic | 529 | 34 | 6.4 |
| tesla | 2023_Q4 | 2023 Q4 | third_party_transcript_motley_fool | sentence | 1 | transition_phrase_heuristic | 589 | 35 | 5.9 |
| tesla | 2024_Q1 | 2024 Q1 | third_party_transcript_motley_fool | sentence | 1 | transition_phrase_heuristic | 640 | 71 | 11.1 |
| tesla | 2024_Q2 | 2024 Q2 | third_party_transcript_motley_fool | sentence | 1 | transition_phrase_heuristic | 542 | 84 | 15.5 |
| tesla | 2024_Q3 | 2024 Q3 | third_party_transcript_motley_fool | sentence | 1 | transition_phrase_heuristic | 603 | 90 | 14.9 |
| tesla | 2024_Q4 | 2024 Q4 | third_party_transcript_motley_fool | sentence | 1 | transition_phrase_heuristic | 590 | 75 | 12.7 |
| tesla | 2025_Q1 | 2025 Q1 | youtube_auto_captions | caption_sentence | 1 | transition_phrase_heuristic | 697 | 56 | 8.0 |
| tesla | 2025_Q2 | 2025 Q2 | youtube_auto_captions | caption_sentence | 1 | transition_phrase_heuristic | 466 | 73 | 15.7 |
| tesla | 2025_Q3 | 2025 Q3 | youtube_auto_captions | caption_sentence | 1 | transition_phrase_heuristic | 497 | 89 | 17.9 |
| tesla | 2025_Q4 | 2025 Q4 | youtube_auto_captions | caption_sentence | 1 | transition_phrase_heuristic | 455 | 73 | 16.0 |
| tesla | 2026_Q1 | 2026 Q1 | youtube_auto_captions | caption_sentence | 1 | transition_phrase_heuristic | 424 | 79 | 18.6 |
| tesla | 2026_Q2 | 2026 Q2 | youtube_auto_captions | caption_sentence | 1 | transition_phrase_heuristic | 491 | 68 | 13.8 |

Other per-call fields worth knowing [R]:
- `call_date` is blank for 57 of 133 calls. It is filled only when stated in the file (`earnings_call_scope.py:call_date`, lines 168-185) and is never inferred.
- `source_url` is blank for 6 calls (Nvidia FY26 Q1 – FY27 Q2, whose metadata gives no URL).
- `acquisition_status`: 122 `already_present`, 11 `acquired`. The 17 extras show `already_present` because the build reads the
  manifest status of whatever file exists in the scratch copy. This label is misleading for the extras (see Discrepancies D12).

## III.2 Fiscal-to-calendar mapping [F, code] / first and last period labels [R]

Code: `earnings_call_scope.py:calendar_quarter` (lines 41-62). Rule: each fiscal quarter is assigned to the calendar quarter
that holds most of its months. `period_label` is never rewritten; `calendar_year` and `calendar_quarter` are added fields.

| Firm | FY end | Mapping in code | First label | Last label |
|---|---|---|---|---|
| Alphabet, Amazon, Meta, Tesla | Dec 31 | identity: `YYYY_Qn` → (YYYY, n) | 2021_Q4 | 2026_Q2 |
| Microsoft | Jun 30 | FY Q1→(FY−1, 3), Q2→(FY−1, 4), Q3→(FY, 1), Q4→(FY, 2) | FY22_Q2 | FY26_Q4 |
| Apple | last Sat of Sep | FY Q1→(FY−1, 4), Q2→(FY, 1), Q3→(FY, 2), Q4→(FY, 3) | FY22_Q1 | FY26_Q3 |
| Nvidia | last Sun of Jan | FY Qn→(FY−1, n) | FY22_Q4 | FY27_Q2 |

Caveats:
- Nvidia's fiscal quarters (~Feb–Apr, May–Jul, Aug–Oct, Nov–Jan) run about one month behind the calendar quarter they are
  assigned to. For example, FY23 Q4 (Nov 2022 – Jan 2023) is assigned to calendar 2022 Q4.
  `fiscal_quarter_end` (lines 96-103) encodes the +1 month for Nvidia.
- The teammate passage filter uses the same assignment (`earnings_calls/filter_ai_passages.py:cal_quarter`). Its docstring says
  "ends in", which is not accurate for Nvidia (the scope doc notes this). Approval was recorded on 2026-10-10 (Task 0).

## III.3 Source mix [R]

Classification code: `earnings_call_scope.py:source_type` (lines 132-148). It checks metadata strings in this order:
"motley fool", "youtube auto-generated captions", "faster-whisper", "callstreet" (body), "official company ir transcript (docx)",
"microsoft investor relations", "official transcript"; anything else is `unknown`.

| source_type | Calls | Firms |
|---|---:|---|
| official_ir_transcript_pdf | 37 | Alphabet 18, Meta 19 |
| third_party_transcript_motley_fool | 29 | Apple 6, Nvidia 12, Tesla 11 |
| youtube_auto_captions | 22 | Apple 13, Tesla 8, Nvidia 1 |
| machine_transcript_whisper_of_official_ir_audio | 19 | Amazon 19 |
| official_ir_transcript_html | 15 | Microsoft 15 |
| official_ir_pdf_factset_callstreet | 6 | Nvidia 6 (FY26 Q1 – FY27 Q2) |
| official_ir_transcript_docx | 4 | Microsoft 4 (FY22 Q2 – FY23 Q1) |
| unknown | 1 | Alphabet 2021_Q4 |
| **Total** | **133** | |

**The `unknown` call is `alphabet_2021_Q4`** (one of the 17 extras). Its metadata line reads "official Alphabet transcript PDF
(removed from abc.xyz; retrieved from an Internet Archive capture dated 2024-07-16)". `source_type()` tests for the substring
"official transcript" (line 146), and "official **Alphabet** transcript" does not contain it, so the function falls through
to `unknown`. In substance it is an official IR PDF retrieved through the Internet Archive. This is a classifier-string issue,
not missing provenance. It does not change units or AI counts: the parser is chosen by company (`detect_format`, line 820),
not by source_type.

## III.4 The 17 extended calls [F README + R cross-check]

Source: `earnings_calls_pre2022_extra/README.md`, cross-checked against each file's metadata header and the call-units file.

| Firm | Period(s) | Calendar | Source (file header) | How acquired (README) | source_type in build | unit_type | Speaker labels |
|---|---|---|---|---|---|---|---|
| Alphabet | 2021_Q4 | 2021 Q4 | Official Alphabet transcript PDF, removed from abc.xyz; Internet Archive capture 2024-07-16 (`web.archive.org/web/20240716084722/...2021_Q4_Earnings_Transcript.pdf`) | official text via archive | unknown (see III.3) | sentence | yes |
| Amazon | 2021_Q4, 2022_Q1, 2022_Q2, 2022_Q3 | 2021 Q4 – 2022 Q3 | Amazon IR call audio (q4cdn URLs in headers: Q4-2021 .wav, Q1-2022 .mp3, Q2-2022 .mp3, Q3-2022 .wav) | transcribed locally with faster-whisper `small.en` | machine_transcript_whisper_of_official_ir_audio | whisper_unit | no |
| Apple | FY22_Q1 – FY22_Q4 | 2021 Q4 – 2022 Q3 | Motley Fool pages dated 2022-01-28, 04-29, 07-28, 10-27 | third-party text | third_party_transcript_motley_fool | sentence | yes |
| Nvidia | FY22_Q4, FY23_Q1 – FY23_Q3 | 2021 Q4 – 2022 Q3 | Motley Fool pages dated 2022-02-17, 05-26, 08-24, 11-16 | third-party text | third_party_transcript_motley_fool | sentence | yes |
| Tesla | 2021_Q4, 2022_Q2, 2022_Q3 | 2021 Q4, 2022 Q2, 2022 Q3 | Motley Fool pages dated 2022-01-27, 07-21, 10-20 | third-party text | third_party_transcript_motley_fool | sentence | yes |
| Tesla | 2022_Q1 | 2022 Q1 | YouTube auto-captions of Tesla's own upload (`youtu.be/kOyZ_Rypeto`); Fool has no page | machine captions | youtube_auto_captions | caption_segment | no |

Counts: 1 + 4 + 4 + 4 + 4 = 17 [R]. The extras contribute 7,611 units and 498 AI units [R].
- Before inclusion, 9 of these were "awaiting a human source decision" and 8 were "unavailable public source" (no company
  source exists) (`earnings_call_scope.py` `GAPS`, lines 193-242; `GATE4_VALIDATION_REPORT.md` §1).
- **[ND]** Retrieval dates for the Fool and YouTube files, faster-whisper settings beyond the model name (beam size, VAD,
  language, compute type, version), and who ran the transcription. Missing: an acquisition log for the extras (the README
  gives source and type only).
- Inclusion approved by Advik on 2026-10-10 (recorded in `EARNINGS_CALL_SCOPE.md` §10 by this task).

## III.5 Exclusions and restrictions actually applied in code

| Rule | Where | Status |
|---|---|---|
| Window and cutoff: only the 133 (company, period) pairs from `expected_calls()` are processed. Calls after calendar Q2 2026 are never read. | `earnings_call_scope.py:expected_calls`; `build_earnings_call_canonical.py:build` loops over `S.expected_calls()` (line 369) | [F] |
| Main call only: enforced **by file naming**, not by code. Only `<company>_<period>.md` in `earnings_calls/<company>/` is read. There is no code that detects or drops follow-up calls. Meta's "Follow Up Call" exclusion is a curation decision (scope §2). **[ND]** whether any follow-up file was ever present and removed (no record in the repo). | `earnings_call_scope.py:raw_path` | [F] |
| Files outside the expected set would be listed as "stray" by `--check` | `earnings_call_scope.py:316-320` | [R] none present |
| Non-call text removed before counting (metadata, cover/title block, page numbers, headers, disclaimers, Fool roster and ads, pre-call livestream chatter, caption tags and timestamps) | see Task 2 / Appendix A3 | [F] |
| Operator lines are part of the call and count in the denominator | scope §6; no code removes Operator turns | [F] |
| Borderline automation and infrastructure units: in the denominator, not in the AI numerator | `filter_earnings_calls.py:classify` (lines 222-225); `total_units` counts all units | [F] |
| Analysis-time restriction: pooled lines, the headline figure and the tone figure use only calls/units with `units_comparable_to_sentences == 1` (`sentence` or `caption_sentence`) | `01_timeseries.py:95,113`; `05_tone_figures.py:205` | [F] |
| Headline firms: only firms with ≥3 comparable calls both before and after launch (drops Amazon) | `01_timeseries.py:balanced_firms` (lines 103-108) | [F] |
| No call is dropped from the canonical build for quality reasons. All 133 parse (no `PARSE FAILED`), and no call has `section_method = not_detected_all_prepared` | call-units file | [R] |

## III.6 Corpus totals [R]

Source: `earnings_calls_canonical_extended/earnings_call_call_units.csv` (column sums). Flag counts are cross-checked
against `earnings_call_sentences.csv` and agree.

| Measure | All | sentence | caption_sentence | whisper_unit | caption_segment |
|---|---:|---:|---:|---:|---:|
| Calls | 133 | 92 | 14 | 19 | 8 |
| Total units | 61,961 | 46,098 | 7,017 | 7,925 | 921 |
| Prepared-remarks units | 24,472 | 18,486 | 2,271 | 3,351 | 364 |
| Q&A units | 37,489 | 27,612 | 4,746 | 4,574 | 557 |
| AI units | 10,382 | 8,506 | 774 | 979 | 123 |
| AI units, prepared | 5,165 | 4,320 | 302 | 501 | 42 |
| AI units, Q&A | 5,217 | 4,186 | 472 | 478 | 81 |
| Borderline automation/robotics | 488 | 230 | 185 | 71 | 2 |
| Borderline infrastructure | 2,234 | 1,874 | 116 | 230 | 14 |
| AI units flagged uncertain (weak term only) | 2,788 | 2,227 | 299 | 236 | 26 |
| AI units flagged context-dependent | 623 | 505 | 38 | 80 | 0 |
| AI units flagged safe-harbor | 0 | 0 | 0 | 0 | 0 |
| AI units flagged long (>150 words) | 1 | 0 | 1 | 0 | 0 |

- Pooled AI share across everything: 10,382 / 61,961 = 16.8% (not used in any figure).
- Core-term AI units (`is_uncertain = 0`): 7,594; weak-only (`is_uncertain = 1`): 2,788.
- Units in comparable calls (sentence + caption_sentence): 53,115 total, 9,280 AI.
- Unit-type definitions: `build_earnings_call_canonical.py:unit_type` (lines 246-251). See Appendix A3.

## III.7 10-K Item 1A comparison sample

| Fact | Value | Source | Status |
|---|---|---|---|
| Input file | `export/ai_washing_10-K.csv`: one row per (filing, section) with the full section text. 822 rows covering many firms; last changed in commit `c912827` (2026-08-10, older pipeline) | `02_finbert_tone.py:57-59` | [F] |
| Rows used | `ticker ∈ Mag 7` and `section` contains "1A" | `02_finbert_tone.py:59`, `02b_baseline_tone.py:115` | [F] |
| Item 1A filings available | **72** Mag 7 Item 1A rows (one per 10-K), filing dates 2006-03-16 to 2026-07-29 | [R] |
| Filings per firm (filing years) | AAPL 11 (2015–2025); AMZN 6 (2021–2026); GOOGL 3 (2024–2026); META 2 (2025–2026); MSFT 21 (2006–2026); NVDA 21 (2006–2026); TSLA 8 (2019–2026) | [R] |
| Filings that contribute ≥1 AI sentence | **36** of 72. 36 filings have zero AI sentences: AAPL 2015–2022, MSFT 2006–2016, NVDA 2006–2020, TSLA 2020–2021 filings | [R] |
| AI sentences (all years) | **682** (after `drop_duplicates` on ticker, filing_date, text) | `tenk_item1a_ai_tone.csv` | [R] |
| AI sentences by filing year | 2017:1, 2018:12, 2019:13, 2020:12, 2021:14, 2022:26, 2023:54, 2024:110, 2025:192, 2026:247 | [R] |
| AI sentences used in the tone figure (filing year ≥ 2023) | **604** | `05_tone_figures.py:212` | [R] |
| AI sentences by firm, filing year ≥ 2023 | AAPL 10, AMZN 34, GOOGL 98, META 108, MSFT 172, NVDA 167, TSLA 15 | [R] |
| Non-AI baseline frame | 27,313 non-AI sentences ≤600 chars before dedupe, **27,076** after `drop_duplicates`; all 72 filings, all years 2006–2026 | `02b_baseline_tone.py:tenk_sentences` | [R] |
| Non-AI baseline sample | **2,500**, `DataFrame.sample(2500, random_state=3)` | `02b_baseline_tone.py:96,138` | [R] |
| Baseline sample by filing year | 2006–2018: 939 total; 2019–2022: 652; 2023–2026: 909 (2023:162, 2024:207, 2025:285, 2026:255) | [R] |

**How 10-K AI sentences are identified: a different filter from the calls.**
- Calls use the canonical sentence filter (`filter_earnings_calls.py:classify`: core + weak terms, nltk Punkt units).
- 10-K Item 1A uses `analysis_calls/common.py:is_ai` (lines 22-32): a **narrower, core-only regex with no weak terms and no
  named-product list** beyond Copilot, Gemini, OpenAI, ChatGPT/GPT and Apple Intelligence. It is applied to sentences from a
  **regex splitter** (`02_finbert_tone.py:split_sentences`, lines 41-43: split after `.?!` followed by whitespace and a capital
  letter, quote or parenthesis; sentences ≤25 chars dropped).
- Script: `analysis_calls/02_finbert_tone.py:main` (lines 57-68). Input: `export/ai_washing_10-K.csv`.

```python
# analysis_calls/common.py:22-32
RE_AI = re.compile(
    r"artificial intelligence|machine learning|deep learning|neural net(?:work)?s?"
    r"|large language models?|\bLLMs?\b|\bgenerative\b|chat ?GPT|\bGPT[- ]?\d?|open ?AI|\bcopilot\b|\bgemini\b"
    r"|\bagentic\b|foundation models?|apple intelligence",
    re.I,
)
RE_AI_CS = re.compile(r"\bA\.?I\.?(?![A-Za-z])")  # "AI" must be upper-case

def is_ai(sentence):
    return bool(RE_AI_CS.search(sentence) or RE_AI.search(sentence))
```

**Item 1A extraction method** [F]: `edgar.py:extract_sections` (lines 334-403), called from `main.py:collect_for_company`
(old SEC pipeline). It fetches the filing text, finds line-anchored headings matching
`item\s*1a\b[^A-Za-z0-9]{0,60}r\s*i\s*s\s*k\s+f\s*a\s*c\s*t\s*o\s*r\s*s`, drops quoted cross-references
(`_XREF_TAIL`), takes the first candidate followed by at least 8 lowercase prose words (`MIN_PROSE_WORDS`, which rejects
table-of-contents lines), and ends the section at the next line-anchored heading for a different item. **[ND]** whether
the committed CSV (last written 2026-08-10) was produced by this exact version of `edgar.py`. No extraction log or
version stamp is stored in the CSV (`retrieved_at` exists, but no code hash). Note also that `accession` and `period_end`
are blank for 43 of the 72 Mag 7 Item 1A rows [R] (present only for MSFT 2006–2019 and NVDA 2006–2020), so filings can be identified only by ticker and filing date.

**Coverage gaps (confirmed)** [R]: Alphabet filings start with the 10-K filed **2024-01-31** (fiscal 2023), and Meta with the
10-K filed **2025-01-30** (fiscal 2024). By *filing year*, Alphabet starts 2024 and Meta 2025, as you believed. By *fiscal
year*, Alphabet covers FY2023–FY2025 and Meta FY2024–FY2025. Apple has no 2026 filing (its FY2026 10-K is due ~Nov 2026).
Amazon's earliest is 2021.

## III.8 Table 1 draft data [R]

Computation (scratch `facts3.py`, from `earnings_call_call_units.csv`): per call, `share = ai_units / total_units × 100`.
"Mean share" = unweighted mean of per-call shares. Pre = calendar quarter < 2022 Q4; post = ≥ 2022 Q4 (same rule as
`01_timeseries.py`). "Comparable" restricts to `units_comparable_to_sentences == 1`.

| Firm | Calls | Source types | Unit types | Total units | AI units | Mean share, all calls | Mean pre (n), all | Mean post (n), all | Mean pre (n), comparable | Mean post (n), comparable |
|---|---:|---|---|---:|---:|---:|---:|---:|---:|---:|
| Alphabet | 19 | official PDF 18; unknown (official via archive) 1 | sentence 19 | 9,456 | 1,840 | 19.3 | 4.6 (4) | 23.2 (15) | 4.6 (4) | 23.2 (15) |
| Amazon | 19 | Whisper of IR audio 19 | whisper_unit 19 | 7,925 | 979 | 11.9 | 0.4 (4) | 14.9 (15) | – (0) | – (0) |
| Apple | 19 | YouTube captions 13; Motley Fool 6 | caption_sentence 7; sentence 6; caption_segment 6 | 7,076 | 321 | 6.7 | 0.1 (4) | 8.4 (15) | 0.1 (4) | 5.1 (9) |
| Meta | 19 | official PDF 19 | sentence 19 | 9,123 | 1,570 | 17.5 | 5.0 (4) | 20.9 (15) | 5.0 (4) | 20.9 (15) |
| Microsoft | 19 | official HTML 15; official DOCX 4 | sentence 19 | 9,328 | 1,750 | 18.5 | 2.8 (4) | 22.7 (15) | 2.8 (4) | 22.7 (15) |
| Nvidia | 19 | Motley Fool 12; FactSet CallStreet 6; YouTube captions 1 | sentence 18; caption_sentence 1 | 9,461 | 2,877 | 30.4 | 18.4 (4) | 33.6 (15) | 18.4 (4) | 33.6 (15) |
| Tesla | 19 | Motley Fool 11; YouTube captions 8 | sentence 11; caption_sentence 6; caption_segment 2 | 9,592 | 1,045 | 11.4 | 6.4 (4) | 12.8 (15) | 5.1 (3) | 12.4 (14) |
| **All** | **133** | | | **61,961** | **10,382** | 16.5 | 5.4 (28) | 19.5 (105) | 6.0 (23) | 20.8 (83) |

Recommendation for the writer: report the comparable-only pre/post columns. They are what Fig 1/1b and
`ai_share_pre_post.csv` use, and the "all" columns mix in caption-segment and Whisper units. Amazon's all-calls means are
not comparable to the others.

---

# IV.A AI-sentence filter

Code: `filter_earnings_calls.py` (sha256 of the LF version: `3a9b355c5877…`; this file's hash appears in
`extraction_version`). The canonical build imports and re-runs it read-only (`build_earnings_call_canonical.py:extract_call`)
and asserts that its units equal `process_file` output (lines 318-321).

## IV.A.1 Term lists (verbatim from code)

**Core terms**: a hit puts the unit in the AI set with no flag. `filter_earnings_calls.py:93-132`. `_rx(p, cs=False)` compiles
with `re.IGNORECASE` unless `cs=True` (lines 89-90).

```python
# Core terms: a hit puts the sentence in the AI set, no flag.
CORE_TERMS = [
    ("AI", _rx(r"(?<![A-Za-z])AIs?(?![A-Za-z])", cs=True)),
    ("A.I.", _rx(r"(?<![A-Za-z])A\.I\.")),
    ("artificial intelligence", _rx(r"\bartificial (?:general )?intelligence\b")),
    ("GenAI/OpenAI/xAI", _rx(r"\b(?:GenAI|OpenAI|xAI)\b", cs=True)),
    ("OpenAI/ChatGPT (any case)", _rx(r"\bopen ?ai\b|\bchat ?gpt\b")),
    ("x.ai / Character.ai", _rx(r"\bx\.ai\b|\bcharacter\.ai\b|\bXAi\b")),
    ("Apple Intelligence", _rx(r"\bapple intelligence\b")),
    ("generative", _rx(r"\bgenerative\b")),
    ("agentic", _rx(r"\bagentic\b")),
    ("machine learning", _rx(r"\bmachine[- ]learning\b")),
    ("deep learning", _rx(r"\bdeep[- ]learning\b")),
    ("neural network", _rx(r"\bneural (?:net|nets|network|networks|engine|engines)\b")),
    ("LLM", _rx(r"\bLLMs?\b", cs=True)),
    ("language model", _rx(r"\b(?:large )?language models?\b")),
    ("ML model phrase", _rx(
        r"\b(?:foundation(?:al)?|frontier|reasoning|multimodal|diffusion|"
        r"open[- ]source|open[- ]weights?|ranking|recommendation|retrieval|"
        r"ML|trained|video[- ]generation|image[- ]generation|world)\s+models?\b")),
    ("training/inference compute", _rx(
        r"\b(?:training|inference)\s+(?:compute|clusters?|runs?|workloads?|"
        r"capacity|infrastructure|chips?|costs?|demand|tokens?|requests?)\b|"
        r"\bmodels?\s+(?:training|inference)\b|\btrain(?:ing|ed)?\s+(?:\w+\s+){0,3}models?\b")),
    ("parameter model", _rx(
        r"\bparameters?\s+models?\b|\b\d+(?:\.\d+)?\+?\s?(?:B|billion|trillion|T)\+?\s+parameters?\b")),
    ("superintelligence", _rx(r"\bsuperintelligen(?:ce|t)\b")),
    ("AGI", _rx(r"\bAGI\b", cs=True)),
    ("chatbot", _rx(r"\bchat ?bots?\b")),
    ("computer vision / NLP", _rx(r"\bcomputer vision\b|\bnatural language processing\b|\bNLP\b")),
    # Named AI products, models, labs, AI chips (case-sensitive).
    ("named AI product", _rx(
        r"\b(?:ChatGPT|Copilots?|Gemini|Gemma|Bard|Llama|Claude|Anthropic|"
        r"Bedrock|Trainium\d?|Inferentia\d?|TPUs?|Nova|Amazon Q|Q Developer|"
        r"DeepMind|DeepSeek|Grok|Mistral|Perplexity|NotebookLM|Imagen|Veo|"
        r"Midjourney|Stable Diffusion|Sora|Phi|Phi-\d|NIMs?|NeMo|TensorRT|GR00T|"
        r"MTIA|Maia|MAI|Emu|Movie Gen|Segment Anything|Stargate|AlphaFold|Dojo)\b|"
        r"\bTraining and Inference Accelerator\b", cs=True)),
    ("named AI product (any case)", _rx(r"\bcopilots?\b|\bgemini\b|\banthropic\b|\bdeepseek\b")),
]
```

**Machine-transcript lowercase "ai" rule** (`filter_earnings_calls.py:134-137`, applied in `classify` lines 204-206).
It applies only when the parser format is `captions` (Whisper or YouTube; `MACHINE_FORMATS = {"captions"}`, line 831).
It adds the pseudo-core term `"AI (machine transcript, any case)"` if no case-sensitive "AI" hit exists. In
non-machine transcripts, lowercase/mixed-case "ai" tokens are counted as false positives instead and are **not** AI
(lines 175-179, 208). 17 AI units carry this term [R].

```python
MACHINE_AI = _rx(r"(?<![A-Za-z])ai'?s?(?![A-Za-z])")
FALSE_POSITIVE_AI = _rx(r"(?<![A-Za-z])(?:ai|Ai|aI)s?(?![A-Za-z])", cs=True)
AI_COMPANY_DOMAIN = _rx(r"\bx\.ai\b|\bcharacter\.ai\b|\bXAi\b")
SURNAME_AI = _rx(r"\b(?:Mr|Ms|Mrs|Dr)\.\s+Ai\b", cs=True)   # "Mr. Ai" scrubbed before matching
```

**Weak terms**: a hit with no core hit puts the unit in the AI set with flag `uncertain`. `filter_earnings_calls.py:139-165`.

```python
MODEL_BARE = _rx(
    r"(?<!business )(?<!operating )(?<!financial )(?<!revenue )(?<!pricing )"
    r"(?<!subscription )(?<!economic )(?<!cost )(?<!delivery )(?<!hybrid )"
    r"(?<!partnership )(?<!retail )(?<!franchise )(?<!go-to-market )(?<!role )"
    r"(?<!licensing )(?<!monetization )(?<!consumption )(?<!distribution )"
    r"(?<!sales )(?<!service )(?<!services )(?<!margin )(?<!pricing )"
    r"\bmodels?\b(?!\s+(?:year|[3SXY]\b|lineup))")
WEAK_TERMS = [
    ("AI accelerator name", _rx(
        r"\b(?:Blackwell|Hopper|Rubin|GB[23]00|[AHB]100|H20|H200|DGX|HGX|NVLink|CUDA)\b", cs=True)),
    ("AI platform name", _rx(
        r"\b(?:Foundry|Fairwater|Omniverse|Cosmos|Isaac|Dynamo|Siri|Private Cloud Compute)\b", cs=True)),
    ("Meta ads-model name", _rx(r"\b(?:GEM|Andromeda|Lattice)\b", cs=True)),
    ("agent", _rx(r"\bagents?\b")),
    ("inference", _rx(r"\binferenc\w*")),
    ("tokens", _rx(r"\btokens?\b")),
    ("algorithm", _rx(r"\balgorithm\w*")),
    ("recommendation system", _rx(r"\brecommendation (?:systems?|engines?)\b")),
    ("model architecture/performance", _rx(
        r"\bmodels?\s+(?:architecture|performance|capabilit\w+|weights|parameters)\b")),
    ("model (bare)", MODEL_BARE),
    ("Alexa", _rx(r"\bAlexa\b", cs=True)),
    ("autonomous driving", _rx(
        r"\bWaymo\b|\bself[- ]driving\b|\bautonom\w+|\bFSD\b|\bAutopilot\b|"
        r"\brobo[- ]?taxi\w*|\bCybercab\b")),
]
# Weak terms switched off per company because they mean something else there.
WEAK_OFF = {"tesla": {"model (bare)"}, "apple": {"model (bare)"}}   # car / device models
```

Per-firm exceptions: **only** `WEAK_OFF`. Bare "model(s)" is off for Tesla and Apple (line 167). There are no other
per-firm term exceptions. (Note that `(?<!pricing )` appears twice in `MODEL_BARE`; the duplicate has no effect.)

**Borderline lists**: units with no core or weak term (`filter_earnings_calls.py:169-173`).

```python
AUTOMATION_TERMS = _rx(r"\bautomat\w*|\brobot\w*|\bOptimus\b|\bhumanoid\w*")
INFRA_TERMS = _rx(
    r"\bGPUs?\b|\bdata ?cent(?:er|re)s?\b|\bcap ?ex\b|\bcapital expenditures?\b|"
    r"\baccelerated computing\b|\bcompute\b|\bservers?\b|\bsupercomput\w+|"
    r"\baccelerators?\b|\binfrastructure\b")
```

**Flags on AI units** (`filter_earnings_calls.py:181-189`, applied lines 212-220):

```python
SAFE_HARBOR = _rx(
    r"forward[‐-]looking statements?|safe harbor|undertake no obligation|"
    r"could cause (?:actual )?results to differ|differ materially")
CONTEXT_DEPENDENT = _rx(
    r"^(?:(?:And|So|But|Now|Well|Yes|Yeah|Okay|OK)[,]?\s+)?"
    r"(?:It|It's|It’s|This|That|That's|That’s|These|Those|They|They're|They’re|Them|Which)\b"
    r"(?!\s+(?:month|year|quarter|week|morning|afternoon|time|fall|spring|summer|winter)\b)",
    cs=True)
LONG_WORDS = 150   # flag "long" if len(sentence.split()) > 150
```

## IV.A.2 Decision order (`filter_earnings_calls.py:classify`, lines 200-226) [F]

1. Scrub `Mr./Ms./Mrs./Dr. Ai` from the text (surname guard).
2. Collect **core** hits on the scrubbed text. In machine transcripts, add the lowercase-"ai" pseudo-core term if no
   uppercase "AI" hit exists.
3. Collect **weak** hits, skipping weak terms switched off for the company.
4. If any core **or** weak hit: kind = **AI**. Flags: `uncertain` if no core hit; `uncertain: safe-harbor` if
   `SAFE_HARBOR` matches; `context-dependent` if `CONTEXT_DEPENDENT` matches; `long` if >150 words.
5. Otherwise, if `AUTOMATION_TERMS` matches: kind = **borderline automation/robotics** (`auto`).
6. Otherwise, if `INFRA_TERMS` matches: kind = **borderline infrastructure** (`infra`).
7. Otherwise: kind = **out** (non-AI; still counted in `total_units`).

Note: borderline tests run on the original text, core/weak tests on the surname-scrubbed text. A unit that contains both an
AI term and an automation or infra term is AI; borderline means "no AI term at all".

Trigger tallies on the extended build [R] (a unit can carry several triggers): AI 5,292; model (bare) 1,647; named AI
product 1,536; named AI product (any case) 975; AI accelerator name 892; autonomous driving 828; generative 628; agent 576;
inference 529. Weak-only (`uncertain`) units by trigger: autonomous driving 732, AI accelerator name 690, model (bare) 622,
agent 305, inference 248, AI platform name 145, tokens 101, Alexa 44, recommendation system 32, algorithm 29,
Meta ads-model name 29, model architecture/performance 27.

## IV.A.3 Filter comparison with the teammate passage filter (93.4% / 96.7%) [R]

Code: `earnings_calls_canonical/gate4_validate.py:compare_filters` (lines 491-612). Teammate filter:
`earnings_calls/filter_ai_passages.py` → `earnings_calls/ai_passages.csv`.

**Method (from code):** lowercase the text and turn every non-alphanumeric run into one space (`tnorm`). Word 6-gram
shingles (`NGRAM = 6`).
- A canonical AI unit "overlaps" if ≥50% of its 6-grams occur anywhere in that call's teammate passages. Units under 6 tokens
  use substring containment instead.
- A teammate passage "overlaps" if at least one canonical AI unit of the same call has ≥50% of its 6-grams inside that
  passage.

**What each percentage means:**
- **93.4%** = share of canonical **core-term** AI units (`is_uncertain = 0`) that overlap a teammate passage:
  6,665 / 7,133. Read it as "the teammate filter finds ~93% of what our core terms find".
- **96.7%** = share of teammate passages that contain at least one canonical AI unit: 3,226 / 3,335. Read it as "nearly
  every teammate passage is also found by our filter". This is not a precision or recall estimate against human truth:
  both filters are unvalidated.
- Companions: all canonical units 7,339 / 9,669 = 75.9%; weak-only units 674 / 2,536 = 26.6% (low by design, because the
  teammate filter has no weak terms); strict containment 7,063 / 9,669 = 73.0%.

**Which corpus:** the **105 calls** in both sources. `ai_passages.csv` was produced on 2026-10-01 from the original 105
files. The Gate 4 run used the 116-call canonical build, and the 11 Gate 2 acquisitions had no teammate passages. I re-ran
`compare_filters` with the **extended** sentences against the committed `ai_passages.csv`: same 105 calls, identical
numbers (93.4 / 96.7). This is expected, because canonical rows for those 105 calls are unchanged.

**Does it hold for 133?** I re-ran the teammate filter on all 133 raw files in a scratch copy. It reproduces the committed
3,335 passages exactly on the original 105 calls and yields 3,581 passages in total. Comparison over **all 133 calls**:

| Measure | 105 calls (as reported) | 133 calls (recomputed) |
|---|---|---|
| Core-term canonical units overlapping a teammate passage | 6,665 / 7,133 = **93.4%** | 7,104 / 7,594 = **93.5%** |
| Teammate passages containing a canonical unit | 3,226 / 3,335 = **96.7%** | 3,471 / 3,581 = **96.9%** |
| All canonical units (shingle) | 7,339 / 9,669 = 75.9% | 7,835 / 10,382 = 75.5% |
| Weak-only canonical units | 674 / 2,536 = 26.6% | 731 / 2,788 = 26.2% |
| Strict containment | 7,063 / 9,669 = 73.0% | 7,555 / 10,382 = 72.8% |

The 133-call row is from a scratch run only; no committed file holds these numbers. To quote them in the paper, the
comparison should be committed (e.g. a `filter_comparison_extended.csv`).

## IV.A.4 Manual review sample (`earnings_calls_canonical/manual_review_sample.csv`) [R]

| Fact | Value |
|---|---|
| Rows | **150** |
| Seed | **20261006** (`gate4_validate.py:44`, `random.Random(SEED)`) |
| Sampling frame | AI rows of the **116-call** canonical build (`earnings_calls_canonical/earnings_call_sentences.csv`) |
| Design | 28 strata = company (7) × section (2) × match type (core / uncertain). 5 per stratum = 140, plus a top-up of 10 `caption_segment` rows. Within each stratum, rows are sorted by (calendar_year, calendar_quarter, sentence_id), cut into k equal chunks, and one row is drawn per chunk (time-spread). Shortfalls are re-allocated to the largest strata (`gate4_validate.py:review_sample`, lines 679-752) |
| Realised composition | Apple 29, Tesla 21, others 20 each; prepared 74 / Q&A 76; core 79 / uncertain 71; sentence 95, caption_sentence 22, whisper_unit 20, caption_segment 13; calendar years 2022:6, 2023:28, 2024:43, 2025:50, 2026:23 |
| Columns to fill | `reviewer_id`, `review_date`, `q_is_about_ai`, `q_text_matches_source`, `q_speaker_correct`, `q_section_correct`, `q_unit_boundary_ok`, `reviewer_notes` |
| Fill status | **All 8 judgment columns are empty in all 150 rows** |
| Covers the 17 extended calls? | **No**: 0 of 150 rows come from the extras (498 AI rows there). All 150 sentence_ids still exist unchanged in the extended build |
| Covers 2021 Q4 – 2022 Q3? | Only 6 rows are from calendar 2022, from the Gate 2-acquired calls and 2022 Q4. None are from the extras |

**What can be computed once filled:**
- **Precision** of the AI filter (`q_is_about_ai`) overall, and separately for core and weak-only matches. Because selection
  is stratified with unequal probabilities, a corpus-level precision needs **inverse-probability weights**: stratum size /
  rows sampled per stratum. The stratum sizes are available from the sentence file.
- Accuracy rates for verbatim text, speaker, section and unit boundaries.

**What cannot be computed from it:**
- **Recall.** Only filter-positive units are sampled, so false negatives (AI talk without any listed term) are never seen.
  Recall would need a sample of non-AI (`out`) and borderline units.
- Precision for the 17 extras or the pre-ChatGPT window. Any claim restricted to the extended calls needs a top-up sample.
- Any substantive label (opportunity, risk, etc.). The sheet has none by design.

## IV.A.5 Earlier validation numbers and whether they may be quoted

| Number | Where | Corpus state | Quotable for the current build? |
|---|---|---|---|
| "Core-term matches were 100% precise in the sample" (28/28 core; 33/40 = 82.5% clearly AI overall; 3/40 not AI; all from weak-only matches) | `earnings_calls_ai_only/FILTER_METHOD.md` §Validation 3 | 40 random AI sentences, seed 20260930, **105-call corpus (pre-Gate 2)**, filter version before the canonical build | **No, not as a validation of the current build.** `GATE4_VALIDATION_REPORT.md` says these legacy results "must not be quoted as describing this corpus". Re-running the sample code on today's corpus would draw a different 40 (the pool changed). At most, describe it as an informal pilot spot-check on an earlier corpus state |
| "48,555 checked, 0 verbatim failures"; recall spot-check table | `FILTER_METHOD.md` | 105 calls; conflicts with `_validation.json` (45,293 / 8, a stale overwrite per Gate 4 B4) | No |
| Gate 4: 0 verbatim failures among AI rows; 1 failure among 54,350 units | `GATE4_VALIDATION_REPORT.md` §5 | 116 calls | Not for 133 as stated. For the extended build, `build_validation.json` reports **0 verbatim failures over 10,382 AI rows** [F, reproduced] (it checks AI rows only, not all units) |
| Filter overlap 93.4% / 96.7% | Gate 4 B3 | 105 calls | Yes, if described as an agreement statistic between two unvalidated filters on 105 calls. The 133-call values are 93.5% / 96.9% (IV.A.3) |

Bottom line: there is **no measured precision or recall** for the current filter. Scope §8 says the filter "must not be
described as validated".

---

# IV.B AI share (`analysis_calls/01_timeseries.py`)

## Definitions [F]

| Item | Definition | Code |
|---|---|---|
| Unit | One parsed transcript unit (a Punkt sentence, punctuated caption sentence, Whisper unit or caption segment) | build `unit_type` |
| Numerator | `ai_units`: units classified AI (core or weak; borderline excluded) | call-units file |
| Denominator | `total_units`: all parsed units in the call after noise removal, including Operator, borderline and non-AI units | call-units file |
| Call AI share | `share = ai_units / total_units * 100` | `01_timeseries.py:94` |
| Prepared / Q&A shares | Available as `ai_units_prepared / total_units_prepared` and `ai_units_qa / total_units_qa`, but **no figure uses section-level shares**; Figs 1, 1b and 2 use the whole-call share only | call-units file |
| Pre / post | `post = q >= qkey(2022, 4)`, where `qkey(y, q) = y + (q-1)/4`. The first post-launch calls are those reporting **calendar Q4 2022** (held Jan–Feb 2023, after ChatGPT's 30 Nov 2022 launch). Pre = calendar 2021 Q4 – 2022 Q3 | `common.py:14`; `01_timeseries.py:106,222`; the figure uses `launch_x() = qkey(2022,4) - 0.125` (line 100), which gives the same split |
| Comparable | `units_comparable_to_sentences == 1` | `01_timeseries.py:95` |

Caveat on the date rule: the split is by *reported calendar quarter*, not by call date. For Nvidia, calendar 2022 Q4 =
FY23 Q4 (Nov 2022 – Jan 2023), so it straddles the launch. Its call was held after the launch.

## 6-firm average [R]

- Firms: `balanced_firms()` = firms with ≥3 comparable calls both pre and post = **Alphabet, Apple, Meta, Microsoft, Nvidia,
  Tesla**. Amazon is excluded (0 comparable calls).
- Calls: **23 pre, 83 post** (Tesla pre = 3 because Tesla 2022 Q1 is a caption-segment call; Apple post = 9 because 6
  caption-segment calls are excluded).
- **12 of the 23 pre-launch calls come from the 17 extras** (Alphabet 2021 Q4; Apple ×4; Nvidia ×4; Tesla ×3). Without
  them, only Alphabet (3), Meta (4) and Microsoft (4) would have comparable pre-launch calls.

**What exactly "6.0% → 20.8%" is.** Several aggregations exist:

| Aggregation | Pre | Post | Diff | Where used |
|---|---:|---:|---:|---|
| A. Mean over quarters of the per-quarter cross-firm mean (the black line) | 6.06 | 20.78 | 14.72 | **Fig 1 annotations** ("6%", "21%", rounded `:.0f`), `fig_headline` lines 114-115, 133-135 |
| **B. Mean of per-call shares, pooled over all calls** | **6.05** | **20.79** | **14.74** | **matches the MEETING_SUMMARY numbers** (6.0 / 20.8 / +14.7; no-Nvidia 3.5 / 18.0 / +14.5) |
| C. Mean of per-firm means | 6.01 | 19.65 | 13.64 | not used |
| D. Pooled ratio Σai/Σtotal | 6.07 | 20.61 | – | not used |

So the summary used B: an unweighted **mean of per-call shares**, not a pooled ratio. The figure annotation uses A. They
agree to one decimal for the pre value (6.0 vs 6.1 at higher precision) and round to the same integers. **No script
computes B**: the summary numbers come from an uncommitted calculation (see bootstrap below).

**Without Nvidia** (Alphabet, Apple, Meta, Microsoft, Tesla; 19 pre / 68 post calls): B = **3.45 → 17.97, +14.52**
(quoted 3.5 → 18.0, +14.5 ✓). A = 3.40 → 17.94.

## Bootstrap [ND for the original; R for candidates]

- **No bootstrap code exists anywhere in the repo or its git history** (`git log -S bootstrap` finds only `MEETING_SUMMARY.md`).
  Resampling unit, number of resamples, seed and CI method of the quoted "95% CI 11.4–17.8" and "12.4–16.7" are **NOT
  DETERMINABLE FROM REPO**.
- Recomputed candidates (B = 10,000 resamples, percentile 2.5/97.5, several seeds):

| Design | 6 firms | Without Nvidia |
|---|---|---|
| Call-level iid: resample pre calls and post calls separately with replacement; difference of means of per-call shares | 11.3–11.4 to 17.8–18.0 (seed-dependent) | 12.3 to 16.7 |
| Firm-stratified (resample calls within firm × period) | 13.4 to 16.1 | 13.2 to 15.8 |
| Firm-cluster (resample firms) | 10.5–10.6 to 17.9–18.0 | 9.5 to 18.6 |
| Quarter-level (resample quarterly means, aggregation A) | 12.8 to 16.4 | 12.5 to 16.4 |

The quoted CIs (11.4–17.8; 12.4–16.7) agree, within seed noise, only with the **call-level iid percentile bootstrap of
the difference in mean per-call share**. That is very likely what was done, but it is not documented. Before the paper
quotes a CI, commit a bootstrap with a fixed seed. Also note that call-level iid ignores within-firm correlation; the
firm-cluster interval is wider (≈10.5–18.0).

## Per-company pre/post (comparable calls only) [R]

Identical to `analysis_calls/out_extended/ai_share_pre_post.csv` (`01_timeseries.py:summary`, mean of per-call shares).

| Firm | Pre calls | Pre mean % | Post calls | Post mean % |
|---|---:|---:|---:|---:|
| Alphabet | 4 | 4.63 | 15 | 23.24 |
| Amazon | 0 | – | 0 | – |
| Apple | 4 | 0.11 | 9 | 5.11 |
| Meta | 4 | 5.03 | 15 | 20.86 |
| Microsoft | 4 | 2.83 | 15 | 22.69 |
| Nvidia | 4 | 18.36 | 15 | 33.56 |
| Tesla | 3 | 5.07 | 14 | 12.44 |

Matches the MEETING_SUMMARY (2.8→22.7, 4.6→23.2, 5.0→20.9, 5.1→12.4, 0.1→5.1, 18.4→33.6) ✓.

## Latest-quarter share per firm [R]

Important: the Fig 1b "now ~X%" label is **not** the latest quarter. It is the mean share of calls with
`q >= max(q) - 1`, i.e. the **last 5 calendar quarters (2025 Q2 – 2026 Q2)**, over **all unit types**
(`01_timeseries.py:167`).

| Firm | Fig 1b "now ~" (mean of 5 calls, 2025 Q2 – 2026 Q2) | Actual latest call (calendar 2026 Q2) |
|---|---:|---:|
| Nvidia | 33.8 | 29.0 (FY27 Q2) |
| Alphabet | 30.4 | 33.3 |
| Microsoft | 26.0 | 26.6 (FY26 Q4) |
| Meta | 25.4 | 28.1 |
| Amazon | 19.1 (Whisper units) | 20.4 |
| Tesla | 16.4 | 13.8 |
| Apple | 6.2 | 7.8 (FY26 Q3) |

The MEETING_SUMMARY's "Latest quarters: Nvidia ~34%, Alphabet ~30%, …" are the 5-quarter means, so "latest quarters" (plural)
is accurate but easy to misread.

## Handling of non-comparable unit types [F]

| Figure | Treatment |
|---|---|
| Fig 1 (headline) | Non-comparable calls (Whisper, caption_segment) are **dropped** before averaging; Amazon is absent |
| Fig 1b (by company) | All calls in the line; non-comparable calls are drawn as **hollow markers** (`01_timeseries.py:165-166`). The line connects through them. The "now" label includes them |
| Fig 2 (heatmap) | All 133 calls shown. Non-comparable cells get a **star (\*)** and non-bold text (lines 201-203). Row order = post-launch mean share over all unit types (line 189) |
| `ai_share_pre_post.csv` | Comparable only (line 221) |

---

# IV.C Topics (`analysis_calls/04_network.py`)

## Topic patterns (verbatim, `04_network.py:35-55`)

Applied with `str.contains(rx, flags=re.IGNORECASE, regex=True)` to `text_verbatim` of AI units only (`load`, lines 79-85).
**All patterns are case-insensitive**, including `\bAGI\b`, `\bxAI\b` and `AI overviews?`.

```python
# (label, kind, regex). kind: concept = generic AI idea, product = named model/product/chip/stack.
TOPICS = [
    ("generative AI", "concept", r"generative|gen[- ]?AI|genai"),
    ("AI agents", "concept", r"agentic|AI agents?|\bagents\b"),
    ("LLMs / foundation models", "concept", r"large language model|\bLLMs?\b|language models?|foundation models?|frontier models?"),
    ("machine learning", "concept", r"machine learning|deep learning|neural net"),
    ("AGI / superintelligence", "concept", r"\bAGI\b|superintelligence|general intelligence"),
    ("training & inference compute", "concept", r"\binference\b|AI training|training (?:and|&) inference|training clusters?|compute"),
    ("AI chatbots / assistants", "concept", r"chatbots?|AI assistants?|virtual assistants?"),
    ("Copilot", "product", r"copilot"),
    ("Gemini", "product", r"gemini"),
    ("OpenAI / ChatGPT", "product", r"open ?AI|chat ?GPT|\bGPT[- ]?\d"),
    ("Llama / Meta AI", "product", r"llama|meta AI"),
    ("Apple Intelligence / Siri", "product", r"apple intelligence|siri"),
    ("AWS AI stack (Bedrock, Trainium, Nova...)", "product", r"bedrock|trainium|inferentia|sagemaker|\bnova\b|amazon q\b|alexa"),
    ("NVIDIA stack (Blackwell, Hopper, CUDA...)", "product", r"blackwell|hopper|\bH100|\bH200|\bCUDA|nvlink|\bGPUs?\b|\bRubin"),
    ("Tesla autonomy (FSD, Optimus, robotaxi...)", "product", r"\bFSD\b|full self[- ]driving|optimus|robotaxi|\bdojo\b|cybercab|autopilot"),
    ("xAI / Grok", "product", r"\bxAI\b|grok"),
    ("Anthropic / Claude", "product", r"anthropic|\bclaude\b"),
    ("DeepSeek", "product", r"deepseek"),
    ("Google AI Overviews / AI Mode", "product", r"AI overviews?|AI mode\b"),
]
```

7 concepts, 12 products, 19 topics. Caveats from the code: many patterns lack word boundaries (`compute` also matches
"computer"/"computing"; `copilot`, `siri`, `grok`, `hopper`, `llama` match as substrings). "Agents" matches only plural
`\bagents\b` or "AI agent(s)". Topics are matched on AI units only. Some topic terms (e.g. "compute", "GPU", "Optimus") are not AI terms in the filter, so
they are counted only when the same unit also contains an AI term; a unit that mentions them alone is borderline and is never
topic-coded.

## Topic share definition [F]

- **Per quarter (Figs 4a, 4b):** `share(topic, q) = #AI units in q matching topic / #AI units in q × 100`
  (`shares_by_quarter`, lines 199-202). The denominator is **all AI units in that calendar quarter, pooled across all 7 firms
  and all unit types** (Whisper and caption-segment units included; no comparability filter).
- **Per company × period (Fig 3):** `k/n`, where n = the company's AI units in the period and k = those matching the topic.
  A link is drawn if k ≥ 3 and k/n ≥ 0.04 (`fig_company_topic_map`, lines 137, 165-167). Periods: pre = calls for 2021 Q4 –
  2022 Q3; 2023; 2024 – 2026 Q2 (`PERIODS`, lines 65-67). Calendar 2022 Q4 is in **no** Fig 3 panel.
- **Multiple topics:** yes, a unit can match several topics; rows are independent and do not sum to 100. Of 10,382 AI units,
  4,809 match no topic, 4,710 match exactly one and 863 match two or more [R].

## "First quarter with 3+ mentions" rule [F]

`first_appearance` (lines 109-126): for each topic, count matching AI units per calendar quarter, pooled across firms. The
first quarter with ≥3 matches is reported; if none reaches 3, the first quarter with any match is reported.
`companies_that_quarter` lists firm counts in that quarter; `total_mentions` and per-firm columns are totals across all
quarters. The CSV is sorted by the quarter string, with an unstable sort (ties come out in arbitrary order).

## topic_first_appearance.csv (recomputed, identical rows) [R]

| Topic | Kind | First qtr ≥3 | Firms that quarter | Total | GOOGL | AMZN | AAPL | META | MSFT | NVDA | TSLA |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| machine learning | concept | 2021Q4 | meta 7, alphabet 3 | 157 | 49 | 11 | 4 | 46 | 9 | 34 | 4 |
| training & inference compute | concept | 2021Q4 | nvidia 14, tesla 1 | 862 | 132 | 54 | 12 | 167 | 107 | 315 | 75 |
| Tesla autonomy (FSD, Optimus, robotaxi...) | product | 2021Q4 | tesla 29, nvidia 2 | 458 | 0 | 0 | 0 | 0 | 3 | 12 | 443 |
| NVIDIA stack (Blackwell, Hopper, CUDA...) | product | 2021Q4 | nvidia 21 | 951 | 33 | 26 | 0 | 19 | 41 | 799 | 33 |
| AI agents | concept | 2021Q4 | microsoft 3 | 648 | 115 | 69 | 0 | 106 | 216 | 75 | 67 |
| Copilot | product | 2021Q4 | microsoft 3 | 535 | 0 | 0 | 0 | 0 | 535 | 0 | 0 |
| LLMs / foundation models | concept | 2022Q1 | nvidia 8, microsoft 1 | 429 | 52 | 77 | 15 | 76 | 28 | 178 | 3 |
| OpenAI / ChatGPT | product | 2022Q2 | microsoft 3 | 308 | 24 | 6 | 13 | 4 | 222 | 38 | 1 |
| generative AI | concept | 2022Q3 | nvidia 5 | 760 | 111 | 155 | 12 | 133 | 157 | 186 | 6 |
| AI chatbots / assistants | concept | 2023Q1 | alphabet 2, microsoft 2, amazon 1, meta 1 | 76 | 20 | 7 | 8 | 30 | 8 | 1 | 2 |
| Llama / Meta AI | product | 2023Q1 | meta 13 | 308 | 0 | 0 | 0 | 297 | 0 | 11 | 0 |
| Gemini | product | 2023Q2 | alphabet 4 | 327 | 315 | 0 | 2 | 1 | 0 | 7 | 2 |
| AWS AI stack (Bedrock, Trainium, Nova...) | product | 2023Q2 | amazon 32 | 186 | 0 | 183 | 0 | 0 | 0 | 0 | 3 |
| Anthropic / Claude | product | 2023Q3 | amazon 5, alphabet 2 | 115 | 25 | 69 | 1 | 2 | 6 | 10 | 2 |
| Apple Intelligence / Siri | product | 2024Q2 | apple 14 | 144 | 0 | 0 | 143 | 0 | 0 | 0 | 1 |
| Google AI Overviews / AI Mode | product | 2024Q2 | alphabet 17 | 161 | 161 | 0 | 0 | 0 | 0 | 0 | 0 |
| xAI / Grok | product | 2024Q2 | tesla 6 | 62 | 0 | 0 | 0 | 0 | 0 | 0 | 62 |
| AGI / superintelligence | concept | 2024Q2 | tesla 3, nvidia 1 | 79 | 2 | 0 | 0 | 55 | 7 | 7 | 8 |
| DeepSeek | product | 2024Q4 | meta 3, nvidia 1, microsoft 2 | 31 | 2 | 0 | 0 | 8 | 7 | 9 | 5 |


## Key topic numbers [R]

Pre = AI units in calls for calendar 2021 Q4 – 2022 Q3 (n = 713); post = 2022 Q4 – 2026 Q2 (n = 9,669); pooled across all
firms and unit types. **These pre/post topic percentages are not computed by any committed script**; they are recomputed
here with the same definitions as `shares_by_quarter`.

| Claim | Recomputed | Status |
|---|---|---|
| Machine learning 5.9% → 1.2% | 42/713 = **5.89%** → 115/9,669 = **1.19%** | ✓ |
| Generative AI 0.7% → 7.8% | 5/713 = **0.70%** → 755/9,669 = **7.81%** | ✓ |
| Gen AI "peaking near 20% in 2023" | quarterly: 2022Q4 8.6, **2023Q1 17.0, 2023Q2 19.7 (peak)**, 2023Q3 15.3, 2023Q4 18.1; 2024Q1 12.4, Q2 14.5, Q3 6.5, Q4 6.6; ≤4.1 from 2025 | ✓ |
| Gen AI pre-launch mentions | 5, all Nvidia, all in calendar 2022 Q3 (FY23 Q3, Nov 2022 call) | ✓ |
| When agents rise | AI agents share by quarter: ≤2.6% through 2024Q2; **4.7% 2024Q3, 6.0% 2024Q4, 7.8% 2025Q1, 10.1% 2025Q2**, 9.6, 11.1, **16.0% (2026Q1, peak)**, 12.7% 2026Q2 | "from 2025" is fair; the rise starts in 2024 H2 |
| Training & inference compute | 8.3% pre, 8.3% post; quarterly range 5.8–12.4% | "on throughout" ✓ |

Robustness [R]: restricting to comparable units (sentence + caption_sentence), machine learning is 5.76% → 0.94% and
generative AI 0.72% → 6.34%. The direction is unchanged; levels shift because Amazon's Whisper units carry many
generative-AI mentions post-launch.

Fig 3 "top topic" per firm [R] (share of the firm's AI units, links with ≥3 and ≥4% only): pre-launch Nvidia = NVIDIA stack
22.6%, Tesla = autonomy 68.7%, Meta = machine learning 14.6%, Microsoft = OpenAI/ChatGPT 16.7%, Alphabet = machine
learning 4.3% (Amazon n = 5, Apple n = 2, no links). 2024–2026 Q2: Microsoft Copilot 29.7%, Alphabet Gemini 22.2%,
Meta Llama/Meta AI 21.3%, Amazon AWS AI stack 17.9%, Apple Apple Intelligence/Siri 48.3%, Nvidia NVIDIA stack 35.1%,
Tesla autonomy 36.5%. These match the MEETING_SUMMARY (23%, 69%, 15%, 17% rounded).

---

# IV.D Tone (`02_finbert_tone.py`, `02b_baseline_tone.py`, `05_tone_figures.py`)

## Model and scoring [F]

| Item | Value | Source |
|---|---|---|
| Model ID | `ProsusAI/finbert` (off-the-shelf, not fine-tuned) | `02_finbert_tone.py:20` |
| Revision / hash | **Not pinned in code** (`from_pretrained(MODEL)` with no `revision=`). Original run: **[ND]**. Local HF cache on this machine: `refs/main` → `4556d13015211d73dccd3fdd39d39232506f3e43` (a second snapshot, `7db323f79b751944bcfa66298ec06977e4518306`, is also cached). The scratch re-run used main and reproduced the committed probabilities to ≤5e-6, which is consistent with the same weights | — |
| Tokenizer | `AutoTokenizer.from_pretrained("ProsusAI/finbert")` (BertTokenizer), `padding=True, truncation=True, max_length=160` | `02_finbert_tone.py:23,29` |
| Truncation in practice [R] | Inputs over 160 tokens: 2 of 10,382 call AI units; 23 of 682 10-K AI sentences; 16 of 5,000 call baseline; 1 of 2,500 10-K baseline | — |
| Batch size | 64, with batches built from length-sorted inputs (results re-ordered back) | `02_finbert_tone.py:23-37` |
| Device | `mps` if available, else `cpu`. CUDA is never used | `common.py:get_device` (43-45) |
| Device of the committed run | **[ND]**. Not logged. The extended build was made with Python 3.14.6 (`build_validation.json`), but the tone run's environment is not recorded |
| Probabilities | `softmax(logits)` over the model's three labels → `p_positive`, `p_negative`, `p_neutral` (names from `model.config.id2label`) | lines 24, 31 |
| **Tone score** | `tone = p_positive − p_negative` ∈ [−1, 1] | `05_tone_figures.py:203-204` |
| Inputs | Call: `text_verbatim` of every AI unit (10,382 rows → `ec_sentence_tone.csv`, 10,382 rows ✓). 10-K: see III.7 (682 rows ✓) | — |

## Non-AI baselines [F + R]

**Calls** (`02b_baseline_tone.py:call_sentences`, lines 99-110; `main`, lines 124-134):
- **Sampling frame:** every raw transcript in `CALLS_DIR` (for the extended run, the scratch copy holding all 133 calls),
  split with the **teammate splitter** (`earnings_calls/filter_ai_passages.py:process`), **not** the canonical
  parser/Punkt.
- Exclusions: units with `common.is_ai(text)` true (the narrower 10-K regex, **not** the canonical filter); length
  < 40 or > 600 chars; section not in {prepared, qa}. A call whose Q&A boundary the teammate splitter cannot find has all
  sentences labelled `unknown` and is excluded entirely.
- **No unit-type or year restriction:** caption, Whisper and all years 2021–2026 are included.
- Frame size [R]: 47,891 sentences (prepared 21,053, Q&A 26,838).
- Draw: **2,500 per section**, `groupby("section")` then `g.sample(2500, random_state=3)` (`SEED = 3`, line 96).
  `random.seed(3)` is also set but unused by pandas sampling.
- Realised composition [R]: prepared = official 1,270, Whisper 570, Fool 349, caption 287, unknown 24; Q&A = official
  1,001, Fool 659, Whisper 496, caption 322, unknown 22. Years 2021–2026; Amazon is the largest firm (prepared 570, Q&A 496).

**10-K** (`02b_baseline_tone.py:tenk_sentences`, lines 113-121): all Mag 7 Item 1A rows, same regex splitter as the AI
sentences, not `is_ai`, ≤600 chars, de-duplicated. Frame 27,076; sample 2,500 with `random_state=3`; **all filing years
2006–2026** (909 of 2,500 from 2023+).

## CIs in the tone figure [F]

`ci(x) = 1.96 × sd(x, ddof=1) / sqrt(n)`, a normal-approximation 95% CI of the mean that treats sentences as independent
(`05_tone_figures.py:170-172`). Drawn only on the filled (AI) dots, **not** on the baseline (hollow) dots. No clustering by
call or firm.

## Tone figure numbers (recomputed) [R]

Left panel. AI dots: comparable units only (`unit_type ∈ {sentence, caption_sentence}`), calls with **calendar_year ≥ 2023**,
10-K with **filing year ≥ 2023** (`05_tone_figures.py:205,210-212`). Baselines: means of the full 2,500-row samples.

| Source | AI mean ± CI half-width (n) | Non-AI baseline (n) | "AI vs other" gap |
|---|---|---|---|
| Calls: prepared remarks | **+0.464** ± 0.012 (4,189) | **+0.348** (2,500) | **+0.116** |
| Calls: Q&A | **+0.200** ± 0.009 (4,072) | **+0.166** (2,500) | **+0.033** |
| 10-K Item 1A | **−0.170** ± 0.043 (604) | **−0.259** (2,500) | **+0.089** |

Matches the quoted +0.46/+0.35, +0.20/+0.17, −0.17/−0.26 and gaps +0.12/+0.03/+0.09 ✓.

**Comparability caveat (affects the "AI-specific effect" interpretation).** The AI dots and their baselines are not drawn
from the same frame. AI dots are 2023+ and sentence-like units; baselines are all years, include Whisper/caption units,
use a different splitter, and exclude AI by a different regex. Gaps recomputed with matched baselines [R]:

| Baseline variant (calls) | Prepared baseline | Gap | Q&A baseline | Gap |
|---|---:|---:|---:|---:|
| As in figure (all) | 0.348 | +0.116 | 0.166 | +0.033 |
| Excluding Whisper/caption | 0.375 | +0.089 | 0.171 | +0.028 |
| Year ≥ 2023 only | 0.361 | +0.103 | 0.169 | +0.030 |
| Both restrictions | 0.396 | +0.068 | 0.178 | +0.022 |

The 10-K baseline also spans 2006–2026 while the AI dots are 2023+. A year-matched 10-K baseline was not computed here
(only 909 rows of the sample are 2023+).

Right panel (per company, 2023+, dot drawn if n ≥ 5) [R]:

| Firm | Prepared (n) | Q&A (n) | 10-K Item 1A (n) |
|---|---|---|---|
| Alphabet | +0.486 ± 0.022 (1,041) | +0.293 ± 0.025 (631) | −0.009 ± 0.102 (98) |
| Amazon | – (0; Whisper excluded) | – (0) | −0.040 ± 0.144 (34) |
| Apple | +0.437 ± 0.051 (99) | +0.200 ± 0.054 (129) | −0.170 ± 0.286 (10) |
| Meta | +0.500 ± 0.027 (718) | +0.265 ± 0.023 (715) | −0.085 ± 0.091 (108) |
| Microsoft | +0.437 ± 0.027 (1,050) | +0.151 ± 0.024 (597) | −0.149 ± 0.084 (172) |
| Nvidia | +0.478 ± 0.024 (1,012) | +0.177 ± 0.015 (1,381) | −0.348 ± 0.079 (167) |
| Tesla | +0.349 ± 0.046 (269) | +0.127 ± 0.021 (619) | −0.395 ± 0.294 (15) |

Firms are ordered in the figure by prepared-remarks tone, descending; Amazon is placed last (no call dots).

## tone_summary.csv (2021–22 vs 2023–26) [R]

`05_tone_figures.py:267-277`. Calls: comparable units split by `calendar_year ≤ 2022` vs `≥ 2023`. **Calendar 2022 Q4
(post-launch) calls fall in "2021–2022".** 10-K: split by filing year, and **"2021–2022" actually contains filings from
2017–2022** (AI sentences start 2017).

| Source | Period | n | Mean tone | Share p_neg > 0.5 | Share p_pos > 0.5 |
|---|---|---:|---:|---:|---:|
| calls_prepared | 2021–2022 | 433 | 0.430 | 0.014 | 0.418 |
| calls_prepared | 2023–2026 | 4,189 | 0.464 | 0.022 | 0.486 |
| calls_qa | 2021–2022 | 586 | 0.215 | 0.019 | 0.189 |
| calls_qa | 2023–2026 | 4,072 | 0.200 | 0.014 | 0.174 |
| tenk_1a | "2021–2022" (= filed 2017–2022) | 78 | −0.293 | 0.577 | 0.154 |
| tenk_1a | 2023–2026 | 604 | −0.170 | 0.366 | 0.141 |
| calls_prepared non-AI baseline | all | 2,500 | 0.348 | – | – |
| calls_qa non-AI baseline | all | 2,500 | 0.166 | – | – |
| tenk_1a non-AI baseline | all | 2,500 | −0.259 | – | – |

Row-count reconciliation: 433 + 4,189 + 586 + 4,072 = **9,280** = comparable AI units. The other 1,102 AI units (979
Whisper + 123 caption_segment) are scored in `ec_sentence_tone.csv` (10,382 rows) but excluded from the figure and the summary.

---

# V. Limitations (facts the writer can cite)

1. **Unvalidated filter.** No measured precision or recall; the 150-row review sheet is blank and excludes the 17 extras (IV.A.4–5).
2. **Mixed sources and units.** 8 source types; 4 unit types. 27 calls (19 Whisper + 8 caption-segment) are non-comparable.
   All 4 Apple and Nvidia pre-launch calls and 3 of 4 Tesla pre-launch calls are Motley Fool text, while their post-launch
   calls mix Fool, captions and FactSet. Source changes coincide with the treatment window for these firms (III.1b).
3. **Pre-launch evidence leans on the extras:** 12 of the 23 pre-launch calls in the headline are from the 17 added
   calls (IV.B). 11 of these are third-party text, one is an archived official PDF.
4. **Small pre period:** 4 calendar quarters (Tesla 3 comparable pre calls).
5. **No speaker labels** for 1,876 AI units (Whisper/captions); 802 AI units unverified (733 Meta label-loss risk, 69 meta
   2022 Q2/Q3 misplacement); 53 unresolved (44 bare names, 9 "Unknown speaker") (A4).
6. **Machine-transcript errors are preserved** (names, numbers, casing); lowercase "ai" is treated as AI there (17 units).
7. **Filter scope:** infrastructure/robotics sentences without an AI term are borderline (2,722 units) and are outside
   the numerator, which understates Nvidia and Tesla AI talk.
8. **Calendar mapping:** Nvidia is ~1 month behind its assigned calendar quarter.
9. **Tone:** generic financial-news sentiment model; baselines not frame-matched (IV.D); normal-approximation CIs ignore
   clustering; 10-K coverage uneven (Alphabet from FY2023, Meta from FY2024; 36 of 72 filings have no AI sentences).
10. **10-K and call AI identification differ** (`common.is_ai` vs the canonical filter), so the tone comparison across genres
    also compares two different AI definitions.
11. **Topic dictionary** is hand-written, case-insensitive, partly substring-based; topic shares pool non-comparable units.
12. **Attention, not adoption:** shares measure talk, not adoption or spending (scope §8); there is no causal identification
    of ChatGPT versus other late-2022/2023 events.

---

# Appendix A1: Variable definitions (draft table)

| Variable | Definition (as in code) | Computed in |
|---|---|---|
| Unit | One row of the parsed transcript after noise removal: a Punkt sentence (`sentence`), a Punkt sentence of punctuated YouTube captions (`caption_sentence`), a Punkt-split segment group of Whisper text (`whisper_unit`), or one ~30 s unpunctuated caption segment (`caption_segment`) | `build_earnings_call_canonical.py:unit_type`, `split_units`; `filter_earnings_calls.py:split_sentences`, `parse_captions` |
| unit_type (call level) | The set of unit types in the call; `units_comparable_to_sentences` = 1 iff all units are `sentence` or all are `caption_sentence` | `build_earnings_call_canonical.py:501-502` |
| AI unit | Unit with ≥1 core or weak term (`classify(...).kind == "ai"`) | `filter_earnings_calls.py:classify` |
| AI share (call) | `ai_units / total_units × 100` | `01_timeseries.py:94` |
| AI share (prepared) | `ai_units_prepared / total_units_prepared × 100` (available in data; not plotted) | call-units columns |
| AI share (Q&A) | `ai_units_qa / total_units_qa × 100` (available; not plotted) | call-units columns |
| Borderline share | Not computed by any script. Definable as `(borderline_automation + borderline_infrastructure) / total_units`; borderline units are in the denominator only | call-units columns |
| Uncertain (weak-only) flag | AI unit with weak hit(s) and no core hit | `classify`, line 214 |
| Topic share (quarter) | `#AI units in quarter matching topic regex / #AI units in quarter × 100`, all firms and unit types pooled; topics not exclusive | `04_network.py:shares_by_quarter` |
| Topic share (firm × period) | `#firm AI units in period matching topic / #firm AI units in period`; plotted if ≥3 units and ≥4% | `04_network.py:fig_company_topic_map` |
| Tone | `P(positive) − P(negative)` from `ProsusAI/finbert` softmax, input truncated at 160 tokens | `02_finbert_tone.py:score`; `05_tone_figures.py:203` |
| AI-specific tone ("AI vs other") | Mean tone of AI units (comparable, year ≥ 2023) − mean tone of the 2,500-sentence non-AI baseline sample for the same source (all years/units) | `05_tone_figures.py:217-225` |
| Pre/post indicator | `post = 1` if (calendar_year, calendar_quarter) ≥ (2022, 4). **Tone figure instead uses calendar_year ≥ 2023** (10-K: filing year ≥ 2023) | `common.py:14`; `01_timeseries.py:106,222`; `05_tone_figures.py:210-212` |
| Calendar quarter | Calendar quarter holding most of the fiscal quarter's months; identity for calendar-FY firms | `earnings_call_scope.py:calendar_quarter` |
| Section | `prepared_remarks` / `qa` per unit, from the Q&A start detection | `build_earnings_call_canonical.py:SECTION_CODE`; parsers |
| Source type | Metadata-string classification (III.3) | `earnings_call_scope.py:source_type` |

# Appendix A2: Sample construction summary

- 133 calls → 61,961 units → 10,382 AI units (7,594 core, 2,788 weak-only) + 2,722 borderline units.
- Comparable subset: 106 calls (92 sentence + 14 caption_sentence), 53,115 units, 9,280 AI units.
- Headline panel: 6 firms, 106 comparable calls (23 pre / 83 post).
- Tone: 9,280 comparable AI units scored in the summary; the figure uses 8,261 (2023+). 10-K: 682 AI sentences (604 in 2023+).

# Appendix A3: Transcript cleaning and parsing

## A3.1 Cleaning/removal rules by format (code wins) [F]

Common to all: `split_metadata` (`filter_earnings_calls.py:262-267`) drops everything above the first `---` line (the
metadata block). The parser format is chosen by company, then by content (`detect_format`, lines 814-828): meta → `meta`;
microsoft → `msft`; alphabet → `alphabet`; else "callstreet" in the first 400 body lines → `factset`; else "Motley Fool"
in the metadata or "Prepared Remarks:" in the body → `fool`; else `[mm:ss]` lines in the first 20 → `captions`.

| Format (source types) | Function | Removal and cleaning rules |
|---|---|---|
| `meta` (Meta official PDF) | `parse_meta` (372-436) | Paragraph split on blank lines; a new paragraph starts at an inline `Name:` line after a finished sentence. Paragraphs that are only 1–3 digits are page numbers and are removed (`PAGE_NUMBER`). After a page break, a paragraph whose predecessor lacks final punctuation is re-joined (no space if hyphen-wrapped). Paragraphs before the first speaker (title block) are dropped. `Name, Title` header lines (≤10 words, title keyword, no final punctuation) set the speaker and are not text |
| `msft` (Microsoft HTML/DOCX) | `parse_msft` (449-475) | Lines before the first `NAME:` label (title/date block) dropped; everything after a line `END` dropped; blank lines dropped |
| `factset` (Nvidia FactSet CallStreet) | `parse_factset` (490-533) | Cover page and participant list dropped (nothing kept before `MANAGEMENT DISCUSSION SECTION`); stops at `Disclaimer`; drops lines matching `FACTSET_NOISE` (company header, "Qn YYYY Earnings Call", "Corrected Transcript", dd-Mon-yyyy date, `1-877-FACTSET`, bare page numbers, copyright, "Total Pages:"); dotted rules mark speaker blocks (name line, then title line, trailing ` Q`/` A` stripped) |
| `fool` (Motley Fool) | `parse_fool` (545-609) | Nothing before `Prepared Remarks:` is kept; everything from `Duration:`, `Call participants:` or `More XXX analysis` onward is dropped (`FOOL_STOP`); `Name -- Title` lines are labels, not text; "Unknown speaker -- Analyst" prefix stripped |
| `alphabet` (Alphabet official PDF) | `parse_alphabet` (667-717) | Detects layout. One word per line with blank lines → page numbers found by `find_inline_pages` (sequence 1, 2, 3… with scoring) and removed. Otherwise digit-only lines followed by a blank line are removed. Text before the first speaker label is the title block and is dropped |
| `captions` (Whisper, YouTube) | `parse_captions` (740-807) | Only `[mm:ss]` segment lines are kept; HTML entities decoded (`html.unescape`); `CAPTION_NOISE` removed (`foreign` before `[Music]`, `[Music]`/`[Applause]`/`[Laughter]`/`[clears throat]`/`[__]` in either case, `>>`, `&gt;&gt;`); whitespace collapsed. Pre-call trimming: text starts at the first `CALL_START` match (welcome to Apple/Tesla/Amazon/NVIDIA, "my name is Suhasini/Travis", "conference is now being recorded", "speaking first today is Apple", "be followed by CFO", "thank you for standing by"); everything earlier is dropped. Post-call trimming by `CALL_END` for Tesla, Apple and Amazon (last match kept, rest dropped). Nvidia captions have no end trim |

Exact regexes for caption trimming (`filter_earnings_calls.py:724-737`):

```python
SEGMENT = re.compile(r"^\s*\[(\d+:\d{2}(?::\d{2})?)\]\s?(.*)$")
CAPTION_NOISE = re.compile(
    r"\bforeign\s*(?=\[Music\])|\[(?:Music|music|Applause|applause|Laughter|laughter|"
    r"clears throat|__)\]|>>|&gt;&gt;")
CALL_START = _rx(
    r"(?:good (?:afternoon|day|evening)[^.]{0,30}?)?welcome to (?:the )?(?:apple|tesla|amazon|nvidia)|"
    r"my name is (?:suhasini|travis)|conference is now being recorded|"
    r"speaking first today is apple|be followed by CFO|thank you for standing by")
CALL_END = {
    "tesla": _rx(r"(?:that's|that is) all the time we have|look forward to talking to you next quarter|"
                 r"see you (?:again )?(?:next quarter|in three months)|thank you very much and goodbye"),
    "apple": _rx(r"this does conclude today's conference"),
    "amazon": _rx(r"(?:this|that) concludes (?:today's|the|our) (?:call|conference|teleconference)"),
}
```

Recorded effects in the extended build [R, `call_parse_flags`]: pre-call segments dropped: Apple FY24 Q3 121, FY23 Q4 28,
FY23 Q2 14; Tesla 2022 Q1 8, 2023 Q1 8, 2025 Q1 9, 2025 Q2 6, 2025 Q3 12, 2025 Q4 5. "Call opening not detected" for Amazon
2022 Q1, 2022 Q3 (both extras) and 2023 Q2. Units outside 400–900 for 8 caption-segment calls (107–126 units) and 7 Amazon
calls (320–392).

Doc-vs-code on cleaning: `FILTER_METHOD.md` §3 says Amazon is trimmed after "this concludes today's call", but the code
accepts (this|that) concludes (today's|the|our) (call|conference|teleconference). FILTER_METHOD also does not mention the
Fool "Unknown speaker" handling or Nvidia caption files having no end trim. Otherwise it matches the code.

## A3.2 Sentence splitting [F + R]

- Library: **nltk `PunktTokenizer("english")`** (`filter_earnings_calls.py:47,75`), which loads the **`punkt_tab`** resource.
  Version: **nltk 3.10.0** is installed here and recorded in both `build_validation.json` files [R]. The README's claim
  that "nltk 3.10.0 with punkt_tab reproduces the committed CSVs" was confirmed for the extended build (byte-identical apart from
  the Python version string). **[ND]** the `punkt_tab` data package version (not recorded anywhere).
- Custom abbreviations added to `_punkt._params.abbrev_types` (`filter_earnings_calls.py:68-73`):

```python
ABBREVIATIONS = {
    "u.s", "u.k", "inc", "vs", "mr", "mrs", "ms", "dr", "no", "e.g", "i.e",
    "approx", "a.i", "corp", "co", "ltd", "jr", "sr", "st", "dept", "fig",
    "est", "cf", "al", "p.m", "a.m", "jan", "feb", "mar", "apr", "jun", "jul",
    "aug", "sep", "sept", "oct", "nov", "dec",
}
```

  (`FILTER_METHOD.md` omits `dept`, `fig`, `est`, `cf`, `al` from its prose list; the code wins.)
- Splitting happens **within a speaker turn** after `join_lines` re-flow (`process_file`, lines 910-912; build
  `split_units`, 290-301).
- **Caption/Whisper differences** (`parse_captions`, 778-803). Punctuation density = count of `.?!` per word.
  - **< 1 per 100 words → `caption_segment`:** unit mode `lines`, each caption segment is one unit, and no Punkt is applied.
  - **Whisper (metadata contains "whisper") → `whisper_unit`:** segments are grouped; a new group starts when the
    previous segment has no final punctuation and the next starts with a capital letter. Groups are re-flowed and
    Punkt-split, and each resulting piece becomes one line (unit mode `lines`).
  - **Otherwise (punctuated YouTube) → `caption_sentence`:** segments are joined and Punkt-split normally.
- Teammate splitter (used **only** for the call tone baseline and the filter comparison) is different: a regex split
  `(?<=[\.\?\!])\s+(?=[A-Z⟦\"“(])|\n{2,}`, with one line per unit for Whisper (`filter_ai_passages.py:96-98`).

## A3.3 Verbatim rule [F]

Allowed differences between `text_verbatim` and the raw file (code: parsers + `join_lines`; check:
`verbatim_found`, `filter_earnings_calls.py:1012-1033`):
1. **Line re-flow:** wrapped lines joined with one space; a line ending in letter + single hyphen (`-` or `‐`, not `--`) is
   joined with no space (`join_lines`, 246-259; also the Meta page-break join).
2. **Removed noise between words:** page numbers, FactSet header lines, timestamps, caption tags, `>>`, speaker labels
   (including the canonical `NAME, Firm:` label removal, A4).
3. **HTML entity decoding** in caption/Whisper files (`html.unescape`, line 747). The verbatim check unescapes the raw body
   for all formats.
4. **Whitespace collapse** (captions) and strip.
5. **Nothing else:** no spelling, casing or transcription corrections. Encoding damage is kept (`FILTER_METHOD.md` §3).

Verification [R]: `build_validation.json` (extended) reports `verbatim_check`: 10,382 AI rows checked, **0 failures**.
The check is `verbatim_found` against the HTML-unescaped body: whitespace- and caption-tag-insensitive containment first,
then a noise-tolerant word-sequence match. The stricter two-tier check over all units (incl. non-AI) exists only in the
116-call Gate 4 run.

## A3.4 Q&A start detection [F + R]

| `section_method` | Rule | Formats | Calls (extended) |
|---|---|---|---:|
| `explicit_section_header` | FactSet `QUESTION AND ANSWER SECTION`; Fool line `Questions & Answers:` / `Questions and Answers:` | factset; fool when the header exists | **24** (Nvidia 18 = 12 Fool + 6 FactSet; Apple 6 Fool) |
| `first_operator_turn_after_management` | The first `Operator` turn after any non-operator has spoken switches to Q&A | meta, alphabet | **38** (Meta 19, Alphabet 19) |
| `transition_phrase_heuristic` | Regex `QA_MARKERS[fmt]` (below); everything from the sentence containing the first match onward is Q&A. In caption-segment mode the cut is at the match itself, which can split a segment | msft; fool without header (all 11 Tesla Fool calls); captions (Whisper, YouTube) | **71** (Microsoft 19, Amazon 19, Apple 7 caption_sentence + 6 caption_segment, Tesla 19, Nvidia 1) |
| `not_detected_all_prepared` | No marker found → everything is prepared remarks | — | **0** |

[R] 24 + 38 + 71 = 133. Tesla's 11 Fool files have no `Questions & Answers:` header, so they fall to the transition-phrase rule.

`section_method` is assigned by format in `build_earnings_call_canonical.py:section_method` (254-264), not by observing
which branch fired. For `fool` the code re-tests for the header regex. The marker regexes are in `filter_earnings_calls.py:313-327`:

```python
QA_MARKERS = {
    "msft": _rx(r"(?:let['’]s|we['’]ll|we will|now)\s+(?:now\s+)?(?:go|move|turn|open)\w*\s+"
                r"(?:over\s+|on\s+)?(?:to\s+)?(?:the\s+)?Q&A"),
    "fool": _rx(r"(?:go|move|head|moving|going|start|begin)\w*\s+(?:on\s+|over\s+|through\s+|with\s+)?"
                r"(?:to\s+)?(?:the\s+)?(?:investor|say\.com|analyst|retail)\s+(?:questions|Q&A)|"
                r"(?:let['’]s|we['’]ll|we will)\s+(?:now\s+)?(?:go|move|open)\w*\s+(?:on\s+|over\s+)?"
                r"(?:to\s+)?(?:the\s+)?(?:Q&A|questions)"),
    "apple": _rx(r"may we (?:have|take|get) the (?:the |first )?question|"
                 r"(?:our|the) (?:first|next) question (?:is|comes) from"),
    "nvidia": _rx(r"first question|question comes from|question is from"),
    "tesla": _rx(r"(?:go|move|head|moving|going|start|begin)\w*\s+(?:on\s+|over\s+|through\s+|with\s+)?"
                 r"(?:to\s+)?(?:the\s+)?(?:investor|say\.com|analyst|retail)\s+(?:questions|Q&A)|"
                 r"covers? (?:uh )?the say\.com questions|questions on say\.com relate"),
    "amazon": _rx(r"first question|question comes from|question is from"),
}
```

Which marker applies: msft → `msft`; fool without header → `fool` (Tesla Fool files use `fool`, not `tesla`); captions →
the company's key (apple/nvidia/tesla/amazon), falling back to `fool` (line 804). Tesla Q&A includes retail/say.com questions
read by IR.

## A3.5 Speaker identification [F + R]

**Where labels come from (same transcript only):**

| Format | Label source |
|---|---|
| meta | `Name, Title` header lines; inline `Name:`/`Operator:`; operator introductions ("from the line of X with Firm") give analyst firms (`OPERATOR_INTRO`, 306-309) |
| msft | `NAME:` labels (ALL CAPS, title-cased for display); titles from the IR opening's "Name, title" list (`INTRO_TITLE`); analyst firms from operator intros |
| factset | name line + title line after a dotted rule |
| fool | `Name -- Title` lines and the closing `Call participants:` roster; bare-name lines that appear in the roster |
| alphabet | inline `Name, Title:` (title keyword required) or `Name (Firm):` |
| captions (Whisper/YouTube) | **none**: every unit is `Speaker not labeled` |

Bare names are expanded to `Name, descriptor` via `SpeakerBook` (`names_match`: same last name and one first name a prefix of
the other).

**Canonical correction rules** (`build_earnings_call_canonical.py:correct_turns`, 196-239). These run only in the build, on
top of the filter's own parse:
1. `msft_name_comma_firm_label` / `alphabet_name_comma_firm_label`: a `NAME, Firm:` label left inside a turn starts a new
   turn for that speaker, and the label text is removed (regexes `LABEL_FIX`, 196-202).
2. `same_transcript_name_propagation`: a bare name gets the unique `Name, descriptor` that the same transcript gives
   elsewhere (only if exactly one candidate).

Statuses: `speaker_status` (170-188). Two Meta calls (`meta_2022_Q2`, `meta_2022_Q3`) are quarantined as
`unverified_raw_label_misplacement` (`RAW_LABEL_MISPLACEMENT`, 164-167). Original-corpus Meta Q&A (non-operator, `already_present`)
is `unverified_meta_label_loss_risk`.

**Counts, extended build [R]:**

| Measure | Count |
|---|---:|
| Units (all kinds) with speaker changed by correction | 1,484 (msft 973, alphabet 342, propagation 169) |
| …of which label text removed from the unit | 230 |
| **AI units corrected** (`resolved_corrected`) | **180** (msft 171, alphabet 8, propagation 1) |
| AI units resolved (incl. corrected + operator) | 7,468 + 180 + 3 = 7,651 |
| **Unresolved AI units** | **53** = 44 bare names (Tesla: Elon Musk 21, Martin Viecha 16; Meta: David Wehner 3, Brian Nowak, Eric Sheridan, Javier Olivan, Kenneth Gawrelski 1 each) + 9 "Unknown speaker" in source (Tesla 2024 Q3 8, 2024 Q2 1) |
| **Unverified AI units** | **802** = 733 Meta label-loss risk + 69 Meta 2022 Q2/Q3 misplacement |
| **Unlabelled AI units** (caption/Whisper) | **1,876** (Whisper 979, caption_sentence 774, caption_segment 123) |
| Sum check | 7,651 + 53 + 802 + 1,876 = 10,382 ✓ |

Note: the call-units column `ai_units_speaker_unresolved` sums to **44**. It counts only `unresolved_bare_name`, not the 9
"Unknown speaker" rows; Gate 4's "unresolved" includes both.

# Appendix A4: Data dictionary pointers

Field definitions for the canonical files: `earnings_calls_canonical/data_dictionary.md` (written for the 116 build; the
extended build has the same schema, `SENTENCE_FIELDS`/`CALL_FIELDS` in `build_earnings_call_canonical.py:69-104`). Unit and
sentence IDs: `<company>_<period_label>_u<4-digit order>_<first 10 hex of sha256(text)>` (`unit_id`, line 283).

# Appendix A5: Filter-comparison and validation provenance

See IV.A.3–IV.A.5. Gate 4 artefacts (`gate4_validation.json`, `filter_comparison.csv`, `speaker_attribution_audit.csv`,
`manual_review_sample.csv`) all describe the **116-call** build. No Gate 4 run exists for the extended build.

---

# Figures map

All committed figures in `figures_calls_extended/` were last changed in commit **`c80f6a6`** ("updated graphs",
2026-10-08 19:34 −0400, Tanush Appapogu). fig6 is excluded (out of scope).

| File | Script / function | Input data | What it shows |
|---|---|---|---|
| `fig1_headline_ai_talk.png` | `01_timeseries.py:fig_headline` | `earnings_call_call_units.csv` (extended) | Per-call AI share for the 6 balanced firms (comparable calls only) plus the quarterly cross-firm mean (black line); annotations "6%" / "21%" = mean of quarterly means pre/post |
| `fig1b_ai_talk_by_company.png` | `01_timeseries.py:fig_by_company` | same | Small multiples, one panel per firm (all 133 calls); hollow dots = non-comparable units; "now ~X%" = mean of the last 5 calendar quarters |
| `fig2_ai_share_heatmap.png` | `01_timeseries.py:fig_heatmap` | same | Firm × calendar quarter heatmap of AI share (all calls; * = non-comparable); colour scale 0–45 |
| `fig3_company_topic_map.png` | `04_network.py:fig_company_topic_map` | `earnings_call_sentences.csv` (extended) | Bipartite firm → topic links in 3 periods (pre-launch, 2023, 2024–2026 Q2); link if ≥3 units and ≥4% of the firm's AI units; width ∝ share |
| `fig4a_topic_storyline.png` | `04_network.py:fig_storyline` | same | Quarterly share of AI units mentioning: machine learning, generative AI, LLMs/foundation models, AI agents, training & inference compute |
| `fig4b_topic_heatmap.png` | `04_network.py:fig_topic_heatmap` (+ writes `topic_first_appearance.csv`) | same | Topic × quarter heatmap of topic share (cells <1% blank); rows ordered by first ≥3-mention quarter |
| `fig5_tone_calls_vs_10k.png` | `05_tone_figures.py:fig_tone` (+ writes `tone_summary.csv`) | `ec_sentence_tone.csv`, `tenk_item1a_ai_tone.csv`, `ec_nonai_baseline_tone.csv`, `tenk_item1a_nonai_baseline_tone.csv` (from `02_finbert_tone.py`, `02b_baseline_tone.py`) + `earnings_call_sentences.csv` | Left: mean tone of AI units vs non-AI baseline per source (2023+); right: per-firm AI tone by source |

**Currency check (Task 5.2) [R].** Every script was re-run into a scratch directory against the extended data:
- **Underlying numbers are identical** (pre/post CSV identical; topic table same rows; tone CSVs within 5e-6; tone_summary
  agrees to ≥6 decimals).
- **PNG comparison:** same pixel dimensions for all 7. Pixel differences of 5–14% are antialiasing/font rasterisation
  differences between machines (this machine: matplotlib 3.10.8 on Windows). `fig1` was inspected side by side and is
  visually identical in data, labels and layout. The others were checked by dimensions plus identical inputs, not by eye.
- **Conclusion:** the committed `figures_calls_extended/` figures are current against the extended data.

**Proposed numbering:**

| New # | Content | Current file |
|---|---|---|
| Figure 1 | Workflow diagram (raw transcripts → parsing/cleaning → unit split → AI filter → measures) | **does not exist yet**; must be drawn |
| Figure 2 | Before/after headline | `fig1_headline_ai_talk.png` |
| Figure 3 | AI share by company | `fig1b_ai_talk_by_company.png` |
| Figure 4 | Company × quarter heatmap | `fig2_ai_share_heatmap.png` |
| Figure 5 | Topic storyline | `fig4a_topic_storyline.png` |
| Figure 6 | Topic heatmap | `fig4b_topic_heatmap.png` |
| Figure 7 | Company–topic map | `fig3_company_topic_map.png` |
| Figure 8 | Tone | `fig5_tone_calls_vs_10k.png` |

Several figures carry in-image titles and captions with interpretive claims, e.g. "Earnings calls turned sharply toward AI
right after ChatGPT" and "most of that gap is just genre". The writer should decide whether paper versions keep them.

---

# Reproducibility

## Environment

| Item | Committed extended build | This verification run | Status |
|---|---|---|---|
| Python | 3.14.6 (canonical build, from `build_validation.json`) | 3.13.14 | [F]/[R] |
| nltk | 3.10.0 (+ `punkt_tab`) | 3.10.0 | [F]/[R] |
| pandas | [ND] | 3.0.3 | |
| numpy | [ND] | 2.4.3 | |
| matplotlib | [ND] | 3.10.8 | |
| networkx | [ND] | 3.6.1 | |
| torch | [ND] | 2.6.0+cpu | |
| transformers | [ND] | 5.14.1 | |
| FinBERT revision | [ND] (not pinned) | `4556d13015211d73dccd3fdd39d39232506f3e43` (cache `main`) | |
| Device (tone) | [ND] (`mps` if available, else `cpu`) | cpu | |

`requirements.txt` status: lower bounds only, unpinned (`pandas>=2.0`, `nltk>=3.8`, `torch>=2.0`, `transformers>=4.40`, …).
It does **not** pin nltk 3.10.0 or name the `punkt_tab` data. It omits `Pillow` (pulled in by matplotlib anyway) and
includes unused legacy packages (`anthropic`, `statsmodels`, `scikit-learn`, `accelerate`). Recommendation: add a
lock file (`pip freeze`) from the machine that produced the committed outputs.

## Seeds

| Seed | Use | Where |
|---|---|---|
| 20260930 | Legacy 40-sentence precision sample (`--validate`) | `filter_earnings_calls.py:60` |
| 20260931 | Legacy 50-unit verbatim sample (SEED + 1) | `filter_earnings_calls.py:1115` |
| 20261006 | Gate 4 manual review sample (150 rows) | `gate4_validate.py:44` |
| 3 | Non-AI baseline samples (calls 2×2,500; 10-K 2,500), `pandas.sample(random_state=3)` | `02b_baseline_tone.py:96` |
| none | Canonical build, AI share, topics and FinBERT scoring are deterministic (no RNG) | — |
| [ND] | Headline bootstrap CIs | no code in repo |

## Command sequence (extended build, from raw transcripts)

Verified on 2026-10-10 (Windows, Git Bash). Steps 1–4 reproduced the committed outputs as described above.

```bash
# 0. Environment
pip install -r requirements.txt "nltk==3.10.0"
python -c "import nltk; nltk.download('punkt_tab')"        # if punkt_tab is not already on disk

# 1. Scratch copy with the extras merged (the "<scratch copy>" in MEETING_SUMMARY)
SCR=/path/to/scratch/repo
mkdir -p "$SCR"
cp -r earnings_call_scope.py filter_earnings_calls.py build_earnings_call_canonical.py \
      earnings_calls earnings_calls_ai_only analysis_calls export "$SCR"/
for c in alphabet amazon apple nvidia tesla; do cp earnings_calls_pre2022_extra/$c/*.md "$SCR/earnings_calls/$c/"; done
# On Windows with core.autocrlf=true, convert the .py files to LF first if you want the extraction_version hash to match:
#   for f in "$SCR"/*.py; do tr -d '\r' < "$f" > "$f.tmp" && mv "$f.tmp" "$f"; done
cd "$SCR" && python earnings_call_scope.py --check          # expect: expected 133 ... present 133

# 2. Canonical extended dataset (writes 4 CSVs + build_validation.json)
python build_earnings_call_canonical.py --out <repo>/earnings_calls_canonical_extended

# 3. Analyses and figures (run from the repo root or the scratch copy; CALLS_DIR only matters for 02b)
export CANON_DIR=<repo>/earnings_calls_canonical_extended OUT_DIR=<repo>/analysis_calls/out_extended \
       FIG_DIR=<repo>/figures_calls_extended CALLS_DIR="$SCR/earnings_calls"
python analysis_calls/01_timeseries.py        # fig1, fig1b, fig2, ai_share_pre_post.csv
python analysis_calls/04_network.py           # fig3, fig4a, fig4b, topic_first_appearance.csv
python analysis_calls/02_finbert_tone.py      # ec_sentence_tone.csv, tenk_item1a_ai_tone.csv (downloads ProsusAI/finbert; ~6 min CPU)
python analysis_calls/02b_baseline_tone.py    # baseline tone CSVs (~4 min CPU)
python analysis_calls/05_tone_figures.py      # fig5, tone_summary.csv (fig6 is drawn only if ec_passage_labels.csv exists)
```

Notes:
- `export/ai_washing_10-K.csv` is a committed input; rebuilding it from EDGAR uses the old pipeline (`main.py`), which is
  out of scope here.
- `01_timeseries.py` and `04_network.py` delete old figure names in `FIG_DIR` (lines 235-238, 280-283).
- Running the scripts from the repo creates `__pycache__/` (git-ignored). Set `PYTHONDONTWRITEBYTECODE=1` to avoid it.

---

# Discrepancies and open questions

Format: **what** | **where** | **correct now** | **affects Methods?**

| # | What | Where | Correct value now | Methods? |
|---|---|---|---|---|
| D1 | Bootstrap CI (11.4–17.8; 12.4–16.7) has no code, seed or resample count | `MEETING_SUMMARY.md` | Reproducible within seed noise only as a call-level iid percentile bootstrap (IV.B). Original [ND] | **Yes**: commit a bootstrap before quoting |
| D2 | Headline "6.0 → 20.8" (mean of per-call shares) ≠ figure annotation (mean of quarterly means, 6.06 → 20.78) | `MEETING_SUMMARY.md` vs `01_timeseries.py:133-135` | Both valid; they differ at the 2nd decimal. The B numbers are not produced by any committed script | Yes: state which aggregation |
| D3 | "Latest quarters: Nvidia ~34% …" are 5-quarter means over all unit types, not the latest quarter | `MEETING_SUMMARY.md`; `01_timeseries.py:167` | See IV.B table (Nvidia latest call = 29.0%) | Yes, if quoted |
| D4 | Tone "2023+" uses calendar_year ≥ 2023, while AI-share "post" starts at calendar 2022 Q4; `tone_summary` puts 2022 Q4 calls in "2021–2022" | `05_tone_figures.py:210-212,269` vs `common.py:14` | Both as coded; disclose | Yes |
| D5 | 10-K "2021–2022" row actually contains filings 2017–2022 | `tone_summary.csv` | n = 78 from 2017–2022 | Yes, if quoted |
| D6 | Tone baselines not frame-matched (all years; include Whisper/captions; different splitter and AI regex) | `02b_baseline_tone.py` | Matched-baseline gaps are smaller (prepared +0.068 to +0.116) | **Yes** |
| D7 | 10-K AI identification ≠ call AI filter | `common.py:is_ai` vs `filter_earnings_calls.py` | Different definitions | **Yes** |
| D8 | "72 filings" in the meeting summary = all Mag 7 Item 1A rows 2006–2026; only 36 contribute AI sentences, and 604 sentences enter the figure | `MEETING_SUMMARY.md` caveat 4 | 72 filings / 36 with AI / 682 sentences (604 in 2023+) | Yes |
| D9 | Row counts: tone CSV 10,382 = AI units ✓; summary/figure use 9,280 (1,102 non-comparable excluded) | tone files | As stated | Disclose |
| D10 | Gate 4 report and all its artefacts cover 116 calls only (e.g. 9,884 AI rows, 176 AI corrections, 46 unresolved, 1,858 unlabelled) | `GATE4_VALIDATION_REPORT.md`, `gate4_validation.json` | Extended: 10,382 AI rows, 180 corrected, 53 unresolved, 802 unverified, 1,876 unlabelled; no Gate 4 run on 133 | Yes: don't quote 116 numbers |
| D11 | `alphabet_2021_Q4` source_type = `unknown` | `earnings_call_scope.py:146` string test | It is an official IR PDF via the Internet Archive | Minor; describe correctly in text |
| D12 | The 17 extras show `acquisition_status = already_present` in the extended call-units file | build reads the manifest of the scratch copy | They are newly added non-company/archival sources | Minor; don't use this column to describe provenance |
| D13 | `figures_calls/` and `analysis_calls/out/` are the 116-call versions (they reproduce exactly from `earnings_calls_canonical/`). In those, Nvidia, Apple and Tesla have 0 pre-launch calls and the headline has 3 firms | folder | Superseded by `figures_calls_extended/` | Yes: never cite them |
| D14 | Scope §9.1, §9.3, §9.6 outdated for 133: "all 15 Amazon" Whisper → 19; Tesla captions 7 → 8; unpunctuated list lacks Tesla 2022 Q1; "17 of the 28 … not in the corpus" → all present | `EARNINGS_CALL_SCOPE.md` §9 | Per III.1b / III.3 | Yes, if the scope doc is cited |
| D15 | `FILTER_METHOD.md` corpus description outdated: "Apple 15 YouTube captions" (now 13 captions + 6 Fool in 133; FY23 Q1 and FY24 Q4 replaced with Fool on 2026-10-01); unpunctuated list includes Apple FY23 Q1 (now a Fool sentence call); Tesla "9 Fool / 6 captions" (actually 8/7 in the 105, 11/8 in 133); all its validation numbers are 105-call legacy | `earnings_calls_ai_only/FILTER_METHOD.md` §1, §3, Validation | Code and III.3 | Yes: cite code, not this doc |
| D16 | FILTER_METHOD abbreviation list omits dept, fig, est, cf, al; Amazon end-trim regex broader than described | FILTER_METHOD §3 vs code | Code (A3) | Minor |
| D17 | `common.py` comment says `RE_AI` "mirrors the core idea of the canonical filter", but it is much narrower | `common.py:20-21` | See III.7 | Yes (D7) |
| D18 | `04_network.py` docstring: "17 early calls are missing" (stale for extended); figure captions compute coverage dynamically and say "all 133 expected calls are included" | `04_network.py:11` | 0 missing in extended | No (docstring only) |
| D19 | Topic shares pool non-comparable units (Whisper, caption segments), although scope §4 says such units must be "reported separately or excluded, never pooled silently". Fig 3's caption mentions it; Fig 4a/4b do not | `04_network.py:shares_by_quarter` | Comparable-only robustness numbers in IV.C | Yes: disclose |
| D20 | Filter overlap 93.4/96.7 is a 105-call statistic | Gate 4 B3 | 133-call: 93.5/96.9 (scratch only, not committed) | Yes |
| D21 | Manual review sample drawn from the 116 build; excludes all 17 extras; blank | `manual_review_sample.csv` | — | Yes |
| D22 | `ai_units_speaker_unresolved` (44) ≠ Gate 4 "unresolved" definition (bare + unknown = 53 in extended) | build line 511 vs gate4 line 341 | Report 53 with the breakdown | Minor |
| D23 | No main-call/follow-up exclusion in code; it is enforced by which files exist | — | [ND] whether any follow-up file was removed | Minor |
| D24 | `requirements.txt` unpinned; no lock file; tone run environment and device not recorded | `requirements.txt` | — | Yes, for the reproducibility statement |
| D25 | `export/ai_washing_10-K.csv` lacks `accession`/`period_end` for 43 of 72 Mag 7 Item 1A rows; extractor version not recorded | export file | — | Minor (identify filings by ticker + filing date) |
| D26 | `EARNINGS_CALL_SCOPE.md` §3 and §9 still say the Nvidia rule "needs approval" | scope doc | Approved 2026-10-10 (§10 note added by this task) | No (now recorded) |
| D27 | The scope doc's "Q4 2021 – Q3 2022 must show which firms are present" (§9.6) | scope | All 7 firms present in every quarter in the extended build, but Amazon pre-launch is Whisper-only | Disclose |

## NOT DETERMINABLE FROM REPO (summary)

1. Bootstrap behind the quoted CIs: resampling unit, number of resamples, seed, CI method (no code).
2. FinBERT revision/hash used for the committed tone outputs, and the device/environment of that run.
3. Package versions (pandas, numpy, matplotlib, torch, transformers) used for the committed extended outputs. Only Python 3.14.6 and nltk 3.10.0 are recorded.
4. `punkt_tab` data-package version.
5. Acquisition details of the 17 extras beyond source and type: retrieval dates, faster-whisper settings and version, operator.
6. Whether follow-up calls or other non-main calls ever existed and were removed (no code or log).
7. Which version of `edgar.py` produced `export/ai_washing_10-K.csv`.
