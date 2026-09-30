# Earnings call transcripts — Mag 7, Q4 2022 → Q2 2026

One markdown file per call, in `earnings_calls/<company>/`. Window starts with the first call after ChatGPT (Nov 30, 2022).

| Company | Files | Source | Speaker labels | Notes |
|---|---|---|---|---|
| Alphabet | 15/15 | Official IR transcript PDFs | yes | |
| Meta | 15/15 | Official IR transcript PDFs | yes | Main call only; separate "Follow Up Call" transcripts exist on IR and are not included |
| Microsoft | 15/15 | Official IR transcript pages | yes | Fiscal year ends June (file names use FY, e.g. FY23_Q2 = Dec 2022 quarter) |
| Nvidia | 15/15 | Official IR PDFs for FY26 Q1 → FY27 Q2 (6); Motley Fool transcripts for FY23 Q4 → FY25 Q4 except FY24 Q4 (8); YouTube auto-captions for FY24 Q4 (Feb 2024) (1) | yes, except FY24 Q4 | Fool transcripts are third-party (each file's header links its source). Nvidia only hosts official transcripts from May 2025 on |
| Tesla | 15/15 | YouTube auto-captions of Tesla's official upload (2026 Q2 from Benzinga) | no | No official transcripts published |
| Apple | 15/15 | YouTube auto-captions of live streams (mostly Benzinga) | no | Audio-only call. FY24 Q3 file is ~19k words (stream ran 129 min, includes non-call content) |
| Amazon | in progress | Official IR audio (mp3/wav) transcribed locally with faster-whisper small.en | no | Audio-only call. Runs in background; see folder for finished files |

## Caveats
- Caption/Whisper transcripts have **no speaker labels** and can garble names and numbers, so management vs. Q&A splitting needs a heuristic.
- Fiscal labels differ: Apple FY ends Sept, Microsoft June, Nvidia January. Align to calendar quarter before pooling.
- Audio-only calls (Apple, Amazon) have no video, so they can't be used for the later VLM/facial analysis.
