# Half 2 completeness audit (S&P 493, Motley Fool)

Audited 2026-10-29 on branch `sp493-half2-rebuild`. The audited data is the half-2 **rebuild** with
the fixed script (`sp493_pull.py` blob `2afd9da`, identical to `origin/main` at c48bbdd). The rebuild
followed the steps in `ADVIK_DATA.md` ("Rebuilding half 2"). This audit applies the checks in
`half1_completeness_audit.md` to that data. Nothing in `cache/` or any script was changed. The audit
added this file and three CSVs:

- `half2_audit_issues.csv`: 7 rows, one per affected firm-quarter or URL. Each row gives the current
  status, what it should be, the evidence and the fix.
- `half2_audit_missed_urls.csv`: 7 Fool transcript URLs in the cached sitemaps that belong to
  half-2 firms but were never matched.
- `half2_audit_quote_page_check.csv`: every transcript link on 14 Fool quote pages, checked against
  the sitemaps, the candidate list and the fetch log.

**Network use:** 25 requests to fool.com, one at a time, at least 4.5 s apart, with the pipeline's
User-Agent.
- 18 were quote-page requests. 14 returned 200. 4 returned 404: VYLR under nyse and nasdaq, and SKYD
  under psky and skyd.
- 7 were transcript pages the pipeline never fetched.

The responses are kept in the scratchpad only, not in `cache/`.

## Verdict

**Tier A (the main series): yes, essentially complete relative to what Fool offers.**

- **The sitemaps are complete.** All 69 quote-page links dated inside the sitemap range are in the
  cached sitemaps.
- **Every old-layout page the sitemaps list for our firms was downloaded,** except one.
- **The one Tier A defect is Seagate FY23 Q4 (STX, 2023 Q2).** Fool's slug has no quarter number
  (`…-stx-qearnings-call-transcri`), and the page has no date line, so the call was never matched.
  If it had been matched, it would still have been dropped as having no fiscal quarter.
- **The before/after firm counts (79 / 36 / 8 / 123) change only if STX is added.** STX already
  has Tier A calls before and after ChatGPT, so they don't change at all.

**Tier B (2025+ LLM pages): yes, apart from three quarters.**

- **The rebuild fixed what the half-1 audit found.**
  - 128 firm-quarters went from `missing` to `tierB`.
  - 8 wrongly filled slots were emptied (AES 2026 Q1, AZO 2025 Q4, FERG 2025 Q4, HBAN 2026 Q1 and
    others).
  - 48 slots now hold the correct call, where they had held a misdated one (for example AMD
    2025 Q4, and BAX and BEN 2026 Q1).
- **3 firm-quarters that Fool has are still `missing`:**
  - SO 2025 Q3, because of a name-only slug ending in "co"
  - SKYD 2025 Q4 and 2026 Q2: Fool uses ticker PSKY, but the universe uses SKYD
- **No filled slot holds the wrong call.**
  - All 1,990 kept calls have a real call date from the page, and every one lies within −45 to
    +130 days of the end of its assigned calendar quarter.
  - No two kept pages have the same body.

**Before vs after the rebuild:**

| Build | Tier A | Tier B | Missing |
|---|---|---|---|
| First build | 1,100 | 770 | 2,804 |
| Rebuild | 1,100 | 890 | 2,684 |
| With the fixes below | 1,101 | 893 | 2,680 |

The rebuild changed no Tier A transcript body and no filter count. 611 Tier A files changed only in
their `Retrieved` line, which now comes from the fetch log (UTC).

---

## 1. Candidate reconciliation (every URL accounted for)

| Step | Count | Notes |
|---|---|---|
| Candidate URLs in `half2_fool_urls.csv` | 2,230 | no duplicate URLs |
| Skipped by download (prelim window false and slug has a quarter) | 3 | HD, KR and ULTA "Q3 2021" (calls on 2021-11-16 and 2021-12-03 for quarters ending Oct/Nov 2021, so CY 2021 Q3). **All are genuinely outside the window.** |
| Prelim false but downloaded anyway (no quarter in a truncated slug) | 2 | CRL and PEG Q3 2021, later `outside window` |
| Download candidates | 2,227 | |
| Fetched with HTTP 200 | 2,227 | 2,171 in the first run and 56 new in the rebuild. Every cache file is referenced by a candidate, and the SHA-256 of every cache file matches `results.jsonl`. |
| Fetched with any other status | 0 | 1 connection reset in the first run was retried automatically |
| Same-slug URLs | handled | The cache is now keyed by URL. Both FIX `comfort-systems-fix-earnings-call-transcript` pages (2025-08-05 and 2026-02-20) were fetched and are both kept, as different calls. |
| Rows in `half2_calls.csv` | 2,227 | one per fetched URL |

