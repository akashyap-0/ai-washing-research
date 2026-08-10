"""SEC EDGAR collection.

Everything here hits fully public SEC endpoints. SEC's fair-access policy
requires a descriptive User-Agent (name + email) on every request and asks
clients to stay under ~10 req/sec; both are handled centrally in `_get`.

Note on robustness: 10-K HTML is notoriously messy and inconsistent across
filers, so `extract_sections` is heuristic. The student should spot-check its
output on a couple of real filings and adjust the item patterns if needed.
The full-text-search response shape can also drift; if `full_text_search`
returns nothing on data you can see in the EDGAR web UI, print the raw JSON
and adjust the parsing below.
"""
import re
import time

import requests
from bs4 import BeautifulSoup

import config


def _headers():
    return {
        "User-Agent": config.SEC_USER_AGENT or "ai-washing-research (contact-not-set)",
        "Accept-Encoding": "gzip, deflate",
    }


def _get(url, **kwargs):
    time.sleep(config.SEC_REQUEST_DELAY)
    resp = requests.get(url, headers=_headers(), timeout=30, **kwargs)
    resp.raise_for_status()
    return resp


def _archive_url(cik, accession, primary_doc):
    # Archives paths use the CIK with leading zeros stripped.
    cik_int = str(int(cik))
    return config.EDGAR_ARCHIVES.format(
        cik=cik_int,
        accession=accession.replace("-", ""),
        doc=primary_doc,
    )


def _parse_display_name(display_name):
    """'Apple Inc.  (AAPL)  (CIK 0000320193)' -> ('Apple Inc.', 'AAPL')."""
    ticker = None
    m = re.search(r"\(([A-Z][A-Z.\-]{0,5})\)", display_name or "")
    if m:
        ticker = m.group(1)
    name = re.sub(r"\s*\(.*?\)", "", display_name or "").strip()
    return name, ticker


# --- Full-text search --------------------------------------------------------

def full_text_search(query, forms=None, date_from=None, date_to=None, limit=20):
    """Run EDGAR full-text search and return a list of hit dicts.

    Each hit: accession, accession_nodash, primary_doc, cik, company, ticker,
    form, filing_date, url.
    """
    params = {"q": query}
    if forms:
        params["forms"] = forms if isinstance(forms, str) else ",".join(forms)
    if date_from:
        params["startdt"] = date_from
        params["dateRange"] = "custom"
    if date_to:
        params["enddt"] = date_to
        params["dateRange"] = "custom"

    data = _get(config.EDGAR_FULLTEXT_SEARCH, params=params).json()
    hits = data.get("hits", {}).get("hits", [])
    results = []
    for h in hits[:limit]:
        src = h.get("_source", {})
        # _id looks like '0000320193-24-000123:aapl-20240928.htm'
        accession, _, primary_doc = (h.get("_id", "")).partition(":")
        ciks = src.get("ciks") or []
        names = src.get("display_names") or []
        cik = ciks[0] if ciks else None
        company, ticker = _parse_display_name(names[0] if names else "")
        results.append({
            "accession": accession,
            "accession_nodash": accession.replace("-", ""),
            "primary_doc": primary_doc,
            "cik": str(int(cik)) if cik else None,
            "company": company or None,
            "ticker": ticker,
            "form": src.get("root_form") or src.get("file_type"),
            "filing_date": src.get("file_date"),
            "url": _archive_url(cik, accession, primary_doc)
                   if (cik and primary_doc) else None,
        })
    return results


# --- Submissions / filing history -------------------------------------------

def get_submissions(cik):
    """Fetch a company's filing history JSON. `cik` int/str is zero-padded."""
    cik10 = str(int(cik)).zfill(10)
    return _get(config.EDGAR_SUBMISSIONS.format(cik=cik10)).json()


