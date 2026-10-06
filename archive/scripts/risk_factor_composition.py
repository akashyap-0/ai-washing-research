"""PHASE 3 -- AI risk-factor COMPOSITION measures, replacing the single
severity scalar for the Infrastructure vs. Power Adopters question.

WHY
---
Prof. Schloetzer's objection to the Infrastructure vs. Power Adopters severity
test: a single net-tone scalar can net out a difference in KIND. If
Infrastructure firms frame AI risk as demand/competitive risk and Power
Adopters frame it as execution/displacement risk, both can average to roughly
the same net tone while describing completely different things. The Phase-2
firm-level permutation test confirmed there is nothing left to defend on the
severity scalar for that comparison (exact p = 0.73), so the question has to be
asked with measures that preserve composition instead of collapsing it.

This module builds those measures. It deliberately does NOT combine them into
a new composite index -- that would repeat the exact mistake being corrected.
Each measure is a separate column and is reported separately.

WHAT IT PRODUCES
----------------
  1. output/risk_factor_text/{Company}_{year}.md
     Readable full text of every AI-related risk-factor passage, with its
     heading, its ordinal position, and its surrounding subsection context.
     This is for direct human reading, not for a model.

  2. export/risk_factor_composition_panel.csv
     One row per firm-year, carrying:
       - both grouping labels (a firm can be in both framings at once)
       - the existing tone/severity numbers, carried over unchanged
       - 3b  AI share of Item 1A, by two different denominators
       - 3c  ordinal position of AI risk factors, raw and normalized
       - 3d  specificity (numeric-token density) and two year-over-year
             text-recycling measures
       - SIC code / industry and a size proxy from EDGAR company facts
     No regressions are run here. The panel is built and described only.

HOW RISK-FACTOR SUBSECTIONS ARE IDENTIFIED
------------------------------------------
Blank-line paragraph structure in the stored plain text is not usable for
this. It varies from unusable to degenerate across filers:
    Microsoft 2026   151 blocks, but every risk-factor heading is glued to the
                     body paragraph that follows it, and "PART I Item 1A" plus
                     a bare page number repeat as separate blocks on every page
    Accenture 2025    14 blocks total, one of which is 57,352 characters --
                     essentially no paragraph structure survives at all
    Deere 2025        headings arrive shattered across blocks: "AND" /
                     "MACROECONOMIC" / "RISKS Our financial results largely..."

So headings are recovered from the HTML emphasis markup that
`edgar.fetch_filing_text` discards. Risk-factor headings in 10-K HTML are
near-universally bold (occasionally bold italic), and that survives even when
the text layout does not. Each bold/italic run is then located back inside the
stored Item 1A text by normalized-whitespace search, which gives its character
offset, and the offsets define the subsection boundaries.

Three honest caveats, all recorded per filing in the panel:
  - `heading_method` says which method actually worked: "html_emphasis",
    "paragraph" (fallback), or "sentence_window" (last resort).
  - A bold run repeated more than twice inside Item 1A is treated as a running
    page header and dropped, not as a heading.
  - The heading sequence includes any sub-headings the filer bolded, so it is
    the FILER'S OWN heading sequence, not a canonical list of risk factors.
    This is why position is reported normalized (fraction of the way through
    the sequence) as well as raw -- the raw index is not comparable across
    filers, and the normalized one only is to the extent that filers bold at
    similar granularity. Filings where this clearly breaks down are flagged.

WHAT IS NOT MEASURED
--------------------
Law-firm / outside-counsel drafting style. Schloetzer named it as a confound
and it is NOT proxied here. There is no field in EDGAR identifying who drafted
a filing, and every available proxy for it (auditor, filer agent, boilerplate
similarity to other filers) is confounded with exactly the firm
characteristics under study -- industry, size, and how much of the disclosure
is recycled. A weak proxy would be worse than none, because it would look like
a control while absorbing real variation. It is recorded as a limitation.

Market capitalization is also not pulled: EDGAR company facts contains shares
outstanding but no share price, so market cap cannot be built from EDGAR
alone. Revenue and total assets are used as the size proxies instead.

Run:
    python risk_factor_composition.py
"""
import csv
import hashlib
import json
import math
import os
import re
import sys
from collections import Counter, defaultdict

import numpy as np
from bs4 import BeautifulSoup

import ai_vs_other_risk_factors as avo
import config
import edgar
import extract_ai_sentiment as ais
import firm_characteristics_test as fct

