# S&P 493 earnings calls: search and data-pull method

Written 2026-10-28. This file does two things. Section 2 records how the Mag 7 transcripts were
searched for and pulled, taken from `EARNINGS_CALL_SCOPE.md`, `earnings_calls/INDEX.md`,
`earnings_calls/ACQUISITION_LOG.md` and `earnings_calls_pre2022_extra/README.md`. Sections 3 to 5
set out how the same rules carry over to the other 493 S&P 500 companies, so the two laptops
running the pull produce one consistent corpus.

Scope note: `EARNINGS_CALL_SCOPE.md` §1 says S&P 500 expansion is out of scope until Gate 10 is
approved. Prof. Schloetzer asked for the S&P 493 extension on 2026-10-27. This pull is
exploratory until Advik signs off on it as a scope change.

---

## 1. Rules that never change

These are carried over from the Mag 7 pull unchanged.

- **Never write or edit transcript text by hand, and never summarize it.** Machine errors stay in.
- **Never overwrite a raw file.** Re-running a step skips files that already exist.
- **Every downloaded original is cached** (in `cache/`, which is gitignored) with its URL, HTTP
  status, byte size, SHA-256 and retrieval date logged.
- **Every raw file states its source in a metadata block** above a `---` line. The body below the
  line is the transcript text only.
- **Main earnings call only.** Follow-up calls, investor days and conferences are excluded.
- **Same filter code, read-only.** AI sentences are found by `filter_earnings_calls.py` exactly as
  committed. Neither laptop edits it.
- **No paywalled or login-only sources** (Seeking Alpha, FactSet resale, gurufocus, roic.ai and
  similar).

## 2. How the Mag 7 corpus was searched and pulled

### 2.1 Window

Calendar Q4 2021 through calendar Q2 2026, which is 19 calendar quarters. That covers 4 quarters
before ChatGPT (released 2022-11-30) and 15 after. Q2 2026 was the last quarter all seven firms had
reported. 7 × 19 = 133 expected calls.

Period labels were kept exactly as the source gives them: fiscal labels for fiscal-year firms
(`FY24_Q1`) and calendar labels for the others (`2024_Q1`). Each fiscal quarter was assigned to
the **calendar quarter that holds most of its months**, for pooling (scope §3).

### 2.2 Source order

For each call the first source available on this list was used:

| Order | Source | How it was found | Mag 7 calls that used it |
|---|---|---|---|
| 1 | Official company IR transcript (PDF, HTML or DOCX) | IR event feed `<ir-site>/feed/Event.svc/GetEventList`, IR event-detail pages, and known CDN path patterns (e.g. `s206.q4cdn.com/.../doc_financials/<yr>/<q>/..._Earnings_Transcript.pdf`) | Alphabet, Meta, Microsoft, Nvidia FY26 Q1 on |
| 2 | Motley Fool verbatim transcript (third-party, speaker-labeled) | `fool.com/earnings/call-transcripts/<yyyy>/<mm>/<dd>/<slug>/` | Nvidia FY23 Q4 to FY25 Q4, Tesla 2022 Q4 to 2024 Q4, 2 Apple calls, all pre-2022 extras for Apple, Nvidia and Tesla |
| 3 | YouTube auto-captions of the firm's own or a known livestream upload | YouTube search for the call; `[mm:ss]` caption segments | 13 Apple, 8 Tesla, Nvidia FY24 Q4 |
| 4 | Local Whisper transcript (faster-whisper `small.en`) of the official IR audio | Audio link in the IR event feed | All Amazon calls |

Two rules decided between sources:

- **Fool pages produced with an LLM were not used.** From 2025 on, Fool pages are LLM-written,
  so Tesla 2025 Q1 to 2026 Q2 stayed on captions instead.
- **Third-party and archive copies need approval.** Fool, and the archive.org copy of Alphabet
  2021 Q4, were used only for the pre-2022 extras. They sit in a separate folder
  (`earnings_calls_pre2022_extra/`) pending Advik's approval.

### 2.3 Raw file format

Path: `earnings_calls/<company>/<company>_<period_label>.md`. Header, as in every Fool file:

```
# NVIDIA Corporation — Q1 FY24 Earnings Call (transcript)

- **Company:** NVIDIA (NVDA); fiscal year ends late January
- **Period:** Q1 FY24 (call held May 24, 2023)
- **Source:** third-party transcript, The Motley Fool — <url>
- **Note:** ... third-party (minor errors possible) ...

---

Prepared Remarks:

Operator

<paragraph>
...
Questions & Answers:
...
Call participants:

<Name> -- <Title>
```