def recent_filings(cik, forms=None):
    """Flatten the submissions 'recent' arrays into a list of filing dicts,
    optionally filtered to given form types (e.g. ['10-K', '8-K'])."""
    data = get_submissions(cik)
    recent = data.get("filings", {}).get("recent", {})
    company = data.get("name")
    cols = ["accessionNumber", "filingDate", "reportDate", "form",
            "primaryDocument", "primaryDocDescription"]
    want = set(forms) if forms else None
    filings = []
    for accession, filing_date, report_date, form, primary_doc, desc in zip(
            *[recent.get(c, []) for c in cols]):
        if want and form not in want:
            continue
        filings.append({
            "company": company,
            "cik": str(int(cik)),
            "accession": accession,
            "accession_nodash": accession.replace("-", ""),
            "form": form,
            "filing_date": filing_date,
            "period_end": report_date or None,
            "primary_doc": primary_doc,
            "description": desc,
            "url": _archive_url(cik, accession, primary_doc),
        })
    return filings


def all_filings(cik, forms=None):
    """Every filing EDGAR holds for `cik`, not just the most recent ones.

    submissions/CIK##########.json only inlines a company's latest ~1000
    filings under `filings.recent`; anything older is paged out into the extra
    JSON shards listed in `filings.files`. recent_filings() reads only the
    inline block, which silently truncates history for high-volume filers --
    fine for "pull this year's 10-K", wrong for "how far back does EDGAR go?".
    This walks the shards too and returns the filings in the same dict shape.
    """
    data = get_submissions(cik)
    company = data.get("name")
    want = set(forms) if forms else None
    cols = ["accessionNumber", "filingDate", "reportDate", "form",
            "primaryDocument", "primaryDocDescription"]

    blocks = [data.get("filings", {}).get("recent", {})]
    for shard in data.get("filings", {}).get("files", []):
        name = shard.get("name")
        if not name:
            continue
        blocks.append(_get(f"https://data.sec.gov/submissions/{name}").json())

    filings = []
    for block in blocks:
        for accession, filing_date, report_date, form, primary_doc, desc in zip(
                *[block.get(c, []) for c in cols]):
            if want and form not in want:
                continue
            filings.append({
                "company": company,
                "cik": str(int(cik)),
                "accession": accession,
                "accession_nodash": accession.replace("-", ""),
                "form": form,
                "filing_date": filing_date,
                "period_end": report_date or None,
                "primary_doc": primary_doc,
                "description": desc,
                "url": _archive_url(cik, accession, primary_doc),
            })
    filings.sort(key=lambda f: f["filing_date"])
    return filings


# --- Ticker -> CIK resolution ------------------------------------------------

_TICKER_CACHE = None


def resolve_ticker(ticker):
    """Map a ticker symbol to its CIK (as a leading-zero-stripped string)."""
    global _TICKER_CACHE
    if _TICKER_CACHE is None:
        data = _get(config.EDGAR_TICKER_MAP).json()
        _TICKER_CACHE = {row["ticker"].upper(): str(row["cik_str"])
                         for row in data.values()}
    return _TICKER_CACHE.get(ticker.upper())


# --- Document fetch + section extraction -------------------------------------

def _decode_html(raw_bytes):
    """Decode filing HTML ourselves instead of handing raw bytes to
    BeautifulSoup. Its auto-detection has been observed to mis-guess plain
    'ascii' on real UTF-8 SEC filings, which silently mangles curly quotes
    and dashes. Try UTF-8 first, since that covers virtually all current
    filings, and fall back to Windows-1252 for older filings that really
    are legacy-encoded (it's a full single-byte codec, so it never raises).
    """
    try:
        return raw_bytes.decode("utf-8")
    except UnicodeDecodeError:
        return raw_bytes.decode("windows-1252")


def fetch_filing_text(url):
    """Download a filing document and return cleaned plain text."""
    resp = _get(url)
    html = _decode_html(resp.content)
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup(["script", "style"]):
        tag.decompose()
    text = soup.get_text(separator="\n")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{2,}", "\n\n", text)
    return text.strip()


