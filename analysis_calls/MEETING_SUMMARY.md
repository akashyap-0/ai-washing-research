# Mag 7 earnings-call analysis: results for the Oct 9 meeting

Show the figures in **`figures_calls_extended/`**: they use all 133 expected calls (Q4 2021 to Q2 2026). The older
`figures_calls/` folder is the first version on Advik's 116 committed calls (it lacks the pre-ChatGPT calls for Apple,
Nvidia, Amazon, Tesla and one Alphabet quarter), so it understates pre-launch AI talk. Everything here is
**descriptive and pre-validation** (Gate 5 human review has not happened). No causal claims about margins, jobs or
productivity (EARNINGS_CALL_SCOPE.md section 8).

**Sources note, needs Advik's approval.** 17 of the 133 calls are not in Advik's tracked corpus and break his
company-sources-only rule: 11 are third-party Motley Fool text (Apple FY22 Q1-Q4, Nvidia FY22 Q4-FY23 Q3, Tesla 2021 Q4 and 2022 Q2-Q3),
Amazon 2021 Q4-2022 Q3 is machine transcription of Amazon's official audio, Alphabet 2021 Q4 is the official PDF via an Internet
Archive copy, and Tesla 2022 Q1 is YouTube captions. Details: `earnings_calls_pre2022_extra/README.md`. His tracked dataset is unchanged;
the extended build is in `earnings_calls_canonical_extended/`.

## What to show (in order)

| Figure | File in `figures_calls_extended/` | One-line takeaway |
|---|---|---|
| 1 | `fig1_headline_ai_talk.png` | Six firms with comparable calls before and after (Alphabet, Apple, Meta, Microsoft, Nvidia, Tesla): **6.0% of the call was about AI before ChatGPT, 20.8% after** (+14.7 pts, 95% bootstrap CI 11.4 to 17.8; 23 pre-launch calls, 83 post). Without Nvidia: 3.5% to 18.0% (+14.5, CI 12.4 to 16.7). |
| 1b | `fig1b_ai_talk_by_company.png` | Per company, before to after: Microsoft 2.8% to 22.7%, Alphabet 4.6% to 23.2%, Meta 5.0% to 20.9%, Tesla 5.1% to 12.4%, Apple 0.1% to 5.1%, **Nvidia 18.4% to 33.6%**. Latest quarters: Nvidia ~34%, Alphabet ~30%, Microsoft ~26%, Meta ~25%, Amazon ~19%, Tesla ~16%, Apple ~6%. |
| 2 | `fig2_ai_share_heatmap.png` | Heatmap, company x quarter (see "How to read the heatmaps"). |
| 3 | `fig3_company_topic_map.png` | Which topics each company owns. Before ChatGPT: Nvidia's own stack (23% of its AI talk), Tesla autonomy (69%), Meta machine learning (15%), Microsoft OpenAI/ChatGPT (17%). By 2024-26: Microsoft = Copilot, Alphabet = Gemini, Meta = Llama, Amazon = AWS AI, Apple = Apple Intelligence, Nvidia = its stack, Tesla = autonomy. |
| 4a | `fig4a_topic_storyline.png` | What "AI" means changes: machine learning (5.9% of AI sentences before the launch, 1.2% after), then generative AI (0.7% before, 7.8% after, peaking near 20% in 2023), then AI agents from 2025. |
| 4b | `fig4b_topic_heatmap.png` | Heatmap, topic x quarter (see below). Table: `out_extended/topic_first_appearance.csv`. |
| 5 | `fig5_tone_calls_vs_10k.png` | Tone of AI sentences (off-the-shelf FinBERT): prepared remarks +0.46, Q&A +0.20, 10-K risk factors -0.17 (2023+). **Mostly genre**: ordinary sentences score +0.35, +0.17, -0.26 in the same sources, so the AI-specific effect is about +0.12 in prepared remarks, +0.03 in Q&A and +0.09 in 10-K risk factors. |
| 6 | `fig6_exploratory_opportunity_vs_risk.png` | **Exploratory, present with its caveats.** Share of AI sentences a fine-tuned FinBERT flags as AI-opportunity or AI-risk. Calls are flagged mostly as opportunity (prepared remarks ~83%, Q&A ~63%) and rarely as risk (~6%); 10-K risk factors are the reverse (risk ~84-88%, opportunity ~28-42%). The Q&A opportunity share drifts down from ~70-80% in 2022-23 to ~37% by 2026 Q2. See caveat 6 before drawing conclusions. |

