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
    cols = ["accessionNumber", "filingDate", "form", "primaryDocument",
            "primaryDocDescription"]
    want = set(forms) if forms else None
    filings = []
    for accession, filing_date, form, primary_doc, desc in zip(
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
            "primary_doc": primary_doc,
            "description": desc,
            "url": _archive_url(cik, accession, primary_doc),
        })
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
_SEP = r"[^A-Za-z0-9]{0,8}"


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


def extract_sections(text, sections=("Item 1A Risk Factors", "Item 7 MD&A")):
    """Slice the requested 10-K item sections out of plain text.

    Returns {section_label: section_text}. A heading can legitimately show
    up several times in one filing: once in the Table of Contents, and once
    (or more, as a repeated running header) in the real body. Cross-
    references to other items, like "see Item 7...", can also match the
    pattern. We first drop any match that isn't line-anchored (see
    `_is_heading_anchored`) to get rid of those inline cross-references.
    Among what's left, we pick whichever occurrence is followed by the
    longest run of text before the next heading-like match shows up: a real
    section runs for thousands of characters before the next item starts,
    while a Table-of-Contents entry is followed almost immediately, within a
    couple hundred characters, by the next item's TOC line. This is still a
    heuristic, so it's worth spot-checking against real filings.
    """
    lowered = text.lower()
    marks = []
    for label, pat in _ITEM_PATTERNS.items():
        for m in re.finditer(pat, lowered):
            if _is_heading_anchored(text, m.start()):
                marks.append((m.start(), label))
    marks.sort()
    all_positions = [pos for pos, _ in marks]

    def next_mark_after(pos):
        for p in all_positions:
            if p > pos:
                return p
        return len(text)

    out = {}
    for want in sections:
        candidates = [pos for pos, lab in marks if lab == want]
        if not candidates:
            continue
        best_start = max(candidates, key=lambda pos: next_mark_after(pos) - pos)
        end = next_mark_after(best_start)
        out[want] = text[best_start:end].strip()
    return out


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
