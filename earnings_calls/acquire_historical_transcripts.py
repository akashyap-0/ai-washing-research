"""
Acquire the historical (Q4 2021 - Q3 2022) earnings-call transcripts that are
published as text by the company's own investor-relations site.

Gate 2 of the earnings-call work packet. Only official, company-hosted sources
are fetched; nothing is fabricated or summarized. Calls without a company-hosted
text transcript are NOT handled here; see ACQUISITION_LOG.md.

Reads   nothing in earnings_calls/ except to check a target does not exist
Writes  earnings_calls/<company>/<company>_<period>.md   (new files only, never overwrites)
        cache/earnings_call_sources/<file>               (downloaded originals, gitignored)
        earnings_calls/acquisition_results.json          (URL, retrieval date, SHA-256, sizes)

Extraction:
  PDF  (Alphabet, Meta): poppler `pdftotext -layout -enc UTF-8`, then each line has
       runs of whitespace collapsed to one space and is stripped; form feeds become
       newlines. Page-number lines are kept (the filter removes them, as for the
       existing files). Checked on alphabet_2022_Q4 and meta_2022_Q4: re-extracting
       their official PDFs this way gives the same unit and AI-sentence counts as the
       committed files.
  DOCX (Microsoft): text of each <w:p> paragraph (w:t runs concatenated, w:tab -> tab,
       w:br -> newline), one paragraph per line, blank line between paragraphs.
       XML entities decoded; no other change.

Usage:
  python earnings_calls/acquire_historical_transcripts.py           # fetch + write missing files
  python earnings_calls/acquire_historical_transcripts.py --dry-run # list targets only
"""

import argparse
import datetime as dt
import hashlib
import html
import json
import re
import shutil
import subprocess
import sys
import urllib.request
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CALLS = ROOT / "earnings_calls"
CACHE = ROOT / "cache" / "earnings_call_sources"
RESULTS = CALLS / "acquisition_results.json"

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126.0 Safari/537.36")

ALPHABET_IR = "official transcript published on Alphabet Investor Relations"
META_IR = "official transcript published on Meta Investor Relations"
MSFT_IR = "official transcript on Microsoft Investor Relations"

# (company, period_label, title_period, kind, source_url, landing_page)
TARGETS = [
    ("alphabet", "2022_Q1", "Q1 2022", "pdf",
     "https://s206.q4cdn.com/479360582/files/doc_financials/2022/q1/2022_Q1_Earnings_Transcript.pdf",
     "https://abc.xyz/investor/events/event-details/2022/2022-Q1-Earnings-Call/default.aspx"),
    ("alphabet", "2022_Q2", "Q2 2022", "pdf",
     "https://s206.q4cdn.com/479360582/files/doc_financials/2022/q2/2022_Q2_Earnings_Transcript.pdf",
     "https://abc.xyz/investor/events/event-details/2022/2022-Q2-Earnings-Call/default.aspx"),
    ("alphabet", "2022_Q3", "Q3 2022", "pdf",
     "https://s206.q4cdn.com/479360582/files/doc_financials/2022/q3/2022_Q3_Earnings_Transcript.pdf",
     "https://abc.xyz/investor/events/event-details/2022/2022-Q3-Earnings-Call/default.aspx"),
    ("meta", "2021_Q4", "Q4 2021", "pdf",
     "https://s21.q4cdn.com/399680738/files/doc_financials/2021/q4/Meta-Q4-2021-Earnings-Call-Transcript.pdf",
     "https://investor.atmeta.com/investor-events/event-details/2022/Q4-2021-Earnings/default.aspx"),
    ("meta", "2022_Q1", "Q1 2022", "pdf",
     "https://s21.q4cdn.com/399680738/files/doc_financials/2022/q1/Meta-Q1-2022-Earnings-Call-Transcript.pdf",
     "https://investor.atmeta.com/investor-events/event-details/2022/Q1-2022-Earnings/default.aspx"),
    ("meta", "2022_Q2", "Q2 2022", "pdf",
     "https://s21.q4cdn.com/399680738/files/doc_financials/2022/q2/Meta-Q2-2022-Earnings-Call-Transcript.pdf",
     "https://investor.atmeta.com/investor-events/event-details/2022/Q2-2022-Earnings/default.aspx"),
    ("meta", "2022_Q3", "Q3 2022", "pdf",
     "https://s21.q4cdn.com/399680738/files/doc_financials/2022/q3/Meta-Q3-2022-Earnings-Call-Transcript.pdf",
     "https://investor.atmeta.com/investor-events/event-details/2022/Q3-2022-Earnings/default.aspx"),
    ("microsoft", "FY22_Q2", "FY22 Q2", "docx",
     "https://cdn-dynmedia-1.microsoft.com/is/content/microsoftcorp/TranscriptFY22Q2",
     "https://www.microsoft.com/en-us/investor/events/fy-2022/earnings-fy-2022-q2 (returned HTTP 404 on 2026-10-06; transcript file still on Microsoft's CDN)"),
    ("microsoft", "FY22_Q3", "FY22 Q3", "docx",
     "https://cdn-dynmedia-1.microsoft.com/is/content/microsoftcorp/TranscriptFY22Q3",
     "https://www.microsoft.com/en-us/investor/events/fy-2022/earnings-fy-2022-q3"),
    ("microsoft", "FY22_Q4", "FY22 Q4", "docx",
     "https://cdn-dynmedia-1.microsoft.com/is/content/microsoftcorp/TranscriptFY22Q4",
     "https://www.microsoft.com/en-us/investor/events/fy-2022/earnings-fy-2022-q4"),
    ("microsoft", "FY23_Q1", "FY23 Q1", "docx",
     "https://cdn-dynmedia-1.microsoft.com/is/content/microsoftcorp/TranscriptFY23Q1",
     "https://www.microsoft.com/en-us/investor/events/fy-2023/earnings-fy-2023-q1"),
]