csv.field_size_limit(sys.maxsize // 10)

TENK_PATH = os.path.join(config.EXPORT_DIR, "ai_washing_10-K.csv")
WITHIN_DOC_PATH = os.path.join(
    config.EXPORT_DIR, "ai_vs_other_risk_factors_results.csv")
PANEL_PATH = os.path.join(config.EXPORT_DIR, "risk_factor_composition_panel.csv")
TEXT_DIR = os.path.join("output", "risk_factor_text")
CACHE_DIR = os.path.join("cache", "filing_html")
FACTS_CACHE = os.path.join("cache", "company_facts")

# A bold run needs at least this many words to count as a heading rather than
# a bolded number, label, or table cell.
MIN_HEADING_WORDS = 4
# A bold run repeating more than this many times inside one Item 1A is a
# running page header, not a heading.
MAX_HEADING_REPEATS = 2
# Below this many headings, the heading sequence is too coarse for ordinal
# position to mean anything; the filing is flagged rather than dropped.
MIN_HEADINGS_FOR_POSITION = 5
# Sentence-window fallback: how many sentences of context on each side.
WINDOW_SENTENCES = 2
# Word n-gram size for the boilerplate-recycling measure.
SHINGLE_N = 5

# Numeric tokens for the specificity measure: percentages, currency amounts,
# 4-digit years, and bare numbers (including comma/decimal forms). Deliberately
# simple and inspectable rather than clever.
_NUMERIC_TOKEN = re.compile(
    r"(?:\d+(?:[.,]\d+)*\s*%)"          # 15%, 1,5 %
    r"|(?:[$€£]\s*\d+(?:[.,]\d+)*)"     # $1.2, $ 500
    r"|(?:\b(?:19|20)\d{2}\b)"          # years
    r"|(?:\b\d+(?:[.,]\d+)*\b)"         # bare numbers
)
_WORD = re.compile(r"[A-Za-z][A-Za-z'\-]*")

# --- page-break noise ------------------------------------------------------
# The stored Item 1A text carries the filing's own pagination furniture, which
# survives HTML-to-text conversion as its own lines: a bare page number, a
# "Table of Contents" link, and often the registrant's name, repeated at every
# page break inside the section. Alphabet's 2025 Item 1A interrupts a
# risk-factor paragraph with "9. / Table of Contents / Alphabet Inc." and does
# it again two paragraphs later.
#
# This is stripped before any measure is computed, not just before display,
# because it is not neutral for the measures:
#   - a bare page number is counted as a numeric token, so pagination inflates
#     the specificity score of exactly the longest passages (the ones spanning
#     the most page breaks);
#   - "Table of Contents" repeated 20 times contributes real words to the
#     denominator of the AI word-share;
#   - it is the single most reliably recycled text in the whole document, which
#     biases the year-over-year similarity measures upward.
# Removing it makes all four measures cleaner, so it is removed everywhere
# rather than kept for fidelity in one place and dropped in another.
_PAGE_NOISE_LINE = re.compile(
    r"^(?:"
    r"\d{1,4}\.?"                                   # bare page number
    r"|table\s+of\s+contents"
    r"|part\s+[ivx]+(?:\s*[-|]?\s*item\s*\d{1,2}[a-c]?\.?)?"
    r"|item\s*\d{1,2}[a-c]?\.?"                     # running item header alone
    r"|form\s+10-k"
    r"|\(?continued\)?"
    r")$",
    re.IGNORECASE,
)
# "Table of Contents" also appears glued to the front of a continuing
# paragraph (Deere: "Table of Contents exported products and the profit...").
_INLINE_TOC = re.compile(r"(?mi)^table\s+of\s+contents[ \t]+")


def strip_page_noise(text, company_name=""):
    """Remove pagination furniture (page numbers, Table-of-Contents links,
    running headers, registrant name lines) from Item 1A text."""
    text = _INLINE_TOC.sub("", text)
    # registrant-name-only lines, e.g. "Alphabet Inc." / "DEERE & COMPANY"
    name_variants = set()
    if company_name:
        base = re.sub(r"[,.]", "", company_name).strip()
        name_variants.add(base.lower())
        for suffix in (" inc", " corp", " corporation", " company", " co",
                       " plc", " ltd", " holdings", " & company"):
            if base.lower().endswith(suffix):
                name_variants.add(base.lower()[: -len(suffix)].strip())
    kept = []
    for line in text.split("\n"):
        flat = " ".join(line.split())
        if not flat:
            kept.append(line)
            continue
        if _PAGE_NOISE_LINE.match(flat):
            continue
        probe = re.sub(r"[,.]", "", flat).strip().lower()
        if probe in name_variants:
            continue
        kept.append(line)
    return re.sub(r"\n{3,}", "\n\n", "\n".join(kept))


# ---------------------------------------------------------------------------
# Caching fetch
# ---------------------------------------------------------------------------

def _cache_path(directory, key, ext):
    os.makedirs(directory, exist_ok=True)
    return os.path.join(directory,
                        hashlib.sha256(key.encode()).hexdigest()[:20] + ext)


def cached_html(url):
    path = _cache_path(CACHE_DIR, url, ".html")
    if os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            return f.read()
    html = edgar._decode_html(edgar._get(url).content)
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    return html


def cached_json(url):
    path = _cache_path(FACTS_CACHE, url, ".json")
    if os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    data = edgar._get(url).json()
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f)
    return data


# ---------------------------------------------------------------------------
# Heading recovery from HTML emphasis markup
# ---------------------------------------------------------------------------

_BOLD_TAGS = {"b", "strong"}
_ITAL_TAGS = {"i", "em"}


def _is_bold(tag):
    if tag.name in _BOLD_TAGS:
        return True
    style = (tag.get("style") or "").lower().replace(" ", "")
    return ("font-weight:bold" in style or "font-weight:700" in style
            or bool(re.search(r"font-weight:[89]00", style)))


def _is_italic(tag):
    if tag.name in _ITAL_TAGS:
        return True
    style = (tag.get("style") or "").lower().replace(" ", "")
    return "font-style:italic" in style


def emphasis_runs(html):
    """Every bold/italic text run in document order, innermost-only so nested
    markup doesn't produce duplicates."""
    soup = BeautifulSoup(html, "html.parser")
    for t in soup(["script", "style"]):
        t.decompose()
    runs = []
    for tag in soup.find_all(True):
        if not (_is_bold(tag) or _is_italic(tag)):
            continue
        if any(_is_bold(d) or _is_italic(d) for d in tag.find_all(True)):
            continue
        txt = " ".join(tag.get_text(separator=" ").split())
        if txt:
            runs.append(txt)
    return runs