Every `ok` row cites a URL that was actually fetched. The SHA-256 in its file header equals that
URL's fetch log and cache file (0 mismatches). No two `ok` rows share a file path.

## 2. Status checks

| Status | Rows |
|---|---|
| ok | 1,990 |
| outside window | 189 |
| duplicate of … | 32 |
| same text as … | 14 |
| title names another company | 2 |
| no fiscal quarter / unknown layout / not a main call | 0 |

### (a) `outside window` (189 rows): all correct

- **95 rows are CY 2021 Q3, all Tier A with real call dates.** 90 calls are in Nov 2021 and 5 in
  Dec 2021. The December calls (CASY FY22 Q2, CIEN FY21 Q4, COO FY21 Q4, CRWD FY22 Q3, NDSN FY21 Q4)
  all report quarters that end in October 2021, so their middle month is September.
- **94 rows are CY 2026 Q3, all Tier B with a page `Date` section.** 87 calls are in Oct 2026 and 7
  in Sep 2026 (AZO FY26 Q4; CCL FY26 Q3; CTAS, DRI and GIS FY27 Q1; FDS FY26 Q4; LEN FY26 Q3). All of
  those report quarters ending in August 2026.
- **CAH FY22 Q2, JCI FY21 Q3 and PH FY21 Q3 disagree with their labels.** All three are calls from
  Nov 2021 about the September 2021 quarter, so all are out under any reading.

### (b) `duplicate` and `same text` (46 rows): all correct

- **32 `duplicate of`: all share the kept call's call date.** They are:
  - Tier B copies of Tier A calls
  - reposts
  - two Fool mislabels: HBAN "Q1 2026", which is the Jan 22, 2026 Q4 2025 call, and PFE "Q2 2025",
    which is the Feb 4, 2025 Q4 2024 call
- **14 `same text as`: identical bodies at two URLs, same call date.**
  - 12 are 07-30/08-03 pairs of Q2 2026 pages: AJG, AVY, EIX, GEHC, HSY, ICE, ILMN, MO, SO, SYK, TT
    and XEL.
  - 2 are dual-class pairs: FOXA/FOX and NWSA/NWS.
- **No distinct call was lost.** No duplicate's real call date is more than 45 days from the kept
  call's.

### (c) `title names another company` (2 rows): correct

Both are Fortress Transportation & Infrastructure Investors (FTAI) pages matched to F (Ford) on the
slug token `f`. They are dated 2022-02-25 and 2022-07-28, and the title check now rejects them.

### (d) `label_agrees == False` (67 rows)

