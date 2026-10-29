# Advik's half of the S&P 493 data pull (half 2)

This file is written for the Claude Code agent on Advik's laptop. Give it this whole file as its
task. It covers everything for half 2: setup, finding transcripts, downloading, filtering,
checking, and handing back. Tanush's laptop is doing half 1 with the same script at the same time.

**Read [SEARCH_AND_PULL_METHOD.md](SEARCH_AND_PULL_METHOD.md) first.** It has the full method
and the reasons behind it. This file is the to-do list. If the two ever disagree, the method doc
wins: stop and ask.

---

## What this is for

- **The ask.** Prof. Schloetzer (Georgetown) wants the Mag 7 earnings-call AI study extended to
  the other 493 S&P 500 companies, quickly. The question is whether AI talk on earnings calls
  outside big tech rose, plateaued, or fell after ChatGPT (2022-11-30).
- **The split.** The 493 firms are split in two. **You do half 2: the 246 firms with
  `assigned_half = 2` in `sp493/universe.csv`.**
- **The source.** Everything comes from Motley Fool transcripts. Fool is the one source that
  covers most of the S&P 500 in a layout our existing filter already parses.
- **The two tiers.**
  - *Tier A:* Fool's verbatim pages, which are the main corpus.
  - *Tier B:* Fool's 2025+ LLM-written pages. These are saved separately and **not** filtered.

## Rules (do not break these)

1. **Only half 2.** Never run `--half 1`, and never write into a ticker folder that belongs to
   half 1. Every output file you create starts with `half2_` or sits in a half-2 ticker folder.
2. **Never edit `filter_earnings_calls.py`, `sp493/sp493_pull.py`, `sp493/universe.csv` or
   `sp493/ENVIRONMENT.txt`.** If something in them looks wrong, stop and report it. Do not patch
   it. Both halves must run identical code, or the corpus is not consistent.
3. **Never run `sp493_pull.py universe`.** The universe file is already built, and rebuilding it
   would change the split.
4. **Never write, edit, summarize, rename, move or delete transcript text.** The script never
   overwrites a raw file, so don't work around that.
5. **No other sources.** Do not fill gaps from Seeking Alpha, company IR sites, YouTube, Whisper
   or anything else in this round. Missing quarters stay missing and are reported.
6. **Be polite to fool.com.** Run one script at a time and do not lower `FOOL_DELAY` (2.5 s).
   Do not run two downloads in parallel.
7. **No claims.** This is data collection only. Don't write up findings or say anything about
   margins, layoffs or causal effects.
8. **Commit only to branch `sp493-half2`.** Never commit directly to `main`.

---

## Step 0: Setup

```bash
cd ai-washing-research
git checkout main && git pull origin main          # Tanush pushed sp493/ setup files to main
git checkout -b sp493-half2
python3 -m venv .venv && source .venv/bin/activate # skip if .venv already exists
pip install "requests>=2.31" "beautifulsoup4>=4.12" "nltk==3.10.2"
python -c "import nltk; nltk.download('punkt_tab')"
```

- **nltk must be exactly the version in `sp493/ENVIRONMENT.txt` (3.10.2).** Sentence splitting
  depends on it.
- **These files must exist before you go on:**
  - `sp493/sp493_pull.py`
  - `sp493/universe.csv`
  - `sp493/universe.sha256`
  - `sp493/ENVIRONMENT.txt`
  - `sp493/SEARCH_AND_PULL_METHOD.md`
  - `filter_earnings_calls.py`
  - the committed Mag 7 folders `earnings_calls/nvidia/`, `earnings_calls/tesla/` and
    `earnings_calls_ai_only/_stats.json`

  If any are missing, stop and ask Tanush to push.

## Step 1: Self-test (must fully pass)

```bash
python sp493/sp493_pull.py selftest
```

All five lines must say `PASS`:

| Check | What it proves |
|---|---|
| universe.csv matches universe.sha256 | Same 493 firms and same split as Tanush |
| nltk version equals ENVIRONMENT.txt | Same sentence splitter |
| filter_earnings_calls.py unchanged | Same filter code |
| converter reproduces committed nvidia_FY24_Q1.md body | Our Fool-to-text conversion matches the Mag 7 files exactly |
| filter reproduces committed counts on 16 Mag 7 Fool calls | Same AI counts as the Mag 7 corpus |

