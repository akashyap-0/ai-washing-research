"""Orchestrate the AI-washing data-collection pipeline.

For each target company: resolve ticker -> CIK, pull recent filings, extract the
relevant 10-K/10-Q sections and 8-K press-release exhibits, optionally look up
earnings-call transcript URLs via Serper, normalize everything to the schema,
dedup against previously exported files, write each source_type to its own
CSV/JSON, then upload the export dir to Google Drive.

Examples (env vars must be set first, see README):
    python main.py --companies IBM,DELL,SAP
    python main.py --companies IBM --forms 10-K,10-Q,8-K --challenger
    python main.py --challenger --challenger-pages 3 --companies ""
"""
import argparse

import challenger
import config
import edgar
import gdrive
import normalize
import serper_search
import storage


def collect_for_company(company_or_ticker, forms, dataset, do_serper=True):
    saved = 0
    ticker = company_or_ticker.upper()

    cik = None
    try:
        cik = edgar.resolve_ticker(ticker)
    except Exception as e:
        print(f"  [warn] ticker resolve failed for {company_or_ticker}: {e}")

    if not cik:
        print(f"  [skip EDGAR] could not resolve CIK for {company_or_ticker}")
    else:
        try:
            filings = edgar.recent_filings(cik, forms=forms)
        except Exception as e:
            print(f"  [warn] recent_filings failed: {e}")
            filings = []

        for filing in filings:
            form = filing.get("form")
            company = filing.get("company") or company_or_ticker
            try:
                if form in ("10-K", "10-Q"):
                    text = edgar.fetch_filing_text(filing["url"])
                    sections = (("Item 1 Business", "Item 1A Risk Factors",
                                 "Item 7 MD&A", "Item 8 Financial Statements")
                                if form == "10-K" else
                                ("Item 1A Risk Factors",))
                    for label, sec_text in edgar.extract_sections(
                            text, sections=sections).items():
                        if not sec_text:
                            continue
                        doc = normalize.from_edgar_section(
                            company, ticker, filing, label, sec_text)
                        _, is_new = dataset.save_document(doc)
                        saved += int(is_new)
                elif form == "8-K":
                    primary_text = edgar.fetch_filing_text(filing["url"])
                    for label, sec_text in edgar.extract_8k_items(primary_text).items():
                        doc = normalize.from_edgar_section(
                            company, ticker, filing, label, sec_text)
                        _, is_new = dataset.save_document(doc)
                        saved += int(is_new)
                    for ex in edgar.fetch_8k_exhibits(cik, filing["accession"]):
                        if not ex.get("text"):
                            continue
                        doc = normalize.from_edgar_exhibit(
                            company, ticker, filing, ex)
                        _, is_new = dataset.save_document(doc)
                        saved += int(is_new)
            except Exception as e:
                print(f"  [warn] failed on {form} "
                      f"{filing.get('accession')}: {e}")

    if do_serper and config.SERPER_API_KEY:
        try:
            for hit in serper_search.find_transcript_links(company_or_ticker):
                doc = normalize.from_serper(company_or_ticker, hit)
                _, is_new = dataset.save_document(doc)
                saved += int(is_new)
        except Exception as e:
            print(f"  [warn] serper search failed: {e}")

    return saved


def collect_challenger(dataset, max_pages=1):
    saved = 0
    try:
        reports = challenger.list_reports(max_pages=max_pages)
    except Exception as e:
        print(f"[warn] challenger listing failed: {e}")
        return 0
    for rep in reports:
        try:
            text = challenger.fetch_report_text(rep["url"])
            for sentence in challenger.extract_ai_stats(text):
                doc = normalize.from_challenger(rep, text, sentence)
                _, is_new = dataset.save_document(doc)
                saved += int(is_new)
        except Exception as e:
            print(f"[warn] challenger report failed {rep.get('url')}: {e}")
    return saved


def main(argv=None):
    parser = argparse.ArgumentParser(description="AI-washing data scraper")
    parser.add_argument("--companies", default="",
                        help="comma-separated tickers, e.g. IBM,DELL,SAP")
    parser.add_argument("--forms", default="10-K,8-K",
                        help="comma-separated EDGAR form types")
    parser.add_argument("--challenger", action="store_true",
                        help="also scrape Challenger Gray job-cuts reports")
    parser.add_argument("--challenger-pages", type=int, default=1)
    parser.add_argument("--no-serper", action="store_true",
                        help="skip earnings-call URL lookups")
    parser.add_argument("--no-drive-upload", action="store_true",
                        help="skip uploading the export dir to Google Drive")
    args = parser.parse_args(argv)

    for w in config.validate():
        print(f"[config warning] {w}")

    dataset = storage.Dataset()
    total = 0

    companies = [c.strip() for c in args.companies.split(",") if c.strip()]
    forms = [f.strip() for f in args.forms.split(",") if f.strip()]
    for company in companies:
        print(f"Collecting: {company}")
        total += collect_for_company(
            company, forms, dataset, do_serper=not args.no_serper)

    if args.challenger:
        print("Collecting: Challenger Gray job-cuts reports")
        total += collect_challenger(dataset, max_pages=args.challenger_pages)

    print(f"Saved {total} new documents.")

    results = dataset.export()
    for group, (csv_path, json_path, n) in sorted(results.items()):
        print(f"[{group}] {n} docs -> {csv_path}")

    if args.no_drive_upload:
        return

    try:
        folder_id, uploaded = gdrive.upload_export_dir()
        print(f"Uploaded {len(uploaded)} files to Drive folder "
              f"'{config.GDRIVE_FOLDER_NAME}' (id={folder_id}): "
              f"{', '.join(uploaded)}")
    except Exception as e:
        print(f"[warn] Drive upload failed: {e}")


if __name__ == "__main__":
    main()
