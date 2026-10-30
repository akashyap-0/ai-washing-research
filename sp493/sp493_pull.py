"""
S&P 493 earnings-call pull: universe, discovery, download, filter, report.

Method and rules: sp493/SEARCH_AND_PULL_METHOD.md. Both laptops run the same
commit. Each runs only its own half (--half 1 or 2), so no output file is ever
written on both laptops and merging is a plain copy.

  python sp493/sp493_pull.py universe            # built once on half 1's laptop; never re-run
  python sp493/sp493_pull.py selftest            # both laptops, before anything else
  python sp493/sp493_pull.py discover --half N   # Fool monthly sitemaps -> candidate URLs
  python sp493/sp493_pull.py download --half N   # fetch pages, write raw transcripts
  python sp493/sp493_pull.py filter   --half N   # filter_earnings_calls on Tier A files
  python sp493/sp493_pull.py report   --half N   # who has calls before / after ChatGPT

Raw transcripts are never overwritten and never edited. Downloaded originals are
cached gzipped under cache/sp493_sources/ (gitignored) and logged with URL,
HTTP status, bytes and SHA-256.
"""

import argparse
import csv
import gzip
import hashlib
import html
import json
import os
import platform
import re
import sys
import time
from calendar import monthrange
from collections import Counter, defaultdict
from datetime import date, datetime, timezone
from pathlib import Path

import requests
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parent.parent
SP = ROOT / "sp493"
COVER = SP / "coverage"
ACQ = SP / "acquisition"
RAW_A = SP / "earnings_calls"            # Tier A: Fool verbatim (old layout)
RAW_B = SP / "earnings_calls_fool_llm"   # Tier B: Fool LLM layout, kept apart
AI_OUT = SP / "earnings_calls_ai_only"
CACHE = ROOT / "cache" / "sp493_sources"
UNIVERSE = SP / "universe.csv"
UNIVERSE_SHA = SP / "universe.sha256"
ENV_FILE = SP / "ENVIRONMENT.txt"
FILTER_PY = ROOT / "filter_earnings_calls.py"

WIKI_REVID = 1382178819
WIKI_API = "https://en.wikipedia.org/w/api.php"
SEC_SUBMISSIONS = "https://data.sec.gov/submissions/CIK{cik}.json"
MAG7 = {"AAPL", "AMZN", "GOOGL", "GOOG", "META", "MSFT", "NVDA", "TSLA"}

WINDOW = ((2021, 4), (2026, 2))          # calendar quarters, inclusive (scope §2)
CHATGPT = date(2022, 11, 30)
SITEMAP_MONTHS = [(y, m) for y in range(2021, 2027) for m in range(1, 13)
                  if (2021, 11) <= (y, m) <= (2026, 10)]

FOOL = "https://www.fool.com"
FOOL_UA = "Mozilla/5.0 (compatible; ai-washing-research academic study of earnings calls)"
FOOL_DELAY = 2.5                         # seconds between Fool requests, one at a time
MAX_FAILS = 5

# Mag 7 Fool call used by selftest to prove the converter reproduces committed files
SELFTEST_URL = (FOOL + "/earnings/call-transcripts/2023/05/24/"
                "nvidia-nvda-q1-2024-earnings-call-transcript/")
SELFTEST_FILE = ROOT / "earnings_calls" / "nvidia" / "nvidia_FY24_Q1.md"
MAG7_FOOL_DIRS = ["nvidia", "tesla"]

MONTH_RX = (r"(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec)[a-z]*\.?\s+(\d{1,2}),\s+(20\d\d)")
MONTH_ABBR = ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"]
REAL_CALL_DATE = {"page date line", "page DATE section"}
MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August",
          "September", "October", "November", "December"]


# ---------------------------------------------------------------------------
# Small helpers
# ---------------------------------------------------------------------------

def sha256(data):
    return hashlib.sha256(data).hexdigest()


def now_utc():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def read_csv(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def write_csv(path, rows, fields):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)


def norm_ticker(t):
    return re.sub(r"[^a-z0-9]", "", t.lower())


def folder_for(ticker):
    return ticker.lower().replace(".", "-")


# SEC data errors found by the half-1 audit. universe.csv stays as built (its hash is checked);
# the correction is applied here so both laptops get it.
FYE_OVERRIDE = {"BRO": "12"}   # SEC fiscalYearEnd 0119; Brown & Brown reports on the calendar year


def load_universe(half=None):
    rows = read_csv(UNIVERSE)
    for r in rows:
        if r["ticker"] in FYE_OVERRIDE:
            r["fye_month"] = FYE_OVERRIDE[r["ticker"]]
            r["fiscal_year_end"] += f", overridden to month {r['fye_month']}"
    return [r for r in rows if half is None or r["assigned_half"] == str(half)]


class Throttle:
    """One request at a time, at least `delay` seconds apart."""

    def __init__(self, delay):
        self.delay, self.last = delay, 0.0

    def wait(self):
        gap = time.monotonic() - self.last
        if gap < self.delay:
            time.sleep(self.delay - gap)
        self.last = time.monotonic()


_fool = Throttle(FOOL_DELAY)


def fool_get(url):
    """GET a fool.com URL politely. Returns (status, bytes). Backs off on 429/5xx."""
    for attempt in range(4):
        _fool.wait()
        try:
            r = requests.get(url, headers={"User-Agent": FOOL_UA}, timeout=60)
        except requests.RequestException as e:
            print(f"  network error {e!r}; retry in {30 * (attempt + 1)}s")
            time.sleep(30 * (attempt + 1))
            continue
        if r.status_code == 429 or r.status_code >= 500:
            wait = int(r.headers.get("Retry-After", 0) or 0) or 60 * (attempt + 1)
            print(f"  HTTP {r.status_code}; backing off {wait}s")
            time.sleep(wait)
            continue
        return r.status_code, r.content
    return r.status_code if "r" in locals() else 0, b""


# ---------------------------------------------------------------------------
# Calendar mapping (sp493/SEARCH_AND_PULL_METHOD.md §4.2, scope §3)
# ---------------------------------------------------------------------------

def fye_month(fye):
    """SEC fiscalYearEnd 'MMDD' -> month. A year end in the first 7 days of a
    month belongs to the previous month (52/53-week years, e.g. '0201' -> Jan)."""
    m, d = int(fye[:2]), int(fye[2:])
    if d <= 7:
        m = 12 if m == 1 else m - 1
    return m


