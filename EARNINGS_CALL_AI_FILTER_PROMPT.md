# Task prompt: filter earnings-call transcripts down to AI sentences

Paste everything below the line into the other account's VS Code agent. Open the
`ai-washing-research` repo as the workspace first.

---

## 1. Project context (read this first)

This repo is a research project on **AI washing**: how large public companies
*talk about* AI, workforce, and productivity in their disclosures, and whether
that language is specific and evidenced or vague and promotional. The design
separates AI **opportunity**, **risk**, **efficiency**, and **workforce
reduction** as distinct signals, and contrasts formal SEC filings (10-K risk
factors, 8-Ks) with less formal earnings-call language.

So far the pipeline has:
- pulled SEC filings from EDGAR and built a passage dataset (8,990 candidate passages),
- labeled a 1,200-passage sample under a blinded LLM protocol (see
  `ANNOTATION_CODEBOOK.md`, `annotation_prompt.md`, `derived/annotation_complete_labeled.csv`),
- **just added earnings-call transcripts** for five companies in `earnings_calls/`.

The transcripts are the next text source. Before any labeling, each transcript
needs to be reduced to only the sentences that are about AI. That is your job.

Useful background if you want it: `9.17.26 current standing.md` (plain-language
status), `INTRO_REFERENCE.md`. You do not need to read the code.

## 2. The input

`earnings_calls/<company>/<company>_<period>.md` — 54 files, ~150k lines total.

| Company folder | Files | Period naming | Notes |
|---|---|---|---|
| `alphabet` | 15 | `2022_Q4` … `2026_Q2` | **Text is broken across lines, often one word per line.** Must be re-flowed before sentence splitting. |
| `amazon` | 3 | `2022_Q4`, `2023_Q1`, `2023_Q2` | **Machine (Whisper) transcript**, `[mm:ss]` timestamps, **no speaker labels**, lines are fragments, expect errors on names and numbers. |
| `meta` | 15 | `2022_Q4` … `2026_Q2` | Clean official PDFs converted to text; speaker name on its own line, then paragraphs. Page numbers appear as stray lines. |
| `microsoft` | 15 | `FY23_Q2` … `FY26_Q4` | Fiscal year ends June 30. Speakers shown as `NAME:` headers. |
| `nvidia` | 6 | `FY26_Q1` … `FY27_Q2` | FactSet CallStreet format: repeated headers/footers, page numbers, disclaimers. Fiscal year ends late January. |

Every file starts with a metadata block (company, ticker, period, source URL,
sometimes a note), then `---`, then the transcript body. **Preserve that
metadata in your output.** The `Period` labels are fiscal for Microsoft and
Nvidia and calendar for the others; do not convert or "fix" them.

`earnings_calls/alphabet/` is currently untracked in git. That is fine.

**Do not modify, rename, or delete anything in `earnings_calls/`.** It is the
raw source. All output goes somewhere new.

## 3. What to produce

Create a new directory `earnings_calls_ai_only/` with:

1. **One markdown file per transcript**, mirroring the layout:
   `earnings_calls_ai_only/<company>/<company>_<period>_ai.md`
2. **`earnings_calls_ai_only/INDEX.md`**: a table with one row per transcript
   (company, period, total sentences, AI sentences, % AI, any flags) plus
   company and overall totals.
3. **`earnings_calls_ai_only/FILTER_METHOD.md`**: the exact rules you applied,
   the term list, edge-case decisions, and known limitations. Anyone should be
   able to reproduce your output from this file.
4. **The script** you used: `filter_earnings_calls.py` at the repo root, so the
   run is reproducible and re-runnable.

### Format of each `_ai.md` file

Copy the metadata block from the source, add one line
`- **Filter:** AI-sentence extraction, see FILTER_METHOD.md`, then a summary
line (`N AI sentences of M total`), then the sentences grouped like this:

```
## Prepared remarks
### Sundar Pichai, CEO
1. <sentence, verbatim>
2. <sentence, verbatim>

## Q&A
### Analyst name, Firm
1. <sentence>
```

Rules for the content:
- **Verbatim.** Only whitespace and line-break repair are allowed. Do not
  paraphrase, correct, summarize, or fix the speaker's grammar.
- **Keep the speaker and the section** (prepared remarks vs. Q&A) for every
  sentence. Earlier work in this project found that AI risk language differs
  sharply by section, so this structure matters for later analysis. Where a
  source has no speaker labels (Amazon), use `Speaker not labeled` and still
  separate prepared remarks from Q&A if you can detect the turn (operator
  announcing questions). If you cannot, say so in the flags rather than guessing.
- **Keep original order** within each section.
- Do not include context sentences that are not themselves about AI. If a
  neighboring sentence is needed to make one intelligible (e.g. "It" with no
  antecedent), do not add it; instead, mark the sentence with `⚑ context-dependent`
  so the human can decide later.
- Include the operator/analyst questions if the sentence is about AI. Analysts'
  words count as AI sentences too; just attribute them correctly.

## 4. What counts as an "AI sentence"

A sentence is in if it is **about AI** in the ordinary sense: it names or
clearly refers to artificial intelligence as a technology, product, capability,
investment, risk, or workforce topic.

**Include** a sentence containing any of these (case-insensitive, word-boundary
aware):
- `AI`, `A.I.`, `artificial intelligence`, `generative AI`, `gen AI`, `genAI`,
  `agentic`, `AI agent(s)`
- `machine learning`, `deep learning`, `neural network(s)`, `LLM(s)`,
  `large language model(s)`, `foundation model(s)`, `frontier model(s)`,
  `inference`/`training` **only when** clearly about models (see edge cases)