def normalize_with_map(text):
    """Collapse whitespace, lowercase, and return (normalized, index_map) where
    index_map[i] is the offset of normalized[i] in the original text."""
    out, idx = [], []
    prev_space = True
    for i, ch in enumerate(text):
        if ch.isspace():
            if prev_space:
                continue
            out.append(" ")
            idx.append(i)
            prev_space = True
        else:
            out.append(ch.lower())
            idx.append(i)
            prev_space = False
    return "".join(out), idx


def _looks_like_heading(txt):
    words = txt.split()
    if len(words) < MIN_HEADING_WORDS:
        return False
    # mostly numeric / tabular
    alpha_words = _WORD.findall(txt)
    if len(alpha_words) < MIN_HEADING_WORDS:
        return False
    if re.fullmatch(r"[\W\d\s$€£%.,()\-]+", txt):
        return False
    # the Item 1A heading itself, or a running "PART I Item 1A" header
    if re.match(r"^\s*(part\s+[ivx]+\s*)?item\s*1a\b", txt, re.IGNORECASE):
        return False
    return True


def find_headings(item1a_text, runs):
    """Locate heading-like emphasis runs inside the Item 1A text.

    Returns a list of (offset, heading_text) sorted by offset. Runs that occur
    more than MAX_HEADING_REPEATS times are dropped as running page headers.
    """
    norm, idx_map = normalize_with_map(item1a_text)
    candidates = [r for r in runs if _looks_like_heading(r)]

    # count occurrences first so running headers can be dropped wholesale
    found = defaultdict(list)
    for run in dict.fromkeys(candidates):        # unique, document order
        needle, _ = normalize_with_map(run)
        if len(needle) < 8:
            continue
        start = 0
        while True:
            pos = norm.find(needle, start)
            if pos < 0:
                break
            found[run].append(idx_map[pos])
            start = pos + 1
            if len(found[run]) > MAX_HEADING_REPEATS:
                break

    out = []
    for run, offsets in found.items():
        if len(offsets) > MAX_HEADING_REPEATS:
            continue                              # running page header
        for off in offsets:
            out.append((off, run))
    out.sort()

    # drop headings whose offsets coincide (nested markup landing twice)
    deduped = []
    for off, txt in out:
        if deduped and off - deduped[-1][0] < 5:
            continue
        deduped.append((off, txt))
    return deduped


# ---------------------------------------------------------------------------
# Subsection construction, with fallbacks
# ---------------------------------------------------------------------------

def subsections_from_headings(text, headings):
    """[(heading, body_with_heading)] from heading offsets."""
    subs = []
    for i, (off, htxt) in enumerate(headings):
        end = headings[i + 1][0] if i + 1 < len(headings) else len(text)
        subs.append((htxt, text[off:end]))
    return subs


def subsections_from_paragraphs(text):
    """Fallback: blank-line blocks, dropping page-number/running-header noise."""
    blocks = [b.strip() for b in re.split(r"\n\s*\n", text) if b.strip()]
    keep = []
    for b in blocks:
        flat = " ".join(b.split())
        if len(_WORD.findall(flat)) < 10:
            continue                             # page numbers, "PART I Item 1A"
        keep.append((flat[:120], b))
    return keep


def subsections_from_sentence_windows(text):
    """Last resort: each AI sentence plus WINDOW_SENTENCES of context on each
    side, merged when the windows overlap."""
    import nltk
    sents = nltk.sent_tokenize(text)
    hits = [i for i, s in enumerate(sents) if ais.is_ai_related(s)]
    if not hits:
        return []
    spans = []
    for i in hits:
        lo = max(0, i - WINDOW_SENTENCES)
        hi = min(len(sents), i + WINDOW_SENTENCES + 1)
        if spans and lo <= spans[-1][1]:
            spans[-1] = (spans[-1][0], max(spans[-1][1], hi))
        else:
            spans.append((lo, hi))
    return [(" ".join(sents[lo:hi])[:120], " ".join(sents[lo:hi]))
            for lo, hi in spans]


def build_subsections(text, runs):
    """Return (subsections, method, n_headings)."""
    headings = find_headings(text, runs)
    if len(headings) >= MIN_HEADINGS_FOR_POSITION:
        return (subsections_from_headings(text, headings),
                "html_emphasis", len(headings))
    paras = subsections_from_paragraphs(text)
    if len(paras) >= MIN_HEADINGS_FOR_POSITION:
        return paras, "paragraph", len(headings)
    windows = subsections_from_sentence_windows(text)
    return windows, "sentence_window", len(headings)


# ---------------------------------------------------------------------------
# Measures
# ---------------------------------------------------------------------------

def word_count(text):
    return len(_WORD.findall(text))


# Which AI keyword actually fired -- now a VERIFICATION column, not a filter.
#
# `automat*`-only matches used to be a live false-positive source here: one
# incidental "automatic extension" tagged a whole 300-500 word subsection as
# AI-related (AMD FY2020, Amazon FY2020, AMD FY2021, Apple FY2023 were each a
# single such match with zero scoreable AI sentences). They were recorded and
# flagged, then dropped downstream by sensitivity_unflagged_filings.py's
# "UNFLAGGED+" sample.
#
# That is no longer how it works. ais.is_ai_related now excludes `automat*`-only
# text at extraction time, and every "is this AI-related?" decision in this
# module goes through it -- so subsections and sentences resting entirely on
# `automat*` never enter ai_subs or ai_text in the first place. See the
# exclusion note in extract_ai_sentiment.py for the rule and its rationale.
#
# ai_match_summary is kept because the provenance is still worth publishing, and
# because `ai_match_automat_only` is now a self-check: it should be empty for
# EVERY row. A "yes" means is_ai_related and this function have diverged, and
# check_automat_only_excluded() below fails the run loudly rather than letting a
# false positive back into the panel unnoticed.
_AUTOMAT_ONLY = re.compile(r"^automat", re.IGNORECASE)


