# Historical earnings-call acquisition log (Gate 2)

Covers the 28 calls missing from the Q4 2021 – Q3 2022 part of the study window (four per
firm). Attempts were made on **2026-10-06**. Only company investor-relations sources were
used. No paid service, paywalled provider, or third-party transcript (Motley Fool, FactSet
resale, Seeking Alpha, gurufocus, roic.ai and similar) was used, and no text was written by
hand or summarized.

Reproduce the acquired files with `python earnings_calls/acquire_historical_transcripts.py`.
It never overwrites an existing file. Downloaded originals are kept in
`cache/earnings_call_sources/` (gitignored), and URL, HTTP status, byte size and SHA-256 are in
`earnings_calls/acquisition_results.json`. Each row's status is in
`earnings_calls/coverage_manifest.csv`.

## Summary

| Status | Count | Calls |
|---|---:|---|
| Already present (not part of the 28) | 105 | the original corpus, untouched |
| **Acquired** | **11** | Alphabet 2022 Q1–Q3; Meta 2021 Q4, 2022 Q1–Q3; Microsoft FY22 Q2–Q4, FY23 Q1 |
| **Awaiting human source decision** | **9** | Alphabet 2021 Q4; Amazon 2021 Q4, 2022 Q1–Q3; Tesla 2021 Q4, 2022 Q1–Q3 |
| **Unavailable from a public company source** | **8** | Apple FY22 Q1–Q4; Nvidia FY22 Q4, FY23 Q1–Q3 |
| Corrupted | 0 | all 11 acquired files parse with no flags (checked with `filter_earnings_calls.process_file`, read-only) |

Expected 133 = 105 + 11 + 9 + 8. Present now: 116. Still missing: 17.

## Acquired (11)

New raw files follow the existing naming convention `earnings_calls/<company>/<company>_<period>.md`.
Each has a metadata block with company, ticker, period, source URL, IR landing page, source
type, retrieval date, source SHA-256, extraction method and a quality warning.

| File | Source URL (company-hosted) | Format | Speaker labels / sections | Call date (from text) | Units parsed |
|---|---|---|---|---|---:|
| alphabet_2022_Q1.md | https://s206.q4cdn.com/479360582/files/doc_financials/2022/q1/2022_Q1_Earnings_Transcript.pdf | PDF | yes / operator-led Q&A | 2022-04-26 | 456 |
| alphabet_2022_Q2.md | https://s206.q4cdn.com/479360582/files/doc_financials/2022/q2/2022_Q2_Earnings_Transcript.pdf | PDF | yes / operator-led Q&A | 2022-07-26 | 485 |
| alphabet_2022_Q3.md | https://s206.q4cdn.com/479360582/files/doc_financials/2022/q3/2022_Q3_Earnings_Transcript.pdf | PDF | yes / operator-led Q&A | 2022-10-25 | 475 |
| meta_2021_Q4.md | https://s21.q4cdn.com/399680738/files/doc_financials/2021/q4/Meta-Q4-2021-Earnings-Call-Transcript.pdf | PDF | yes / operator-led Q&A | 2022-02-02 | 513 |
| meta_2022_Q1.md | https://s21.q4cdn.com/399680738/files/doc_financials/2022/q1/Meta-Q1-2022-Earnings-Call-Transcript.pdf | PDF | yes / operator-led Q&A | 2022-04-27 | 517 |
| meta_2022_Q2.md | https://s21.q4cdn.com/399680738/files/doc_financials/2022/q2/Meta-Q2-2022-Earnings-Call-Transcript.pdf | PDF | yes / operator-led Q&A | 2022-07-27 | 559 |
| meta_2022_Q3.md | https://s21.q4cdn.com/399680738/files/doc_financials/2022/q3/Meta-Q3-2022-Earnings-Call-Transcript.pdf | PDF | yes / operator-led Q&A | 2022-10-26 | 464 |
| microsoft_FY22_Q2.md | https://cdn-dynmedia-1.microsoft.com/is/content/microsoftcorp/TranscriptFY22Q2 | DOCX | yes / "go to Q&A" phrase | 2022-01-25 | 448 |
| microsoft_FY22_Q3.md | https://cdn-dynmedia-1.microsoft.com/is/content/microsoftcorp/TranscriptFY22Q3 | DOCX | yes / "go to Q&A" phrase | 2022-04-26 | 453 |
| microsoft_FY22_Q4.md | https://cdn-dynmedia-1.microsoft.com/is/content/microsoftcorp/TranscriptFY22Q4 | DOCX | yes / "go to Q&A" phrase | 2022-07-26 | 466 |
| microsoft_FY23_Q1.md | https://cdn-dynmedia-1.microsoft.com/is/content/microsoftcorp/TranscriptFY23Q1 | DOCX | yes / "go to Q&A" phrase | 2022-10-25 | 509 |