If any line fails, **stop**. Report the exact output to Tanush. Don't try to fix it.

## Step 2: Discover which firms have transcripts, before and after ChatGPT

```bash
python sp493/sp493_pull.py discover --half 2
```

- **What it does:** downloads 60 Fool monthly sitemaps (Nov 2021 to Oct 2026, about 3 minutes)
  and matches every transcript URL to the half-2 firms.
- **The output must include** `Mag 7 fiscal-year-end check: ... PASS`. If it says FAIL, stop.

**Expected scale.** Half 1 gave the numbers below; half 2 should be similar.

| Number | Half 1 |
|---|---|
| In-window URLs | about 2,400 |
| Firms with any URL | 244 of 247 |
| Firms with calls before and after ChatGPT | about 135 |
| Firms with calls after only | about 108 |

The "after only" count is high because Fool has no 2021–2023 pages for many firms; that is real,
not a bug. If your numbers are wildly different (for example under 1,000 URLs), stop and report.

**Review these files before downloading:**

- **`sp493/coverage/half2_name_check.csv`.** These are URLs matched on ticker where Fool uses a
  short or old name (`amex` for AXP, `general-electric` for GE, `raytheon-technologies` for RTX),
  plus any name-only matches, which only happen when a ticker changed (as with Block SQ → XYZ).
  Skim every row. If a row is clearly a **different company** (for example "Black Stone
  Minerals" matched to Blackstone, or "Coca-Cola FEMSA" to Coca-Cola), list it in your report.
  **Do not edit any CSV.** We'll fix the matching in the script for both halves.
- **`sp493/coverage/half2_fiscal_year_ends.csv`.** Rows with `agree = False` are expected for
  firms whose quarters aren't three calendar months (Costco), firms with only one or two Fool
  calls, firms that changed fiscal year, and firms with many late backfills. The SEC value is the
  one used. Just list the tickers in your report.

## Step 3: Download (about 1.5 to 2 hours, run in the background)

```bash
python -u sp493/sp493_pull.py download --half 2 > cache/sp493_sources/download_half2.log 2>&1
```

- **Run it in the background** and check `cache/sp493_sources/download_half2.log` now and then.
  It prints a line every 25 pages and on any non-200 status.
- **It can be resumed.** If it stops (network drop, laptop sleep, or `5 failures in a row`), wait
  10 minutes and run the same command again. Pages already cached are skipped. If it stops on
  HTTP 403 or 429 more than twice, stop and report; don't try to get around a block.
- **Keep the laptop awake and plugged in** while it runs.
- **When it finishes it writes:**
  - `sp493/earnings_calls/<ticker>/<ticker>_<period>.md` for Tier A
  - `sp493/earnings_calls_fool_llm/<ticker>/...` for Tier B
  - `sp493/coverage/half2_calls.csv`
  - `sp493/coverage/half2_availability.csv`
  - `sp493/acquisition/half2_results.jsonl`
- **The last line of the log** looks like
  `raw files written; availability for 246 firms x 19 quarters: {...}`. Half 1 got
  `tierA 1276, tierB 873, missing 2544`, and half 2 should be similar.
- **If you ran Step 3 with a copy of `sp493_pull.py` from before Tanush's date fix:** that version
  misdated Fool backfills, for example Ametek Q3 2024 filed as 2026. Pull the fixed script, then
  delete only the *generated* outputs:
  - `sp493/earnings_calls/`
  - `sp493/earnings_calls_fool_llm/`
  - `sp493/earnings_calls_ai_only/`
  - `sp493/coverage/half2_calls.csv`
  - `sp493/coverage/half2_availability.csv`
  - `sp493/coverage/half2_call_units.csv`
  - `sp493/coverage/half2_coverage_summary.csv`

  Then re-run Step 3. Every page is already cached, so it rebuilds in about a minute without
  downloading anything. Never delete `cache/` or `acquisition/`.

**Spot-check after the download.** Do all of these and put the answers in your report:

1. **Open three random Tier A files.** Each should have the metadata block, a `---` line, then
   `Prepared Remarks:`, speaker lines like `Name -- Title`, `Questions & Answers:`, and a
   `Call participants:` list at the end.
2. **Open one Tier B file.** Its header should carry the `Quality warning` line.
3. **Look at `half2_calls.csv` `status` counts.** `ok` should dominate. Report the counts of
   `duplicate of ...`, `outside window`, `unknown layout`, `not a main earnings call`, and
   `no fiscal quarter in title or slug`.
4. **Count rows with `label_agrees = False` in `half2_calls.csv`.** These are calls where the
   calendar quarter from the call date and from Fool's fiscal label differ. Report the count and
   five examples, and don't change anything.

## Step 4: Filter the Tier A transcripts

```bash
python sp493/sp493_pull.py filter --half 2
```

- **What it does:** runs `filter_earnings_calls.process_file` unchanged on every Tier A file. The
  last line reads `filtered N Tier A calls; M with parse flags`.
- **It writes:**
  - `sp493/earnings_calls_ai_only/<ticker>/<stem>_ai.md`
  - `sp493/earnings_calls_ai_only/_stats_half2.json`
  - `sp493/coverage/half2_call_units.csv`
- **Parse flags.** Most flags will say `N units, outside the typical 400-900`. That is fine for
  short or long calls. Report how many files have each other flag, especially
  `Q&A start not detected` and `PARSE FAILED`. **Tier B is not filtered**, by design.

## Step 5: Coverage report

```bash
python sp493/sp493_pull.py report --half 2
```

This prints:

- how many half-2 firms have Tier A calls both before and after ChatGPT
- how many have calls before only or after only, and how many have none
- calls per calendar quarter (Tier A / Tier B / missing)

It also writes `sp493/coverage/half2_coverage_summary.csv`. Copy the printed output into your
report.

For comparison, half 1 got:

| Measure | Half 1 |
|---|---|
| Firms with Tier A calls both before and after ChatGPT | 93 |
| Before only | 41 |
| After only | 13 |
| No Tier A call at all | 100 |

Tier A stops at 2025 Q1. Everything after that is Tier B, which reflects Fool's layout switch, not
a bug.

## Step 6: Commit and hand back

```bash
git add sp493/coverage/half2_* sp493/acquisition/half2_* sp493/earnings_calls/ \
        sp493/earnings_calls_fool_llm/ sp493/earnings_calls_ai_only/
git status        # only half-2 files and half-2 ticker folders; nothing else, no cache/
git commit -m "S&P 493 half 2: Fool transcripts, availability, filter output"
git push -u origin sp493-half2
```

**Check `git status` before committing.** It must show no changes to tracked files outside
`sp493/`, and no `cache/` files (cache is gitignored; keep it that way). If `git status` shows a
modified script or universe file, **do not commit it**. Report it instead.

## Report back to Tanush

Send this, filled in:

```
Half 2 done (branch sp493-half2, commit <hash>)
selftest: all PASS (paste output)
discover: <URLs in window>, <firms with any URL>/246, before+after <n>, after only <n>, none <n>
name_check rows that look like a different company: <list or "none">
fiscal year end disagreements: <tickers>
download: <pages fetched>, non-200: <counts by status>, stopped/resumed: <yes/no, how many times>
calls.csv status counts: <ok / duplicate / outside window / unknown layout / ...>
label_agrees = False: <count>, examples: <5 rows>
Tier A files: <n>, Tier B files: <n>
filter: <N> calls, parse flags: <counts by flag>
report output: <paste>
anything odd: <free text>
```

## If something goes wrong

| Problem | What to do |
|---|---|
| selftest fails | Stop. Send the output. Don't edit anything. |
| `Mag 7 fiscal-year-end check ... FAIL` | Stop and send the output. |
| HTTP 429 or 403 repeatedly | Stop. Wait at least an hour before one retry. Never lower the delay or change the user agent. |
| A ticker folder already exists with files you didn't make | Stop. It may be half 1's; check `assigned_half` for that ticker. |
| `KeyError` or crash in the script | Stop and send the traceback. Don't patch the script. |
| A transcript looks garbled or empty | Leave it. Note the file in your report. |