# Item-heading heuristics, in filing order. Used both to locate the sections
# we want and to find the next boundary that ends them.
#
# Real filings turn out to be messier than a simple "Item 7. Management's
# Discussion" pattern can handle. The separator style varies: some filers
# use "Item 7." with a period, others use "ITEM 7 - MANAGEMENT'S DISCUSSION"
# in all caps with a dash. And some filers' HTML wraps individual characters
# in their own inline tag, like a page-break or superscript span, which
# get_text() then renders as a stray newline in the middle of a word. One
# real Oracle heading came through as literally "R\nisk Factors".
#
# `_SEP` tolerates junk punctuation and whitespace between tokens.
# `_loose_word` and `_loose_phrase` tolerate whitespace injected between
# individual letters.
# Tolerance for junk between the item number and the item title. This was
# originally 8 characters, which turned out to be too tight: Deere's
# 2014-2018 10-Ks render the heading across table cells as
# "ITEM 1A.\n" + 13 non-breaking spaces + " \nRISK FACTORS", i.e. 17
# non-alphanumeric characters, so the real heading never matched at all and
# only the table-of-contents line survived (which is why those filings
# extracted as ~400-character TOC fragments). Widened to 40.
#
# Widening is safe rather than sloppy because the character class excludes
# every letter and digit: a match can only span whitespace and punctuation,
# so no intervening word or page number can be swallowed. Any run this long
# is necessarily a heading laid out across table cells.
#
# Raised again from 40 to 60 after finding Deere's 2014 Item 7 heading uses
# "ITEM 7.\n" + 47 non-breaking spaces + " \n" (about 50 characters). At 40
# that heading went undetected, so Item 1A found no following boundary and
# ran to the end of the document (362K characters).
_SEP = r"[^A-Za-z0-9]{0,60}"


def _loose_word(word):
    return r"\s*".join(re.escape(c) for c in word)


def _loose_phrase(phrase):
    return r"\s+".join(_loose_word(w) for w in phrase.split(" "))


_ITEM_PATTERNS = {
    "Item 1 Business": r"item\s*1\b" + _SEP + _loose_word("business"),
    "Item 1A Risk Factors": r"item\s*1a\b" + _SEP + _loose_phrase("risk factors"),
    "Item 7 MD&A": (r"item\s*7\b" + _SEP + _loose_word("management") + _SEP
                     + "s" + _SEP + _loose_word("discussion")),
    "Item 7A": r"item\s*7a\b" + _SEP + _loose_word("quantitative"),
    "Item 8 Financial Statements": r"item\s*8\b" + _SEP + _loose_phrase("financial statements"),
}


def _is_heading_anchored(text, pos):
    """True if `pos` opens its own line (ignoring any spaces or nbsp right
    before it) instead of sitting in the middle of a sentence. Real section
    headings and Table-of-Contents entries are both anchored this way,
    while inline cross-references like "...see Item 7, Management's
    Discussion..." aren't, since they're embedded in running prose.
    Filtering down to line-anchored matches gets rid of those cross-
    references before we even try to tell a TOC entry apart from the real
    heading (see `extract_sections` below)."""
    prefix = text[:pos].rstrip(" \t\xa0")
    return prefix == "" or prefix.endswith("\n")


# Any line that opens with an item number, including the items that aren't in
# _ITEM_PATTERNS (1B, 1C, 2, 3, ...). Used only to find where the text
# following a heading stops, so that text can be inspected. Kept separate
# from _ITEM_PATTERNS on purpose -- widening the boundary set itself would
# shorten every existing section and change output for filings that already
# parse correctly.
_ANY_ITEM_LINE = re.compile(r"^[ \t\xa0]*item\s*\d{1,2}[a-c]?\b",
                            re.IGNORECASE | re.MULTILINE)

