"""Reshape raw pulled text from each source into the storage schema.

Target schema (doc_id + retrieved_at are added later by storage.save_document):
    {
      "company": str, "ticker": str|None, "cik": str|None,
      "accession": str|None, "source_type": str,
      "filing_date": ISO date str|None, "period_end": ISO date str|None,
      "section": str,
      "url": str, "text": str
    }
source_type is one of:
    "10-K", "10-Q", "8-K", "challenger_report", "earnings_call_snippet"
"""

VALID_SOURCE_TYPES = {
    "10-K", "10-Q", "8-K", "challenger_report", "earnings_call_snippet",
}


def _base(company, source_type, url, text, ticker=None, cik=None,
          accession=None, filing_date=None, period_end=None, section=None):
    return {
        "company": company,
        "ticker": ticker,
        "cik": cik,
        "accession": accession,
        "source_type": source_type,
        "filing_date": filing_date,
        "period_end": period_end,
        "section": section,
        "url": url,
        "text": text,
    }


def from_edgar_section(company, ticker, filing, section_label, section_text):
    """A 10-K / 10-Q item section. source_type mirrors the filing form."""
    form = filing.get("form", "10-K")
    if form not in VALID_SOURCE_TYPES:
        form = "10-K"
    return _base(
        company=company, ticker=ticker, cik=filing.get("cik"),
        accession=filing.get("accession"), source_type=form,
        url=filing.get("url"), text=section_text,
        filing_date=filing.get("filing_date"), period_end=filing.get("period_end"),
        section=section_label,
    )


def from_edgar_exhibit(company, ticker, filing, exhibit):
    """An 8-K EX-99 press release / prepared-remarks exhibit."""
    return _base(
        company=company, ticker=ticker, cik=filing.get("cik"),
        accession=filing.get("accession"), source_type="8-K",
        url=exhibit.get("url"), text=exhibit.get("text", ""),
        filing_date=filing.get("filing_date"), period_end=filing.get("period_end"),
        section="prepared_remarks",
    )


def from_challenger(report, text, sentence=None):
    """A Challenger Gray job-cuts report (whole article or a single sentence)."""
    return _base(
        company="Challenger Gray & Christmas",
        source_type="challenger_report",
        url=report.get("url"), text=sentence or text,
        filing_date=report.get("date"), section="job_cuts_report",
    )


def from_serper(company, hit):
    """An earnings-call search hit: URL plus a short snippet only (see
    sources/serper_search.py for the copyright boundary)."""
    return _base(
        company=company, source_type="earnings_call_snippet",
        url=hit.get("url"), text=hit.get("snippet", ""),
        section="search_snippet",
    )
