# Extra pre-ChatGPT calls (17 calls, Q4 2021 - Q3 2022)

These are the 17 calls that `earnings_calls/ACQUISITION_LOG.md` listed as missing or awaiting a source decision.
They are **not merged into Advik's tracked corpus** (`earnings_calls/`) and **have not been approved** under his
company-sources-only rule (EARNINGS_CALL_SCOPE.md section 10). Raw files here use the same format as `earnings_calls/`.

| Call(s) | Source | Type | Speaker labels |
|---|---|---|---|
| alphabet 2021_Q4 | Alphabet's official transcript PDF, now removed from abc.xyz; Internet Archive capture dated 2024-07-16 | official text via archive | yes |
| amazon 2021_Q4, 2022_Q1-Q3 | Amazon IR official call audio (file sizes match the acquisition log), transcribed locally with faster-whisper small.en | machine transcript | no |
| apple FY22_Q1-Q4 | Motley Fool | third-party text | yes |
| nvidia FY22_Q4, FY23_Q1-Q3 | Motley Fool | third-party text | yes |
| tesla 2021_Q4, 2022_Q2, 2022_Q3 | Motley Fool | third-party text | yes |
| tesla 2022_Q1 | YouTube auto-captions of Tesla's official upload (Fool has no page for this call) | machine captions | no |

Each file's header states its source. Tesla 2022_Q1 and the Amazon files use non-sentence units (caption segments / Whisper
lines), so they are excluded from comparable-unit pooled lines.

## Rebuilding the extended dataset
Copy these files into `earnings_calls/<company>/` of a scratch copy of the repo, then run
`python build_earnings_call_canonical.py --out <dir>` there (nltk 3.10.0 with punkt_tab reproduces Advik's committed CSVs
exactly on the original 116 calls, apart from the `extraction_version` hash). The result for all 133 calls is saved in
`earnings_calls_canonical_extended/`. Analysis scripts read it with `CANON_DIR=... OUT_DIR=... FIG_DIR=... python3 analysis_calls/<script>.py`;
outputs are in `analysis_calls/out_extended/` and `figures_calls_extended/`.
