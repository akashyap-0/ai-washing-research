# AI washing in Mag 7 earnings calls

Study of how the seven largest US tech firms (Alphabet, Amazon, Apple, Meta, Microsoft, Nvidia,
Tesla) talk about AI on quarterly earnings calls, calendar Q4 2021 – Q2 2026 (133 expected calls).

The frozen scope, unit of analysis, denominators and what may not be claimed are in
[EARNINGS_CALL_SCOPE.md](EARNINGS_CALL_SCOPE.md). Read that first.

## Layout

| Path | What it is |
|---|---|
| `EARNINGS_CALL_SCOPE.md`, `earnings_call_scope.py` | Frozen scope (Gate 1) and the code that checks it, writes `earnings_calls/coverage_manifest.csv` |
| `earnings_calls/` | Raw transcripts per firm, acquisition log, manifest, teammate passage filter (audit only) |
| `filter_earnings_calls.py`, `earnings_calls_ai_only/` | Primary sentence-level AI filter and its legacy outputs |
| `build_earnings_call_canonical.py`, `earnings_calls_canonical/` | Canonical dataset (sentences, passages, call units) and Gate 4 validation |
| `analysis_calls/`, `figures_calls/` | Exploratory analyses (time series, FinBERT tone, fine-tune, topic network) and figures |
| `ANNOTATION_CODEBOOK.md`, `annotation_prompt.md`, `label_schema.py`, `llm_annotate.py` | Label definitions and LLM annotation tooling, reused for call labeling |
| `EARNINGS_CALL_AI_FILTER_PROMPT.md`, `INTRO_REFERENCE.md` | Background and handoff prompts |
| `export/ai_washing_10-K.csv` | Mag 7 10-K AI sentences, used as a comparison in `analysis_calls/02_finbert_tone.py` |
| `derived/` (git-ignored) | `annotation_complete_labeled.csv`, the SEC-passage labels used to train in `analysis_calls/03_finetune_predict.py` |

The earlier SEC-filing (8-K vs 10-K) pipeline was removed from the working tree; it is still in git
history before the cleanup commit.

## Setup

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```