HEADERS = {
    "alphabet": ("Alphabet Inc.", "Alphabet (GOOGL / GOOG)", ALPHABET_IR),
    "meta": ("Meta Platforms, Inc.", "Meta Platforms (META)", META_IR),
    "microsoft": ("Microsoft Corporation", "Microsoft (MSFT); fiscal year ends June 30", MSFT_IR),
}
TICKERS = {"alphabet": "GOOGL / GOOG", "meta": "META", "microsoft": "MSFT"}


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "*/*"})
    with urllib.request.urlopen(req, timeout=120) as r:
        return r.status, r.headers.get("Content-Type", ""), r.read()


def pdf_to_text(path):
    exe = shutil.which("pdftotext")
    if not exe:
        sys.exit("pdftotext (poppler) not found on PATH")
    out = subprocess.run([exe, "-layout", "-enc", "UTF-8", str(path), "-"],
                         capture_output=True, check=True).stdout.decode("utf-8")
    out = out.replace("\f", "\n")
    lines = [re.sub(r"[ \t]+", " ", l).strip() for l in out.split("\n")]
    return "\n".join(lines).strip() + "\n"


def docx_to_text(path):
    xml = zipfile.ZipFile(path).read("word/document.xml").decode("utf-8")
    paras = []
    for p in re.findall(r"<w:p[ >].*?</w:p>|<w:p/>", xml, flags=re.S):
        p = re.sub(r"<w:tab/>", "\t", p)
        p = re.sub(r"<w:br[^>]*/>", "\n", p)
        text = "".join(re.findall(r"<w:t(?: [^>]*)?>(.*?)</w:t>", p, flags=re.S))
        text = html.unescape(text)
        if text.strip():
            paras.append(text.strip())
    return "\n\n".join(paras).strip() + "\n"


def header_block(company, period_title, url, landing, kind, retrieved, sha, warning):
    title_name, company_line, source_phrase = HEADERS[company]
    lines = [
        f"# {title_name} — {period_title} Earnings Call (transcript)",
        "",
        f"- **Company:** {company_line}",
        f"- **Ticker:** {TICKERS[company]}",
        f"- **Period:** {period_title}",
        f"- **Source:** {source_phrase} — {url}",
        f"- **IR landing page:** {landing}",
        f"- **Source type:** official company IR transcript ({kind.upper()})",
        f"- **Retrieved:** {retrieved} (Gate 2 historical acquisition; see earnings_calls/ACQUISITION_LOG.md)",
        f"- **Source SHA-256:** {sha}",
        ("- **Extraction:** poppler pdftotext -layout, per-line whitespace collapsed; "
         "page numbers left in place" if kind == "pdf" else
         "- **Extraction:** DOCX paragraph text (w:t runs), one paragraph per line"),
        f"- **Quality warning:** {warning}",
    ]
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    retrieved = dt.date.today().isoformat()
    CACHE.mkdir(parents=True, exist_ok=True)
    results = json.loads(RESULTS.read_text(encoding="utf-8")) if RESULTS.exists() else {}

    for company, period, title_period, kind, url, landing in TARGETS:
        stem = f"{company}_{period}"
        dest = CALLS / company / f"{stem}.md"
        if dest.exists():
            print(f"{stem:22s} exists, skipped (never overwritten)")
            continue
        if args.dry_run:
            print(f"{stem:22s} would fetch {url}")
            continue
        status, ctype, data = fetch(url)
        sha = hashlib.sha256(data).hexdigest()
        ext = ".pdf" if kind == "pdf" else ".docx"
        orig = CACHE / f"{stem}{ext}"
        orig.write_bytes(data)
        text = pdf_to_text(orig) if kind == "pdf" else docx_to_text(orig)
        warning = ("none known; text extracted from the official document, PDF layout "
                   "artifacts (page numbers, line wraps) remain" if kind == "pdf" else
                   "none known; text extracted from the official document")
        if "�" in text:
            warning += "; source contains U+FFFD replacement characters (kept as is)"
        md = header_block(company, title_period, url, landing, kind, retrieved, sha, warning)
        dest.write_text(md + "\n\n---\n\n" + text, encoding="utf-8")
        results[stem] = {
            "company": company, "period_label": period, "source_url": url,
            "ir_landing_page": landing, "http_status": status, "content_type": ctype,
            "bytes": len(data), "sha256": sha, "retrieved": retrieved,
            "format": kind, "raw_file": str(dest.relative_to(ROOT)).replace("\\", "/"),
            "text_words": len(text.split()),
            "replacement_chars": text.count("�"),
        }
        print(f"{stem:22s} {status} {len(data):>8d} bytes -> {dest.name} ({len(text.split())} words)")

    if not args.dry_run:
        RESULTS.write_text(json.dumps(results, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