How the links were found:

- **Alphabet:** found by the q4cdn path pattern used by the existing Alphabet files, and
  confirmed against the Alphabet IR event feed (`abc.xyz/feed/Event.svc/GetEventList`), which
  lists 2022 Q1–Q3 calls on 2022-04-26, 2022-07-26 and 2022-10-25.
- **Meta:** each URL is taken from the transcript link on the Meta IR event page
  (`investor.atmeta.com/investor-events/event-details/2022/<Qn>-2022-Earnings/default.aspx`;
  2021 Q4 by the same q4cdn pattern). The separate "Follow-Up Call" transcripts on those pages
  were not taken, matching the existing Meta files.
- **Microsoft:** the IR event pages for FY22 Q3, FY22 Q4 and FY23 Q1 return the transcript as
  HTML and link it as `cdn-dynmedia-1.microsoft.com/.../TranscriptFY22Q3` (a Word file). The
  FY22 Q2 IR page now returns HTTP 404, but the same Microsoft-hosted transcript file
  (`TranscriptFY22Q2`) is still published, and its title line reads "Microsoft FY22 Second
  Quarter Earnings Conference Call … Tuesday, January 25, 2022". The DOCX was used for all four
  so the extraction is the same. The existing Microsoft files came from the HTML page, so their
  layout is slightly different (labels on their own line versus inline), which the `msft`
  parser handles either way.

Extraction method:

- **PDF:** `pdftotext -layout -enc UTF-8`, then each line has whitespace runs collapsed and is
  stripped. Page numbers are left in, and the filter removes them. As a check, re-extracting
  the official PDFs of the committed `alphabet_2022_Q4.md` and `meta_2022_Q4.md` this way
  gives exactly the same unit, AI and section counts as the committed files.
- **DOCX:** text of each paragraph (`w:t` runs), one paragraph per line.
- No U+FFFD replacement characters appear in any acquired file.

Quality notes on acquired files (also in each file's header):

- **Analyst labels are not parsed in the Alphabet 2022 Q1–Q3 and all Microsoft files.** These
  PDFs and DOCX files label analysts as `Name, Firm:`. The existing Alphabet parser accepts the
  comma form only with a title keyword, and the Microsoft parser never accepts it. So the
  analyst's first question in each exchange is attributed to the previous speaker (operator or
  IR host). Sections are not affected. The same limitation already affects committed Microsoft
  files (e.g. `microsoft_FY23_Q2`). Gate 3 flags affected rows in
  `speaker_attribution_warning` and does not reassign speakers. Fixing the parser is a Gate 4
  decision.
- **The committed Meta files lost some inline labels.** Re-extracting the official
  `meta_2022_Q4` PDF recovers inline Q&A labels (e.g. `Javier Olivan:`) that are missing from
  the committed text, so some committed Meta Q&A sentences are attributed to the previous
  speaker. Committed files were not changed. This is recorded for Gate 4.

## Awaiting human source decision (9)

