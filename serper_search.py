"""Serper (Google Search API) wrapper.

SCOPE / COPYRIGHT BOUNDARY, read this before extending:
This module is used ONLY to locate earnings-call transcript URLs and the short
result snippets Google returns, so the student can open and read the sources
manually. It must NEVER be used to fetch or store the full body of paywalled /
ToS-protected transcript sites (e.g. Motley Fool, Seeking Alpha). For fully
public earnings-call-adjacent text, use the 8-K EX-99 exhibit press releases in
edgar.py instead, since that text is free and public on SEC EDGAR.
"""
import requests

import config


def search(query, num=10):
    if not config.SERPER_API_KEY:
        raise RuntimeError("SERPER_API_KEY not set.")
    resp = requests.post(
        config.SERPER_SEARCH,
        headers={"X-API-KEY": config.SERPER_API_KEY,
                 "Content-Type": "application/json"},
        json={"q": query, "num": num},
        timeout=30,
    )
    resp.raise_for_status()
    return resp.json()


def find_transcript_links(company, quarter=None):
    """Return [{title, url, snippet}] candidates for a company's earnings call.

    Only the short Google snippet is captured, never the full transcript.
    The student opens the links to review the actual material.
    """
    q = f"{company} earnings call transcript"
    if quarter:
        q += f" {quarter}"
    data = search(q)
    results = []
    for item in data.get("organic", []):
        results.append({
            "title": item.get("title"),
            "url": item.get("link"),
            "snippet": item.get("snippet"),
        })
    return results