def ai_match_summary(text):
    """(distinct matched terms joined, True if every match is an `automat*`
    form). The second value is now expected to be False for all scored text;
    see check_automat_only_excluded."""
    hits = ais.ai_keyword_hits(text)
    if not hits:
        return "", False
    distinct = sorted(set(hits))
    return "|".join(distinct), all(_AUTOMAT_ONLY.match(h) for h in hits)


def check_automat_only_excluded(records):
    """Post-condition on the extraction-time `automat*` exclusion: no scored
    filing may still rest entirely on `automat*` matches. Returns the offending
    rows (empty when the exclusion is working)."""
    return [r for r in records if r["ai_match_automat_only"]]


def numeric_density(text):
    """Numeric tokens per 100 words (3d, specificity)."""
    w = word_count(text)
    if w == 0:
        return None
    return 100.0 * len(_NUMERIC_TOKEN.findall(text)) / w


def shingles(text, n=SHINGLE_N):
    words = [w.lower() for w in _WORD.findall(text)]
    return {tuple(words[i:i + n]) for i in range(max(0, len(words) - n + 1))}


def jaccard(a, b):
    if not a or not b:
        return None
    return len(a & b) / len(a | b)


def tfidf_vectors(docs):
    """docs: list of strings -> list of {term: tfidf}. IDF over the whole
    corpus of firm-year AI passage texts, so the weighting is comparable
    across firms."""
    tokenized = [[w.lower() for w in _WORD.findall(d) if len(w) >= 3]
                 for d in docs]
    n = len(tokenized)
    df = Counter()
    for toks in tokenized:
        df.update(set(toks))
    vecs = []
    for toks in tokenized:
        if not toks:
            vecs.append({})
            continue
        tf = Counter(toks)
        total = len(toks)
        vecs.append({t: (c / total) * (math.log(n / (1 + df[t])) + 1.0)
                     for t, c in tf.items()})
    return vecs


def cosine(u, v):
    if not u or not v:
        return None
    common = set(u) & set(v)
    num = sum(u[t] * v[t] for t in common)
    du = math.sqrt(sum(x * x for x in u.values()))
    dv = math.sqrt(sum(x * x for x in v.values()))
    if du == 0 or dv == 0:
        return None
    return num / (du * dv)


# ---------------------------------------------------------------------------
# EDGAR firm characteristics: SIC, fiscal period, size
# ---------------------------------------------------------------------------

_URL_RE = re.compile(r"/data/(\d+)/(\d{18})/(.+)$")
_DOC_PERIOD_RE = re.compile(r"[-_](\d{8})\.(?:htm|html)$", re.IGNORECASE)

REVENUE_TAGS = [
    "RevenueFromContractWithCustomerExcludingAssessedTax",
    "Revenues",
    "RevenueFromContractWithCustomerIncludingAssessedTax",
    "SalesRevenueNet",
    "SalesRevenueGoodsNet",
]


def parse_url(url):
    m = _URL_RE.search(url)
    if not m:
        return None, None, None
    cik, acc_nodash, doc = m.groups()
    accession = f"{acc_nodash[:10]}-{acc_nodash[10:12]}-{acc_nodash[12:]}"
    return cik, accession, doc


def period_from_doc(doc):
    m = _DOC_PERIOD_RE.search(doc or "")
    if not m:
        return None
    d = m.group(1)
    return f"{d[:4]}-{d[4:6]}-{d[6:]}"


def submissions_meta(cik):
    """SIC + a {accession: reportDate} map from the submissions JSON."""
    url = config.EDGAR_SUBMISSIONS.format(cik=str(int(cik)).zfill(10))
    data = cached_json(url)
    recent = data.get("filings", {}).get("recent", {})
    acc = recent.get("accessionNumber", [])
    rep = recent.get("reportDate", [])
    return {
        "sic": data.get("sic") or "",
        "sic_description": data.get("sicDescription") or "",
        "entity_name": data.get("name") or "",
        "report_dates": dict(zip(acc, rep)),
    }


def company_facts(cik):
    url = (f"https://data.sec.gov/api/xbrl/companyfacts/"
           f"CIK{str(int(cik)).zfill(10)}.json")
    try:
        return cached_json(url)
    except Exception:
        return {}


def size_at_period(facts, period_end):
    """(revenue, revenue_tag, assets) for the fiscal year ending period_end.

    Revenue is a duration fact, so entries are additionally required to span
    350-380 days; without that the quarterly and nine-month facts filed in the
    same 10-K would be indistinguishable from the annual one.
    """
    gaap = (facts.get("facts") or {}).get("us-gaap") or {}
    revenue, rev_tag = None, ""
    for tag in REVENUE_TAGS:
        units = ((gaap.get(tag) or {}).get("units") or {}).get("USD") or []
        best = None
        for e in units:
            if e.get("end") != period_end or e.get("form") != "10-K":
                continue
            start, end = e.get("start"), e.get("end")
            if not start:
                continue
            try:
                days = (np.datetime64(end) - np.datetime64(start)).astype(int)
            except Exception:
                continue
            if not (350 <= days <= 380):
                continue
            if best is None or abs(e.get("val", 0)) > abs(best):
                best = e.get("val")
        if best is not None:
            revenue, rev_tag = best, tag
            break

    assets = None
    units = ((gaap.get("Assets") or {}).get("units") or {}).get("USD") or []
    for e in units:
        if e.get("end") == period_end and e.get("form") == "10-K":
            assets = e.get("val")
            break
    return revenue, rev_tag, assets


