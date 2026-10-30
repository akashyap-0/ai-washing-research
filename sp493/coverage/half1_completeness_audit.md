# Half 1 completeness audit (S&P 493, Motley Fool)

Audited 2026-10-29 on branch `sp493-half1` (commit 19fd2f9). Nothing in `sp493/`, `cache/` or any
script was changed. The only outputs are this file and three CSVs:

- `half1_audit_issues.csv`: 69 rows, one per affected firm-quarter or URL. Each row gives the
  current status, what it should be, the evidence and the fix.
- `half1_audit_missed_urls.csv`: 33 Fool transcript URLs that are in the cached sitemaps but
  were never matched to a half-1 firm.
- `half1_audit_quote_page_check.csv`: every transcript link on 16 Fool quote pages, checked
  against the sitemaps, the candidate list and the fetch log.

Network use: 20 requests to fool.com, one at a time, at least 4 s apart, with the specified
User-Agent. 16 were quote pages and 4 were transcript pages the pipeline never fetched. The
responses are kept in the scratchpad only, not in `cache/`.

## Verdict

**Tier A (the main series): yes, essentially complete relative to what Fool offers.**

- The sitemaps are complete. All 83 quote-page links dated inside the sitemap range are in the
  cached sitemaps.
- Every old-layout page that the sitemaps list for our firms was downloaded.
- The one Tier A defect is Costco. Four Costco verbatim calls were wrongly dropped as
  "duplicates", and two more sit in the wrong calendar quarter. This is a quarter-mapping bug,
  described below.
- The before/after firm counts (93 / 41 / 13 / 100) do not change under any of the fixes.

**Tier B (2025+ LLM pages): no.**

- **51 firm-quarters that Fool does have are marked `missing`.** Five bugs cause this: slug
  parsing, the case of the `Date` heading, same-slug cache collisions, an unretried 404, and the
  Costco and BRO quarter mapping.
- **14 filled slots hold the wrong call.**
  - 7 should be empty:
    - DG, ROST, TGT and CCI 2025 Q1, which hold calls placed a year or a quarter off
    - BRO 2025 Q1 and 2026 Q2
    - CME 2026 Q1, whose body is the Q4 2024 call
  - 7 should hold a different page:
    - TECH 2025 Q3, which holds a Minerals Technologies call
    - COST 2022 Q1, 2023 Q1 and 2026 Q1
    - BRO 2025 Q2–Q4
  - Two of the 14 are Tier A: COST 2022 Q1 and 2023 Q1.

If all fixes are applied, the corrected counts are Tier A 1,280, Tier B about 913 and missing
about 2,500, against the current 1,276, 873 and 2,544.

---

## 1. Candidate reconciliation (every URL accounted for)

| Step | Count | Notes |
|---|---|---|
| Candidate URLs in `half1_fool_urls.csv` | 2,413 | no duplicate URLs |
| Skipped by download (prelim window false and slug has a quarter) | 8 | DG, DLTR, LOW, LULU, ROST, TGT, WSM Q3 2021 (fiscal quarters ending Oct 2021, so CY 2021 Q3), and IR "Q3 2020" (URL 2021-11-06). **All are genuinely outside the window.** |
| Prelim false but downloaded anyway (no quarter in a truncated slug) | 1 | FIS Q3 2021, later `outside window` |
| Download candidates | 2,405 | |
| Fetched with HTTP 200 | 2,374 | 2,374 cache files; every one is referenced by a candidate; SHA-256 of every cache file matches `results.jsonl` |
| Fetched with HTTP 404 | 1 | EOG Q1 2026 `.../2026/05/06/eog-eog-q1-2026-earnings-call-transcript/`. **Transient: it returned 200 on 2026-10-30 and is still listed on EOG's quote page.** It was never retried, because the script counts a 404 as done. |
| Never fetched (same slug already cached) | 30 | parsed from the other URL's cache file |
| Rows in `half1_calls.csv` | 2,404 | 2,374 fetched + 30 same-slug rows |

Every `ok` row cites a URL that was actually fetched. The SHA-256 in its file header equals that
URL's fetch log and cache file (0 mismatches). No two `ok` rows share a file path.

