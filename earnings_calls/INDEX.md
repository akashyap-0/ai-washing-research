# Earnings call transcripts — Mag 7, Q4 2022 → Q2 2026

One markdown file per call, in `earnings_calls/<company>/`. Window starts with the first call after ChatGPT (Nov 30, 2022).

| Company | Files | Source | Speaker labels | Notes |
|---|---|---|---|---|
| Alphabet | 15/15 | Official IR transcript PDFs | yes | |
| Meta | 15/15 | Official IR transcript PDFs | yes | Main call only; separate "Follow Up Call" transcripts exist on IR and are not included |
| Microsoft | 15/15 | Official IR transcript pages | yes | Fiscal year ends June (file names use FY, e.g. FY23_Q2 = Dec 2022 quarter) |
| Nvidia | 15/15 | Official IR PDFs for FY26 Q1 → FY27 Q2 (6); Motley Fool transcripts for FY23 Q4 → FY25 Q4 except FY24 Q4 (8); YouTube auto-captions for FY24 Q4 (Feb 2024) (1) | yes, except FY24 Q4 | Fool transcripts are third-party (each file's header links its source). Nvidia only hosts official transcripts from May 2025 on |
| Tesla | 15/15 | Motley Fool transcripts for 2022 Q4, 2023 Q2 → 2024 Q4 (8, speaker-labeled); YouTube auto-captions for 2023 Q1 and 2025 Q1 → 2026 Q2 (7) | 8 of 15 | No official transcripts. Fool pages from 2025 on are LLM-written summaries, not verbatim, so those calls stay as captions |
| Apple | 15/15 | Motley Fool transcripts for FY23 Q1 and FY24 Q4 (2, speaker-labeled); YouTube auto-captions for the other 13 | 2 of 15 | Audio-only call. Fool skipped most Apple calls. FY24 Q3 caption file is ~19k words (stream ran 129 min, includes non-call content) |
| Amazon | 15/15 | Official IR audio (mp3/wav) transcribed locally with faster-whisper small.en | no | Audio-only call; machine transcript, expect errors on names and numbers |

## Caveats
- Caption/Whisper transcripts have **no speaker labels** and can garble names and numbers, so management vs. Q&A splitting needs a heuristic.
- Fiscal labels differ: Apple FY ends Sept, Microsoft June, Nvidia January. Align to calendar quarter before pooling.
- Audio-only calls (Apple, Amazon) have no video, so they can't be used for the later VLM/facial analysis.

## AI-passage filter
`python3 filter_ai_passages.py` → `ai_passages.csv` (one row per passage: company, period, calendar quarter, section, speaker, matched keywords, text) and `call_summary.csv` (per-call sentence counts and AI share).
- A passage is a sentence containing an explicit AI term (AI, generative, LLM, ChatGPT, OpenAI, Copilot, Gemini, agentic, ...) plus one sentence of context either side.
- Adjacent terms (GPU, inference, FSD, robotaxi, data center, ...) are counted in `weak_only_sentences` but are NOT in the passages file.
- `section` (prepared vs qa) comes from a cue-based heuristic; `speaker` is best effort and blank for most caption/Whisper files and Nvidia's official PDFs.

