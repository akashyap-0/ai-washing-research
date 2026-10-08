# Mag 7 earnings-call analysis: results for the Oct 9 meeting

Built on Advik's canonical dataset (`earnings_calls_canonical/`, 116 calls, 9,884 AI sentences). Everything here is
**descriptive and pre-validation** (Gate 5 human review has not happened). No causal claims about margins, jobs or
productivity (EARNINGS_CALL_SCOPE.md section 8).

## What to show (in order)

| Figure | File in `figures_calls/` | One-line takeaway |
|---|---|---|
| 1 | `fig1_headline_ai_talk.png` | The one-chart answer. Same three firms (Alphabet, Meta, Microsoft): **4% of the call was about AI before ChatGPT, 22% after** (+18.3 pts, 95% bootstrap CI 16.3 to 20.1; 11 pre-launch calls, 45 post). |
| 1b | `fig1b_ai_talk_by_company.png` | Same measure per company: Nvidia ~34% now, Alphabet ~30%, Microsoft ~26%, Meta ~25%, Amazon ~19%, Tesla ~16%, Apple ~6%. |
| 2 | `fig2_ai_share_heatmap.png` | Heatmap, company x quarter (see "How to read the heatmaps"). |
| 3 | `fig3_company_topic_map.png` | Which topics each company owns: Microsoft = Copilot, Alphabet = Gemini, Meta = Llama, Amazon = AWS AI, Apple = Apple Intelligence, Nvidia = its own stack, Tesla = autonomy. Three panels (before / 2023 / 2024-26) with identical positions. |
| 4a | `fig4a_topic_storyline.png` | What "AI" means changes: machine learning, then generative AI (zero until the launch), then AI agents from 2025. |
| 4b | `fig4b_topic_heatmap.png` | Heatmap, topic x quarter (see below). Table: `out/topic_first_appearance.csv`. |
| 5 | `fig5_tone_calls_vs_10k.png` | Tone of AI sentences (off-the-shelf FinBERT): prepared remarks +0.46, Q&A +0.20, 10-K risk factors -0.17 (2023+). **Mostly genre**: ordinary sentences score +0.34, +0.16, -0.26 in the same sources, so the AI-specific effect is about +0.12 in prepared remarks, +0.04 in Q&A and +0.09 in 10-K risk factors. |

Do **not** show `fig6_EXPLORATORY_do_not_present.png` (see below).

## How to read the heatmaps (and why they matter)

**Fig 2: company x quarter, each cell = % of that call that is about AI.**
- *Common shock, not company trends.* Every firm with data jumps at the same line (the first post-ChatGPT calls), including firms that never discussed AI before. A shared break at one date is what you would expect if ChatGPT triggered the change, rather than each firm drifting up on its own.
- *Who moved first and who is structurally different.* Nvidia is already high at the first post-launch call (AI is its product), Microsoft, Alphabet and Meta ramp over 2-4 quarters, and Apple stays low except for spikes around Apple Intelligence (2024).
- *Persistence.* The cells stay dark after the jump, so it is a level change, not a one-quarter fad. Meta and Alphabet keep climbing, Nvidia has peaked.
- *Limits.* It is a share of the call, so it measures attention, not adoption or spending. Cells marked * use unit types that are not comparable, and n/a cells are calls we do not have.

**Fig 4b: topic x quarter, each cell = % of that quarter's AI sentences that mention the topic.**
- *It shows what the AI talk is about, not just how much.* The same "AI talk" total hides a change in content: machine learning (2021-22) is replaced by generative AI at the launch (zero before, ~20% right after), which is then overtaken by AI agents in 2025.
- *Named products show diffusion order.* Copilot and OpenAI appear before the launch (Microsoft), Gemini and Llama appear in 2023, Apple Intelligence in 2024, DeepSeek in a single quarter (Q4 2024 / Q1 2025), and each lights up at the firm that owns it.
- *Compute never goes away.* The "training & inference compute" row stays at 5-12% throughout, so the infrastructure story runs underneath the application story.
- *Limits.* Rows are independent (one sentence can mention several topics), topics come from a hand-written pattern list, and pre-launch quarters pool only 3 firms so they are noisier.

## Caveats to say out loud

1. **Pre-launch coverage is thin.** 17 of 133 expected calls are missing (all Apple, Nvidia FY22-FY23 Q3, most Amazon and Tesla before 2022Q4). The before/after test uses only Alphabet, Meta and Microsoft. Fig 1's pooled mean changes composition (n shown under the axis), which is why the fixed-firm line is drawn.
2. **Units are not all sentences.** Amazon (Whisper lines), 7 caption-segment calls and some Apple/Tesla calls use different units, so their shares are not comparable. They are hollow markers in Fig 1 and excluded from pooled lines and the tone figure.
3. **The ChatGPT date.** Calls for calendar Q4 2022 were held Jan-Feb 2023, so they are the first post-launch calls. AI share was already rising through 2022.
4. **Tone is generic.** `ProsusAI/finbert` was not fine-tuned on this project. It measures financial-news-style positivity, not "AI opportunity vs risk". 10-K sample is small (682 AI sentences, 72 filings); Alphabet filings start 2024 and Meta 2025.
5. **Filter is not validated.** Advik's AI sentence filter has no measured precision or recall yet, and the borderline terms (GPU, FSD, robotaxi) are outside the AI numerator, so Tesla's AI share is understated.
6. **The fine-tuned model is exploratory and confounded.** FinBERT was fine-tuned on `derived/annotation_complete_labeled.csv` (held-out-company test AUC about 0.95). But those 1,200 labels are all **Claude-generated and unreviewed** (`label_source = claude_blind_*`). The `coder_id` values AK/TA were randomly assigned and are **not** human coders, so do not describe the labels as human annotation. "Risk" labels come overwhelmingly from Item 1A, so the model partly learns risk-factor style: it flags about 86% of 10-K AI sentences as risk and about 83% of call sentences as opportunity. Thresholds were tuned on only 80 validation passages. That is why Fig 6 is withheld.

## Reproduce

```
pip install torch transformers          # FinBERT scripts only
python3 analysis_calls/01_timeseries.py  # fig1, fig1b, fig2 (counts only)
python3 analysis_calls/04_network.py     # fig3, fig4a, fig4b
python3 analysis_calls/02_finbert_tone.py && python3 analysis_calls/02b_baseline_tone.py
python3 analysis_calls/05_tone_figures.py   # fig5 (+ withheld fig6 if 03 has been run)
python3 analysis_calls/03_finetune_predict.py   # optional, exploratory
```
Outputs: `analysis_calls/out/*.csv`. Seeds fixed; the first run downloads `ProsusAI/finbert` from Hugging Face.

## Next steps (after this meeting)

1. Gate 5: review the 150-row sample (`earnings_calls_canonical/manual_review_sample.csv`) to get real filter precision/recall.
2. Hand-label a few hundred call sentences for opportunity vs risk, then fine-tune on those. Replace the SEC-passage labels.
3. Fill the 9 calls awaiting a source decision and re-extract the two misplaced-label Meta PDFs.
4. Backfill 10-K Item 1A for Alphabet (2021-23) and Meta (2021-24) so the risk-factor comparison covers the full window.
5. Add Item 1A topic modeling (LDA) over five years, then scale to the S&P 500 (industries need that).
