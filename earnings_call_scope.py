"""
Frozen scope for the Mag 7 earnings-call study (Gate 1) and the coverage manifest.

Single source of truth for: the seven firms, the Q4 2021 - Q2 2026 window, period
labels, the fiscal -> calendar quarter mapping, call-date extraction, and the
acquisition status of every expected call. EARNINGS_CALL_SCOPE.md explains the rules
in prose; build_earnings_call_canonical.py imports this module.

Writes  earnings_calls/coverage_manifest.csv   (one row per expected company-period call)

Usage:
  python earnings_call_scope.py            # write the manifest (parses every present file, read-only)
  python earnings_call_scope.py --check    # verify 133 expected / 7 x 19 and print counts only
"""

import argparse
import csv
import datetime as dt
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CALLS = ROOT / "earnings_calls"
MANIFEST = CALLS / "coverage_manifest.csv"

COMPANIES = ["alphabet", "amazon", "apple", "meta", "microsoft", "nvidia", "tesla"]
TICKER = {"alphabet": "GOOGL", "amazon": "AMZN", "apple": "AAPL", "meta": "META",
          "microsoft": "MSFT", "nvidia": "NVDA", "tesla": "TSLA"}
FISCAL = {"microsoft", "apple", "nvidia"}           # period labels are fiscal (FYyy_Qn)

WINDOW_START = (2021, 4)                             # calendar Q4 2021
WINDOW_END = (2026, 2)                               # calendar Q2 2026 = common cutoff
EXPECTED_CALLS = 133                                 # 7 firms x 19 calendar quarters


# ---------------------------------------------------------------------------
# Period labels and calendar mapping
# ---------------------------------------------------------------------------

def calendar_quarter(company, period_label):
    """(calendar_year, calendar_quarter) a period is assigned to.

    Calendar firms: identity. Fiscal firms: the calendar quarter holding most of the
    fiscal quarter's months.
      Microsoft (FY ends Jun 30):         Q1 Jul-Sep (FY-1, 3), Q2 Oct-Dec (FY-1, 4),
                                          Q3 Jan-Mar (FY, 1),   Q4 Apr-Jun (FY, 2)
      Apple (FY ends last Sat of Sep):    Q1 ~Oct-Dec (FY-1, 4), Q2 (FY, 1), Q3 (FY, 2), Q4 (FY, 3)
      Nvidia (FY ends last Sun of Jan):   Qn spans ~Feb-Apr / May-Jul / Aug-Oct / Nov-Jan,
                                          2 of 3 months in calendar (FY-1, n)
    Same assignment as earnings_calls/filter_ai_passages.py:cal_quarter.
    """
    if company in FISCAL:
        m = re.fullmatch(r"FY(\d\d)_Q([1-4])", period_label)
        fy, q = 2000 + int(m[1]), int(m[2])
        if company == "microsoft":
            return {1: (fy - 1, 3), 2: (fy - 1, 4), 3: (fy, 1), 4: (fy, 2)}[q]
        if company == "apple":
            return {1: (fy - 1, 4), 2: (fy, 1), 3: (fy, 2), 4: (fy, 3)}[q]
        return (fy - 1, q)
    m = re.fullmatch(r"(\d{4})_Q([1-4])", period_label)
    return int(m[1]), int(m[2])


def period_for(company, cy, cq):
    """Inverse of calendar_quarter: the file period label for a calendar quarter."""
    if company == "microsoft":
        fy, q = (cy + 1, cq - 2) if cq >= 3 else (cy, cq + 2)
        return f"FY{fy % 100:02d}_Q{q}"
    if company == "apple":
        fy, q = (cy + 1, 1) if cq == 4 else (cy, cq + 1)
        return f"FY{fy % 100:02d}_Q{q}"
    if company == "nvidia":
        return f"FY{(cy + 1) % 100:02d}_Q{cq}"
    return f"{cy}_Q{cq}"


def calendar_quarters():
    y, q = WINDOW_START
    while (y, q) <= WINDOW_END:
        yield y, q
        y, q = (y + 1, 1) if q == 4 else (y, q + 1)


def fiscal_label(company, period_label):
    if company == "microsoft":
        return period_label.replace("_", " ") + " (fiscal; FY ends June 30)"
    if company == "apple":
        return period_label.replace("_", " ") + " (fiscal; FY ends last Saturday of September)"
    if company == "nvidia":
        return period_label.replace("_", " ") + " (fiscal; FY ends last Sunday of January)"
    y, q = period_label.split("_")
    return f"{q} {y} (calendar)"