| Cause | Rows | Firms | Assignment |
|---|---|---|---|
| Start-year fiscal naming (Fool's year = the year the FY starts) | 47 | HD 16, KR 15, ULTA 16 | **correct** (label read the way that fits the call date) |
| Lam Research: Fool labels LRCX calls by **calendar** quarter (the Jan 2022 call is "Q4 2021"); SEC year end is June | 11 | LRCX (Tier A) | **correct** (real call date used). File names such as `lrcx_FY21_Q4.md` are really FY22 Q2, i.e. CY 2021 Q4. |
| Ferguson moved its year end from July to December in 2025; Fool's 2025 labels follow the old July year | 4 | FERG (Tier B) | **correct** under the middle-month rule. The Dec 10, 2024 call covers Aug–Oct 2024, so it falls in 2024 Q3. |
| Fool mislabel, page dropped as a duplicate | 2 | HBAN, PFE | correct (see b) |
| Out of window either way | 3 | CAH, JCI, PH | correct |

**Independent quarter check.** For every kept call, the real call date was compared with the end of
its assigned calendar quarter. All 1,990 fall between −45 and +130 days, so no call sits a year or
a quarter away from its slot.

Two other points:
- **Every Tier B page now has a parsed `Date` section** (890/890). The `datePublished` fallback is
  never used, so the half-1 blind spot does not arise in half 2. In that blind spot, a label-based
  quarter makes `label_agrees` True by construction.
- **Only one pair of consecutive kept calls is under 50 days apart:** JCI FY23 Q4 (2023-12-12) and
  FY24 Q1 (2024-01-30). This is real: Johnson Controls delayed its FY23 Q4 call after a cyber
  incident.

**Fiscal year end cross-check.** `half2_fiscal_year_ends.csv` has 10 disagreements: AES, AZO, BXP,
CASY, FERG, LRCX, NWSA, PKG, Q and URI.
- **None is a BRO-type error in SEC's value.** The Dec-year-end firms (AES, BXP, PKG, URI) are real
  calendar-year reporters whose URLs include backfills. AZO (Aug), CASY (Apr) and NWSA (Jun) match
  their known fiscal years. LRCX and FERG are explained above. Q has one call.
- **The quarter check above confirms it.** A wrong year end would push calls outside the
  −45 to +130 day band.

## 3. Discovery completeness

### (a) Sitemap URLs never matched

I scanned all 21,997 transcript URLs in the 60 cached sitemaps for unmatched slugs that contain a
half-2 ticker or the leading words of a half-2 firm name. That gave 204 near-matches, and every one
was checked by hand. **7 belong to half-2 firms** (`half2_audit_missed_urls.csv`). The rest are
different companies.

**The 7 that belong to half-2 firms:**

| URL | Firm-quarter | Cause |
|---|---|---|
| `2023/07/28/seagate-technology-plc-stx-qearnings-call-transcri` | **STX 2023 Q2, Tier A** | Fool's slug has `q` with no digit, so `SLUG` fails and `TRUNC_TAIL` does not strip `qearnings`. The ticker is never reached. |
| `2025/10/30/southern-co-q3-2025-earnings-call-transcript` | SO 2025 Q3, Tier B | The name branch treats the last token (`co`) as an old ticker and matches "southern" → SO as "name only (ticker differs)". The rule that drops such matches dated after the firm's first ticker page then removes it. This is the 1 "name-only match dropped" in the discover log. |
| `2026/02/25/paramount-skydance-psky-earnings-transcript` | SKYD 2025 Q4, Tier B | `universe.csv` has ticker SKYD, name "Skydance" (CIK 0002041610). Fool uses PSKY and "Paramount Skydance". |
| `2026/08/12/paramount-skydance-psky-q2-2026-earnings-call-transcript` | SKYD 2026 Q2, Tier B | same |
| `2021/11/30/equinix-inc-eqix-fy-2021-…`, `…lyondellbasell-industries-nv-lyb-fy-2021-…`, `…quanta-services-inc-pwr-fy-2021-…` | none | **Investor conferences, not earnings calls**, although titled "FY 2021 Earnings Call Transcript": a Nasdaq investor conference, an analyst conference and a net-zero panel. They are outside the window by date anyway. **Harmless.** |

**Different companies checked and rejected.** The 197 other near-matches are look-alikes:
- "american-…" firms vs AIG
- BlackRock BDCs vs BLK
- Cooper-Standard and Mr. Cooper vs COO
- Phillips Edison vs EIX
- Stitch Fix (SFIX) vs FIX
- On Holding (ONON) vs ON
- Owens Corning vs GLW
- Goldman Sachs BDC vs GS
- Ideanomics vs IEX
- Invesco Mortgage vs IVZ
- Johnson Outdoors vs JNJ
- Marriott Vacations vs MAR
- Southern Copper, Great Southern and Southern Missouri vs SO
- Shoe Carnival vs CCL

**Firms with zero URLs (5):**
- **BRK.B:** Berkshire holds no earnings calls, and its quote page lists no transcripts.
- **FDXF:** FedEx Freight, added to the index 2026-06-01, has no call in the window.
- **VMRK** (Vivmark Residential): its quote page lists no transcripts.
- **VYLR** (Vylor): it has no quote page (404).
- **SKYD:** see the table above.

**Name-check rows.** Of the 80 rows in `half2_name_check.csv`, two are different companies:
- the Fortress (FTAI) pages under F, now rejected by the title check
- `physicians-realty-trust-reit-doc-q3-2021`: Physicians Realty used ticker DOC before merging into
  Healthpeak, and the page is outside the window

The rest are short or old names of the same companies:
- `bofa`, `pseg`, `pca`, `bd`, `jj`
- generic `<ticker>-q…` slugs
- PEAK→DOC, MMC→MRSH and BK→BNY
- name-only `johnson-johnson`, `mastercard`, `linde`, `abbvie`, `merck`, `xcel-energy`, `trane`,
  `procter-and-gamble` and `texas-pacific-land`

**No kept page names a different firm.** Every kept page's title names its firm or one of its old
tickers (MMC for MRSH, BK for BNY).

### (b) Quote-page check

Each Fool quote page lists the **8 most recent** transcripts. I chose 16 firms in the same three
groups as half 1:
- **No URLs:** BRK.B, VMRK, VYLR and SKYD.
- **No Tier A:** SO, LYB, PWR and ERIE, plus a seeded random 5 (seed 20261029): MDLZ, ICE, DELL,
  PCAR and FIX.
- **Well covered, including fiscal-label edge cases:** STX, HD and KR.

| Firm | Group | Quote page vs our data |
|---|---|---|
| BRK.B, VMRK | 0 URLs | page exists, **no transcripts listed** |
| VYLR, SKYD | 0 URLs | **no quote page** (404 under nyse/nasdaq, and under psky and skyd) |
| MDLZ, ICE, DELL, PCAR, FIX | no Tier A | exact match. The links skip from 2021 (or earlier) to mid-2025, which confirms Fool has **nothing from Nov 2021 to mid-2025** for these firms. |
| LYB, ERIE | no Tier A | exact match |
| SO | no Tier A | 1 in-range link missed: `southern-co-q3-2025` |
| PWR | no Tier A | 1 link missed: the `fy-2021` conference page (harmless) |
| STX, HD, KR | well covered | exact match. STX's quote page reaches back only to mid-2025, so it cannot show the 2023 miss; that came from the sitemap scan. |

**Result:**
- **All 69 links dated within the sitemap range (to 2026-10-28) are in the cached sitemaps
  (69/69).**
- 67 matched our firms and all 67 were fetched. The 2 misses are listed above.
- Two links posted 2026-10-29, after the sitemaps were fetched: PWR and ICE Q3 2026. Both are
  outside the window.
- 19 links predate the window.

**The monthly sitemaps look complete for half 2 too.** The thin 2022–2024 coverage is a real Fool
gap, not a discovery failure.

## 4. File integrity

| Check | Result |
|---|---|
| Tier A files / availability `tierA` / `call_units` rows / `*_ai.md` | 1,100 / 1,100 / 1,100 / 1,100, one-to-one |
| Tier B files / availability `tierB` | 890 / 890. No orphan files; every file is in a half-2 folder, and no changed path belongs to half 1. |
| File header vs `half2_calls.csv` (calendar quarter, SHA-256, URL) | 0 mismatches |
| Tier A: metadata block, `---`, body starts `Prepared Remarks:`, `Call participants:`, ≥5 `Name -- Title` lines, ≥3,000 words | all pass. Shortest is VRSN 2022 Q1 at 3,040 words. |
| Tier A without `Questions & Answers:` | 54. Of these, 9 use `Questions and Answers:` or are detected by the filter (ACN, AZO, CCL, CTAS, DRI, FDS and GIS FY22; AXON 2021 Q4; PANW FY24 Q4). **45 are flagged `Q&A start not detected`**, so all their units count as prepared remarks. |
| Tier B `Quality warning` line and `motley_fool_llm` source type | 890/890 |
| Identical bodies (SHA-256 of the parsed body over all 2,227 cached pages) | 14 groups, all within one firm and all logged `same text as` (see 2b). No body is shared across firms, and no kept slot holds another quarter's text (the CME case in half 1). |
| Unit outliers | none under 150 units (minimum 191, VRSN 2022 Q1). 86 files carry the "outside 400–900" flag. |
| IT-sector calls with 0 AI units | 11 of 211 (APH, CIEN, FSLR, GLW and VRSN). 9 are pre-ChatGPT; FSLR 2022 Q4 and 2023 Q1 are after. Not suspicious: these are hardware, solar and registry firms. |
| Short Tier B pages | ERIE 2025 Q3, 2025 Q4 and 2026 Q1 (1,408–1,645 words). Fool's whole article is 2,167–2,521 words, and the difference is Fool's LLM summary above `Full Conference Call Transcript`. Erie's calls are short; the extractor is not cutting them. |
| Path separators | **`file` in `half2_calls.csv` and `half2_call_units.csv` uses Windows backslashes** (`sp493\earnings_calls\…`, 1,990/1,990). Half 1 uses `/`. The cause is `str(dest.relative_to(ROOT))` on Windows. This is cosmetic, but any join across the halves must normalise it. |

The 45 `Q&A start not detected` files break down as follows:

- **AXON ×12, PANW ×12, APP ×4, GDDY ×3, HOOD ×1:** analyst Q&A is present (24–49 `-- Analyst`
  lines per call), but Fool's page has no `Questions & Answers:` header.
- **PLTR ×12:** IR first reads shareholder questions submitted online, then takes analysts. The
  format has no operator and no header.
- **TWLO 2022 Q3:** this is **Twilio's 2022 Investor Day**, held with SIGNAL, plus a Q&A on the Q3
  results. It runs 29,584 words and 1,565 units, about three times a normal call. It is the main
  Q3 2022 earnings event, like VZ 2024 Q3 in half 1. Whole-call shares are usable, but unit counts
  are inflated.

All 45 are main earnings events. Section-level analysis should drop them or split them by hand, but
they are fine for whole-call totals. Palantir, Palo Alto and AppLovin are heavy AI talkers, so
dropping them from section-level results is not neutral.

## 5. Coverage

### By calendar quarter

| Quarter | A | B | missing | A % | A+B % |
|---|---|---|---|---|---|
| 2021 Q4 | 110 | 0 | 136 | 45% | 45% |
| 2022 Q1 | 100 | 0 | 146 | 41% | 41% |
| 2022 Q2 | 109 | 0 | 137 | 44% | 44% |
| 2022 Q3 | 79 | 0 | 167 | 32% | 32% |
| 2022 Q4 | 79 | 0 | 167 | 32% | 32% |
| 2023 Q1 | 55 | 0 | 191 | 22% | 22% |
| 2023 Q2–2024 Q2 | 78–79 | 0 | 167–168 | 32% | 32% |
| 2024 Q3 | 85 | 25 | 136 | 35% | 45% |
| 2024 Q4 | 87 | 9 | 150 | 35% | 39% |
| 2025 Q1 | 3 | 25 | 218 | 1% | 11% |
| 2025 Q2 | 0 | 116 | 130 | 0% | 47% |
| 2025 Q3 | 0 | 131 | 115 | 0% | 53% |
| 2025 Q4 | 0 | 206 | 40 | 0% | 84% |
| 2026 Q1 | 0 | 226 | 20 | 0% | 92% |
| 2026 Q2 | 0 | 152 | 94 | 0% | 62% |

Half 2's Tier A share runs 0–8 points below half 1's through 2024 Q4. The gap is largest (8
points) in 2021 Q4–2022 Q2, and zero in 2023 Q1.

### By GICS sector (firms; % of firm-quarters)

| Sector | Firms | Both pre & post Tier A | Pre-ChatGPT Tier A % | Post Tier A % (22Q4–25Q1) | A+B % (25Q2–26Q2) | None |
|---|---|---|---|---|---|---|
| Energy | 13 | 69% | 69% | 61% | 78% | 4 |
| Consumer Discretionary | 22 | 50% | 50% | 48% | 64% | 6 |
| Information Technology | 37 | 41% | 53% | 36% | 71% | 12 |
| Real Estate | 21 | 38% | 38% | 34% | 68% | 13 |
| Health Care | 30 | 33% | 46% | 29% | 73% | 13 |
| Consumer Staples | 13 | 31% | 35% | 26% | 65% | 8 |
| Financials | 34 | 29% | 40% | 25% | 62% | 17 |
| Communication Services | 7 | 29% | 29% | 27% | 51% | 4 |
| Materials | 14 | 21% | 27% | 18% | 69% | 10 |
| Industrials | 38 | 18% | 30% | 17% | 68% | 23 |
| **Utilities** | 17 | **0%** | **16%** | **0%** | 66% | 13 |

**The thinnest sectors before ChatGPT are Utilities (16%), Materials (27%), Communication Services
(29%) and Industrials (30%).**
- **Half 2 has no utility with Tier A calls after ChatGPT.** Utilities are 6.9% of half-2 firms but
  0% of post-ChatGPT Tier A calls.
- **Industrials (15.4% of firms) fall from 11.6% of pre-ChatGPT calls to 8.9% after.**
- **Consumer Discretionary and Energy are over-represented** (13.5% and 10.5% of calls vs 8.9% and
  5.3% of firms). IT is over-represented in both periods (19.9% / 18.8% of calls vs 15.0% of firms).
- **The sector mix shifts by more than in half 1.** Consumer Discretionary rises from 10.9% to
  15.1% of calls, and Industrials falls 2.7 points.

The firm-fixed-effects / balanced-panel recommendation from half 1 applies. Pooled across both
halves, the panel is 172 firms with Tier A calls both before and after (93 + 79).

| Sector | Half-2 firms with both |
|---|---|
| IT | 15 |
| Consumer Discretionary | 11 |
| Health Care | 10 |
| Financials | 10 |
| Energy | 9 |
| Real Estate | 8 |
| Industrials | 7 |
| Consumer Staples | 4 |
| Materials | 3 |
| Communication Services | 2 |
| Utilities | 0 |

**Sector-level claims are not possible from half 2 alone for Utilities, Communication Services or
Materials.**

## 6. Half 1 and the pooled S&P 493

`git fetch origin` (read-only). `origin/main` is at c48bbdd: half 1 is rebuilt, and the half-2 first
build is merged from PR #1.

- **The script and filter match.**
  - `sp493_pull.py` here is identical to `origin/main` (git blob `2afd9da`).
  - The selftest passes all five checks, and the filter SHA-256 is `3a9b355c…`.
  - Python here is 3.13.14, while `ENVIRONMENT.txt` records 3.14.6. The selftest does not check the
    Python version, and the filter reproduces the 16 Mag 7 counts exactly.
- **Windows note:** with `core.autocrlf=true`, git checks out `filter_earnings_calls.py` with CRLF
  line endings. That fails the "filter unchanged" selftest check, although the code is identical.
  Re-check it out with `git -c core.autocrlf=false checkout -- filter_earnings_calls.py`.
- **The halves do not overlap.** 247 + 246 firms, no shared ticker folder, and no half-1 file
  touched on this branch.

**Pooled S&P 493 (after this rebuild):**

| | Half 1 | Half 2 | Total |
|---|---|---|---|
| Tier A firm-quarters | 1,280 | 1,100 | **2,380** |
| Tier B | 912 | 890 | **1,802** |
| Missing | 2,501 | 2,684 | **5,185** (of 9,367) |
| Firms with Tier A both before and after ChatGPT | 93 | 79 | **172** |
| Before only | 41 | 36 | 77 |
| After only | 13 | 8 | 21 |
| No Tier A call | 100 | 123 | 223 |

## 7. Mag 7

No change since the half-1 audit. `earnings_calls_canonical_extended/earnings_call_call_units.csv`
still has **133 calls: 7 firms × 19 quarters**. Its last change was c80f6a6, before both audits.
The 17 unapproved `earnings_calls_pre2022_extra/` calls are listed in half 1 §7.

## Recommended fixes to `sp493_pull.py` (not applied)

Fixes are listed in order of how much they matter.

1. **Malformed quarter token (STX).**
   - In `cmd_discover`, treat a final token matching `^q(?:earn\w*)?$` as part of the truncated
     tail, so the ticker before it is tested.
   - In `write_raw`, an old-layout (verbatim) page with no date line and no quarter in its title
     should get its label from `datePublished`. Verbatim pages are not backfilled; STX's was
     published a day after the call.
   - This recovers the one lost Tier A call, STX FY23 Q4 (2023 Q2).
2. **Name-only slugs ending in a stop word (SO).** In `cmd_discover`, skip the "name only (ticker
   differs)" branch when `toks[-1]` is in `NAME_STOP`, so `southern-co` falls through to "name only
   (no ticker in slug)". This recovers SO 2025 Q3. Half 1 should be re-checked for the same pattern.