# ---------------------------------------------------------------------------
# Passage text export (3a)
# ---------------------------------------------------------------------------

def write_passage_file(rec, ai_subs, all_subs):
    os.makedirs(TEXT_DIR, exist_ok=True)
    fname = f"{rec['company_short']}_{rec['fiscal_year'] or rec['filing_date'][:4]}.md"
    path = os.path.join(TEXT_DIR, fname)
    n_all = len(all_subs)
    with open(path, "w", encoding="utf-8") as f:
        f.write(f"# {rec['company_short']} -- AI-related risk-factor passages\n\n")
        f.write(f"- **Ticker:** {rec['ticker']}\n")
        f.write(f"- **10-K filed:** {rec['filing_date']}\n")
        f.write(f"- **Fiscal period end:** {rec['period_end'] or 'unknown'}"
                f"  (fiscal year {rec['fiscal_year'] or 'unknown'})\n")
        f.write(f"- **AI-centrality group:** {rec['ai_centrality'] or '-'}\n")
        f.write(f"- **AI stack-role group:** {rec['ai_stack_role'] or '-'}\n")
        f.write(f"- **SIC:** {rec['sic']} {rec['sic_description']}\n")
        f.write(f"- **Item 1A total words:** {rec['item1a_words']:,}\n")
        f.write(f"- **Subsection unit:** `{rec['heading_method']}` "
                f"({n_all} subsections detected)\n")
        f.write(f"- **AI-related subsections:** {len(ai_subs)} of {n_all} "
                f"({rec['ai_word_share_subsection'] if rec['ai_word_share_subsection'] != '' else 'n/a'} "
                f"of Item 1A words)\n")
        f.write(f"- **AI sentences (FinBERT-scored subset):** "
                f"{rec['n_ai_sentences']}\n")
        f.write(f"- **AI keywords that matched:** "
                f"`{rec['ai_match_terms'] or 'none'}`\n")
        f.write(f"- **Source:** {rec['url']}\n\n")
        if rec["position_flag"]:
            f.write(f"> **Flag:** {rec['position_flag']}\n\n")
        if rec["ai_match_automat_only"]:
            f.write("> **BUG -- THIS SHOULD NOT APPEAR:** every AI keyword "
                    "match in this filing is an `automat*` form (e.g. "
                    "\"automatic extension\", \"automatically\"), with no "
                    "AI/ML/generative-AI term anywhere. `ais.is_ai_related` is "
                    "supposed to exclude such text at extraction time, so this "
                    "passage should never have been built. Do not treat this "
                    "filing as AI disclosure; report the divergence.\n\n")
        f.write("---\n\n")
        if not ai_subs:
            f.write("_No AI-related risk-factor passage found in this "
                    "filing's Item 1A._\n")
            return path
        for i, (pos, heading, body) in enumerate(ai_subs, 1):
            frac = (pos / n_all) if n_all else float("nan")
            f.write(f"## Passage {i} of {len(ai_subs)}\n\n")
            f.write(f"**Position in Item 1A:** subsection {pos} of {n_all} "
                    f"({frac:.1%} of the way through)\n\n")
            f.write(f"**Heading as filed:** {heading.strip()}\n\n")
            f.write(f"**Words:** {word_count(body):,}  |  "
                    f"**Numeric tokens per 100 words:** "
                    f"{numeric_density(body):.2f}\n\n")
            f.write("```text\n")
            f.write(body.strip())
            f.write("\n```\n\n")
    return path


# ---------------------------------------------------------------------------
# Panel assembly
# ---------------------------------------------------------------------------

PANEL_FIELDS = [
    # identity
    "company_short", "company", "ticker", "cik", "accession",
    "filing_date", "period_end", "fiscal_year",
    # grouping labels (a firm can appear in more than one framing)
    "ai_centrality", "ai_stack_role", "ai_infra_subsplit",
    # firm characteristics (confound controls)
    "sic", "sic_description", "revenue_usd", "revenue_tag", "assets_usd",
    # existing severity / tone measures, carried over unchanged
    "n_ai_sentences", "n_other_sentences", "ai_tone", "other_tone",
    "within_doc_distance", "tone_flag",
    # 3b -- share of Item 1A devoted to AI
    "item1a_words", "n_subsections", "n_ai_subsections",
    "ai_subsection_words", "ai_word_share_subsection",
    "ai_sentence_words", "ai_word_share_sentences",
    # 3c -- ordinal position
    "ai_pos_first", "ai_pos_first_norm", "ai_pos_mean_norm",
    "ai_pos_spread_norm", "ai_content_concentrated", "position_flag",
    # keyword-match provenance (exposes AI_KEYWORD_PATTERN false positives)
    "ai_match_terms", "ai_match_automat_only",
    # 3d -- specificity and year-over-year recycling
    "specificity_numeric_per_100w", "item1a_specificity_numeric_per_100w",
    "yoy_tfidf_cosine", "yoy_shingle_jaccard", "yoy_prior_year",
    # provenance
    "heading_method", "n_headings_found",
    "item1a_words_raw", "page_noise_words_removed", "url",
]


def load_tone_rows():
    """company/date -> the existing within-doc tone numbers, carried over."""
    out = {}
    with open(WITHIN_DOC_PATH, newline="", encoding="utf-8-sig") as f:
        for r in csv.DictReader(f):
            out[(r["ticker"], r["filing_date"])] = r
    return out


