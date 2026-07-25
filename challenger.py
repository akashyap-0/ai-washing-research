"""Scraper for Challenger, Gray & Christmas public job-cuts blog posts.

These are the firm's own public blog articles (the source of the AI-attribution
layoff statistics cited in the paper's background). The listing markup is a
typical CMS blog layout; the CSS selectors below are best-effort. If nothing
comes back, inspect the live page in Colab (right-click -> Inspect) and tune
the `select(...)` calls.
"""
import re
import time

import requests
from bs4 import BeautifulSoup

import config


def _get(url):
    resp = requests.get(
        url,
        headers={"User-Agent": config.SEC_USER_AGENT or "ai-washing-research"},
        timeout=30,
    )
    resp.raise_for_status()
    return resp


def _decode_html(raw_bytes):
    """Decode page HTML ourselves instead of handing raw bytes to
    BeautifulSoup. Its auto-detection has been observed to mis-guess plain
    'ascii' on real UTF-8 pages, which silently mangles curly quotes and
    dashes. Try UTF-8 first, falling back to Windows-1252 -- a full
    single-byte codec that never raises -- for pages that really are
    legacy-encoded.
    """
    try:
        return raw_bytes.decode("utf-8")
    except UnicodeDecodeError:
        return raw_bytes.decode("windows-1252")


def list_reports(max_pages=1):
    """Return [{title, url}] for job-cuts blog posts across `max_pages`."""
    reports = []
    for page in range(1, max_pages + 1):
        url = config.CHALLENGER_JOB_CUTS
        if page > 1:
            url = url.rstrip("/") + f"/page/{page}/"
        try:
            resp = _get(url)
        except Exception:
            break
        soup = BeautifulSoup(_decode_html(resp.content), "html.parser")
        for a in soup.select("article a[href], h2 a[href], h3 a[href]"):
            href = a.get("href")
            title = a.get_text(strip=True)
            if href and title and "/blog/" in href:
                if href.startswith("/"):
                    href = "https://www.challengergray.com" + href
                reports.append({"title": title, "url": href})
        time.sleep(0.5)

    seen, uniq = set(), []
    for r in reports:
        if r["url"] not in seen:
            seen.add(r["url"])
            uniq.append(r)
    return uniq


def fetch_report_text(url):
    """Return cleaned article body text for one report."""
    html = _decode_html(_get(url).content)
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup(["script", "style", "nav", "footer", "header", "aside"]):
        tag.decompose()
    main = soup.select_one("article") or soup.select_one("main") or soup.body
    text = main.get_text(separator="\n") if main else soup.get_text("\n")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{2,}", "\n\n", text)
    return text.strip()


def extract_ai_stats(text):
    """Return sentences that mention AI, for hand-labeling / stat extraction.

    Kept deliberately simple: pull any sentence referencing AI so the student
    can eyeball the surrounding percentages (e.g. 'AI ... 40% of cuts') rather
    than trusting a brittle number regex.
    """
    sentences = re.split(r"(?<=[.!?])\s+", text)
    return [s.strip() for s in sentences
            if re.search(r"\bAI\b|artificial intelligence", s, re.I)]
