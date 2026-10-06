# Archive

Files moved out of the repo root to declutter it. Nothing here is deleted, and git history is
intact (`git log --follow archive/scripts/<file>`).

## scripts/

One-off analysis and audit scripts. No other code imports them. Several produced numbers
cited in `RESULTS_PACKET.md` and outputs in `export/` (e.g. `risk_factor_composition_panel.csv`,
`sensitivity_unflagged_filings.csv`), so they are kept for reproducibility.

- `analyze_ai_sentiment_results.py`
- `edgar_backfill_10k.py`
- `firm_characteristics_robustness.py`
- `oracle_ai_risk_sentences.py`
- `risk_factor_composition.py`
- `sensitivity_unflagged_filings.py`
- `spotcheck_8k_ai_gap.py`
- `validate_finbert_against_labels.py`

They import modules that still live in the repo root (`config`, `edgar`,
`extract_ai_sentiment`, ...). To run one, do it from the repo root with the root on the
import path:

```
PYTHONPATH=. python archive/scripts/risk_factor_composition.py
```

## docs/

Older project-status snapshots, superseded by `PROJECT_EXPLAINED_SIMPLE.md`:

- `STATUS.md`: status as of 2026-08-10
- `9.17.26 current standing.md`: status as of 2026-09-17

Other docs still refer to these files by bare filename; look for them here.
