# AI-sentence filter: method, rules, and validation

This folder holds one file per earnings-call transcript in `earnings_calls/`, reduced to the
sentences that are about AI. It is a first-stage, recall-oriented filter for later human
review. No labeling (opportunity / risk / efficiency / workforce) has been done.

Reproduce everything with:

```
python filter_earnings_calls.py              # writes every *_ai.md, INDEX.md, _stats.json
python filter_earnings_calls.py --validate   # writes _validation.json (numbers below)
```

Local Python only (nltk Punkt data already on disk). No network access, no APIs. Source files
in `earnings_calls/` are read, never modified.

## 1. Corpus actually processed

The brief described 54 transcripts from five companies. When the run was done the folder held
**98 transcripts from seven companies**. All 98 were processed:

| Company | Files | Source type (from each file's metadata) | Parser |
|---|---:|---|---|
| alphabet | 15 | Official IR PDF text; 7 files are one word per line (6 of them with a blank line after every word) | `alphabet` |
| amazon | 8 | Whisper machine transcript of the call audio, `[mm:ss]` segments, no speakers | `captions` (Whisper) |
| apple | 15 | YouTube auto-captions of third-party livestreams (Benzinga, Shacknews, EARNMOAR), no speakers | `captions` |
| meta | 15 | Official IR PDF text | `meta` |
| microsoft | 15 | Official IR transcript, `NAME:` labels | `msft` |
| nvidia | 15 | 6 FactSet CallStreet PDFs (FY26–FY27); 8 Motley Fool (FY23 Q4–FY25 Q4 except FY24 Q4); 1 Yahoo Finance YouTube captions (FY24 Q4) | `factset` / `fool` / `captions` |
| tesla | 15 | 9 Motley Fool; 6 YouTube auto-captions (5 Tesla's own upload, 2026 Q2 Benzinga) | `fool` / `captions` |

`Period` labels are copied unchanged: fiscal for Microsoft, Nvidia and Apple, calendar for
the others.

## 2. Output format

`earnings_calls_ai_only/<company>/<company>_<period>_ai.md`:

1. The source metadata block, verbatim, plus `- **Filter:** AI-sentence extraction, see FILTER_METHOD.md`.
2. `N AI sentences of M total`, a line with borderline counts, and (if any) a
   `Source/parse flags:` line.
3. `## Prepared remarks` and `## Q&A`. Inside each, a `### Speaker` header starts every time
   the speaker changes, so the call's order is preserved. Numbering runs continuously through
   each section.
4. `## Borderline: automation/robotics without an AI term` and
   `## Borderline: infrastructure without an AI term`. Each item is prefixed
   `[section · speaker]`.

Sentence flags: `⚑ uncertain` (only a weak term matched), `⚑ uncertain: safe-harbor`,
`⚑ context-dependent`, `⚑ long` (over 150 words; never cut).

Speaker labels use only what the same transcript states: the header line or label
(Meta, Alphabet, FactSet, Fool), the IR opening's "Name, title" list (Microsoft management),
and the operator's "…from the line of X with Firm" introductions (analyst firms). If a
transcript never gives a title or firm, the bare name is shown. Names are kept as each
transcript prints them, so variants such as "Ken Dorell" / "Kenneth Dorell" and
"Jen Hsun Huang" / "Jensen Huang" remain separate. All-caps Microsoft names are title-cased.

## 3. Text handling (verbatim rule)

Output text is the source text, changed only as follows:

- **Line re-flow.** Wrapped lines are joined with one space. A line ending in a single hyphen
  after a letter (a PDF wrap inside a compound, e.g. `year-over-` / `year`) is joined with no
  space.
- **Noise removed.** Page numbers; FactSet running headers (company line, call title,
  "Corrected Transcript", date, `1-877-FACTSET www.callstreet.com`, copyright), cover page,
  participant list and closing disclaimer; Motley Fool text after `Duration:` /
  `Call participants:` (roster, ads, related articles); Microsoft `END`; the title and date
  block before the first speaker; `[mm:ss]` timestamps; caption tags (`[Music]`,
  `[Applause]`, `[laughter]`, `[clears throat]`, the placeholder word `foreign` before
  `[Music]`); `>>` turn markers.
- **HTML entities decoded** in YouTube captions (`Q&amp;A` → `Q&A`, `&gt;&gt;` removed as a
  turn marker).
- **Nothing else.** Speech errors, transcription errors ("Genre AI", "Anat Ashkenazi" →
  "Debateneia", "AP Is"), and encoding damage (`we�ve`) are kept as they appear.

### Page numbers

- Meta: a paragraph that is only 1–3 digits. If the text before it has no final punctuation,
  the next paragraph is joined on (a sentence cut by the page break).
- Alphabet, wrapped-line layout and one-word-per-line layout (2024 Q1): a digit-only line
  followed by a blank line. Checked: each file gives a clean run 1..N.
- Alphabet, blank-after-every-word layout (2024 Q4, 2025 Q1–Q3): page numbers sit inline in
  the word stream with no layout cue ("…our 1 unique full-stack approach…"). Detector
  (`find_inline_pages`): page numbers must appear in order 1, 2, 3, …; for page n it considers
  bare tokens equal to n that are 150–900 words after page n−1. It rejects tokens after a
  product/version word (Gemini, Imagen, Veo, Pixel, TPU, …) or before Pro/Flash/Ultra/Nano. It
  scores the rest: +2 for final punctuation before, +1 for a capital after, −1 for a
  unit/conjunction after ("million", "years", "and", "to", …), −2 after an unpunctuated `$`
  amount. It takes the best candidate with score ≥ −1. It found 25, 21, 25 and 22 pages;
  page-to-page gaps are 213–478 words. **All 93 removed tokens were read in context and all are
  page breaks**, not quantities. Alphabet 2025 Q4 and 2026 Q2 contain no page numbers.
- FactSet: the running-header block, including its page number.

### Sentence splitting

nltk Punkt (`PunktTokenizer("english")`), with added abbreviations so it does not split on
`U.S.`, `U.K.`, `Inc.`, `vs.`, `Mr./Mrs./Ms./Dr.`, `No.`, `e.g.`, `i.e.`, `approx.`, `A.I.`,
`Corp.`, `Co.`, `Ltd.`, `Jr.`, `Sr.`, `St.`, `p.m.`, `a.m.`, and month abbreviations. Decimal
numbers (`$1.5 billion`, `3.2 billion`) are not split by Punkt. Sentences are split inside a
speaker turn, so sentences cut by a page break are rejoined first.

Machine transcripts need two extra rules:

- **Whisper (Amazon).** Only about 2% of Whisper segments end in punctuation, so Punkt alone
  produced 100–300-word run-ons. A new unit starts at a segment boundary when the previous
  segment has no final punctuation and the next segment starts with a capital letter.
  Punkt then splits inside each unit. Units are sentence-like but not true sentences. A
  sentence Whisper broke across a capitalized word is split in two (e.g. "…gain access to
  future" / "Anthropic models through Bedrock…").
- **Unpunctuated YouTube captions** (fewer than 1 `.?!` per 100 words): Apple FY23 Q1, FY23 Q2,
  FY23 Q4, FY24 Q1, FY24 Q2, FY24 Q3, FY25 Q1, and Tesla 2023 Q1. No sentence boundaries
  exist, so **the unit is one caption segment (~30 seconds, ~75 words)**. These files are
  flagged, and their counts are not comparable to sentence counts.

### Sections and speakers per format

| Format | Speakers | Where Q&A starts |
|---|---|---|
| meta | `Name, Title` line (≤10 words, title keyword, no final punctuation); inline `Name:` / `Operator:` | first Operator turn after management has spoken |
| msft | `NAME:` at line start (own line or inline) | sentence containing "let's/we'll/now … (go/move/turn/open) … to Q&A" |
| factset | dotted rule, then name line, then title line (trailing ` Q`/` A` dropped); inline `Operator:` | `QUESTION AND ANSWER SECTION` header |
| fool | `Name -- Title[ -- Firm -- Analyst]` line; bare name lines that appear in the file's `Call participants:` roster; `Operator` | `Questions & Answers:` header (Nvidia); otherwise (Tesla) the sentence containing "go/move/start/begin … (on/over/through/with) to investor / say.com / analyst / retail questions/Q&A" |
| alphabet | inline `Name, Title:` (title keyword required) or `Name (Firm):`; second pass matches the same labels even without a sentence end before them | first Operator turn after management has spoken |
| captions | none: `Speaker not labeled` | Apple: "may we have the first question" / "our first question is from"; Amazon, Nvidia: "first question" / "question comes from"; Tesla: the Tesla pattern above plus "questions on say.com relate" |

When the Q&A marker falls inside a turn, the split is at the start of the sentence that
contains it; the marker sentence goes to Q&A. In unpunctuated caption files the split is at
the marker itself, which can divide one caption segment in two.

**Livestream trimming (captions).** Transcript text starts at the earliest match of: "(good
afternoon/day …) welcome to (the) Apple/Tesla/Amazon/NVIDIA", "my name is Suhasini/Travis",
"conference is now being recorded", "speaking first today is Apple", "be followed by CFO",
"thank you for standing by". Everything before it (host chatter, music) is dropped; the count is
in the flags. Tesla ends after the last "that's all the time we have / look forward to talking
to you next quarter / thank you very much and goodbye" segment; Apple after "this does
conclude today's conference" if present; Amazon after "this concludes today's call".

## 4. What counts as an AI sentence

Matching is on the sentence text; `\b` = word boundary.

**Core terms** (sentence included, no flag):

- `AI` / `AIs` as an uppercase token not inside a word (so `AI5`, `AI-powered`, `AI's` match;
  `GenAI`, `OpenAI`, `xAI` are listed separately); `A.I.`
- `artificial (general) intelligence`, `GenAI`, `OpenAI` / `open ai`, `ChatGPT` / `chat gpt`,
  `Apple Intelligence`, `generative`, `agentic`, `AGI`, `superintelligence/-t`
- `machine learning`, `deep learning`, `neural net(s)/network(s)/engine(s)`, `LLM(s)`,
  `(large) language model(s)`, `computer vision`, `natural language processing`, `NLP`,
  `chatbot(s)`
- model phrases: `foundation/frontier/reasoning/multimodal/diffusion/open-source/open-weight/
  ranking/recommendation/retrieval/ML/trained/video-generation/image-generation/world model(s)`;
  `N billion/B/trillion parameter(s)`, `parameter model(s)`
- training/inference with a compute word: `training|inference` + `compute, cluster(s),
  run(s), workload(s), capacity, infrastructure, chip(s), cost(s), demand, token(s),
  request(s)`; `model(s) training/inference`; `train/training/trained … model(s)`
- named AI products, models, labs and chips (case-sensitive): ChatGPT, Copilot(s), Gemini,
  Gemma, Bard, Llama, Claude, Anthropic, Bedrock, Trainium, Inferentia, TPU(s), Nova,
  Amazon Q, Q Developer, DeepMind, DeepSeek, Grok, Mistral, Perplexity, NotebookLM, Imagen,
  Veo, Midjourney, Stable Diffusion, Sora, Phi / Phi-n, NIM(s), NeMo, TensorRT, GR00T, MTIA /
  "Training and Inference Accelerator", Maia, MAI, Emu, Movie Gen, Segment Anything,
  Stargate, AlphaFold, Dojo; plus `copilot`, `gemini`, `anthropic`, `deepseek` in any case
- **Machine transcripts only:** `ai` / `Ai` in any case. In Whisper and caption text the
  casing is unreliable, and these tokens were checked to mean AI ("harnessing Ai and machine
  learning"). In official and human transcripts, lowercase `ai` is counted as a false
  positive instead (see Validation).

Names added beyond the brief's list: Gemma, DeepMind, DeepSeek, Grok, Mistral, Perplexity,
NotebookLM, Imagen, Veo, Midjourney, Sora, Phi, NIM, NeMo, TensorRT, GR00T, MTIA, Maia, MAI,
Emu, Movie Gen, Segment Anything, Stargate, AlphaFold, Dojo, Apple Intelligence.

**Weak terms** (sentence included **with `⚑ uncertain`** when no core term matched):

- AI accelerator names: Blackwell, Hopper, Rubin, GB200/GB300, A100/H100/B100, H20, H200, DGX,
  HGX, NVLink, CUDA
- AI platform names: Foundry, Fairwater, Omniverse, Cosmos, Isaac, Dynamo, Siri, Private Cloud
  Compute
- Meta ads-model names: GEM, Andromeda, Lattice
- `agent(s)`, `inferenc*`, `token(s)`, `algorithm*`, `recommendation system(s)/engine(s)`,
  `model architecture/performance/capabilities/weights/parameters`
- bare `model(s)`, unless preceded by business, operating, financial, revenue, pricing,
  subscription, economic, cost, delivery, hybrid, partnership, retail, franchise,
  go-to-market, role, licensing, monetization, consumption, distribution, sales, service(s)
  or margin, and not followed by year / 3 / S / X / Y / lineup. **Turned off for Tesla and
  Apple**, where "model" almost always means a car or device model (Apple's
  "Apple Foundation models" is still caught by the core rule).
- `Alexa`; autonomy: Waymo, self-driving, autonom*, FSD, Autopilot, robotaxi, Cybercab

**Borderline sections** (kept but separated, not counted as AI):

- automation/robotics: `automat*`, `robot*`, `Optimus`, `humanoid*`
- infrastructure: `GPU(s)`, `data center(s)`, `capex`, `capital expenditure(s)`,
  `accelerated computing`, `compute`, `server(s)`, `supercomput*`, `accelerator(s)`,
  `infrastructure`

A sentence with any core or weak term goes to the AI sections. Otherwise it goes to Borderline
automation if it has an automation term, else Borderline infrastructure if it has an
infrastructure term. Otherwise it is dropped.

**Other flags**

- `⚑ uncertain: safe-harbor`: an AI sentence that also contains forward-looking-statement
  language ("forward-looking statements", "safe harbor", "undertake no obligation", "could cause
  results to differ", "differ materially"). Kept for a human to decide rather than dropped.
- `⚑ context-dependent`: an AI sentence starting (optionally after And/So/But/Now/Well/Yes/
  Yeah/Okay) with It, It's, This, That, That's, These, Those, They, They're, Them or Which. Not
  applied to "This/That + month/year/quarter/week/time/season". It is a heuristic and marks
  candidates for the human to decide; no neighboring sentence is added.
- `⚑ long`: over 150 words.

**False positives excluded.** In non-machine transcripts, `ai`/`Ai`/`aI` tokens that are not
uppercase `AI`, and `Mr./Ms./Mrs./Dr. Ai`, are not counted as AI and are tallied. Word
boundaries prevent matches inside other words (e.g. `said`, `fulfillment` do not hit `AI` or
`LLM`).

## 5. Known limitations

- **Apple is not an official transcript.** All 15 Apple files are YouTube auto-captions of
  livestreams. Seven are unpunctuated (units are ~30s caption segments). Apple FY23 Q1 begins
  mid-call, and Apple FY24 Q3 had 121 segments of host chatter before the call. Names and
  numbers are often garbled ("suas Chandra Mali"). Apple counts are not comparable to the
  other companies'.
- **No speakers for Amazon, Apple, Nvidia FY24 Q4 or Tesla's caption files.** Prepared vs Q&A
  is still separated using the operator/IR transition phrase.
- **Whisper units are approximate sentences** (see §3).
- **Weak terms are noisy by design.** Most `⚑ uncertain` sentences are genuinely about AI:
  bare "agents" in 2025–26, Nvidia chip names, Tesla FSD. A minority are not: device or
  fulfillment "algorithms", "tokens" in a non-AI sense. They are included because the brief
  asks for recall first.
- **Autonomy/FSD is weak, Optimus is borderline.** Following the brief, robotics without an AI
  word goes to Borderline. Tesla's heavy FSD/Optimus content is therefore split across
  `⚑ uncertain` and Borderline.
- **Context-dependent is a heuristic** based on the first word. It does not resolve
  antecedents.
- **Motley Fool and caption transcripts are third-party.** The metadata notes say minor errors
  are possible, and those errors are preserved.
- **Sentence counts** are outside the brief's 400–900 range for many files. That is expected
  for unpunctuated caption files and Whisper; see INDEX flags.

## Validation

_(filled in from `python filter_earnings_calls.py --validate`; seed recorded below)_