# How much lowercase running prose has to follow a heading before it counts as
# a real section opening.
#
# This replaced a flat minimum-character floor, which could not do the job: a
# Table-of-Contents line and a legitimately one-sentence section are the same
# length. Accenture's TOC line is followed by 325 characters before the next
# item heading; IBM's genuine Item 7 -- which incorporates the MD&A by
# reference and is therefore only ever one sentence long ("Refer to pages 6
# through 38 of IBM's 2025 Annual Report to Stockholders, which are
# incorporated herein by reference.") -- is followed by just 211. Any
# character threshold that drops the first also drops the second.
#
# Lowercase word count separates them cleanly instead. A TOC line is followed
# only by its own Title-Case-or-CAPS title and a page number, so it has almost
# no lowercase running text; a real sentence has plenty. Same test rejects a
# running page header stacked directly on the real heading ("Item 1A. Risk
# Factors \n11\n" -> zero prose words) without needing a special case.
MIN_PROSE_WORDS = 8

_PROSE_WORD = re.compile(r"\b[a-z]{3,}\b")

# The tail of a quoted cross-reference to another item, e.g.
#     ... described in "Item 1A. Risk Factors." under the sub-caption ...
# When such a reference wraps, the quotation mark can land at the start of a
# line, which makes it indistinguishable from a real heading by line-anchoring
# alone -- this is why Walmart's Item 1A extracted as a mid-sentence fragment
# both before and after the running-header fix. A real heading is never
# immediately followed by a closing quote or by an em/en-dash continuation.
# Note the period alone is NOT a rejection signal: Deere's real heading is
# legitimately "RISK FACTORS." -- it's the quote that gives a reference away.
_XREF_TAIL = re.compile(r'^(?:[.,;:]?\s*["“”]|[—–])')


def extract_sections(text, sections=("Item 1 Business", "Item 1A Risk Factors",
                                     "Item 7 MD&A", "Item 8 Financial Statements")):
    """Slice the requested 10-K item sections out of plain text.

    Returns {section_label: section_text}. A heading can legitimately show up
    several times in one filing: once in the Table of Contents, once as the
    real body heading, and often many more times as a repeated running page
    header. Inline cross-references ("see Item 7...") can also match the
    pattern; those are dropped first because they aren't line-anchored (see
    `_is_heading_anchored`).

    Choosing among what's left used to be done by taking whichever occurrence
    had the most text after it before the next heading-like match. That broke
    on filers who repeat the heading as a running page header on every page of
    the section: Accenture emits ~20 line-anchored copies of "Item 1A. Risk
    Factors <page#>", and the max-gap rule picked whichever page happened to
    have the most text after it, yielding a fragment starting mid-sentence
    partway through the section.

    Instead we now walk the candidates in document order and take the FIRST
    one that actually looks like a section opening, judged by whether real
    lowercase prose follows it before the next item heading (see
    MIN_PROSE_WORDS -- this is what separates a TOC line from a genuinely
    one-sentence section, which a length threshold cannot). Document order
    matters: the real heading always precedes the running page headers that
    repeat it, so the earliest qualifying candidate is the right one.

    Matches that are the tail of a quoted cross-reference to another item are
    dropped up front (see _XREF_TAIL), so they can act as neither a section
    start nor a section boundary.

    The section end is the next line-anchored heading for a *different* item.
    Repeats of the same item's own heading are skipped, since a running page
    header restating this section's title is not a boundary -- treating it as
    one is what truncated these sections to a single page's worth of text.

    Still a heuristic; worth spot-checking against real filings.
    """
    lowered = text.lower()
    marks = []
    for label, pat in _ITEM_PATTERNS.items():
        for m in re.finditer(pat, lowered):
            if not _is_heading_anchored(text, m.start()):
                continue
            if _XREF_TAIL.match(text[m.end():m.end() + 60].lstrip(" \t\xa0\n")):
                continue
            marks.append((m.start(), m.end(), label))
    marks.sort()

    def next_other_label_after(pos, label):
        for p, _end, lab in marks:
            if p > pos and lab != label:
                return p
        return len(text)

    def next_item_line_after(pos):
        m = _ANY_ITEM_LINE.search(text, pos)
        return m.start() if m else len(text)

    out = {}
    for want in sections:
        for start, match_end, label in marks:
            if label != want:
                continue
            following = text[match_end:next_item_line_after(match_end)]
            if len(_PROSE_WORD.findall(following)) < MIN_PROSE_WORDS:
                continue
            out[want] = text[start:next_other_label_after(start, want)].strip()
            break
    return out