| Call | What was found | What was tried | Decision needed |
|---|---|---|---|
| alphabet 2021_Q4 | Official PDF `https://abc.xyz/assets/investor/static/pdf/2021_Q4_Earnings_Transcript.pdf` now redirects to the IR site map (HTTP 200, HTML, 18 kB). archive.org reports a capture of the official PDF dated 2024-07-16 (`web.archive.org/web/20240716084722/...`). It was **not downloaded**. | q4cdn patterns `doc_financials/2021/q4/2021_Q4_Earnings_Transcript.pdf`, `2021-q4-earnings-transcript.pdf`, `2021_Q4_Earnings_Transcript_Final.pdf`, `2021_Q4_Earnings-Transcript.pdf` (all 404). IR event feeds for 2021 and 2022 (the archive starts at 2022 Q1). `abc.xyz/investor/events/2021-q4-earnings-call/` (404). | Accept an archive.org copy of the official Alphabet PDF? It is the company's own document, but not served by the company today. |
| amazon 2021_Q4 | Official IR audio `https://s2.q4cdn.com/299287126/files/doc_financials/2021/q4/Amazon-Quarterly-Earnings-Report-Q4-2021-Full-Call-v1.wav` (HTTP 200, audio/x-wav, 665,441,072 bytes). Call 2022-02-03 per the Amazon IR event feed. | Amazon IR event feed (`ir.aboutamazon.com/feed/Event.svc/GetEventList`, 2022): the event carries only audio, a press release and slides. No transcript. | Approve local transcription with `faster-whisper` small.en (the same method as the 15 existing Amazon files). It is **not installed** here, and installing it downloads model weights. |
| amazon 2022_Q1 | `.../2022/q1/Amazon-Quarterly-Earnings-Report-Q1-2022-Full-Call-v1.mp3` (HTTP 200, 48,219,480 bytes). Call 2022-04-28. | same | same |
| amazon 2022_Q2 | `.../2022/q2/Amazon-Quarterly-Earnings-Report-Q2-2022-Full-Call-v1.mp3` (HTTP 200, 93,276,308 bytes). Call 2022-07-28. | same | same |
| amazon 2022_Q3 | `.../2022/q3/Amazon-Quarterly-Earnings-Call-Q3-2022-Full-Call-v2.wav` (HTTP 200, 539,530,478 bytes). Call 2022-10-27. | same | same |
| tesla 2021_Q4 | Tesla publishes no transcript. The press release says the Q&A webcast replay is on ir.tesla.com. Call 2022-01-26 (per the Tesla results press release found by web search). | `https://ir.tesla.com/` returns HTTP 403 to curl and to WebFetch. | The existing Tesla caption files come from Tesla's own YouTube uploads. Approve YouTube auto-captions of Tesla's official uploads (machine text, no speakers), or a local transcription of the official webcast audio, or leave absent. |
| tesla 2022_Q1 | same (no transcript; webcast only) | same | same |
| tesla 2022_Q2 | same | same | same |
| tesla 2022_Q3 | same | same | same |

## Unavailable from a public company source (8)

| Call | IR event (date) | What the company publishes | Attempts |
|---|---|---|---|
| apple FY22_Q1 | "FY 22 First Quarter Results", 2022-01-27 | Press release only. The webcast link is the generic live page `apple.com/investor/earnings-call/`, with no archive. | Apple IR event feed (`investor.apple.com/feed/Event.svc/GetEventList`), all years |
| apple FY22_Q2 | "FY 22 Second Quarter Results", 2022-04-28 | same | same |
| apple FY22_Q3 | "FY 22 Third Quarter Results", 2022-07-28 | same | same |
| apple FY22_Q4 | "FY 22 Fourth Quarter Results", 2022-10-27 | same | same |
| nvidia FY22_Q4 | "NVIDIA 4th Quarter FY22 Financial Results", 2022-02-16 | No transcript attached. The webcast is an `events.q4inc.com` registration app (JavaScript only). NVIDIA hosts transcripts only from FY26 Q1 (May 2025). | NVIDIA IR event feed (`investor.nvidia.com/feed/Event.svc/GetEventList`, 2021–2022); webcast link |
| nvidia FY23_Q1 | "NVIDIA 1st Quarter FY23 Financial Results", 2022-05-25 | same | same |
| nvidia FY23_Q2 | "NVIDIA 2nd Quarter FY23 Financial Results", 2022-08-24 | same | same |
| nvidia FY23_Q3 | "NVIDIA 3rd Quarter FY23 Financial Results", 2022-11-16 | same | same |

For these 8 calls only third-party transcripts exist (for example Motley Fool, which the
existing corpus uses for other Apple and Nvidia quarters). This task does not allow them. If a
human approves third-party sources, the same source type should be used across a firm's
calls where possible, and each file must state that it is third-party.

## Not done, by rule

- No Motley Fool, Seeking Alpha, FactSet, gurufocus, roic.ai, bullfincher, sonix, Rev or
  YouTube text was fetched.
- No archive.org content was downloaded. Only its public availability endpoint was queried.
- No audio was downloaded or transcribed.
- None of the original 105 raw files was modified, renamed or deleted.
