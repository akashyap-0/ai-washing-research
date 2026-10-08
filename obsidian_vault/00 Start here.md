---
tags: [index]
---
# AI diffusion across the Mag 7: knowledge graph

How AI talk spreads across Alphabet, Amazon, Apple, Meta, Microsoft, Nvidia and Tesla earnings calls
(calls reporting Q4 2021 to Q2 2026). This vault is the same graph as `figures_calls/fig3_ai_knowledge_graph.png`.

**Open the graph view** (Ctrl/Cmd+G). Blue = company, grey = AI concept, orange = named product/stack,
green = study period. Click a note to see counts. Use the graph's Filters to hide period nodes for a cleaner view.

- Periods: [[Period - Before ChatGPT (2021Q4-2022Q3)]], [[Period - 2023]], [[Period - 2024 to 2026Q2]]
- Companies: [[Alphabet]], [[Amazon]], [[Apple]], [[Meta]], [[Microsoft]], [[Nvidia]], [[Tesla]]

## Read this first
- An edge means a company had **3+ AI sentences** mentioning the topic in that period. Counts are sentences from the
  canonical dataset (`earnings_calls_canonical/`, built by Advik). Topics come from a hand-written pattern list
  in `analysis_calls/04_network.py`.
- Descriptive only: the AI-sentence filter has not been human-validated, 17 of 133 calls are missing (mostly before
  2022Q4), and Amazon/caption calls use units that are not sentences. No causal claims.
- Obsidian does not weight edges. Edge counts are in the tables inside each note.
- Regenerate with `python3 analysis_calls/06_obsidian_vault.py`.