def fiscal_quarter_end(company, cy, cq):
    """Approximate last day of the fiscal quarter (Nvidia's ends ~1 month after the
    calendar quarter it is assigned to)."""
    m = cq * 3 + (1 if company == "nvidia" else 0)
    y = cy + (m - 1) // 12
    m = (m - 1) % 12 + 1
    nxt = dt.date(y + (m == 12), m % 12 + 1, 1)
    return nxt - dt.timedelta(days=1)


def expected_call_window(company, cy, cq):
    end = fiscal_quarter_end(company, cy, cq)
    return f"{end + dt.timedelta(days=14)}..{end + dt.timedelta(days=60)}"


def expected_calls():
    for company in COMPANIES:
        for cy, cq in calendar_quarters():
            yield company, period_for(company, cy, cq), cy, cq


# ---------------------------------------------------------------------------
# Raw-file metadata
# ---------------------------------------------------------------------------

def read_metadata(path):
    raw = path.read_text(encoding="utf-8")
    meta, _, body = raw.partition("\n---\n")
    return meta, body


def source_url(meta):
    m = re.search(r"\*\*(?:Audio source|Source):\*\*[^\n]*?(https?://\S+)", meta)
    return m.group(1).rstrip(").,") if m else ""


def source_type(meta, body):
    low = meta.lower()
    if "motley fool" in low:
        return "third_party_transcript_motley_fool"
    if "youtube auto-generated captions" in low:
        return "youtube_auto_captions"
    if "faster-whisper" in low:
        return "machine_transcript_whisper_of_official_ir_audio"
    if "callstreet" in body[:3000].lower():
        return "official_ir_pdf_factset_callstreet"
    if "official company ir transcript (docx)" in low:
        return "official_ir_transcript_docx"
    if "microsoft investor relations" in low:
        return "official_ir_transcript_html"
    if "official transcript" in low:
        return "official_ir_transcript_pdf"
    return "unknown"


MONTHS = {m: i for i, m in enumerate(
    ["january", "february", "march", "april", "may", "june", "july", "august",
     "september", "october", "november", "december"], 1)}
_DATE_LONG = re.compile(
    r"\b(January|February|March|April|May|June|July|August|September|October|November|"
    r"December)\s+(\d{1,2})(?:st|nd|rd|th)?,\s+(20\d\d)\b")
_DATE_SHORT = re.compile(r"\b(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+(\d{1,2}),\s+(20\d\d)\b")
_DATE_FACTSET = re.compile(r"\b(\d{1,2})\s*-\s*(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s*-\s*(20\d\d)\b")


def _mk(y, mon, d):
    try:
        return dt.date(int(y), MONTHS[next(k for k in MONTHS if k.startswith(mon.lower()[:3]))], int(d))
    except (ValueError, StopIteration):
        return None


def call_date(company, cy, cq, meta, body):
    """(iso_date, source). Only a date stated in the file itself and inside the plausible
    window (fiscal quarter end, +75 days] is accepted; otherwise ('', 'not_stated_in_source_file').
    The quarter-end day itself is excluded ("year ended December 31, 2023" is not a call date)."""
    lo = fiscal_quarter_end(company, cy, cq) + dt.timedelta(days=1)
    hi = lo + dt.timedelta(days=75)
    m = re.search(r"call held " + _DATE_SHORT.pattern, meta)
    if m:
        d = _mk(m[3], m[1], m[2])
        if d and lo <= d <= hi:
            return d.isoformat(), "file_metadata"
    head = " ".join(body.split()[:700])
    for rx, order in ((_DATE_FACTSET, (3, 2, 1)), (_DATE_LONG, (3, 1, 2))):
        for m in rx.finditer(head):
            d = _mk(m[order[0]], m[order[1]], m[order[2]])
            if d and lo <= d <= hi:
                return d.isoformat(), "transcript_text"
    return "", "not_stated_in_source_file"


# ---------------------------------------------------------------------------
# Status of the 28 historical calls (Gate 2). Evidence: earnings_calls/ACQUISITION_LOG.md
# ---------------------------------------------------------------------------

