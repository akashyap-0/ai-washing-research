# Blinded LLM annotation run — status (2026-09-01)

Double-blind LLM labeling of a stratified 255-passage sample from
`derived/annotation_template.csv`, per `annotation_prompt.md` v1.0.0 extended
with `risk_type` / `risk_type_secondary`. Run was stopped early on request;
this file records exactly what exists and what remains.

## Output

**`derived/annotation_master_sample_llm_blind.csv` — 241 of 255 passages, all
rows pass `label_schema.validate_annotation()`.**

- Protocol: two independent blinded coders per passage (bare passage text only,
  no company/ticker/form/section/date; structured output enforced by JSON
  schema); a blinded adjudicator re-coded every field on any disagreement.
- Provenance (recorded per row): `coder_id =
  llm_blind:claude-fable-5:prompt-1.0.0+risk_type`, `review_status =
  unreviewed`, evidence quote persisted in `annotation_notes`.
- These are **machine labels**. They are not human annotations and must not be
  reported as such. The human gold set (planned coders: TA, AK) is a separate,
  still-to-be-done step; per `RESEARCH_PIPELINE.md` / `annotation_prompt.md`,
  it should be stratified by form so LLM–human kappa can be compared across
  8-K vs 10-K (residual-leakage check).

## Results snapshot

- Inter-coder agreement: **207/241 (85.9%)** passages identical across all 13
  fields; 34 adjudicated.
- Prevalence: ai_risk 28.2%, ai_opportunity 19.1%, ai_adoption 17.8%,
  ai_efficiency 4.6%, ai_worker_augmentation 4.1%, generic_ai_marketing 3.3%,
  ai_workforce_reduction 2.1%, explicit_ai_job_link 1.2%, neutral 54.8%.
- risk_type: not_a_risk 173, governance 23, other 13, implementation 12,
  competition 7, displacement 6, demand 6, export_controls 1.
- causal_link_strength: none 216, co_occurring_only 15, strongly_implied 5,
  explicit 5.
- 23 companies covered.

## Remaining work (14 passages, in `remaining_work.json`)

- **11 need adjudication only** — both coder label sets are saved in
  `remaining_work.json` with the disputed fields listed.
- **3 never started** — need both coders:
  `379de83062cb3255038b413e`, `49f36e76eb1ab8e153aa85ee`,
  `99f0230a7aff03def32440b8`.

## Files in this folder

- `build_sample.py` — deterministic stratified sampler (seed 20260901, ≤12 per
  ticker, largest-remainder across form×section). Re-running it regenerates
  the identical sample and the blinded text files.
- `workflow_script.js` — the exact workflow used (contains the verbatim coder
  and adjudicator prompts and the output JSON schema). The coder prompt is the
  authoritative prompt text for this batch.
- `sample_rows.csv` / `sample_manifest.json` — full provenance of the sample.
- `labels.json` — combined final labels (input to the merge).
- `merge_labels.py` — merge/validation script that produced the output CSV
  (paths inside point at the original scratchpad; regenerate blinded files
  with `build_sample.py` and adjust paths if re-running).
- `remaining_work.json` — everything needed to finish the 14 open passages.

## To finish later

1. Adjudicate the 11 disputed passages and double-code the 3 unstarted ones
   using the prompts in `workflow_script.js` (blinded: bare passage text only).
2. Append the new finals to `labels.json` and re-run `merge_labels.py` →
   the CSV rebuilds with all 255 rows.
