"""Shared paths, ChatGPT-launch marker and the AI sentence regex for the earnings-call analysis scripts."""
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CANON = os.path.join(ROOT, "earnings_calls_canonical")
OUT = os.path.join(ROOT, "analysis_calls", "out")
FIG = os.path.join(ROOT, "figures_calls")
os.makedirs(OUT, exist_ok=True)
os.makedirs(FIG, exist_ok=True)

# ChatGPT launched 2022-11-30. Calls reporting calendar Q4 2022 (held Jan-Feb 2023) are the first post-launch calls.
FIRST_POST_QUARTER = (2022, 4)

COMPANY_ORDER = ["alphabet", "amazon", "apple", "meta", "microsoft", "nvidia", "tesla"]
TICKER = {"alphabet": "GOOGL", "amazon": "AMZN", "apple": "AAPL", "meta": "META",
          "microsoft": "MSFT", "nvidia": "NVDA", "tesla": "TSLA"}

# Explicit AI terms only, mirroring the "core" idea of the canonical filter (used for 10-K sentences,
# which the canonical filter does not cover).
RE_AI = re.compile(
    r"artificial intelligence|machine learning|deep learning|neural net(?:work)?s?"
    r"|large language models?|\bLLMs?\b|\bgenerative\b|chat ?GPT|\bGPT[- ]?\d?|open ?AI|\bcopilot\b|\bgemini\b"
    r"|\bagentic\b|foundation models?|apple intelligence",
    re.I,
)
RE_AI_CS = re.compile(r"\bA\.?I\.?(?![A-Za-z])")  # "AI" must be upper-case


def is_ai(sentence):
    return bool(RE_AI_CS.search(sentence) or RE_AI.search(sentence))


def qkey(year, quarter):
    return year + (quarter - 1) / 4.0


def qlabel(year, quarter):
    return f"{year}Q{quarter}"


def get_device():
    import torch
    return "mps" if torch.backends.mps.is_available() else "cpu"
