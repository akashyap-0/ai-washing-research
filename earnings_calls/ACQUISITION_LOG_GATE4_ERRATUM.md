# Erratum to ACQUISITION_LOG.md (found in Gate 4, 2026-10-06)

`ACQUISITION_LOG.md` reports **0 corrupted** acquisitions. That is wrong for two calls.

| Call | Problem | Evidence |
|---|---|---|
| `meta_2022_Q2.md` | Inline speaker labels (`Name:`) misplaced by the Gate 2 extraction (`pdftotext -layout`): 15 label positions in the raw file do not occur in `pdftotext -raw` of the same official PDF, and 12 of the PDF's do not occur in the file | `earnings_calls_canonical/gate4_validation.json → 6_section_speaker.acquired_pdf_label_placement_check` |
| `meta_2022_Q3.md` | Same: 13 / 10. Example: a stray `Operator:` at a page top attributes part of the CFO's answer to the Operator, and `Justin Post:` lands inside the CFO's text | same |

The text itself is complete and verbatim. The section boundary (prepared remarks vs Q&A) is
correct in both files. Only speaker attribution is unreliable.

The other five PDF acquisitions (`meta_2021_Q4`, `meta_2022_Q1`, `alphabet_2022_Q1`–`Q3`)
place every label exactly as `-raw` mode does. The four Microsoft DOCX acquisitions are not
affected.

**Status:** the raw files are unchanged. Gate 4 did not allow raw-text edits. In the
canonical dataset, every labelled speaker in these two calls has `speaker_status =
unverified_raw_label_misplacement`. A fix (re-extracting both files from the cached official
PDFs with `pdftotext -raw`, then rebuilding) needs approval.

`coverage_manifest.csv` still shows `parser_status = parsed_ok` for these calls. The parser
does run cleanly, but that status does not reflect label placement.
