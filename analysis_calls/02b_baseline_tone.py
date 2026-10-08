"""Genre baseline for the tone comparison: FinBERT tone of NON-AI sentences from the same sources.

Without it, "10-K risk factors sound negative about AI" could just mean "risk factors sound negative".
Calls: sentences from every call transcript (earnings_calls/filter_ai_passages.py splitter), AI terms excluded.
10-K: non-AI sentences of Mag 7 Item 1A. Random samples with a fixed seed. Same off-the-shelf FinBERT, not fine-tuned.
"""
import glob
import importlib.util
import os
import random
import re
import sys

import pandas as pd
import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common
from importlib import import_module

tone = import_module("02_finbert_tone")
SEED, N_CALLS_PER_SECTION, N_TENK = 3, 2500, 2500


def call_sentences():
    spec = importlib.util.spec_from_file_location("fap", os.path.join(common.ROOT, "earnings_calls", "filter_ai_passages.py"))
    fap = importlib.util.module_from_spec(spec); spec.loader.exec_module(fap)
    rows = []
    calls_dir = os.environ.get("CALLS_DIR", os.path.join(common.ROOT, "earnings_calls"))  # CALLS_DIR: raw calls incl. extras
    for path in sorted(glob.glob(os.path.join(calls_dir, "*", "*.md"))):
        company, period, stype, _, sents = fap.process(path)
        cy, cq = fap.cal_quarter(company, period)
        for text, section, _ in sents:
            if 40 <= len(text) <= 600 and not common.is_ai(text) and section in ("prepared", "qa"):
                rows.append((company, period, cy, cq, "prepared_remarks" if section == "prepared" else "qa", stype, text))
    return pd.DataFrame(rows, columns=["company", "period", "year", "quarter", "section", "source_type", "text"])


def tenk_sentences():
    k = pd.read_csv(os.path.join(common.ROOT, "export", "ai_washing_10-K.csv"), usecols=["ticker", "filing_date", "section", "text"])
    k = k[k.ticker.isin(common.TICKER.values()) & k.section.str.contains("1A")]
    rows = []
    for r in k.itertuples():
        for sent in tone.split_sentences(r.text):
            if len(sent) <= 600 and not common.is_ai(sent):
                rows.append((r.ticker, r.filing_date, sent))
    return pd.DataFrame(rows, columns=["ticker", "filing_date", "text"]).drop_duplicates()


def main():
    random.seed(SEED)
    device = common.get_device()
    tok = AutoTokenizer.from_pretrained(tone.MODEL)
    model = AutoModelForSequenceClassification.from_pretrained(tone.MODEL).to(device).eval()

    c = call_sentences()
    print("non-AI call sentences available:", len(c), c.section.value_counts().to_dict())
    c = pd.concat([g.sample(min(N_CALLS_PER_SECTION, len(g)), random_state=SEED) for _, g in c.groupby("section")]).reset_index(drop=True)
    sc = tone.score(c.text.tolist(), tok, model, device)
    pd.concat([c, sc], axis=1).to_csv(os.path.join(common.OUT, "ec_nonai_baseline_tone.csv"), index=False)

    t = tenk_sentences()
    print("non-AI 10-K Item 1A sentences available:", len(t))
    t = t.sample(min(N_TENK, len(t)), random_state=SEED).reset_index(drop=True)
    sc = tone.score(t.text.tolist(), tok, model, device)
    pd.concat([t, sc], axis=1).to_csv(os.path.join(common.OUT, "tenk_item1a_nonai_baseline_tone.csv"), index=False)
    print("done")


if __name__ == "__main__":
    main()
