# AI-Washing Research Scraper

A small, well-scoped data-collection pipeline for the "AI washing in corporate
layoffs" research project. It pulls raw disclosure text from **public** sources,
normalizes it to one schema, groups and deduplicates it into per-category
CSV/JSON files, and uploads that human-readable dataset to Google Drive — the
raw material you'll hand-label to train the disclosure classifier described in
the methods extension.

This is a research tool for a methods appendix, not a production system. Keep it
simple and be able to explain every step.

## What it collects

| Source | What | Legitimacy |
|---|---|---|
| SEC EDGAR 10-K / 10-Q | Item 1A Risk Factors, Item 7 MD&A (section text) | Fully public; SEC encourages programmatic access with a User-Agent |
| SEC EDGAR 8-K | EX-99 press-release / prepared-remarks exhibits | Fully public |
| Challenger, Gray & Christmas | Monthly job-cuts blog posts (AI-attribution stats) | The firm's own public blog |
| Earnings-call transcripts | **URLs + short Google snippets only**, via Serper | See the copyright note below |

## ⚠️ Copyright / Terms-of-Service boundary (read this)

Full earnings-call transcripts on **Motley Fool / Seeking Alpha** are paywalled
and ToS-protected. This pipeline **does not** scrape their full text, and you
should not extend it to do so — that's a copyright/ToS problem, not just a
technical one.

- `sources/serper_search.py` retrieves only the **URL and the short snippet**
  Google already shows, so you can open and read each source **manually**.
- For automatable, fully-public earnings-call-adjacent text, use the **8-K
  EX-99 exhibits** on EDGAR (companies often file prepared remarks / the
  earnings press release there). `edgar.py` already does this.

SEC EDGAR and Challenger's own public blog are fair game. Anything behind a
paywall is limited to what a normal person could read and copy by hand.

## Setup (runs locally or in Colab — no database required)

1. **Install dependencies:**
   ```
   pip install -r requirements.txt
   ```
2. **Get a Serper key (optional):** sign up at <https://serper.dev> (~2,500
   free queries on signup) and copy your API key. Only used for transcript
   URL lookups.
3. **Create a Google Drive OAuth client (one-time, in Google Cloud Console):**
   - Create/select a project, enable the **Google Drive API**.
   - Under "Credentials", create an OAuth client ID of type **Desktop app**.
   - Download its JSON and save it as `credentials.json` next to `main.py`
     (or point `GDRIVE_CREDENTIALS_PATH` at wherever you put it).
   - The first time `main.py` runs, it opens a browser — sign in as
     **advikkashyap1@gmail.com** or **ecfarmer12@gmail.com** and grant
     access. The script creates/reuses a folder named **"Georgetown
     Research"** in that account's Drive and uploads the dataset there. A
     refresh token is cached at `token.json` so later runs don't need the
     browser again.
4. **Set environment variables:**
   ```
   set SEC_USER_AGENT=Your Name research your@email.com   REM required by SEC
   set SERPER_API_KEY=your-serper-key                     REM optional
   set EXPORT_DIR=./export                                REM local staging dir before upload
   ```
   (PowerShell: `$env:SEC_USER_AGENT = "..."`, etc.)
   > `SEC_USER_AGENT` must contain a real name + email. SEC blocks anonymous
   > requests.

## Running it

```
python main.py --companies IBM,DELL,SAP --forms 10-K,8-K

# add 10-Qs and the Challenger job-cuts reports; skip Serper
python main.py --companies IBM,DELL --forms 10-K,10-Q,8-K --challenger --no-serper

# just refresh the Challenger reports (first 3 listing pages)
python main.py --companies "" --challenger --challenger-pages 3

# stage files locally without touching Drive
python main.py --companies IBM --no-drive-upload
```

Output: documents are grouped by `source_type` and deduped by re-reading
whatever's already in `$EXPORT_DIR` — the `source_type + company + url +
section` hash prevents duplicate rows across runs. Each group gets its own
pair of files:

```
$EXPORT_DIR/ai_washing_10-K.csv / .json
$EXPORT_DIR/ai_washing_10-Q.csv / .json
$EXPORT_DIR/ai_washing_8-K.csv / .json
$EXPORT_DIR/ai_washing_challenger_report.csv / .json
$EXPORT_DIR/ai_washing_earnings_call_snippet.csv / .json
```

After export, all files in `$EXPORT_DIR` are uploaded (created or updated by
name) into the **"Georgetown Research"** Drive folder, unless
`--no-drive-upload` is passed.

## Data schema

Every stored document:
```json
{
  "doc_id": "auto hash",
  "company": "IBM",
  "ticker": "IBM",
  "source_type": "10-K | 10-Q | 8-K | challenger_report | earnings_call_snippet",
  "filing_date": "2026-02-01",
  "section": "Item 1A Risk Factors | Item 7 MD&A | prepared_remarks | job_cuts_report | search_snippet",
  "url": "https://...",
  "text": "the pulled text",
  "retrieved_at": "auto ISO datetime"
}
```

## Project layout

```
gtown_research/
├── config.py              # env vars + endpoint constants + validate()
├── storage.py             # file-based dedup + grouped CSV/JSON export
├── gdrive.py               # OAuth + upload export dir to Drive
├── normalize.py           # raw text -> schema
├── main.py                # orchestration + CLI
├── requirements.txt
├── edgar.py               # full-text search, submissions, section extract, 8-K exhibits
├── challenger.py          # public job-cuts blog scraper
└── serper_search.py       # transcript URL/snippet lookup (no paywall scraping)
```

## Things to verify when you first run it (they can't be tested offline)

- **EDGAR full-text search response shape.** If `edgar.full_text_search`
  returns nothing on a query you can see working in the EDGAR web UI, print the
  raw JSON and adjust the `hits.hits` parsing.
- **10-K section extraction is heuristic.** `edgar.extract_sections` slices by
  Item-heading regexes and uses the *last* heading occurrence to skip the table
  of contents. Spot-check the extracted Item 1A / Item 7 text on a couple of
  real filings; some filers use layouts that need the patterns tweaked.
- **Challenger blog selectors.** `challenger.list_reports` guesses common blog
  markup. If the listing comes back empty, inspect the live page and adjust the
  `.select(...)` calls.

## Future additions (not built yet)

- **WARN Act filings** — state-level public layoff notices; a legitimate,
  public source worth adding later.