**The 30 same-slug rows are not all reposts.**

- **27 are harmless.** These are 2026 LLM reposts of 2024 calls whose slug has a quarter (ZTS,
  AVGO, DVA, NKE, RTX, CAT, KO, BIIB, HAS, MRNA), or 07-30/08-03 pairs of Q2 2026 pages.
- **3 have a generic slug with no quarter in it.** I fetched each one:
  - **UNH `2026/01/27/unitedhealth-unh-earnings-call-transcript`:** the Q4 2025 call (Date
    Jan 27, 2026). The cached 01/26 page is the Q3 2025 call. **UNH 2025 Q4 is missed.**
  - **SBAC `2026/04/01/sba-communications-sbac-earnings-call-transcript`:** the Q4 2025 call
    (Feb 26, 2026). It was logged as a duplicate of the Nov 2025 page. **SBAC 2025 Q4 is
    missed.**
  - STZ `2026/04/14/constellation-brands-stz-earnings-transcript`: the Oct 3, 2024 call (FY25
    Q2), which is already Tier A. Harmless.

  In `half1_calls.csv`, these rows carry the other page's date and SHA.

## 2. Status checks

### (a) `outside window` (196 rows): all correct

- **98 rows are CY 2021 Q3, all Tier A with real call dates.** 92 calls are in Nov 2021 and 6 in
  Dec 2021. The December calls (AVGO, HRL, SNPS Q4 FY21; BF.B Q2 FY22; MRVL, VEEV Q3 FY22) all
  report quarters that end in October 2021, so their middle month is September.
- **98 rows are CY 2026 Q3, all Tier B.** 92 calls are in Oct 2026 (Q3 2026). 6 are in Sep 2026
  (ADBE Q3 FY26; COST, JBL, MU Q4 FY26; ORCL, PAYX Q1 FY27), and all of those report quarters
  ending in August 2026.
- **AMCR Q1 FY22 and APD "Q3 2021" disagree with their labels.** Both are calls from Nov 2021
  about the September 2021 quarter, so both are out under any reading.
- No plausible reading of any label puts an outside-window row in the window.

### (b) `duplicate` (52 rows)

- **37 are correct duplicates of the same call:**
  - 27 same-slug reposts
  - 8 Tier B copies of Tier A calls on the same date (BX, CNC×2, HCA, OTIS, SYF, TMUS, UPS)
  - EXR, two pages for the Feb 20, 2026 call
  - LOW: Fool labels the same May 20, 2026 call both "Q1 2026" and "Q1 2027"
- **4 Tier B 2026 reposts of 2024 Tier A calls are correct.** GM, UPS, BIIB and NOW are dated
  by their repost day.
- **SBAC 2026-04-01 is a different call** (see §1).
- **10 are distinct calls that were lost:**
  - **COST ×5** (FY22 Q2, FY23 Q2, FY24 Q3, FY25 Q2 Tier A; FY26 Q2 Tier B): Costco quarter
    mapping, see (d).
  - **DG FY25 Q2, LOW FY25 Q2, WSM FY25 Q2 and LULU FY26 Q1** (each 364–370 days from the
    kept call): Tier B pages whose `Date` heading was not parsed (see §4). The quarter then came
    from the label with end-year naming, which is wrong for these start-year-naming retailers.
  - **TECH FY26 Q1:** the real Bio-Techne page (2025-11-06) is marked as a duplicate of a
    **Minerals Technologies** page. That page (`minerals-tech-earnings-call-transcript`) was
    matched on the slug token `tech` and is now kept as `tech_FY26_Q1.md`.

### (c) `no fiscal quarter in title or slug` (7 rows): all recoverable

The pages are BMY 2025-11-27, CHRW 2025-10-29, STZ 2025-10-07 and 2026-04-14, SWK 2026-02-04,
and UNH 2026-01-26 and 01-27. Every one is a Tier B page with a `Date` section. The parser only
recognises `DATE` in upper case, so these fell back to the publication date and the label could
not be derived.

With a case-insensitive match, 5 calls come back from the cache:

| Firm | Call | Calendar quarter |
|---|---|---|
| BMY | Q3 2025 | 2025 Q3 |
| CHRW | Q3 2025 | 2025 Q3 |
| STZ | Q2 FY26 | 2025 Q3 |
| SWK | Q4 2025 | 2025 Q4 |
| UNH | Q3 2025 | 2025 Q3 |

The remaining two rows are the never-fetched UNH 01-27 page (2025 Q4) and the STZ 04-14 page
(harmless).

### (d) `label_agrees == False` (115 rows)

| Cause | Rows | Firms | Assignment |
|---|---|---|---|
| Start-year fiscal naming (Fool's year = the year the FY starts) | 95 | BBY 2, DG 14, DLTR 15, LOW 15, LULU 16, ROST 2, TGT 14, WSM 17 | **correct** (real call date used) |
| Amcor: Fool labels follow the June fiscal year, SEC now says December | 6 | AMCR | correct (same quarter grid); file names such as `amcr_2026_Q1.md` are FY26 Q1, i.e. CY 2025 Q3 |
| Costco's 12/16-week quarters end mid-month, and calls come under 7 days after the assumed month-end | 8 | COST | **misassigned:** Q2 calls fall one quarter back (dropped as duplicates), Q3 calls one quarter back |
| BRO: `universe.csv` has SEC fiscalYearEnd **0119** for Brown & Brown, but it is a December year end | 5 | BRO | **misassigned:** every call sits one quarter early, and the Q3 2026 call is counted as 2026 Q2 |
| Fool mislabel | 1 | APD | out of window either way |

**`label_agrees` cannot catch the worst Tier B cases.** When a page has no parsed call date, the
quarter is taken from the label, so `label_agrees` is True by construction. That is how
DG/ROST/TGT Q1 2026 were filed under 2025 Q1 and CCI's Mar 12, 2025 call (titled "Q1 2025")
under 2025 Q1. It is also why the `half1_fiscal_year_ends.csv` cross-check did not flag BRO: it
infers the year end from URL dates, and BRO's URLs are all backfills, so it agreed with the wrong
SEC value.

## 3. Discovery completeness

### (a) Sitemap URLs never matched

I re-ran the matcher over all 21,997 transcript URLs in the 60 cached sitemaps. **33 URLs belong
to half-1 firms but were missed** (`half1_audit_missed_urls.csv`). 32 are in the window, and they
fill **29 firm-quarters now marked `missing`**. All are 2025–2026 LLM-era pages, so none would be
Tier A.

- **26 ticker-only slugs**, for example `txn-q1-2026-earnings-transcript`,
  `swk-q2-2025-earnings-transcript`, `gm-q1-2026-…`, `iff-q4-2025-…`, `cinf-q1-2025-…`,
  `mlm-q2-2026-…`. Firms: ADM, AEP, CINF, FIS, FRT, GM, HPE, IFF, IP, ISRG, ITW, MAA, MLM,
  MPWR, SWK, TXN, UHS, WTW.
  - Cause: `cmd_discover` needs `len(toks) > k`, i.e. a name token before the ticker.
- **7 name-only slugs without a ticker:** `texas-instruments-q2-2025-…` and `…q3-2025-…`,
  `conocophillips-q3-2025-…`, `hca-healthcare-q3-2025-…`, `baker-hughes-q3-2025-…`,
  `intl-paper-q3-2025-…`, `willis-towers-watson-earnings-transcript`.
  - Cause: the name fallback always drops the last token as if it were the ticker.
- **Half 2 has the same problem:** 19 ticker-only and 12 name-only unmatched URLs.

Other near-matches were checked and are different companies, for example Veritiv (VRTV) vs Vertiv
and AVITA vs DaVita.

**Name-check rows:** of the 83 rows in `half1_name_check.csv`, only one is a different company,
`minerals-tech-earnings-call-transcript` matched to TECH. A title check over every page found no
other wrong-firm page.

### (b) Quote-page check

Each Fool quote page lists the **8 most recent** transcripts. For firms with sparse coverage, those
8 reach back to 2020–2021 and so cover the whole window. For heavily covered firms they reach back
to about mid-2024.

| Firm | Group | Quote page vs our data |
|---|---|---|
| ED, NVR, EXPD | 0 URLs | **no transcripts listed at all**. NVR and EXPD hold no calls. This is a real gap. |
| SBAC, CDNS, USB, TRV | no Tier A | exact match. The 8 links reach back to 2020–21, which confirms Fool has **nothing from Nov 2021 to mid-2025** for these firms. |
| TXN | no Tier A | 3 of 4 in-window links missed: 2 name-only slugs and 1 ticker-only slug |
| SWK | no Tier A | 3 links missed (ticker-only slugs) and 1 hit by the `Date` bug. Only 1 of 5 Fool calls is in our data. |
| REGN | no Tier A | exact match (all 8 links are 2026) |
| CAT, KO, IBM, UNH, STZ, EOG | well covered | exact match, apart from the UNH 01-27 collision and the EOG transient 404 |

**Result: all 83 links in the sitemap date range are in the cached sitemaps (83/83).** 77 of them
matched our firms, and the 6 misses are all slug-format bugs. 70 were fetched. The 7 not fetched
are 6 same-slug collisions and the EOG 404.

**The monthly sitemaps look complete.** The thin 2022–2024 coverage and the near-empty April 2025
are real Fool gaps, not discovery failures.

## 4. File integrity

| Check | Result |
|---|---|
| Tier A files / availability `tierA` / `call_units` rows / `*_ai.md` | 1,276 / 1,276 / 1,276 / 1,276, one-to-one |
| Tier B files / availability `tierB` | 873 / 873. No orphan files; every file is in a half-1 folder. |
| File header vs `half1_calls.csv` (calendar quarter, SHA-256, URL) | 0 mismatches |
| Tier A: metadata block, `---`, body starts `Prepared Remarks:`, `Call participants:`, ≥5 `Name -- Title` lines, ≥3,000 words | all pass. Shortest is CINF 2022 Q1 at 4,245 words. |
| Tier A without `Questions & Answers:` | 29. Of these, 12 use `Questions and Answers:` or are detected by the filter (MDT). **17 are flagged `Q&A start not detected`**, so all their units count as prepared remarks. |
| Tier B `Quality warning` line and `motley_fool_llm` source type | 873/873 |
| Identical bodies (SHA-256 over all 2,374 cached pages) | Tier A: none. **CME: the `q1-2026` URL serves the Q4 2024 call** (same body as `cme_2024_Q4.md`; the text says "record year in 2024"), so `cme_2026_Q1.md` is wrong. EXR and LOW pairs are correct duplicates. |
| Unit outliers | none under 150 units (minimum 229). The low counts are SJM FY22 Q3 and KHC 2024 Q4, which post their prepared remarks in advance, so the calls are Q&A only. 102 files carry the "outside 400–900" flag. |
| IT-sector calls with 0 AI units | 4 of 222 (AVGO 1, JBL 1, WDC 2). Only WDC FY23 Q2 is after ChatGPT. Not suspicious. |
| Short Tier B pages | PLD 2026 Q1 (2,167 words), SOLV 2025 Q3 and LH 2025 Q3 are short on Fool's own page; the extractor is not cutting them. |

The 17 `Q&A start not detected` files break down as follows:

- **Netflix ×12:** Netflix's calls are an interview format with no operator and no Fool Q&A
  header.
- **MPWR 2021 Q4 and 2022 Q1:** webinar format; Q&A begins in plain text with "Analysts, I would
  now like to begin our Q&A session".
- **TGT FY21 Q4 and FY22 Q4:** Q4 is presented at Target's Financial Community Meeting, which is
  long (1,164 units).
- **VZ 2024 Q3:** an earnings call combined with a broadband update at an in-person event.

All 17 are main earnings events. Section-level analysis should drop them or split them by hand,
but they are fine for whole-call totals.

## 5. Coverage

### By calendar quarter

| Quarter | A | B | missing | A % | A+B % |
|---|---|---|---|---|---|
| 2021 Q4 | 131 | 0 | 116 | 53% | 53% |
| 2022 Q1 | 120 | 0 | 127 | 49% | 49% |
| 2022 Q2 | 129 | 0 | 118 | 52% | 52% |
| 2022 Q3 | 93 | 0 | 154 | 38% | 38% |
| 2022 Q4 | 90 | 0 | 157 | 36% | 36% |
| 2023 Q1 | 55 | 0 | 192 | 22% | 22% |
| 2023 Q2–2024 Q2 | 88–92 | 0 | 155–159 | 36–37% | 36–37% |
| 2024 Q3 | 102 | 14 | 131 | 41% | 47% |
| 2024 Q4 | 101 | 10 | 136 | 41% | 45% |
| 2025 Q1 | 5 | 36 | 206 | 2% | 17% |
| 2025 Q2 | 0 | 124 | 123 | 0% | 50% |
| 2025 Q3 | 0 | 123 | 124 | 0% | 50% |
| 2025 Q4 | 0 | 204 | 43 | 0% | 83% |
| 2026 Q1 | 0 | 210 | 37 | 0% | 85% |
| 2026 Q2 | 0 | 152 | 95 | 0% | 62% |

The quarters most affected by the Tier B bugs are 2025 Q2–Q3 and 2026 Q1.

### By GICS sector (firms; % of firm-quarters)

| Sector | Firms | Both pre & post Tier A | Pre-ChatGPT Tier A % | Post Tier A % (22Q4–25Q1) | A+B % (25Q2–26Q2) | None |
|---|---|---|---|---|---|---|
| Consumer Discretionary | 23 | 57% | 63% | 48% | 64% | 7 |
| Health Care | 30 | 53% | 62% | 46% | 75% | 10 |
| Energy | 8 | 50% | 69% | 45% | 68% | 2 |
| Information Technology | 35 | 46% | 59% | 40% | 66% | 8 |
| Consumer Staples | 21 | 43% | 54% | 43% | 55% | 2 |
| Communication Services | 10 | 40% | 48% | 37% | 68% | 4 |
| Financials | 42 | 31% | 40% | 26% | 61% | 21 |
| Industrials | 45 | 27% | 40% | 23% | 71% | 23 |
| Real Estate | 9 | 22% | 39% | 13% | 64% | 5 |
| Utilities | 14 | 21% | 23% | 13% | 60% | 10 |
| **Materials** | 10 | **10%** | **10%** | 11% | 62% | 8 |

**The thinnest sectors before ChatGPT are Materials (10%), Utilities (23%), Real Estate (39%),
and Financials and Industrials (40%).**

The before/after comparison is balanced in its sector mix, but not across sectors:

- The sector shares of Tier A calls before and after ChatGPT differ by at most 2.5 points. For
  example, IT is 17.5% vs 17.3% and Industrials 15.2% vs 12.7%.
- Compared with the universe, Materials (0.8% of calls vs 4.0% of firms), Utilities, Real Estate
  and Industrials are under-represented. Health Care, IT and Consumer Discretionary are
  over-represented.
- A firm-fixed-effects or balanced-panel design (the 93 firms with both) should be used, with
  sector weights reported. Materials (1 firm with both) and Utilities (3) cannot support
  sector-level claims.

## 6. Half 2 on origin

`git fetch origin` (read-only). **`origin/sp493-half2` exists:** commit 9df02a0 by kash2nasty,
2026-10-28 20:55 EDT, branched from bed0c03.

**Contents:**

- 1,100 Tier A files, 770 Tier B files, 1,101 `earnings_calls_ai_only` files (1,100 + `_stats_half2.json`)
- 9 `half2_*` CSV/JSONL files
- availability: 1,100 tierA, 770 tierB, 2,804 missing
- 79 firms before+after, 123 with no Tier A

**It was already merged into `origin/main`** via PR #1 (4959618, Advik Kashyap, 21:23).

**`origin/main` already has the fixed script.** Commits 37dc8ed and 2ab8396 are rebased copies of
f2b5b06 and 19fd2f9. `origin/main:sp493/sp493_pull.py` is byte-identical to f2b5b06 (SHA-256
`6d00bcfb…`), and the half-1 files on `origin/main` are identical to this branch. This is
contrary to the expectation in the task.

**Half 2 was built with the pre-fix script** (bed0c03, `sp493_pull.py` SHA-256 `022534b5…`; its
`half2_calls.csv` has no `label_source` column). As a result:

- 583 Tier B rows used `datePublished` as if it were the call date.
- 94 of those disagree with Fool's label. These are misdated backfills, for example AMD Q2 2025
  filed under 2025 Q4 and BAX/BEN Q4 2024 filed under 2026 Q1.
- Half 2 also has all the bugs listed below.

**Half 2 needs the rebuild described in `ADVIK_DATA.md` Step 3.**

## 7. Mag 7

`earnings_calls_canonical_extended/earnings_call_call_units.csv` has **133 unique calls: 7 firms ×
19 quarters, with no gaps**.

17 of them come from `earnings_calls_pre2022_extra/`, which is **not approved**. All 17 are in the
pre-ChatGPT quarters (2021 Q4–2022 Q3):

| Calls | Source | Note |
|---|---|---|
| alphabet 2021_Q4 | archive.org copy of the official PDF | `source_type` is "unknown" in the CSV |
| amazon 2021_Q4–2022_Q3 | Whisper | `whisper_unit`; not comparable to sentences |
| apple FY22_Q1–Q4 | Fool | |
| nvidia FY22_Q4, FY23_Q1–Q3 | Fool | |
| tesla 2021_Q4, 2022_Q2, 2022_Q3 | Fool | |
| tesla 2022_Q1 | YouTube captions | `caption_segment` |

27 of the 133 rows have `units_comparable_to_sentences = 0`.

## Recommended fixes to `sp493_pull.py` (not applied)

Fixes are listed in order of how much they matter.

1. **Discovery slugs.** Accept a slug that is just a ticker. In `cmd_discover`, use
   `len(toks) >= k` for the ticker test, then require `(TICKER)` or the firm name in the page
   title. For the name fallback, also try the full token list, not only `toks[:-1]`, and add a
   short-name alias for `intl`. This recovers 29 firm-quarters in half 1 and about 30 URLs in
   half 2.
2. **`Date` heading.** In `parse_fool_page`, match the `DATE` h2 case-insensitively, for example
   by indexing `h2s` on `.upper()`. This recovers 13 firm-quarters and removes 4 wrong ones.
3. **Quarter assignment.** When a real call date and a label both exist, use the label reading
   (year shift 0, +1 or −1) whose quarter end is −15 to +120 days before the call. Fall back to
   `calendar_quarter` otherwise. For pages with only a publication date, use the firm's
   year-shift convention inferred from its real-dated pages, not always 0. This fixes Costco
   (+4 Tier A, +1 Tier B, 3 corrected) and the start-year retailers.
4. **BRO year end.** Add `FYE_OVERRIDE = {"BRO": 12}`, applied when the universe loads; do not
   rebuild `universe.csv`. Move the year-end cross-check after download so it uses real page
   call dates instead of URL dates.
5. **Cache key.** Name cache files by URL date plus slug, or skip on `url in done` only. This
   fetches the 30 same-slug pages and recovers UNH and SBAC 2025 Q4.
6. **Retry 404/410 once** at the end of the run instead of recording them as done. This recovers
   EOG 2026 Q1.
7. **Wrong firm.** Reject ticker-only matches whose title lacks the ticker or the firm name. This
   fixes TECH.
8. **Identical bodies.** Hash bodies within each firm. If two kept pages share a body, keep only
   the one whose text fits its label. This fixes CME 2026 Q1, which then becomes missing.
9. **Rebuild.** About 64 new fetches are needed: the 30 same-slug pages, 33 missed URLs and the
   EOG retry. Then run `write_raw`, `filter` and `report` for both halves.
   - **The generated outputs must be deleted first** (the list in `ADVIK_DATA.md` Step 3), and
     this needs approval.
   - The never-overwrite rule would otherwise keep the wrong `tech_FY26_Q1.md`,
     `cme_2026_Q1.md`, `cost_FY22_Q3.md` and `cost_FY23_Q3.md` (whose headers say 2022 Q1 and
     2023 Q1) and the BRO headers.
10. **Analysis.** Pool by `calendar_year`/`calendar_quarter`, not by `period_label`. Fool's LLM
    labels for retailers switch naming conventions, so DG has both FY25_Q4 and FY27_Q2. Drop the
    17 files with no detected Q&A from section-level results.