def main():
    ais.es.ensure_punkt()

    tenk_rows = ais.sd._load_csv(TENK_PATH)
    tenk_rows = [r for r in tenk_rows if r["ticker"] in ais.APPROVED_TICKERS]
    filings, skipped = ais.group_tenk_risk_factors(tenk_rows)
    print(f"{len(filings)} 10-Ks with a usable Item 1A ({len(skipped)} skipped).")

    tone = load_tone_rows()

    # firm-level metadata, one fetch per company
    meta_cache, facts_cache = {}, {}
    print("\nFetching firm characteristics (SIC, fiscal period, size) from "
          "EDGAR...")
    for f in filings:
        cik, _, _ = parse_url(f["url"])
        if cik and cik not in meta_cache:
            try:
                meta_cache[cik] = submissions_meta(cik)
                facts_cache[cik] = company_facts(cik)
                print(f"  {f['ticker']:<6} CIK {cik:<10} "
                      f"SIC {meta_cache[cik]['sic']} "
                      f"{meta_cache[cik]['sic_description']}")
            except Exception as e:
                print(f"  {f['ticker']:<6} CIK {cik:<10} [failed] {e}")
                meta_cache[cik] = {"sic": "", "sic_description": "",
                                   "entity_name": "", "report_dates": {}}
                facts_cache[cik] = {}

    print(f"\nBuilding composition measures for {len(filings)} filings...")
    records, ai_texts, degenerate = [], [], []
    for i, f in enumerate(sorted(filings,
                                 key=lambda x: (x["company"], x["filing_date"])),
                          start=1):
        short = fct.TICKER_SHORT.get(f["ticker"], f["ticker"])
        date = f["filing_date"].isoformat()
        raw_text = f["text"]
        text = strip_page_noise(raw_text, f["company"])
        cik, accession, doc = parse_url(f["url"])
        meta = meta_cache.get(cik, {})

        # --- subsections -------------------------------------------------
        try:
            runs = emphasis_runs(cached_html(f["url"]))
        except Exception as e:
            print(f"  [{i}/{len(filings)}] {short} {date}: "
                  f"HTML fetch failed ({e}); falling back to paragraphs")
            runs = []
        subs, method, n_head = build_subsections(text, runs)
        n_subs = len(subs)

        ai_subs = [(idx + 1, h, b) for idx, (h, b) in enumerate(subs)
                   if ais.is_ai_related(b)]

        # --- 3b: word share ----------------------------------------------
        item1a_words = word_count(text)
        ai_sub_words = sum(word_count(b) for _, _, b in ai_subs)
        ai_sents, _ = avo.classify_sentences(text)
        ai_sent_words = sum(word_count(s) for s in ai_sents)

        # --- 3c: ordinal position ----------------------------------------
        flag = ""
        if method != "html_emphasis":
            flag = (f"subsection boundaries came from `{method}`, not the "
                    f"filer's own bold headings ({n_head} bold headings found, "
                    f"fewer than {MIN_HEADINGS_FOR_POSITION}) -- ordinal "
                    f"position is not comparable to html_emphasis filings")
        elif n_subs < MIN_HEADINGS_FOR_POSITION:
            flag = f"only {n_subs} subsections; ordinal position not meaningful"
        if method == "sentence_window":
            degenerate.append((short, date, n_head, n_subs))

        if ai_subs and n_subs:
            positions = [p for p, _, _ in ai_subs]
            norms = [p / n_subs for p in positions]
            pos_first = min(positions)
            pos_first_norm = round(min(norms), 4)
            pos_mean_norm = round(float(np.mean(norms)), 4)
            pos_spread = round(float(max(norms) - min(norms)), 4)
            concentrated = "yes" if len(ai_subs) == 1 else (
                "yes" if pos_spread <= 0.15 else "no")
        else:
            pos_first = pos_first_norm = pos_mean_norm = pos_spread = ""
            concentrated = ""

        # --- 3d: specificity ---------------------------------------------
        ai_text = "\n\n".join(b for _, _, b in ai_subs)
        spec = numeric_density(ai_text) if ai_text else None
        spec_all = numeric_density(text)
        match_terms, automat_only = ai_match_summary(ai_text)

        t = tone.get((f["ticker"], date), {})
        period_end = (meta.get("report_dates", {}).get(accession)
                      or period_from_doc(doc))
        fiscal_year = period_end[:4] if period_end else ""
        revenue, rev_tag, assets = (None, "", None)
        if period_end:
            revenue, rev_tag, assets = size_at_period(
                facts_cache.get(cik, {}), period_end)

        rec = {
            "company_short": short,
            "company": f["company"],
            "ticker": f["ticker"],
            "cik": cik or "",
            "accession": accession or "",
            "filing_date": date,
            "period_end": period_end or "",
            "fiscal_year": fiscal_year,
            "ai_centrality": fct.group_of(short, fct.AI_CENTRALITY) or "",
            "ai_stack_role": fct.group_of(short, fct.AI_STACK_ROLE) or "",
            "ai_infra_subsplit": fct.group_of(short, fct.AI_INFRA_SUBSPLIT) or "",
            "sic": meta.get("sic", ""),
            "sic_description": meta.get("sic_description", ""),
            "revenue_usd": revenue if revenue is not None else "",
            "revenue_tag": rev_tag,
            "assets_usd": assets if assets is not None else "",
            "n_ai_sentences": t.get("n_ai_sentences", ""),
            "n_other_sentences": t.get("n_other_sentences", ""),
            "ai_tone": t.get("ai_tone", ""),
            "other_tone": t.get("other_tone", ""),
            "within_doc_distance": t.get("within_doc_distance", ""),
            "tone_flag": t.get("flag", ""),
            "item1a_words": item1a_words,
            "n_subsections": n_subs,
            "n_ai_subsections": len(ai_subs),
            "ai_subsection_words": ai_sub_words,
            "ai_word_share_subsection": (round(ai_sub_words / item1a_words, 5)
                                         if item1a_words else ""),
            "ai_sentence_words": ai_sent_words,
            "ai_word_share_sentences": (round(ai_sent_words / item1a_words, 5)
                                        if item1a_words else ""),
            "ai_pos_first": pos_first,
            "ai_pos_first_norm": pos_first_norm,
            "ai_pos_mean_norm": pos_mean_norm,
            "ai_pos_spread_norm": pos_spread,
            "ai_content_concentrated": concentrated,
            "position_flag": flag,
            "ai_match_terms": match_terms,
            "ai_match_automat_only": "yes" if automat_only else "",
            "specificity_numeric_per_100w": (round(spec, 3)
                                             if spec is not None else ""),
            "item1a_specificity_numeric_per_100w": (round(spec_all, 3)
                                                    if spec_all is not None
                                                    else ""),
            "yoy_tfidf_cosine": "",
            "yoy_shingle_jaccard": "",
            "yoy_prior_year": "",
            "heading_method": method,
            "n_headings_found": n_head,
            "item1a_words_raw": word_count(raw_text),
            "page_noise_words_removed": word_count(raw_text) - item1a_words,
            "url": f["url"],
        }
        records.append(rec)
        ai_texts.append(ai_text)
        path = write_passage_file(rec, ai_subs, subs)
        if i % 20 == 0 or i == len(filings):
            print(f"  [{i}/{len(filings)}] {short} {date} "
                  f"{method:<16} {n_subs:>4} subs, {len(ai_subs):>3} AI")

    # --- 3d: year-over-year recycling, computed after the whole corpus is
    # available so IDF is corpus-wide -----------------------------------
    vecs = tfidf_vectors(ai_texts)
    shing = [shingles(t) for t in ai_texts]
    by_firm = defaultdict(list)
    for i, r in enumerate(records):
        by_firm[r["company_short"]].append(i)
    for firm, idxs in by_firm.items():
        idxs.sort(key=lambda i: records[i]["filing_date"])
        for prev, cur in zip(idxs, idxs[1:]):
            if not ai_texts[prev].strip() or not ai_texts[cur].strip():
                continue
            c = cosine(vecs[prev], vecs[cur])
            j = jaccard(shing[prev], shing[cur])
            records[cur]["yoy_tfidf_cosine"] = round(c, 4) if c is not None else ""
            records[cur]["yoy_shingle_jaccard"] = round(j, 4) if j is not None else ""
            records[cur]["yoy_prior_year"] = (records[prev]["fiscal_year"]
                                              or records[prev]["filing_date"])

    os.makedirs(config.EXPORT_DIR, exist_ok=True)
    with open(PANEL_PATH, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=PANEL_FIELDS)
        w.writeheader()
        for r in records:
            w.writerow(r)

    report_shape(records, degenerate)
    print(f"\nPanel written to {PANEL_PATH}")
    print(f"Readable passages written to {TEXT_DIR}\\ "
          f"({len(records)} files)")