- Named AI products and models: ChatGPT, OpenAI, Copilot (Microsoft 365
  Copilot, GitHub Copilot, etc.), Gemini, Bard, Llama, Meta AI, Claude,
  Anthropic, Bedrock, Trainium, Inferentia, Azure OpenAI, Vertex AI, TPU,
  Nova, Q Developer, Alexa+ when described as AI, etc. Use judgment for names
  not listed, and record any you add in `FILTER_METHOD.md`.
- AI hardware/infrastructure **when the sentence itself ties it to AI**: e.g.
  "demand for GPUs to train models", "AI data centers", "AI infrastructure",
  "AI factory", Nvidia Blackwell/Hopper described in an AI context.

**Edge cases: decide by these rules and log counts in `FILTER_METHOD.md`:**
- **Bare "automation"/"automate"/"robotics" with no AI term**: NOT an AI
  sentence. Put these in a separate section at the end of each file titled
  `## Borderline: automation/robotics without an AI term`, so they are kept
  but clearly separated. The project's earlier keyword retrieval conflated
  these with AI and produced false positives; do not repeat that.
- **GPU / data center / capex / accelerated computing with no AI word**: same
  treatment, into the `Borderline` section, labeled `infrastructure without an AI term`.
- **"AI" as a false positive**: e.g. initials, speaker names ("Mr. Ai"), the
  letters inside another token, "said" artifacts from OCR. Exclude and count them.
- **Safe-harbor / forward-looking-statement boilerplate that mentions AI**:
  include only if the sentence itself is about AI risk. Generic "factors that
  could cause results to differ" boilerplate is out.
- **Sentences that only name an AI product as a list item** (e.g. "…across
  Search, YouTube, and Gemini"): include. A sentence is either about AI or it
  is not; do not try to grade how substantively AI is discussed. **Do not
  assign opportunity/risk/efficiency labels. Labeling is a later, separate step.**
- **Numbers, tables, and pure financial readouts** with no AI term: exclude.

**Recall matters more than precision here.** This is a first-stage filter; a
human will prune it. When genuinely unsure whether a sentence is about AI,
include it and add `⚑ uncertain`. Do not silently drop borderline cases.

## 5. Sentence handling (get this right, it is where errors creep in)

- **Re-flow before splitting.** Alphabet and Amazon are fragmented. Join lines
  into paragraphs first (for Alphabet, rebuild from single words; for Amazon,
  strip `[mm:ss]` stamps and join fragments), *then* split into sentences.
- **Do not split on abbreviations or numbers**: `U.S.`, `Inc.`, `vs.`, `Mr.`,
  `No.`, `$1.5 billion`, `3.2 billion`, `Q1`, `e.g.`, `i.e.`, `approx.`. Use a
  proper sentence tokenizer (nltk punkt is already used in this repo, or
  spaCy) with a custom abbreviation list, and spot-check.
- **Strip noise**: page numbers, `Total Pages: N`, FactSet/CallStreet headers and
  footers, copyright lines, "This transcript is provided for the convenience of
  investors only" boilerplate, repeated running headers.
- **Sentences that span a page break** must be rejoined, not lost or cut.
- A very long sentence (over ~150 words, common in spoken transcripts) stays
  whole; do not chop it. Flag it with `⚑ long`.
- Identify speakers from the format of each company's files. Speaker labels
  differ per company, so write one small parser per format and test it on at
  least two files per company before running everything.

## 6. Quality checks you must run and report

Before declaring done:

1. **Coverage audit**: for each transcript, confirm the total extracted sentence
   count is plausible (a typical call is 400–900 sentences; flag anything far
   outside that). Flag any file where parsing clearly failed (zero speakers,
   zero sentences, all sentences in one section).
2. **Recall spot-check**: for **5 transcripts (at least one per company)**, take
   a raw `grep -i -c` count of each core AI term in the source, and confirm
   your output accounts for essentially every occurrence. Any term hit that is
   missing from the output needs a logged reason.
3. **Precision spot-check**: read **at least 30 randomly selected included
   sentences** across the corpus (use a fixed random seed and record it) and
   report how many are genuinely about AI.
4. **Verbatim check**: for a random sample of 50 output sentences, programmatically
   confirm each appears in the source text after whitespace normalization.
5. **Time coverage**: confirm every transcript file in `earnings_calls/` has a
   corresponding output file (54 of 54). List any that are missing and why.

Put the results of all five in `FILTER_METHOD.md` under a `## Validation` heading,
including numbers, not just "looks good."

## 7. Rules of engagement

- **Do not create or alter** anything outside `earnings_calls_ai_only/` and
  `filter_earnings_calls.py`. In particular, do not touch `derived/`, `export/`,
  `blind_annotation/`, any `*_CODEBOOK.md`, or existing scripts.
- **Do not commit or push.** Leave everything uncommitted for a human to review.
- **Do not call external APIs or use paid services.** This should be done with
  local Python and reading the files yourself. No web requests.
- **Do not fabricate.** If a file is unreadable or a transcript looks truncated
  or corrupted, record it in `INDEX.md` flags and move on. Do not fill gaps.
- **Do not label or analyze.** No sentiment, no opportunity/risk tags, no
  summaries of what each company said. The deliverable is the filtered text.
- Work **company by company**. After each company, pause and report: files
  processed, total vs. AI sentence counts, and any problems. Then continue.
  Do Meta first (cleanest format), then Microsoft, Nvidia, Alphabet, Amazon last.
- Final message: list what was produced, the validation numbers, every
  judgment call you made that the owner should double-check, and anything that
  surprised you.

## 8. Start

Begin with Meta: read `earnings_calls/meta/meta_2024_Q1.md`, write and test the
speaker parser and sentence splitter on it, show me the first 20 extracted AI
sentences plus the flagged ones, and wait for a thumbs-up on the format before
running the full corpus.