## What the pre-launch calls changed (what to say if Jason asks about Nvidia or chips)

- **Nvidia was already talking about AI before ChatGPT**: 22%, 22%, 15%, 15% of its calls (Feb to Nov 2022), then 26% at the first post-launch call. "NVIDIA stack" (GPUs, Blackwell/Hopper, CUDA) is 23% of its pre-launch AI talk. Earlier drafts only looked like Nvidia started at the launch because its pre-launch calls were missing.
- **Nvidia also used the phrase "generative AI" before the launch**: 5 sentences in 2022 (for example its Nov 2022 call), which are the only pre-launch generative-AI mentions in the data. Earlier drafts said "zero"; that was wrong.
- **The jump is not identical everywhere.** At the first post-launch call (calendar 2022 Q4): Alphabet 4.6% to 16.2%, Microsoft 4.5% to 10.1%, Nvidia 14.6% to 26.1%, Tesla 3.7% to 7.2%; Meta 6.9% to 6.7% (it moves in 2023 Q1); Apple 0.0% to 0.4% (it moves in 2024).
- **Tesla's AI talk before the launch was mostly autonomy** (69% of its AI sentences), not general AI.
- **Amazon has no pre/post comparison**: its calls are Whisper machine transcripts with non-sentence units (0 to 1% AI before the launch), so it stays out of pooled lines.
- We cannot separate ChatGPT from other late-2022 and early-2023 AI events in the same window.

## How to read the heatmaps (and why they matter)

**Fig 2: company x quarter, each cell = % of that call that is about AI.**
- *A clear shift, but staggered.* Nearly every firm ends far higher, but the step is not one date for all: Alphabet, Microsoft, Nvidia and Tesla step up at the first post-launch call, Meta a quarter later, Apple only in 2024. That pattern fits ChatGPT acting through each firm's own products and timing, not a single shared switch. Nvidia is the exception: it was high before the launch.
- *Different levels.* Nvidia 15 to 43%, Alphabet/Microsoft/Meta 20 to 33%, Tesla and Amazon around 15 to 20%, Apple mostly under 10%.
- *Persistence.* Cells stay dark after the step, so it is a level change, not a one-quarter fad. Alphabet and Meta keep climbing; Nvidia peaked in 2025 Q1 (43%) and is lower now (29%).
- *Limits.* It is a share of the call, so it measures attention, not adoption or spending. Cells marked * use unit types that are not comparable (all of Amazon, some Apple and Tesla calls).

**Fig 4b: topic x quarter, each cell = % of that quarter's AI sentences that mention the topic.**
- *It shows what the AI talk is about, not just how much.* Machine learning dominates 2021-22 and fades; generative AI jumps at the launch (about 17 to 20% of AI sentences in 2023) and then declines as AI agents take over in 2025.
- *Named products show diffusion order.* Copilot and OpenAI appear before the launch (Microsoft), Gemini and Llama appear in 2023, Apple Intelligence in 2024, DeepSeek in one or two quarters (Q4 2024 / Q1 2025), each lighting up at the firm that owns it.
- *Compute never goes away.* The "training & inference compute" row is on throughout, mostly 5 to 12%, so the infrastructure story runs under the application story.
- *Limits.* Rows are independent (one sentence can mention several topics) and topics come from a hand-written pattern list.

## Caveats to say out loud