_EIGHTK_ITEM_HEADING = re.compile(
    r"^[ \t\xa0]*item\s+(2\.02|2\.05|7\.01|8\.01)\b[^\n]{0,140}",
    re.IGNORECASE | re.MULTILINE,
)


def extract_8k_items(text, items=("2.02", "2.05", "7.01", "8.01")):
    """Extract relevant narrative 8-K items from the primary document.

    The 8-K primary document and its EX-99 exhibits are distinct evidence.
    This captures restructuring and other disclosures that never appear in an
    earnings exhibit. Candidates without meaningful prose are rejected.
    """
    wanted = set(items)
    matches = list(_EIGHTK_ITEM_HEADING.finditer(text))
    output = {}
    for index, match in enumerate(matches):
        number = match.group(1)
        if number not in wanted or number in output:
            continue
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        candidate = text[match.start():end].strip()
        if len(_PROSE_WORD.findall(candidate)) >= MIN_PROSE_WORDS:
            output[f"Item {number}"] = candidate
    return output


# --- 8-K exhibits (press releases / prepared remarks) ------------------------

def list_filing_documents(cik, accession):
    """List every document in a filing via its directory index.json."""
    cik_int = str(int(cik))
    acc_nodash = accession.replace("-", "")
    index_url = (f"https://www.sec.gov/Archives/edgar/data/"
                 f"{cik_int}/{acc_nodash}/index.json")
    data = _get(index_url).json()
    docs = []
    for it in data.get("directory", {}).get("item", []):
        name = it.get("name", "")
        docs.append({
            "name": name,
            "type": it.get("type", ""),
            "url": (f"https://www.sec.gov/Archives/edgar/data/"
                    f"{cik_int}/{acc_nodash}/{name}"),
        })
    return docs


# Most filers (IBM, Oracle, Dell, Salesforce, ...) name their earnings-release
# exhibit with "ex99"/"ex-99" or tag it EX-99.* in the type field, which the
# check below catches. A few don't: expanding to 6 more companies for the
# firm-characteristics cross-section turned up NVIDIA, which files its
# earnings press release and CFO commentary as e.g. "q4fy26pr.htm" /
# "q4fy26cfocommentary.htm" with no EX-99 marker at all, and UnitedHealth,
# which uses names like "earningsrelease2q26_7152.htm" or
# "exhibit991pressrelease.htm" (the latter has "991" but not the literal
# "ex99" substring). This second pattern is purely about recognizing these
# filers' own naming conventions for the same kind of document (the earnings
# press release / prepared remarks) already being pulled for every other
# company -- it doesn't change what counts as AI-related or how sentiment is
# scored.
_EARNINGS_DOC_PATTERN = re.compile(
    r"pressrelease|earningsrelease|cfocommentary|q\dfy\d{2}(pr|commentary)",
    re.IGNORECASE,
)


def fetch_8k_exhibits(cik, accession):
    """Return EX-99.* exhibits (typically the earnings press release / prepared
    remarks) from an 8-K, each with extracted text."""
    exhibits = []
    for doc in list_filing_documents(cik, accession):
        t = (doc.get("type") or "").upper()
        name = (doc.get("name") or "").lower()
        is_pr = (t.startswith("EX-99") or "ex99" in name or "ex-99" in name
                 or _EARNINGS_DOC_PATTERN.search(name))
        if is_pr and name.endswith((".htm", ".html", ".txt")):
            try:
                doc_text = fetch_filing_text(doc["url"])
            except Exception:
                doc_text = ""
            exhibits.append({**doc, "text": doc_text})
    return exhibits