3. **Ticker alias (SKYD).** Add an override next to `FYE_OVERRIDE`, such as
   `TICKER_ALIAS = {"SKYD": "PSKY"}`, merged into `other_tickers` when the universe loads. Do not
   rebuild `universe.csv`. This recovers SKYD 2025 Q4 and 2026 Q2.
4. **POSIX paths in CSVs.** Use `dest.relative_to(ROOT).as_posix()` in `write_raw`, and the same
   in `cmd_filter`, so `file` columns match across laptops.
5. **`fy-YYYY` slugs.** These need no change now. If slug parsing is ever widened to `fy-2021`
   pages, reject the EQIX, LYB and PWR conference pages by content: their titles claim "Earnings
   Call Transcript", and their first speaker is a conference host, not an operator.
6. **Rebuild.** About 4 new fetches (STX, SO and the two PSKY pages), then `write_raw`, `filter` and
   `report`. As in the half-1 rebuild, the generated half-2 outputs must be deleted first, which
   needs approval.
7. **Analysis.**
   - Pool by `calendar_year`/`calendar_quarter`, not by `period_label`. LRCX file names follow
     Fool's calendar labels, and the HD, KR and ULTA labels name the fiscal year by its start.
   - Drop the 45 files with no detected Q&A from section-level results.
   - Treat TWLO 2022 Q3 (Investor Day) as an outlier for unit counts.
   - Half 2 has no Utilities with Tier A calls after ChatGPT.