1. **Pre-launch sources are mixed.** The 17 added calls are not yet approved by Advik (see the sources note). The before/after figure pools sentence-comparable calls only: 23 pre-launch and 83 post-launch calls across six firms.
2. **Units are not all sentences.** Amazon (Whisper lines), 7 caption-segment calls and some Apple/Tesla calls use different units, so their shares are not comparable. They are hollow markers in Fig 1b, starred in Fig 2, and excluded from pooled lines and the tone figure.
3. **The ChatGPT date.** Calls for calendar Q4 2022 were held Jan-Feb 2023, so they are the first post-launch calls. AI share was already rising through 2022 at some firms.
4. **Tone is generic.** `ProsusAI/finbert` was not fine-tuned on this project. It measures financial-news-style positivity, not "AI opportunity vs risk". The 10-K sample is small (682 AI sentences, 72 filings); Alphabet filings start 2024 and Meta 2025.
5. **Filter is not validated.** Advik's AI sentence filter has no measured precision or recall yet. Chip and infrastructure sentences that never say "AI" are outside the AI numerator, so Nvidia's and Tesla's AI shares are understated.
6. **The fine-tuned model behind Fig 6 is exploratory and confounded.** FinBERT was fine-tuned on `derived/annotation_complete_labeled.csv` (held-out-company test AUC about 0.95). But those 1,200 labels are all **Claude-generated and unreviewed** (`label_source = claude_blind_*`). The `coder_id` values AK/TA were randomly assigned and are **not** human coders, so do not describe the labels as human annotation. "Risk" labels come overwhelmingly from Item 1A, so the model partly learns risk-factor style: it flags about 86% of 10-K AI sentences as risk and about 83% of call sentences as opportunity. Thresholds were tuned on only 80 validation passages. The model was retrained for the extended data (test AUC 0.95 opportunity, 0.94 risk on held-out companies CRM, NVDA, TSLA, VZ), and retraining gives slightly different levels from the earlier run (opportunity 83%/63% now vs 89%/75% before on prepared remarks/Q&A), which is another reason to read trends, not levels. Fig 6 carries these caveats on the image.

## Reproduce

```
pip install torch transformers nltk==3.10.0   # nltk 3.10.0 + punkt_tab reproduces Advik's committed CSVs exactly
# original 116 calls (committed data)
python3 analysis_calls/01_timeseries.py && python3 analysis_calls/04_network.py
python3 analysis_calls/02_finbert_tone.py && python3 analysis_calls/02b_baseline_tone.py && python3 analysis_calls/05_tone_figures.py
# extended 133 calls: same scripts with
CANON_DIR=earnings_calls_canonical_extended OUT_DIR=analysis_calls/out_extended FIG_DIR=figures_calls_extended \
  CALLS_DIR=<scratch copy of earnings_calls/ with the extras added> python3 analysis_calls/<script>.py
python3 analysis_calls/06_obsidian_vault.py   # Obsidian vault (currently built from the extended data)
python3 analysis_calls/03_finetune_predict.py # exploratory; retrains FinBERT (~12 min), then 05_tone_figures.py draws fig6
```
Seeds fixed; the first run downloads `ProsusAI/finbert` from Hugging Face.

## Next steps (after this meeting)

1. Get Advik's decision on the 17 added calls and sources, then merge or drop them in his pipeline.
2. Gate 5: review the 150-row sample (`earnings_calls_canonical/manual_review_sample.csv`) to get real filter precision/recall; re-check Nvidia/Tesla with chip and autonomy terms counted.
3. Hand-label a few hundred call sentences for opportunity vs risk, then fine-tune on those. Replace the SEC-passage labels.
4. Backfill 10-K Item 1A for Alphabet (2021-23) and Meta (2021-24) so the risk-factor comparison covers the full window. Re-extract the two misplaced-label Meta PDFs.
5. Add Item 1A topic modeling (LDA) over five years, then scale to the S&P 500 (industries need that).