AMZN_AUDIO = "https://s2.q4cdn.com/299287126/files/doc_financials/"
GAPS = {
    ("alphabet", "2021_Q4"): dict(
        availability_status="archived_official_copy_only", acquisition_status="awaiting_human_source_decision",
        source_url="https://abc.xyz/assets/investor/static/pdf/2021_Q4_Earnings_Transcript.pdf",
        source_type="official_ir_transcript_pdf",
        notes="Official PDF URL now redirects to the IR site map; not in the current IR event feed (starts 2022 Q1). "
              "archive.org holds a 2024-07-16 capture of the official PDF; using it needs approval."),
    ("amazon", "2021_Q4"): dict(
        availability_status="official_ir_audio_only", acquisition_status="awaiting_human_source_decision",
        source_url=AMZN_AUDIO + "2021/q4/Amazon-Quarterly-Earnings-Report-Q4-2021-Full-Call-v1.wav",
        source_type="official_ir_audio",
        notes="IR call audio verified (HTTP 200, 665 MB wav). No text transcript. Matching the existing Amazon files "
              "needs local faster-whisper small.en, which is not installed."),
    ("amazon", "2022_Q1"): dict(
        availability_status="official_ir_audio_only", acquisition_status="awaiting_human_source_decision",
        source_url=AMZN_AUDIO + "2022/q1/Amazon-Quarterly-Earnings-Report-Q1-2022-Full-Call-v1.mp3",
        source_type="official_ir_audio",
        notes="IR call audio verified (HTTP 200, 48 MB mp3). No text transcript; needs local Whisper transcription."),
    ("amazon", "2022_Q2"): dict(
        availability_status="official_ir_audio_only", acquisition_status="awaiting_human_source_decision",
        source_url=AMZN_AUDIO + "2022/q2/Amazon-Quarterly-Earnings-Report-Q2-2022-Full-Call-v1.mp3",
        source_type="official_ir_audio",
        notes="IR call audio verified (HTTP 200, 93 MB mp3). No text transcript; needs local Whisper transcription."),
    ("amazon", "2022_Q3"): dict(
        availability_status="official_ir_audio_only", acquisition_status="awaiting_human_source_decision",
        source_url=AMZN_AUDIO + "2022/q3/Amazon-Quarterly-Earnings-Call-Q3-2022-Full-Call-v2.wav",
        source_type="official_ir_audio",
        notes="IR call audio verified (HTTP 200, 540 MB wav). No text transcript; needs local Whisper transcription."),
}
for _p, _d in (("FY22_Q1", "2022-01-27"), ("FY22_Q2", "2022-04-28"), ("FY22_Q3", "2022-07-28"), ("FY22_Q4", "2022-10-27")):
    GAPS[("apple", _p)] = dict(
        availability_status="no_public_company_source", acquisition_status="unavailable_public_source",
        source_url="https://investor.apple.com/feed/Event.svc/GetEventList (event listed; press release only)",
        source_type="none", ir_event_date=_d,
        notes="Apple IR lists the event with only a press-release link; webcast link is the generic live page, "
              "no archived audio or transcript. Only third-party sources exist (not permitted without approval).")
for _p, _d in (("FY22_Q4", "2022-02-16"), ("FY23_Q1", "2022-05-25"), ("FY23_Q2", "2022-08-24"), ("FY23_Q3", "2022-11-16")):
    GAPS[("nvidia", _p)] = dict(
        availability_status="no_public_company_source", acquisition_status="unavailable_public_source",
        source_url="https://investor.nvidia.com/feed/Event.svc/GetEventList (event listed; no transcript)",
        source_type="none", ir_event_date=_d,
        notes="NVIDIA IR event has no transcript attachment; webcast is an events.q4inc.com registration app. "
              "NVIDIA hosts transcripts only from FY26 Q1. Only third-party sources exist.")
for _p, _d in (("2021_Q4", "2022-01-26"), ("2022_Q1", ""), ("2022_Q2", ""), ("2022_Q3", "")):
    GAPS[("tesla", _p)] = dict(
        availability_status="official_webcast_only", acquisition_status="awaiting_human_source_decision",
        source_url="https://ir.tesla.com/ (HTTP 403 to automated requests)",
        source_type="official_ir_webcast", ir_event_date=_d,
        notes="Tesla publishes no transcript; the webcast replay is on ir.tesla.com, which refuses automated access. "
              "Existing caption files used Tesla's own YouTube uploads; doing the same needs approval.")
