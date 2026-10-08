"""Off-the-shelf FinBERT (ProsusAI/finbert) sentiment on AI sentences.

NOT fine-tuned. Gives P(positive), P(negative), P(neutral) for
  - every AI sentence in the canonical earnings-call dataset
  - AI sentences from Item 1A Risk Factors of the Mag 7's 10-K filings (export/ai_washing_10-K.csv)
Tone = P(pos) - P(neg). This is generic financial-news tone, not "AI opportunity vs risk".
"""
import os
import re
import sys

import numpy as np
import pandas as pd
import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common

MODEL = "ProsusAI/finbert"


def score(texts, tok, model, device, batch=64, max_len=160):
    labels = [model.config.id2label[i].lower() for i in range(model.config.num_labels)]
    out = []
    order = np.argsort([len(t) for t in texts])  # length-sorted batches are much faster
    for i in range(0, len(texts), batch):
        idx = order[i:i + batch]
        enc = tok([texts[j] for j in idx], padding=True, truncation=True, max_length=max_len, return_tensors="pt").to(device)
        with torch.no_grad():
            p = torch.softmax(model(**enc).logits, dim=-1).cpu().numpy()
        out.append((idx, p))
        if (i // batch) % 20 == 0:
            print(f"  {i}/{len(texts)}", flush=True)
    res = np.zeros((len(texts), len(labels)))
    for idx, p in out:
        res[idx] = p
    return pd.DataFrame(res, columns=[f"p_{l}" for l in labels])


def split_sentences(text):
    text = re.sub(r"\s+", " ", text)
    return [s.strip() for s in re.split(r"(?<=[\.\?\!])\s+(?=[A-Z\"“(])", text) if len(s.strip()) > 25]


def main():
    device = common.get_device()
    print("device", device)
    tok = AutoTokenizer.from_pretrained(MODEL)
    model = AutoModelForSequenceClassification.from_pretrained(MODEL).to(device).eval()

    s = pd.read_csv(os.path.join(common.CANON, "earnings_call_sentences.csv"), usecols=["sentence_id", "text_verbatim"])
    print("earnings-call AI sentences:", len(s))
    sc = score(s.text_verbatim.tolist(), tok, model, device)
    pd.concat([s[["sentence_id"]], sc], axis=1).to_csv(os.path.join(common.OUT, "ec_sentence_tone.csv"), index=False)

    k = pd.read_csv(os.path.join(common.ROOT, "export", "ai_washing_10-K.csv"),
                    usecols=["ticker", "filing_date", "section", "text"])
    k = k[k.ticker.isin(common.TICKER.values()) & k.section.str.contains("1A")]
    rows = []
    for r in k.itertuples():
        for sent in split_sentences(r.text):
            if common.is_ai(sent):
                rows.append((r.ticker, r.filing_date, sent))
    t = pd.DataFrame(rows, columns=["ticker", "filing_date", "text"]).drop_duplicates()
    print("10-K Item 1A AI sentences (Mag 7):", len(t))
    sc = score(t.text.tolist(), tok, model, device)
    pd.concat([t.reset_index(drop=True), sc], axis=1).to_csv(os.path.join(common.OUT, "tenk_item1a_ai_tone.csv"), index=False)
    print("done")


if __name__ == "__main__":
    main()