# ---------------------------------------------------------------------------
# Shape / missingness report
# ---------------------------------------------------------------------------

def report_shape(records, degenerate):
    print("\n" + "=" * 78)
    print("PANEL SHAPE")
    print("=" * 78)
    firms = {r["company_short"] for r in records}
    print(f"rows (firm-years): {len(records)}")
    print(f"columns:           {len(PANEL_FIELDS)}")
    print(f"firms:             {len(firms)}")
    years = sorted({r["fiscal_year"] for r in records if r["fiscal_year"]})
    print(f"fiscal years:      {years[0]} - {years[-1]} ({len(years)} distinct)")

    print("\n" + "=" * 78)
    print("MISSINGNESS BY COLUMN (blank / empty)")
    print("=" * 78)
    print(f"{'column':<40}{'present':>9}{'missing':>9}{'% miss':>9}")
    print("-" * 67)
    for col in PANEL_FIELDS:
        miss = sum(1 for r in records if r[col] == "" or r[col] is None)
        pres = len(records) - miss
        star = "  <<" if miss else ""
        print(f"{col:<40}{pres:>9}{miss:>9}{100*miss/len(records):>8.1f}%{star}")

    print("\n" + "=" * 78)
    print("SUBSECTION-DETECTION METHOD (how ordinal position was derived)")
    print("=" * 78)
    counts = Counter(r["heading_method"] for r in records)
    for m, n in counts.most_common():
        print(f"  {m:<18}{n:>4} filings  ({100*n/len(records):.1f}%)")
    flagged = [r for r in records if r["position_flag"]]
    print(f"\n  filings flagged as NOT comparable on ordinal position: "
          f"{len(flagged)}")
    for r in sorted(flagged, key=lambda r: (r["company_short"], r["filing_date"])):
        print(f"    {r['company_short']:<14}{r['filing_date']}  "
              f"{r['heading_method']:<16} {r['n_subsections']:>4} subs, "
              f"{r['n_headings_found']:>4} bold headings")
    if degenerate:
        print(f"\n  filings where Item 1A did NOT subdivide at all "
              f"(sentence-window fallback): {len(degenerate)}")
        for short, date, nh, ns in degenerate:
            print(f"    {short:<14}{date}  {nh} bold headings, {ns} windows")

    print("\n" + "=" * 78)
    print("KEYWORD-MATCH QUALITY (`automat*`-only exclusion self-check)")
    print("=" * 78)
    fp = check_automat_only_excluded(records)
    has_ai = [r for r in records if r["n_ai_subsections"] > 0]
    print(f"  filings with >=1 AI-related subsection: {len(has_ai)}")
    print(f"  of those, filings where EVERY match is an `automat*` form "
          f"(no AI/ML term at all): {len(fp)}")
    if fp:
        print("\n  *** POST-CONDITION FAILED ***")
        print("  ais.is_ai_related is supposed to exclude these at extraction")
        print("  time, so this list must be empty. A non-empty list means the")
        print("  exclusion and ai_match_summary have diverged -- investigate")
        print("  before using this panel.")
        for r in sorted(fp, key=lambda r: (r["company_short"], r["filing_date"])):
            print(f"    {r['company_short']:<14}{r['filing_date']}  "
                  f"{r['n_ai_subsections']:>2} AI subs, "
                  f"n_ai_sentences={r['n_ai_sentences']:>3}, "
                  f"matched: {r['ai_match_terms']}")
    else:
        print("\n  OK: no scored filing rests entirely on `automat*` matches.")
        print("  These are now excluded at extraction time by ais.is_ai_related,")
        print("  not flagged and dropped downstream. A filing left with fewer")
        print(f"  than {ais.MIN_AI_SENTENCES} real AI sentences falls out of the "
              f"scored sample by")
        print("  the existing minimum-evidence threshold, like any filing with")
        print("  no AI content.")
    term_counter = Counter()
    for r in records:
        for t in (r["ai_match_terms"] or "").split("|"):
            if t:
                term_counter[t] += 1
    print(f"\n  Most common matched terms across all filings:")
    for t, n in term_counter.most_common(12):
        print(f"    {t:<28}{n:>4} filings")

    print("\n" + "=" * 78)
    print("PER-FIRM COVERAGE")
    print("=" * 78)
    hdr = (f"{'firm':<14}{'rows':>5}{'yrs':>12}{'AI subs>0':>10}"
           f"{'yoy pairs':>10}{'method':>16}")
    print(hdr)
    print("-" * len(hdr))
    by_firm = defaultdict(list)
    for r in records:
        by_firm[r["company_short"]].append(r)
    for firm in sorted(by_firm):
        rs = sorted(by_firm[firm], key=lambda r: r["filing_date"])
        yrs = [r["fiscal_year"] for r in rs if r["fiscal_year"]]
        span = f"{yrs[0]}-{yrs[-1]}" if yrs else "?"
        n_ai = sum(1 for r in rs if r["n_ai_subsections"] > 0)
        n_yoy = sum(1 for r in rs if r["yoy_tfidf_cosine"] != "")
        methods = Counter(r["heading_method"] for r in rs)
        mstr = ",".join(f"{m[:4]}:{n}" for m, n in methods.most_common())
        print(f"{firm:<14}{len(rs):>5}{span:>12}{n_ai:>10}{n_yoy:>10}"
              f"{mstr:>16}")

    print("\n" + "=" * 78)
    print("MEASURE DISTRIBUTIONS (descriptive only -- no tests run)")
    print("=" * 78)
    numeric_cols = ["item1a_words", "page_noise_words_removed",
                    "n_subsections", "n_ai_subsections",
                    "ai_word_share_subsection", "ai_word_share_sentences",
                    "ai_pos_first_norm", "ai_pos_mean_norm",
                    "specificity_numeric_per_100w",
                    "item1a_specificity_numeric_per_100w",
                    "yoy_tfidf_cosine", "yoy_shingle_jaccard"]
    hdr = (f"{'measure':<40}{'n':>5}{'min':>10}{'p25':>10}{'med':>10}"
           f"{'p75':>10}{'max':>10}")
    print(hdr)
    print("-" * len(hdr))
    for col in numeric_cols:
        vals = [float(r[col]) for r in records
                if r[col] != "" and r[col] is not None]
        if not vals:
            print(f"{col:<40}{0:>5}{'--':>10}")
            continue
        q = np.percentile(vals, [0, 25, 50, 75, 100])
        print(f"{col:<40}{len(vals):>5}{q[0]:>10.4f}{q[1]:>10.4f}"
              f"{q[2]:>10.4f}{q[3]:>10.4f}{q[4]:>10.4f}")

    print("\n" + "=" * 78)
    print("GROUP CELL SIZES (for whatever specification you choose later)")
    print("=" * 78)
    for label, key in [("AI centrality", "ai_centrality"),
                       ("AI stack role", "ai_stack_role"),
                       ("AI infra subsplit (post-hoc)", "ai_infra_subsplit")]:
        print(f"\n  {label}:")
        cells = defaultdict(lambda: [0, set()])
        for r in records:
            g = r[key] or "(not in this framing)"
            cells[g][0] += 1
            cells[g][1].add(r["company_short"])
        for g, (n, fs) in sorted(cells.items()):
            print(f"    {g:<28}{n:>4} firm-years, {len(fs):>3} firms")

    print("\n" + "=" * 78)
    print("NOT MEASURED (recorded as limitations, not proxied)")
    print("=" * 78)
    print("  - Law-firm / outside-counsel drafting style. No EDGAR field")
    print("    identifies it, and every candidate proxy (auditor, filer agent,")
    print("    cross-filer boilerplate similarity) is confounded with the firm")
    print("    characteristics under study. Deliberately left out rather than")
    print("    proxied weakly.")
    print("  - Market capitalization. EDGAR company facts carries shares")
    print("    outstanding but no share price, so market cap cannot be built")
    print("    from EDGAR alone. Revenue and total assets stand in as the size")
    print("    proxies; add price data from another source if market cap is")
    print("    specifically needed.")
    print("  - Genuine-vs-buzzword AI claims. Already established: FinBERT")
    print("    separates promotional from hedged language but cannot tell a")
    print("    real automation claim from a vague one (d = -0.022, p = 0.77).")


if __name__ == "__main__":
    main()