The Fool body is the page's article text with one HTML block (`<h2>` or `<p>`) per line and a
blank line between blocks. Speaker lines read `Name -- Title`. `filter_earnings_calls.py` picks the
Fool parser from `Motley Fool` in the metadata or `Prepared Remarks:` in the body.

### 2.4 Filter

`filter_earnings_calls.py` follows the same steps for every call:

1. It strips non-call text.
2. It assigns each turn to prepared remarks or Q&A, and to a speaker.
3. It splits turns into sentences with nltk Punkt and its own abbreviation list.
4. It classifies each sentence as AI (core term, or weak term only, flagged uncertain),
   borderline automation, borderline infrastructure, or out.

The denominator is all valid units in the call. Counts are kept by section, and the rules are in
`earnings_calls_ai_only/FILTER_METHOD.md`. The canonical builder re-runs the same code with
nltk 3.10.0 and `punkt_tab`.

---

## 3. What changes for the S&P 493, and why

**Official IR text does not scale to 493 firms.** The filter has hand-built parsers for Meta,
Microsoft and Alphabet IR layouts. Every other company's IR PDF would need its own parser, and
many companies publish no transcript at all.

**Motley Fool covers most of the S&P 500 in one layout that the filter already parses.** Using one
source for every firm also addresses Prof. Schloetzer's weakness 2, that mixing sources could
confound the results.

Two measured facts shape the plan. Both were checked on 2026-10-28.

**Fool coverage changes a lot by month.** These counts are Fool transcript URLs per monthly
sitemap, across all companies, not just the S&P 500:

| Month | 2021-11 | 2022-05 | 2023-05 | 2024-05 | 2025-02 | 2025-04 | 2025-07 | 2025-11 | 2026-05 |
|---|---|---|---|---|---|---|---|---|---|
| Transcripts | 1,592 | 780 | 296 | 289 | 297 | **10** | 222 | 693 | 2,132 |

Coverage is thin in 2023 to 2025, and almost nothing exists for the April 2025 reporting season.
The availability matrix from Step 1 is the authoritative count for our firms.

**Fool switched layouts in 2025, and the new layout is not verbatim.** We compared Fool pages with
the official transcripts already in our corpus for the same calls. The test was the share of Fool
words that appear in order in the official text, using difflib on lowercased tokens.

| Call | Fool layout | Match to official |
|---|---|---|
| Meta 2024 Q3 | old: `Prepared Remarks:`, `Name -- Title` | 96.6% |
| Microsoft FY25 Q1 | old | 93.9% |
| Alphabet 2025 Q2 | new: LLM summary, then `Full Conference Call Transcript`, `Name:` labels | 89.4% |
| Alphabet 2026 Q1 | new | 89.1% |
| Microsoft FY26 Q3 | new | 86.8% |

New-layout pages:

- drop the IR opening and safe-harbor text
- reword sentences slightly (e.g. "to aid investors in further understanding" becomes "to aid in
  further understanding")
- often leave analysts unlabeled
- have no `Prepared Remarks:` or `Questions & Answers:` headers, so the existing Fool parser
  cannot read them

The page itself says "Parts of this article were created using Large Language Models".

**Decision for this pull.** The layout determines the tier:

| Tier | What | Folder | Filtered now? |
|---|---|---|---|
| A | Fool verbatim pages (old layout) | `sp493/earnings_calls/<ticker>/` | **Yes**, same filter, same as the Mag 7 Fool files |
| B | Fool LLM pages (new layout) | `sp493/earnings_calls_fool_llm/<ticker>/` | **No.** Pulled and kept, but not filtered or pooled until calibrated (§5) |
| gap | No Fool page | none | Not filled in this round. A later pass can use sources 1, 3 and 4 from §2.2 if the team approves |

This matches the Mag 7 rule that Fool LLM pages are not treated as verbatim text. It also means
the main series stops around early 2025 until Tier B is calibrated.

---

## 4. S&P 493 protocol

Everything runs through one script, `sp493/sp493_pull.py`, and both laptops run the same commit.

### 4.1 Universe and split

- **Source:** the Wikipedia "List of S&P 500 companies" constituents table, revision **1382178819**,
  fetched 2026-10-28. It has 503 tickers.
- **Removed:** the 8 Mag 7 tickers (AAPL, AMZN, GOOGL, GOOG, META, MSFT, NVDA, TSLA). That leaves
  495 tickers.
- **Dual-class firms count once.** FOXA/FOX and NWSA/NWS are each one company; the first listed
  ticker is kept. That leaves 493 companies.
- **Current members only.** Firms that left the index since 2021 are not included, and firms added
  later are tracked across the whole window. This is a known survivorship limitation.
- **Split:** sort by ticker and alternate. Rows 1, 3, 5 and so on are **half 1 (Tanush's laptop)**;
  rows 2, 4, 6 and so on are **half 2 (other laptop)**. Alternating keeps both halves balanced
  across the alphabet and sectors. The result is 247 firms in half 1 and 246 in half 2.
- **The file is the source of truth:** `sp493/universe.csv`, with an `assigned_half` column. It is
  built once and never rebuilt. The other laptop checks its SHA-256 (in `sp493/universe.sha256`)
  before starting. Current hash: `c95f8a1a…`.

### 4.2 Window and calendar mapping

- **Window:** the same as the Mag 7, calendar Q4 2021 through calendar Q2 2026 (19 quarters).
- **Fiscal year end:** taken from SEC EDGAR (`data.sec.gov/submissions/CIK##########.json`,
  `fiscalYearEnd`), only for this purpose: no filings are used. A year end in the first 7 days of a
  month counts as the previous month, which handles 52/53-week years. The lookup ran once, on half
  1's laptop, when `universe.csv` was built, and the values are stored in it. The other laptop
  never contacts SEC.
- **Fiscal year end cross-check:** `discover` also works out each firm's fiscal year end from
  Fool's own quarter labels and call dates. It is the month under which the most calls fall 7 to
  100 days after their quarter end. This inference must reproduce the Mag 7's known year ends
  (Apple Sep, Microsoft Jun, Nvidia Jan, the rest Dec), or the step stops. Firms where it disagrees
  with SEC are listed in `half<N>_fiscal_year_ends.csv` for review.
- **Calendar quarter:** the reported fiscal quarter is the latest fiscal quarter-end month at least
  7 days before the call date. It is assigned to the calendar quarter of its **middle month**,
  which is the same "most of its months" rule as scope §3. Checked against the Mag 7: Nvidia
  FY23 Q4 → 2022 Q4, Apple FY23 Q1 → 2022 Q4, Microsoft FY23 Q2 → 2022 Q4.
- **Period label:** as Fool gives it. Firms with a December year end get `2024_Q3`; all others
  get `FY24_Q3`.
- **Before or after ChatGPT:** `pre_chatgpt = call_date < 2022-11-30`.

### 4.3 Step 1: discovery (who has transcripts, before and after ChatGPT)

`python sp493/sp493_pull.py discover --half N`

1. **Sitemaps.** Download Fool's monthly sitemaps from `fool.com/sitemap/2021/11` to `2026/10`
   (60 files) and record the SHA-256 of each. Keep every `/earnings/call-transcripts/` URL, then
   parse its slug as `<name>-<ticker>-q<N>-<YYYY>-earn…`. Slugs are cut at about 50 characters;
   when the cut falls after the ticker, the cut-off tail (`-q1`, `-earn`, …) is dropped.
2. **Match on ticker.** A slug whose ticker equals a universe ticker is accepted. When Fool's name
   differs from ours, the URL is still accepted but listed in `half<N>_name_check.csv` for a skim.
   All 66 such cases in half 1 were the same company under a short or old name (`amex`, `ibm`,
   `general-electric`, `raytheon-technologies`).
3. **Match on name.** When the ticker changed (Block SQ → XYZ, Ball BLL → BALL, EchoStar
   SATS → ECHO), the full company name must match. The match is also only accepted for pages dated
   before the firm's first page under its current ticker. This rule removes look-alikes such as
   Black Stone Minerals (BSM) vs Blackstone, Coca-Cola FEMSA vs Coca-Cola, and NextEra Energy
   Partners vs NextEra.
4. **Calendar quarter from the fiscal label.** The quarter comes from Fool's fiscal label, not the
   URL date, because **Fool backfills old calls years later**. For example, Caterpillar Q4 2024 was
   posted 2026-04-14 in the LLM layout. The window test is inclusive (label read either way, plus
   URL date); Step 2 makes the exact call.
5. **Fiscal year end cross-check.** See §4.2.
6. **Outputs:** `half<N>_fool_urls.csv`, `half<N>_name_check.csv`, `half<N>_fiscal_year_ends.csv`
   and `half<N>_sitemaps.csv`.

Half 1 result: 2,404 in-window URLs covering 244 of 247 firms. 135 firms have calls both before
and after ChatGPT, 108 after only, and 4 none. Many firms have no Fool page at all for 2021–2023:
Caterpillar's own Fool quote page lists 2020 and then 2024 onward. This is a real coverage gap,
not a matching error.

### 4.4 Step 2: download

`python sp493/sp493_pull.py download --half N`

- **Polite fetching:** one request at a time, at least 2.5 s apart. The user agent names the
  project and a contact email. On HTTP 429 or 5xx the script backs off; it stops after 5 failures
  in a row.
- **Caching:** raw HTML goes to `cache/sp493_sources/<ticker>/<slug>.html.gz`. URL, status, bytes,
  SHA-256 and date go to `sp493/acquisition/half<N>_results.jsonl`.
- **Layout detection:** a page is old layout if it has `<h2>Prepared Remarks:</h2>`, new layout if
  it has `Full Conference Call Transcript`, and otherwise `unknown`, which is logged and not used.
- **Text conversion (Tier A):** take each `<h2>` and `<p>` in the article body, from
  `Prepared Remarks:` through the end of the `Call participants:` list. Write one block per line
  with a blank line between, unescape HTML, and strip tags. This reproduces the Mag 7 Fool file
  layout (checked by `selftest`, §4.6).
- **Text conversion (Tier B):** the same rule from `Full Conference Call Transcript` to the end of
  the article.
- **Calendar quarter:** comes from the call date printed on the page (old layout: the date line;
  new layout: the `DATE` section), using the §4.2 rule. If a page has only a publication date,
  the fiscal label is used instead. The fiscal label is also used if the page date is more than 120
  days after the quarter in its title under any reading of the fiscal year: that is a Fool backfill
  dated by its repost day. New-layout dates are abbreviated ("Oct. 31, 2024"). When a page has no
  quarter in its title or slug, the quarter comes from the real call date. `quarter_method`,
  `label_agrees` and `label_source` in `half<N>_calls.csv` record which rule was used.
  `label_agrees = False` with a real call date is normal for firms that changed fiscal year, such as
  Amcor, which moved from June to December.
- **Reposts with the same slug** share one cache file. The earliest URL is the one fetched and
  cited; later ones are logged as `duplicate`.
- **Picking one call per quarter:** keep the earliest main earnings call in each company-quarter,
  Tier A before Tier B. Other candidates are logged as `duplicate`.
- **Output:** `sp493/earnings_calls/<ticker>/<ticker>_<period>.md` (Tier A) or
  `sp493/earnings_calls_fool_llm/<ticker>/...` (Tier B). The metadata block follows §2.3 and adds
  ticker, CIK, fiscal year end, call date, calendar quarter, source SHA-256 and layout.
- **Coverage file:** `sp493/coverage/half<N>_availability.csv` has one row per company × calendar
  quarter, with status `tierA`, `tierB` or `missing`.

### 4.5 Step 3: filter

`python sp493/sp493_pull.py filter --half N`

- **Same code path as the Mag 7 Fool files.** Each Tier A file runs through
  `filter_earnings_calls.process_file(path, company=<ticker>)`, imported unchanged.
- **Outputs:**
  - `sp493/earnings_calls_ai_only/<ticker>/<stem>_ai.md`, the same rendering as the Mag 7
  - `sp493/earnings_calls_ai_only/_stats_half<N>.json`
  - `sp493/coverage/half<N>_call_units.csv`, with one row per call: total units and AI units,
    overall and by section, uncertain count, borderline counts, parse flags, `pre_chatgpt`,
    calendar quarter
- **Two behaviours that only affect Tesla and Apple.** The filter's per-company exceptions
  (`WEAK_OFF`) apply only to those two firms. For everyone else a bare "model" is a weak term, so
  it is kept and flagged uncertain. That affects carmakers (Ford, GM), whose "model" usually means
  a car model.
- **Q&A detection:** taken from the explicit `Questions & Answers:` header, as with the Mag 7 Fool
  files.

### 4.6 Checks both laptops must pass before Step 2

`python sp493/sp493_pull.py selftest`

1. `sp493/universe.csv` matches `sp493/universe.sha256`.
2. The installed nltk version equals the one recorded in `universe.csv`'s companion file
   `sp493/ENVIRONMENT.txt`.
3. Re-converting the cached Fool page for a Mag 7 Fool call (Nvidia FY24 Q1) reproduces the
   committed raw file's sentences.
4. Running the filter on committed Mag 7 Fool files reproduces their committed counts in
   `earnings_calls_ai_only/_stats.json`.

### 4.7 How the collected transcripts are organized

```
sp493/
├── SEARCH_AND_PULL_METHOD.md        this file
├── ADVIK_DATA.md                    step-by-step task for the half-2 agent (Advik's laptop)
├── sp493_pull.py                    the only script; both laptops run it unchanged
├── universe.csv                     493 firms, assigned_half 1 or 2 (built once, never rebuilt)
├── universe.sha256                  checked by selftest on both laptops
├── ENVIRONMENT.txt                  python / nltk / bs4 versions, filter SHA-256, Wikipedia revid
│
├── earnings_calls/                  TIER A raw transcripts (Fool verbatim), the main corpus
│   └── <folder>/<folder>_<period>.md        e.g. xom/xom_2024_Q3.md, a/a_FY24_Q1.md
├── earnings_calls_fool_llm/         TIER B raw transcripts (Fool LLM layout), kept apart, not filtered
│   └── <folder>/<folder>_<period>.md
├── earnings_calls_ai_only/          filter output, Tier A only
│   ├── <folder>/<folder>_<period>_ai.md
│   └── _stats_half<N>.json
│
├── coverage/                        one CSV set per half (half1_*, half2_*)
│   ├── half<N>_sitemaps.csv           every Fool sitemap read: bytes, SHA-256
│   ├── half<N>_fool_urls.csv          candidate transcript URLs matched to our firms
│   ├── half<N>_name_check.csv         matched on ticker but Fool uses a different name (amex, ibm): skim
│   ├── half<N>_fiscal_year_ends.csv   SEC fiscal year end vs the month implied by Fool's labels
│   ├── half<N>_calls.csv              every downloaded page: period, calendar quarter, call date,
│   │                                  tier, status (ok / duplicate / outside window / ...), file
│   ├── half<N>_availability.csv       firm × 19 calendar quarters: tierA / tierB / missing
│   ├── half<N>_coverage_summary.csv   per firm: Tier A quarters before / after ChatGPT
│   └── half<N>_call_units.csv         per Tier A call: total and AI units, overall and by section
└── acquisition/
    └── half<N>_results.jsonl        one line per page request: URL, HTTP status, bytes, SHA-256, time

cache/sp493_sources/                 gitignored, never committed
├── sitemaps/YYYY_MM.xml             Fool monthly sitemaps
├── fool/<folder>/<slug>.html.gz     every downloaded page, as served
├── sec/CIK##########.json           SEC submissions files (fiscal year end only)
└── selftest/                        the Mag 7 page used by selftest
```

Rules for this layout:

- **Folder names** are the lowercase ticker with `.` replaced by `-`, e.g. `BRK.B` → `brk-b` and
  `BF.B` → `bf-b`. They come from the `folder` column of `universe.csv`.
- **File names** are `<folder>_<period_label>.md`. The period label uses Fool's fiscal year and
  quarter: `2024_Q3` for firms with a December year end, `FY24_Q3` for everyone else, the same as
  the Mag 7 convention.
- **One raw file per firm × calendar quarter.** If Fool has two pages for the same quarter, the
  script keeps the earliest main call (Tier A before Tier B) and logs the others as `duplicate` in
  `half<N>_calls.csv`.
- **The calendar quarter, call date and source SHA-256 are in each file's header and in
  `half<N>_calls.csv`.** File names never change to match the calendar quarter. Pooling across
  firms uses `calendar_year` / `calendar_quarter`.
- **Never rename, move, edit or delete a raw file.** To redo a call, ask first; never overwrite it.
- **A laptop writes only its own half:** folders for its own tickers and `half<N>_*` files. It
  never runs another half's tickers.
- **Committing:** each laptop commits `sp493/` (everything except `cache/`) on its own branch,
  `sp493-half1` or `sp493-half2`, and nothing is pushed to `main` directly. The two branches touch
  disjoint files, so merging them has no conflicts.

### 4.8 Merging the halves

The halves have no tickers in common. Merging means merging the two branches; the
`earnings_calls*/` trees combine as they are. The pooled tables are the `half1_` and `half2_` CSVs
concatenated. No file exists on both laptops.

---

## 5. Open decisions (for Advik and Prof. Schloetzer)

1. **Tier B calibration.** Fool LLM pages exist for Alphabet, Microsoft and others for 2025 and
   2026, quarters where we also have official transcripts. Run the filter on both versions of the
   same calls and compare AI share by section. If they agree closely, Tier B can enter the main
   series with a source flag; otherwise it stays out.
2. **Filling gaps.** Firms or quarters with no Fool page could come from official IR text, YouTube
   captions or Whisper (§2.2, sources 1, 3 and 4). That is a much slower, per-company job.
3. **The scope change.** `EARNINGS_CALL_SCOPE.md` §1 needs a written amendment for the S&P 493.
4. **What may not be claimed.** Scope §8 applies unchanged: descriptive only, no claims about
   margins, layoffs or causal effects, and the filter is not validated. A "leading indicator"
   claim would need outcome data and its own design.