_ACQUIRED = {("alphabet", p) for p in ("2022_Q1", "2022_Q2", "2022_Q3")} | \
            {("meta", p) for p in ("2021_Q4", "2022_Q1", "2022_Q2", "2022_Q3")} | \
            {("microsoft", p) for p in ("FY22_Q2", "FY22_Q3", "FY22_Q4", "FY23_Q1")}

FIELDS = ["company", "ticker", "period_label", "calendar_year", "calendar_quarter",
          "fiscal_or_calendar_label", "expected_call_window", "call_date", "call_date_source",
          "raw_file_path", "source_url", "source_type", "availability_status", "acquisition_status",
          "parser_status", "parser_format", "parser_flags", "total_units", "notes"]


def raw_path(company, period):
    return CALLS / company / f"{company}_{period}.md"


def manifest_rows(parse=True):
    if parse:
        sys.path.insert(0, str(ROOT))
        import filter_earnings_calls as F
    rows = []
    for company, period, cy, cq in expected_calls():
        path = raw_path(company, period)
        row = dict(company=company, ticker=TICKER[company], period_label=period,
                   calendar_year=cy, calendar_quarter=cq,
                   fiscal_or_calendar_label=fiscal_label(company, period),
                   expected_call_window=expected_call_window(company, cy, cq),
                   call_date="", call_date_source="", raw_file_path="", source_url="",
                   source_type="", availability_status="", acquisition_status="",
                   parser_status="not_parsed", parser_format="", parser_flags="",
                   total_units="", notes="")
        gap = GAPS.get((company, period))
        if path.exists():
            meta, body = read_metadata(path)
            row["raw_file_path"] = path.relative_to(ROOT).as_posix()
            row["source_url"] = source_url(meta)
            row["source_type"] = source_type(meta, body)
            row["call_date"], row["call_date_source"] = call_date(company, cy, cq, meta, body)
            acquired = (company, period) in _ACQUIRED
            row["availability_status"] = "acquired_official_ir_text" if acquired else "present_in_repo"
            row["acquisition_status"] = "acquired" if acquired else "already_present"
            if not row["source_url"]:
                row["notes"] = "metadata block gives no source URL"
            if acquired:
                row["notes"] = "Gate 2: retrieved 2026-10-06 from company IR; see ACQUISITION_LOG.md"
            if parse:
                try:
                    _, st, _ = F.process_file(path, company)
                    row["parser_format"] = st["format"]
                    row["parser_flags"] = "; ".join(st["parse_flags"])
                    row["total_units"] = st["total"]
                    bad = any("PARSE FAILED" in f for f in st["parse_flags"])
                    row["parser_status"] = ("failed" if bad else
                                            "parsed_with_flags" if st["parse_flags"] else "parsed_ok")
                except Exception as e:                       # recorded, not hidden
                    row["parser_status"] = "failed"
                    row["parser_flags"] = f"exception: {e}"
        elif gap:
            row.update({k: v for k, v in gap.items() if k in FIELDS})
            if gap.get("ir_event_date"):
                row["call_date"], row["call_date_source"] = gap["ir_event_date"], "company_ir_event_listing"
        else:
            row["availability_status"] = "unknown"
            row["acquisition_status"] = "missing_unexplained"
            row["notes"] = "expected file absent and not in the Gate 2 gap table"
        rows.append(row)
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()
    exp = list(expected_calls())
    per = {c: sum(1 for e in exp if e[0] == c) for c in COMPANIES}
    present = sum(raw_path(c, p).exists() for c, p, _, _ in exp)
    stray = sorted(p.relative_to(ROOT).as_posix() for c in COMPANIES
                   for p in (CALLS / c).glob(f"{c}_*.md")
                   if p.stem.split("_", 1)[1] not in {e[1] for e in exp if e[0] == c})
    print(f"expected {len(exp)} ({per}); present {present}; files outside window: {stray or 'none'}")
    if len(exp) != EXPECTED_CALLS or set(per.values()) != {19}:
        sys.exit("expected-call count is not 133 = 7 x 19; stop and investigate")
    if args.check:
        return
    rows = manifest_rows()
    with MANIFEST.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        w.writerows(rows)
    from collections import Counter
    print(Counter(r["acquisition_status"] for r in rows))
    print(Counter(r["parser_status"] for r in rows))
    print(f"wrote {MANIFEST.relative_to(ROOT)} ({len(rows)} rows)")


if __name__ == "__main__":
    main()
