"""Configuration and environment loading for the AI-washing scraper.

All secrets are read from environment variables so nothing sensitive is ever
hardcoded, e.g.:

    import os
    os.environ["SEC_USER_AGENT"] = "Jane Doe research jane@example.com"
    os.environ["SERPER_API_KEY"] = "your-serper-api-key"
    os.environ["EXPORT_DIR"] = "./export"
    os.environ["GDRIVE_CREDENTIALS_PATH"] = "credentials.json"

(or use Colab's userdata / secrets manager, then copy into os.environ).
"""
import os

# --- Secrets / environment ---------------------------------------------------
SERPER_API_KEY = os.environ.get("SERPER_API_KEY", "")
# SEC requires a descriptive User-Agent containing a real name + email.
# Requests without one are throttled/blocked. Example:
#   "Jane Doe research jane@example.com"
SEC_USER_AGENT = os.environ.get("SEC_USER_AGENT", "")
# Local staging directory where grouped CSV/JSON files are written before
# being uploaded to Drive. Kept local (not a Drive mount) so this also works
# outside Colab -- see gdrive.py for the upload step.
EXPORT_DIR = os.environ.get("EXPORT_DIR", "./export")

# --- Google Drive (OAuth) -----------------------------------------------------
# One-time setup: create an OAuth client (Desktop app) in Google Cloud Console
# with the Drive API enabled, download its JSON, and point this at it. The
# first run opens a browser to sign in as advikkashyap1@gmail.com or
# ecfarmer12@gmail.com; the resulting refresh token is cached at
# GDRIVE_TOKEN_PATH so later runs don't need the browser again.
GDRIVE_CREDENTIALS_PATH = os.environ.get("GDRIVE_CREDENTIALS_PATH", "credentials.json")
GDRIVE_TOKEN_PATH = os.environ.get("GDRIVE_TOKEN_PATH", "token.json")
# Destination folder created/reused in whichever Drive account authenticates.
GDRIVE_FOLDER_NAME = os.environ.get("GDRIVE_FOLDER_NAME", "Georgetown Research")

# --- Endpoint constants ------------------------------------------------------
EDGAR_FULLTEXT_SEARCH = "https://efts.sec.gov/LATEST/search-index"
EDGAR_SUBMISSIONS = "https://data.sec.gov/submissions/CIK{cik}.json"
EDGAR_ARCHIVES = "https://www.sec.gov/Archives/edgar/data/{cik}/{accession}/{doc}"
EDGAR_TICKER_MAP = "https://www.sec.gov/files/company_tickers.json"

SERPER_SEARCH = "https://google.serper.dev/search"

CHALLENGER_JOB_CUTS = "https://www.challengergray.com/blog/category/job-cuts-report/"

# SEC fair-access asks clients to stay under ~10 requests/second. We stay well
# under that with a small per-request delay.
SEC_REQUEST_DELAY = 0.2  # seconds


def validate():
    """Return a list of human-readable warnings for missing configuration.

    Non-fatal: the pipeline can still run partially (e.g. skip Serper) with
    some values unset, so we warn rather than raise here.
    """
    warnings = []
    if not SEC_USER_AGENT:
        warnings.append(
            "SEC_USER_AGENT is not set. SEC EDGAR will block requests without a "
            "descriptive User-Agent like 'Your Name your@email.com'."
        )
    if not os.path.exists(GDRIVE_CREDENTIALS_PATH):
        warnings.append(
            f"GDRIVE_CREDENTIALS_PATH ('{GDRIVE_CREDENTIALS_PATH}') does not "
            "exist. Create an OAuth client (Desktop app) in Google Cloud "
            "Console with the Drive API enabled, download its JSON, and save "
            "it at that path -- otherwise Drive upload will fail."
        )
    if not SERPER_API_KEY:
        warnings.append(
            "SERPER_API_KEY is not set. Earnings-call URL lookups will be skipped."
        )
    if not EXPORT_DIR:
        warnings.append("EXPORT_DIR is not set; falling back to ./export.")
    return warnings