def quarter_end_lag(call_date, fy_end_month, fq):
    """Days from the end of fiscal quarter `fq` (most recent occurrence at least 7 days
    before the call) to the call, for a firm whose fiscal year ends in `fy_end_month`."""
    e = (fy_end_month - 3 * (4 - fq) - 1) % 12 + 1
    for yy in (call_date.year, call_date.year - 1):
        lag = (call_date - date(yy, e, monthrange(yy, e)[1])).days
        if lag >= 7:
            return lag
    return lag


def infer_fye(calls):
    """Fiscal year-end month from Fool's own fiscal quarter labels and call dates: the
    month under which the most calls fall 7-100 days after their quarter end, ties
    broken by the shorter median lag. `calls` is [(date, fiscal_quarter)]."""
    best = None
    for f in range(1, 13):
        lags = sorted(quarter_end_lag(d, f, q) for d, q in calls)
        ok = sum(7 <= x <= 100 for x in lags)
        key = (ok, -lags[len(lags) // 2])
        if best is None or key > best[0]:
            best = (key, f, ok, lags[len(lags) // 2])
    _, f, ok, med = best
    return f, ok, med


def calendar_quarter(call_date, fy_end_month):
    """Reported quarter = latest fiscal quarter-end month at least 7 days before the
    call; it goes to the calendar quarter of its middle month."""
    ends = {(fy_end_month - 3 * k - 1) % 12 + 1 for k in range(4)}
    y, m = call_date.year, call_date.month
    for back in range(0, 14):
        mm = (m - back - 1) % 12 + 1
        yy = y + (m - back - 1) // 12
        if mm in ends and (call_date - date(yy, mm, monthrange(yy, mm)[1])).days >= 7:
            break
    mid_m, mid_y = (mm - 2) % 12 + 1, (yy if mm != 1 else yy - 1)
    return mid_y, (mid_m - 1) // 3 + 1


def label_quarter(fool_y, fool_q, fy_end_month, year_shift=0):
    """Calendar quarter of Fool's fiscal label 'Q<fool_q> <fool_y>', reading the fiscal year
    as the calendar year it ends in (Fool's usual convention; year_shift=+1 covers firms
    that name the fiscal year by the year it starts). Same middle-month rule."""
    e = (fy_end_month - 3 * (4 - fool_q) - 1) % 12 + 1
    ey = (fool_y + year_shift) if e <= fy_end_month else (fool_y + year_shift - 1)
    mid_m, mid_y = (e - 2) % 12 + 1, (ey if e != 1 else ey - 1)
    return mid_y, (mid_m - 1) // 3 + 1


def label_quarter_end(fool_y, fool_q, fy_end_month, year_shift=0):
    """Last day of the fiscal quarter named by Fool's label (see label_quarter)."""
    e = (fy_end_month - 3 * (4 - fool_q) - 1) % 12 + 1
    ey = (fool_y + year_shift) if e <= fy_end_month else (fool_y + year_shift - 1)
    return date(ey, e, monthrange(ey, e)[1])


def label_from_call(call_date, fy_end_month):
    """Fiscal (year, quarter) reported on `call_date`: latest quarter end >= 7 days before,
    fiscal year named by the calendar year it ends in."""
    ends = {(fy_end_month - 3 * k - 1) % 12 + 1 for k in range(4)}
    y, m = call_date.year, call_date.month
    for back in range(0, 14):
        mm = (m - back - 1) % 12 + 1
        yy = y + (m - back - 1) // 12
        if mm in ends and (call_date - date(yy, mm, monthrange(yy, mm)[1])).days >= 7:
            break
    fq = 4 - ((fy_end_month - mm) % 12) // 3
    return (yy if mm <= fy_end_month else yy + 1), fq


def in_window(cy, cq):
    return WINDOW[0] <= (cy, cq) <= WINDOW[1]


def window_quarters():
    out, (y, q) = [], WINDOW[0]
    while (y, q) <= WINDOW[1]:
        out.append((y, q))
        y, q = (y + 1, 1) if q == 4 else (y, q + 1)
    return out


# ---------------------------------------------------------------------------
# universe (run once)
# ---------------------------------------------------------------------------

def cmd_universe(args):
    if UNIVERSE.exists() and not args.force:
        sys.exit(f"{UNIVERSE} exists. It is the source of truth for both laptops; not rebuilding.")
    sec_ua = os.environ.get("SEC_USER_AGENT", "")
    if not sec_ua:
        sys.exit("SEC_USER_AGENT is not set (SEC requires 'Name email' in the User-Agent).")
    r = requests.get(WIKI_API, params={"action": "parse", "oldid": WIKI_REVID, "prop": "text|revid",
                                       "format": "json", "formatversion": 2},
                     headers={"User-Agent": FOOL_UA}, timeout=60)
    r.raise_for_status()
    soup = BeautifulSoup(r.json()["parse"]["text"], "html.parser")
    table = soup.find("table", id="constituents")
    rows = []
    for tr in table.find_all("tr")[1:]:
        c = [td.get_text(" ", strip=True) for td in tr.find_all(["td", "th"])]
        rows.append({"ticker": c[0], "security": c[1], "gics_sector": c[2],
                     "gics_sub_industry": c[3], "date_added": c[5], "cik": c[6].zfill(10)})
    print(f"Wikipedia revision {WIKI_REVID}: {len(rows)} tickers")
    by_cik, order = {}, []
    for row in rows:                                  # dual-class: first listed ticker kept
        if row["cik"] in by_cik:
            by_cik[row["cik"]]["other_tickers"].append(row["ticker"])
            continue
        row["other_tickers"] = []
        by_cik[row["cik"]] = row
        order.append(row["cik"])
    firms = [by_cik[c] for c in order
             if by_cik[c]["ticker"] not in MAG7 and not MAG7 & set(by_cik[c]["other_tickers"])]
    print(f"{len(by_cik)} companies, {len(firms)} after removing the Mag 7")

    sec_dir = CACHE / "sec"                           # only for each firm's fiscal year end
    sec_dir.mkdir(parents=True, exist_ok=True)
    for f in firms:
        p = sec_dir / f"CIK{f['cik']}.json"
        if not p.exists():
            time.sleep(0.25)                          # SEC fair access: < 10 requests/s
            resp = requests.get(SEC_SUBMISSIONS.format(cik=f["cik"]),
                                headers={"User-Agent": sec_ua}, timeout=60)
            resp.raise_for_status()
            p.write_bytes(resp.content)
        fy = json.loads(p.read_text(encoding="utf-8")).get("fiscalYearEnd") or ""
        f["fiscal_year_end"], f["fye_month"] = fy, (fye_month(fy) if fy else "")
    missing = [f["ticker"] for f in firms if not f["fye_month"]]
    if missing:
        sys.exit(f"no SEC fiscalYearEnd for {missing}")

    firms.sort(key=lambda f: f["ticker"])
    for i, f in enumerate(firms):                     # alternate: rows 1,3,5... -> half 1
        f["assigned_half"] = 1 if i % 2 == 0 else 2
        f["folder"] = folder_for(f["ticker"])
        f["other_tickers"] = ";".join(f["other_tickers"])
    fields = ["ticker", "other_tickers", "security", "cik", "gics_sector", "gics_sub_industry",
              "date_added", "fiscal_year_end", "fye_month", "folder", "assigned_half"]
    write_csv(UNIVERSE, firms, fields)
    digest = sha256(UNIVERSE.read_bytes())
    UNIVERSE_SHA.write_text(f"{digest}  universe.csv\n", encoding="utf-8")
    write_environment(digest)
    print(f"wrote {UNIVERSE} ({len(firms)} firms; half 1 = "
          f"{sum(f['assigned_half'] == 1 for f in firms)}, half 2 = "
          f"{sum(f['assigned_half'] == 2 for f in firms)}), sha256 {digest}")


def environment():
    import bs4
    import nltk
    return {"python": platform.python_version(), "nltk": nltk.__version__, "bs4": bs4.__version__,
            "filter_earnings_calls.py sha256": sha256(FILTER_PY.read_bytes())}


def write_environment(universe_digest):
    env = environment()
    lines = [f"{k}: {v}" for k, v in env.items()]
    lines += [f"wikipedia revid: {WIKI_REVID}", f"universe.csv sha256: {universe_digest}",
              f"written: {now_utc()}"]
    ENV_FILE.write_text("\n".join(lines) + "\n", encoding="utf-8")


# ---------------------------------------------------------------------------
# Fool page -> transcript text
# ---------------------------------------------------------------------------

STOP_H2 = {"Read Next", "Premium Investing Services"}
MORE_ANALYSIS = re.compile(r"^More [A-Z.\-]+ analysis$")


def _blocks_from(start):
    """Text of every <h2>/<p> from `start` on, one block each, until the page's
    'Read Next' section or Fool's 'More XYZ analysis' link after the roster."""
    out, on = [], False
    for el in start.parent.find_all(["h2", "p"]):
        if el is start:
            on = True
        if not on:
            continue
        txt = re.sub(r"[ \t\r\f\v]+", " ", el.get_text()).strip()
        if (el.name == "h2" and txt in STOP_H2) or MORE_ANALYSIS.match(txt):
            break
        if txt:
            out.append(txt)
    return out


def parse_fool_page(raw_html):
    """Returns dict(layout, title, fool_q, fool_y, call_date, call_date_source, body)."""
    soup = BeautifulSoup(raw_html, "html.parser")
    h2s = {h.get_text(strip=True).upper(): h for h in soup.find_all("h2")}   # "DATE" or "Date"
    h1 = soup.find("h1")
    title = h1.get_text(" ", strip=True) if h1 else ""
    info = {"title": title, "fool_q": "", "fool_y": "", "call_date": "", "call_date_source": ""}
    m = re.search(r"\bQ([1-4])\s+(20\d\d)\b", title)
    if m:
        info["fool_q"], info["fool_y"] = m.group(1), m.group(2)

    if "PREPARED REMARKS:" in h2s:
        info["layout"] = "fool_verbatim"
        info["body"] = "\n\n".join(_blocks_from(h2s["PREPARED REMARKS:"]))
        d = soup.find("span", id="date")
        if d:
            try:
                info["call_date"] = datetime.strptime(d.get_text(strip=True), "%b %d, %Y").date()
                info["call_date_source"] = "page date line"
            except ValueError:
                pass
    elif "FULL CONFERENCE CALL TRANSCRIPT" in h2s:
        info["layout"] = "fool_llm"
        blocks = _blocks_from(h2s["FULL CONFERENCE CALL TRANSCRIPT"])
        info["body"] = "\n\n".join(blocks)
        if "DATE" in h2s:
            nxt = h2s["DATE"].find_next(["p", "ul", "div"])
            txt = nxt.get_text(" ", strip=True) if nxt else ""
            dm = re.search(MONTH_RX, txt)             # "Thursday, Oct. 31, 2024 at 8:30 a.m. ET"
            if dm:
                info["call_date"] = date(int(dm.group(3)), MONTH_ABBR.index(dm.group(1)[:3].lower()) + 1,
                                         int(dm.group(2)))
                info["call_date_source"] = "page DATE section"
    else:
        info["layout"] = "unknown"
        info["body"] = ""
    if not info["call_date"]:
        pm = re.search(r'"datePublished":"(20\d\d)-(\d\d)-(\d\d)', raw_html)
        if pm:
            info["call_date"] = date(int(pm.group(1)), int(pm.group(2)), int(pm.group(3)))
            info["call_date_source"] = "page datePublished (publication date, not call date)"
    return info


# ---------------------------------------------------------------------------
# selftest
# ---------------------------------------------------------------------------

def cmd_selftest(args):
    ok = True

    def check(name, cond, detail=""):
        nonlocal ok
        ok &= bool(cond)
        print(f"[{'PASS' if cond else 'FAIL'}] {name}{(' - ' + detail) if detail else ''}")

    want = UNIVERSE_SHA.read_text(encoding="utf-8").split()[0]
    got = sha256(UNIVERSE.read_bytes())
    check("universe.csv matches universe.sha256", want == got, got[:16])

    recorded = dict(line.split(": ", 1) for line in ENV_FILE.read_text(encoding="utf-8").splitlines()
                    if ": " in line)
    env = environment()
    check("nltk version equals ENVIRONMENT.txt", env["nltk"] == recorded.get("nltk"),
          f"here {env['nltk']}, recorded {recorded.get('nltk')}")
    check("filter_earnings_calls.py unchanged",
          env["filter_earnings_calls.py sha256"] == recorded.get("filter_earnings_calls.py sha256"))

    cached = CACHE / "selftest" / "nvidia_FY24_Q1.html.gz"
    if not cached.exists():
        status, data = fool_get(SELFTEST_URL)
        if status != 200:
            check("fetch Mag 7 Fool page for converter test", False, f"HTTP {status}")
            sys.exit(1)
        cached.parent.mkdir(parents=True, exist_ok=True)
        cached.write_bytes(gzip.compress(data))
    page = parse_fool_page(gzip.decompress(cached.read_bytes()).decode("utf-8", "replace"))
    committed = SELFTEST_FILE.read_text(encoding="utf-8").split("\n---\n", 1)[1]
    check("converter reproduces committed nvidia_FY24_Q1.md body",
          page["body"].strip() == committed.strip(), f"layout {page['layout']}")

    sys.path.insert(0, str(ROOT))
    import filter_earnings_calls as fec
    stats = json.loads((ROOT / "earnings_calls_ai_only" / "_stats.json").read_text(encoding="utf-8"))
    bad = []
    n = 0
    for company in MAG7_FOOL_DIRS:
        for path in sorted((ROOT / "earnings_calls" / company).glob(f"{company}_*.md")):
            ref = stats.get(path.stem)
            if not ref or ref["format"] != "fool":
                continue
            _, s, _ = fec.process_file(path, company)
            n += 1
            if (s["total"], s["ai"], s["ai_by_section"]) != (ref["total"], ref["ai"], ref["ai_by_section"]):
                bad.append(f"{path.stem}: {s['total']}/{s['ai']} vs committed {ref['total']}/{ref['ai']}")
    check(f"filter reproduces committed counts on {n} Mag 7 Fool calls", not bad, "; ".join(bad[:5]))
    print("selftest", "PASSED" if ok else "FAILED")
    if not ok:
        sys.exit(1)


# ---------------------------------------------------------------------------
# discover
# ---------------------------------------------------------------------------

LOC = re.compile(r"<loc>(https://www\.fool\.com/earnings/call-transcripts/"
                 r"(20\d\d)/(\d\d)/(\d\d)/([^/<]+)/?)</loc>")
SLUG = re.compile(r"^(?P<pre>[a-z0-9-]+?)-q(?P<q>[1-4])-(?P<y>20\d\d)(?:-|$)")
TRUNC_TAIL = re.compile(r"^(?:q[1-4]?|20\d{0,2}|earn\w*|call|transcri\w*|tr\w*|t)$")
NAME_STOP = {"inc", "corp", "corporation", "co", "company", "companies", "the", "group", "holdings",
             "holding", "plc", "ltd", "limited", "incorporated", "class", "a", "b", "and", "of",
             "nv", "sa", "lp", "trust", "international", "technologies", "technology"}


def name_tokens(name):
    toks = re.sub(r"[^a-z0-9 ]", " ", name.lower().replace("&", " ").replace("'", "")).split()
    return [t for t in toks if t not in NAME_STOP]


def names_agree(slug_toks, firm):
    a = [t for t in slug_toks if t not in NAME_STOP]
    for name in (firm["security"],):
        b = name_tokens(name)
        if {t for t in a if len(t) >= 3} & {t for t in b if len(t) >= 3}:
            return True
        ja, jb = "".join(a), "".join(b)
        if ja and jb and (ja.startswith(jb[:5]) or jb.startswith(ja[:5])):
            return True
    return False


def fetch_sitemaps(half):
    d = CACHE / "sitemaps"
    d.mkdir(parents=True, exist_ok=True)
    log = []
    for y, m in SITEMAP_MONTHS:
        p = d / f"{y}_{m:02d}.xml"
        if not p.exists():
            status, data = fool_get(f"{FOOL}/sitemap/{y}/{m:02d}")
            if status != 200 or b"<urlset" not in data:
                sys.exit(f"sitemap {y}/{m:02d}: HTTP {status}; stopping")
            p.write_bytes(data)
            fetched = now_utc()
        else:
            fetched = "cached"
        data = p.read_bytes()
        log.append({"month": f"{y}-{m:02d}", "bytes": len(data), "sha256": sha256(data),
                    "transcript_urls": len(LOC.findall(data.decode("utf-8", "replace"))),
                    "fetched_utc": fetched})
    write_csv(COVER / f"half{half}_sitemaps.csv", log,
              ["month", "bytes", "sha256", "transcript_urls", "fetched_utc"])
    return [p for p in sorted(d.glob("*.xml"))]


def cmd_discover(args):
    universe = load_universe()
    mine = {f["ticker"] for f in universe if f["assigned_half"] == str(args.half)}
    by_tick = {}
    for f in universe:
        for t in [f["ticker"]] + [x for x in f["other_tickers"].split(";") if x]:
            by_tick[norm_ticker(t)] = f
    by_name = {"".join(name_tokens(f["security"])): f for f in universe}

    seen, matched, rejected = set(), [], []
    for p in fetch_sitemaps(args.half):
        for url, y, mo, dd, slug in LOC.findall(p.read_text(encoding="utf-8", errors="replace")):
            if url in seen:
                continue
            seen.add(url)
            m = SLUG.match(slug)
            pre = m.group("pre") if m else slug
            toks = pre.split("-")
            while not m and toks and TRUNC_TAIL.match(toks[-1]):   # slug cut at ~50 chars
                toks.pop()
            firm, how, name = None, "", toks
            for k in (2, 1):                                  # 'brk-b' before 'b'
                if len(toks) >= k and norm_ticker("".join(toks[-k:])) in by_tick:
                    cand = by_tick[norm_ticker("".join(toks[-k:]))]
                    firm, name = cand, toks[:-k]
                    if names_agree(toks[:-k], cand):
                        how = "ticker+name"
                    else:                             # 'txn-q1-2026', or short/old names: amex, ibm
                        how = ("ticker only (no name in slug)" if not toks[:-k]
                               else "ticker only (name differs)")
                        rejected.append({"url": url, "slug_ticker": "-".join(toks[-k:]),
                                         "slug_name": "-".join(toks[:-k]),
                                         "universe_ticker": cand["ticker"],
                                         "universe_name": cand["security"]})
                    break
            if firm is None and len(toks) > 1:              # ticker changed since: full-name match
                key = "".join(t for t in toks[:-1] if t not in NAME_STOP)
                if key in by_name:
                    firm, how = by_name[key], "name only (ticker differs)"
            if firm is None:                                  # 'texas-instruments-q2-2025': no ticker
                key = "".join(t for t in toks if t not in NAME_STOP)
                if key in by_name:
                    firm, how = by_name[key], "name only (no ticker in slug)"
            if firm is None or firm["ticker"] not in mine:
                continue
            matched.append({"ticker": firm["ticker"], "url": url,
                            "url_date": date(int(y), int(mo), int(dd)).isoformat(),
                            "slug": slug, "fool_q": m.group("q") if m else "",
                            "fool_y": m.group("y") if m else "", "matched_by": how})
    first_ticker_page = {}                            # a name-only match must predate the firm's
    for r in matched:                                 # first page under its current ticker
        if not r["matched_by"].startswith("name"):
            first_ticker_page[r["ticker"]] = min(r["url_date"], first_ticker_page.get(r["ticker"], "9999"))
    dropped = [r for r in matched if r["matched_by"] == "name only (ticker differs)"
               and r["url_date"] >= first_ticker_page.get(r["ticker"], "9999")]
    matched = [r for r in matched if r not in dropped]
    for r in matched:
        if r["matched_by"].startswith("name"):
            rejected.append({"url": r["url"], "slug_ticker": r["slug"].split("-q")[0].split("-")[-1],
                             "slug_name": r["slug"], "universe_ticker": r["ticker"],
                             "universe_name": "name-only match: check it is the same company"})
    print(f"name-only matches dropped because the firm already had pages under its ticker: {len(dropped)}")
    mag7_fye_check(seen)
    sec = {f["ticker"]: int(f["fye_month"]) for f in universe}
    check = []
    for t in sorted(mine):                            # cross-check SEC against Fool's own labels
        calls = [(date.fromisoformat(r["url_date"]), int(r["fool_q"]))
                 for r in matched if r["ticker"] == t and r["fool_q"]]
        f, ok, med = infer_fye(calls) if calls else ("", 0, "")
        check.append({"ticker": t, "sec_fye_month": sec[t], "inferred_fye_month": f,
                      "calls_used": len(calls), "calls_consistent": ok, "median_lag_days": med,
                      "agree": (f == sec[t]) if calls else ""})
    write_csv(COVER / f"half{args.half}_fiscal_year_ends.csv", check, list(check[0].keys()))
    disagree = [c["ticker"] for c in check if c["agree"] is False]
    print(f"fiscal year end: SEC vs Fool-label inference disagree for {len(disagree)} firms {disagree[:15]}")
    for r in matched:                                 # Fool backfills old calls years later, so the
        f = sec[r["ticker"]]                          # fiscal label decides, not the URL date
        by_url = calendar_quarter(date.fromisoformat(r["url_date"]), f)
        if r["fool_q"]:
            fy, fq = int(r["fool_y"]), int(r["fool_q"])
            cands = [label_quarter(fy, fq, f, k) for k in (0, 1, -1)]
            cy, cq = cands[0]
        else:
            cands, (cy, cq) = [by_url], by_url
        r["prelim_cal_quarter"] = f"{cy}Q{cq}"
        r["prelim_in_window"] = any(in_window(*c) for c in cands + [by_url])
    matched.sort(key=lambda r: (r["ticker"], r["url_date"]))
    write_csv(COVER / f"half{args.half}_fool_urls.csv", matched, list(matched[0].keys()))
    rej_mine = [r for r in rejected if r["universe_ticker"] in mine]
    write_csv(COVER / f"half{args.half}_name_check.csv", rej_mine,
              ["url", "slug_ticker", "slug_name", "universe_ticker", "universe_name"])
    inwin = [r for r in matched if r["prelim_in_window"]]
    firms_hit = {r["ticker"] for r in inwin}
    print(f"{len(seen)} Fool transcript URLs in {len(SITEMAP_MONTHS)} sitemaps; "
          f"{len(matched)} matched to half {args.half} ({len(inwin)} in window, "
          f"{len(firms_hit)}/{len(mine)} firms); {len(rej_mine)} accepted on ticker with a different name (see half{args.half}_name_check.csv); "
          f"{sum(r['matched_by'].startswith('name') for r in matched)} matched by name only")
    prelim_summary(args.half, inwin, mine)


MAG7_FYE = {"aapl": 9, "msft": 6, "nvda": 1, "googl": 12, "meta": 12, "amzn": 12, "tsla": 12}


def mag7_fye_check(urls):
    """The inference must recover the Mag 7's known fiscal year ends from the same sitemaps."""
    got = {}
    for t, want in MAG7_FYE.items():
        calls = []
        for u in urls:
            m = re.search(rf"/(20\d\d)/(\d\d)/(\d\d)/[a-z0-9-]*-{t}-q([1-4])-20\d\d", u)
            if m:
                calls.append((date(int(m.group(1)), int(m.group(2)), int(m.group(3))), int(m.group(4))))
        got[t] = infer_fye(calls)[0] if calls else None
    wrong = {t: g for t, g in got.items() if g != MAG7_FYE[t]}
    print(f"Mag 7 fiscal-year-end check: {got} -> {'PASS' if not wrong else 'FAIL ' + str(wrong)}")
    if wrong:
        sys.exit("fiscal-year-end inference failed on the Mag 7; stopping")


def prelim_summary(half, rows, mine):
    pre = defaultdict(set)
    post = defaultdict(set)
    for r in rows:
        cy, cq = int(r["prelim_cal_quarter"][:4]), int(r["prelim_cal_quarter"][-1])
        if in_window(cy, cq):
            (pre if (cy, cq) <= (2022, 3) else post)[r["ticker"]].add(r["prelim_cal_quarter"])
    both = sum(1 for t in mine if pre[t] and post[t])
    print(f"preliminary (fiscal labels, any layout): {both} firms with calls both before and after ChatGPT, "
          f"{sum(1 for t in mine if pre[t] and not post[t])} before only, "
          f"{sum(1 for t in mine if post[t] and not pre[t])} after only, "
          f"{sum(1 for t in mine if not pre[t] and not post[t])} none")


# ---------------------------------------------------------------------------
# download
# ---------------------------------------------------------------------------

TITLE_NOISE = re.compile(r"\b(?:Q[1-4]|FY|20\d\d|Earnings|Call|Conference|Transcripts?)\b", re.I)


def old_tickers(cand):
    """A page matched through a ticker change (Block SQ -> XYZ) may show the old ticker."""
    if cand.get("matched_by") != "name only (ticker differs)":
        return ()
    m = SLUG.match(cand["slug"])
    return ((m.group("pre") if m else cand["slug"]).split("-")[-1].upper(),)


def title_names_firm(title, firm, old_tickers=()):
    """The page title must carry one of the firm's tickers (as written) or its name, and must not
    carry a different ticker in parentheses ('Black Stone Minerals (BSM)' is not Blackstone)."""
    mine = [firm["ticker"]] + [x for x in firm["other_tickers"].split(";") if x] + list(old_tickers)
    shown = re.search(r"\(([A-Z][A-Z.\-]{0,6})\)", title)
    if shown and norm_ticker(shown.group(1)) not in {norm_ticker(t) for t in mine}:
        return False
    for t in mine:
        for v in {t, t.replace(".", "-"), t.replace(".", "")}:
            if re.search(rf"(?<![A-Za-z]){re.escape(v)}(?![A-Za-z])", title):
                return True
    return names_agree(name_tokens(TITLE_NOISE.sub(" ", title)), firm)


def header_block(firm, info, url, sha, period_label, cy, cq, half, layout, retrieved):
    d = info["call_date"]
    held = f"{MONTHS[d.month - 1]} {d.day}, {d.year}"
    fye = f"{MONTHS[int(firm['fye_month']) - 1]} (SEC fiscalYearEnd {firm['fiscal_year_end']})"
    stype = ("third_party_transcript_motley_fool" if layout == "fool_verbatim"
             else "third_party_transcript_motley_fool_llm")
    lines = [
        f"# {firm['security']} — {period_label} Earnings Call (transcript)",
        "",
        f"- **Company:** {firm['security']} ({firm['ticker']}); fiscal year ends {fye}",
        f"- **Ticker:** {firm['ticker']}" + (f" (also {firm['other_tickers']})" if firm["other_tickers"] else ""),
        f"- **CIK:** {firm['cik']}",
        f"- **Period:** {period_label} (call held {held}; date from {info['call_date_source']})",
        f"- **Calendar quarter:** {cy} Q{cq} (middle-month rule, sp493/SEARCH_AND_PULL_METHOD.md §4.2)",
        f"- **Source:** third-party transcript, The Motley Fool — {url}",
        f"- **Source type:** {stype}",
        f"- **Retrieved:** {retrieved} (S&P 493 pull, half {half})",
        f"- **Source SHA-256:** {sha}",
        "- **Extraction:** article <h2>/<p> blocks, one per line with a blank line between, "
        "HTML unescaped, tags stripped (sp493/sp493_pull.py)",
        "- **Note:** official company transcripts were not searched for in this pull. Fool "
        "transcripts have speaker labels but are third-party (minor errors possible); fine for "
        "private research, check terms before redistributing",
    ]
    if layout == "fool_llm":
        lines.append("- **Quality warning:** Fool 2025+ layout. The page says parts were created with "
                     "LLMs; text is close to but not verbatim (86.8-89.4% word match to official "
                     "transcripts), the IR opening is usually dropped and analysts are often "
                     "unlabeled. Tier B: not filtered or pooled until calibrated")
    return "\n".join(lines) + "\n\n---\n\n"


def cache_path(folder, url, slug):
    """Cache file per URL: two Fool URLs can share a slug (generic 'unh-earnings-call-transcript')."""
    y, mo, d = re.search(r"/call-transcripts/(20\d\d)/(\d\d)/(\d\d)/", url).groups()
    return CACHE / "fool" / folder / f"{y}-{mo}-{d}_{slug}.html.gz"


def migrate_slug_cache(half, universe, cands):
    """Older runs cached by slug only. Give each such file to the URL it was fetched for
    (matching the logged SHA-256), so a second URL with the same slug gets fetched."""
    log_sha = defaultdict(list)
    log_path = ACQ / f"half{half}_results.jsonl"
    if log_path.exists():
        for line in log_path.read_text(encoding="utf-8").splitlines():
            rec = json.loads(line)
            if rec.get("status") == 200:
                log_sha[rec["sha256"]].append(rec["url"])
    by_slug = defaultdict(list)
    for r in cands:
        by_slug[(universe[r["ticker"]]["folder"], r["slug"])].append(r)
    moved = 0
    for (folder, slug), rs in by_slug.items():
        old = CACHE / "fool" / folder / f"{slug}.html.gz"
        if not old.exists():
            continue
        digest = sha256(gzip.decompress(old.read_bytes()))
        urls = {r["url"] for r in rs}
        owner = next((u for u in log_sha.get(digest, []) if u in urls),
                     min(rs, key=lambda r: r["url_date"])["url"])     # first run fetched earliest first
        new = cache_path(folder, owner, slug)
        if not new.exists():
            os.replace(old, new)
            moved += 1
    if moved:
        print(f"moved {moved} slug-keyed cache files to per-URL names")


def cmd_download(args):
    universe = {f["ticker"]: f for f in load_universe(args.half)}
    cands = [r for r in read_csv(COVER / f"half{args.half}_fool_urls.csv")
             if r["prelim_in_window"] == "True" or not r["fool_q"]]
    ACQ.mkdir(parents=True, exist_ok=True)
    log_path = ACQ / f"half{args.half}_results.jsonl"
    done = set()
    if log_path.exists():
        for line in log_path.read_text(encoding="utf-8").splitlines():
            rec = json.loads(line)
            if rec.get("status") in (200, 410):        # 404s are retried: Fool's are often transient
                done.add(rec["url"])
    print(f"{len(cands)} candidate pages for half {args.half}; {len(done)} already logged")
    migrate_slug_cache(args.half, universe, cands)

    fails = 0
    with open(log_path, "a", encoding="utf-8") as log:
        for i, r in enumerate(cands, 1):
            folder = universe[r["ticker"]]["folder"]
            cpath = cache_path(folder, r["url"], r["slug"])
            if cpath.exists():
                continue
            status, data = fool_get(r["url"])
            rec = {"ticker": r["ticker"], "url": r["url"], "status": status, "bytes": len(data),
                   "sha256": sha256(data) if data else "", "retrieved_utc": now_utc()}
            if status == 200 and data:
                cpath.parent.mkdir(parents=True, exist_ok=True)
                tmp = cpath.with_name(cpath.name + ".part")    # atomic: sleep or kill mid-write
                tmp.write_bytes(gzip.compress(data))            # never leaves a half file
                os.replace(tmp, cpath)
                rec["layout"] = parse_fool_page(data.decode("utf-8", "replace"))["layout"]
                fails = 0
            elif status in (404, 410):
                fails = 0
            else:
                fails += 1
            log.write(json.dumps(rec) + "\n")
            log.flush()
            if i % 25 == 0 or status != 200:
                print(f"  {i}/{len(cands)} {r['ticker']:6s} HTTP {status} {r['slug'][:60]}")
            if fails >= MAX_FAILS:
                sys.exit(f"{MAX_FAILS} failures in a row (last HTTP {status}); stopping. Re-run later.")
    write_raw(args.half, universe, cands)


def write_raw(half, universe, cands):
    """Parse every cached page, keep one main call per company x calendar quarter, write raw files."""
    shas, fetched = {}, {}                            # SHA-256 and fetch date per URL, from the log
    log_path = ACQ / f"half{half}_results.jsonl"
    for line in log_path.read_text(encoding="utf-8").splitlines():
        rec = json.loads(line)
        if rec.get("status") == 200:
            shas[rec["url"]] = rec["sha256"]
            fetched.setdefault(rec["url"], rec["retrieved_utc"][:10])
    calls = []
    for r in cands:
        firm = universe[r["ticker"]]
        cpath = cache_path(firm["folder"], r["url"], r["slug"])
        if not cpath.exists():
            continue
        raw = gzip.decompress(cpath.read_bytes())
        info = parse_fool_page(raw.decode("utf-8", "replace"))
        info["fool_q"] = info["fool_q"] or r["fool_q"]
        info["fool_y"] = info["fool_y"] or r["fool_y"]
        if not info["call_date"]:
            info["call_date"] = date.fromisoformat(r["url_date"])
            info["call_date_source"] = "URL date (publication date, not call date)"
        real_date = info["call_date_source"] in REAL_CALL_DATE
        f = int(firm["fye_month"])
        if not info["fool_q"] and real_date:          # title and slug carry no quarter
            fy_, fq_ = label_from_call(info["call_date"], f)
            info["fool_y"], info["fool_q"] = str(fy_), str(fq_)
            info["label_source"] = "derived from call date"
        else:
            info["label_source"] = "Fool title/slug"
        status = "ok"
        if info["layout"] == "unknown":
            status = "unknown layout"
        elif not re.search(r"Earnings (Call|Transcript)", info["title"], re.I):
            status = "not a main earnings call"
        elif not info["fool_q"]:
            status = "no fiscal quarter in title or slug"
        elif not title_names_firm(info["title"], firm, old_tickers(r)):
            status = "title names another company"
        lab = label_quarter(int(info["fool_y"]), int(info["fool_q"]), f) if info["fool_q"] else None
        fits = []
        if lab is not None:                           # days from the labelled quarter end to the date
            lags = {k: (info["call_date"] - label_quarter_end(int(info["fool_y"]), int(info["fool_q"]), f, k)).days
                    for k in (0, 1, -1)}
            repost = all(x > 120 for x in lags.values())   # dated long after any reading of the label
            fits = [k for k, x in lags.items() if -31 <= x <= 120]
        else:
            repost = False
        if real_date and fits:                        # the label read the way that fits the call date
            (cy, cq), method = label_quarter(int(info["fool_y"]), int(info["fool_q"]), f, fits[0]), \
                "fiscal label (fits call date)"       # Costco-style mid-month quarter ends
        elif lab is None or (real_date and not repost):
            cy, cq = calendar_quarter(info["call_date"], f)
            method = "call date"
        elif repost:                                  # Fool backfill: page date is the repost date
            (cy, cq), method = lab, "fiscal label (page date is a later repost)"
        else:                                         # only a publication date on the page
            (cy, cq), method = lab, "fiscal label (no call date on page)"
        info["quarter_method"] = method
        info["label_agrees"] = "" if lab is None else (lab == (cy, cq))
        if status == "ok" and not in_window(cy, cq):
            status = "outside window"
        calls.append({"ticker": r["ticker"], "url": r["url"], "slug": r["slug"], "info": info,
                      "cy": cy, "cq": cq, "status": status, "sha": shas.get(r["url"]) or sha256(raw),
                      "retrieved": fetched.get(r["url"], "unknown (cached before logging)")})

    same = defaultdict(list)                          # Fool sometimes serves one call at two URLs
    for c in calls:
        if c["status"] == "ok" and c["info"]["body"]:
            same[(c["ticker"], sha256(c["info"]["body"].encode("utf-8")))].append(c)
    for g in same.values():
        g.sort(key=lambda c: c["info"]["call_date"])
        for extra in g[1:]:
            extra["status"] = f"same text as {g[0]['slug']}"

    groups = defaultdict(list)
    for c in calls:
        if c["status"] == "ok":
            groups[(c["ticker"], c["cy"], c["cq"])].append(c)
    rank = {"fool_verbatim": 0, "fool_llm": 1}
    for key, g in groups.items():
        g.sort(key=lambda c: (rank[c["info"]["layout"]], c["info"]["call_date"]))
        for extra in g[1:]:
            extra["status"] = f"duplicate of {g[0]['slug']}"

    rows = []
    for c in calls:
        firm, info = universe[c["ticker"]], c["info"]
        fy2 = info["fool_y"][2:] if info["fool_y"] else ""
        period = (f"{info['fool_y']}_Q{info['fool_q']}" if firm["fye_month"] == "12"
                  else f"FY{fy2}_Q{info['fool_q']}")
        path = ""
        if c["status"] == "ok":
            base = RAW_A if info["layout"] == "fool_verbatim" else RAW_B
            dest = base / firm["folder"] / f"{firm['folder']}_{period}.md"
            if not dest.exists():                           # never overwrite
                dest.parent.mkdir(parents=True, exist_ok=True)
                dest.write_text(header_block(firm, info, c["url"], c["sha"], period, c["cy"], c["cq"],
                                             half, info["layout"], c["retrieved"]) + info["body"] + "\n",
                                encoding="utf-8")
            path = str(dest.relative_to(ROOT))
        rows.append({"ticker": c["ticker"], "period_label": period, "calendar_year": c["cy"],
                     "calendar_quarter": c["cq"], "call_date": info["call_date"].isoformat(),
                     "call_date_source": info["call_date_source"],
                     "quarter_method": info["quarter_method"], "label_agrees": info["label_agrees"],
                     "label_source": info["label_source"],
                     "pre_chatgpt": info["call_date"] < CHATGPT, "layout": info["layout"],
                     "tier": {"fool_verbatim": "A", "fool_llm": "B"}.get(info["layout"], ""),
                     "status": c["status"], "title": info["title"], "url": c["url"],
                     "source_sha256": c["sha"], "file": path})
    rows.sort(key=lambda r: (r["ticker"], r["calendar_year"], r["calendar_quarter"], r["call_date"]))
    write_csv(COVER / f"half{half}_calls.csv", rows, list(rows[0].keys()))

    avail = []
    kept = {(r["ticker"], r["calendar_year"], r["calendar_quarter"]): r for r in rows if r["status"] == "ok"}
    for t in sorted(universe):
        for cy, cq in window_quarters():
            r = kept.get((t, cy, cq))
            avail.append({"ticker": t, "calendar_year": cy, "calendar_quarter": cq,
                          "status": f"tier{r['tier']}" if r else "missing",
                          "period_label": r["period_label"] if r else "",
                          "call_date": r["call_date"] if r else "", "url": r["url"] if r else ""})
    write_csv(COVER / f"half{half}_availability.csv", avail, list(avail[0].keys()))
    st = Counter(r["status"] for r in avail)
    print(f"raw files written; availability for {len(universe)} firms x {len(window_quarters())} "
          f"quarters: {dict(st)}")


# ---------------------------------------------------------------------------
# filter
# ---------------------------------------------------------------------------

def cmd_filter(args):
    sys.path.insert(0, str(ROOT))
    import filter_earnings_calls as fec
    universe = {f["folder"]: f for f in load_universe(args.half)}
    calls = {r["file"]: r for r in read_csv(COVER / f"half{args.half}_calls.csv") if r["file"]}
    all_stats, rows = {}, []
    for folder in sorted(universe):
        for path in sorted((RAW_A / folder).glob(f"{folder}_*.md")):
            md, s, _ = fec.process_file(path, folder)
            dest = AI_OUT / folder / f"{path.stem}_ai.md"
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_text(md, encoding="utf-8")
            all_stats[path.stem] = s
            c = calls.get(str(path.relative_to(ROOT)), {})
            rows.append({
                "ticker": universe[folder]["ticker"], "gics_sector": universe[folder]["gics_sector"],
                "period_label": s["period"], "calendar_year": c.get("calendar_year", ""),
                "calendar_quarter": c.get("calendar_quarter", ""), "call_date": c.get("call_date", ""),
                "pre_chatgpt": c.get("pre_chatgpt", ""), "format": s["format"],
                "total_units": s["total"], "ai_units": s["ai"],
                "total_prepared": s["total_by_section"][fec.PREPARED],
                "ai_prepared": s["ai_by_section"][fec.PREPARED],
                "total_qa": s["total_by_section"][fec.QA], "ai_qa": s["ai_by_section"][fec.QA],
                "ai_uncertain": s["flag_counts"].get("uncertain", 0),
                "borderline_auto": s["borderline_auto"], "borderline_infra": s["borderline_infra"],
                "parse_flags": "; ".join(s["parse_flags"]), "file": str(path.relative_to(ROOT))})
            print(f"{path.stem:24s} total={s['total']:4d} ai={s['ai']:4d} "
                  f"(prep {s['ai_by_section'][fec.PREPARED]:3d} / qa {s['ai_by_section'][fec.QA]:3d}) "
                  f"{'; '.join(s['parse_flags'])}")
    AI_OUT.mkdir(parents=True, exist_ok=True)
    (AI_OUT / f"_stats_half{args.half}.json").write_text(
        json.dumps(all_stats, indent=2, ensure_ascii=False), encoding="utf-8")
    if rows:
        write_csv(COVER / f"half{args.half}_call_units.csv", rows, list(rows[0].keys()))
    flagged = sum(1 for r in rows if r["parse_flags"])
    print(f"filtered {len(rows)} Tier A calls; {flagged} with parse flags")


# ---------------------------------------------------------------------------
# report
# ---------------------------------------------------------------------------

def cmd_report(args):
    universe = load_universe(args.half)
    avail = read_csv(COVER / f"half{args.half}_availability.csv")
    pre_q = {(y, q) for y, q in window_quarters() if (y, q) <= (2022, 3)}
    per = defaultdict(lambda: {"pre_A": 0, "post_A": 0, "post_B": 0, "missing": 0})
    for r in avail:
        k = (int(r["calendar_year"]), int(r["calendar_quarter"]))
        p = per[r["ticker"]]
        if r["status"] == "missing":
            p["missing"] += 1
        elif r["status"] == "tierA":
            p["pre_A" if k in pre_q else "post_A"] += 1
        else:
            p["post_B"] += 1
    rows = []
    for f in universe:
        p = per[f["ticker"]]
        rows.append({"ticker": f["ticker"], "security": f["security"], "gics_sector": f["gics_sector"],
                     "quarters_pre_chatgpt_tierA": p["pre_A"], "quarters_post_chatgpt_tierA": p["post_A"],
                     "quarters_tierB": p["post_B"], "quarters_missing": p["missing"],
                     "has_pre_and_post_tierA": p["pre_A"] > 0 and p["post_A"] > 0})
    write_csv(COVER / f"half{args.half}_coverage_summary.csv", rows, list(rows[0].keys()))
    n = len(rows)
    both = sum(r["has_pre_and_post_tierA"] for r in rows)
    print(f"half {args.half}: {n} firms")
    print(f"  Tier A calls both before (CY Q4 2021 - Q3 2022) and after ChatGPT: {both}")
    print(f"  before only: {sum(r['quarters_pre_chatgpt_tierA'] > 0 and not r['quarters_post_chatgpt_tierA'] for r in rows)}")
    print(f"  after only:  {sum(r['quarters_post_chatgpt_tierA'] > 0 and not r['quarters_pre_chatgpt_tierA'] for r in rows)}")
    print(f"  no Tier A call at all: {sum(not r['quarters_pre_chatgpt_tierA'] and not r['quarters_post_chatgpt_tierA'] for r in rows)}")
    byq = defaultdict(Counter)
    for r in avail:
        byq[f"{r['calendar_year']}Q{r['calendar_quarter']}"][r["status"]] += 1
    print("  calls per calendar quarter (tierA / tierB / missing):")
    for q, c in byq.items():
        print(f"    {q}: {c['tierA']:3d} / {c['tierB']:3d} / {c['missing']:3d}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    u = sub.add_parser("universe")
    u.add_argument("--force", action="store_true")
    sub.add_parser("selftest")
    for name in ("discover", "download", "filter", "report"):
        p = sub.add_parser(name)
        p.add_argument("--half", type=int, choices=(1, 2), required=True)
    args = ap.parse_args()
    {"universe": cmd_universe, "selftest": cmd_selftest, "discover": cmd_discover,
     "download": cmd_download, "filter": cmd_filter, "report": cmd_report}[args.cmd](args)


if __name__ == "__main__":
    main()
