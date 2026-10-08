"""EXPLORATORY: fine-tune FinBERT to flag "AI opportunity" and "AI risk", then score earnings-call passages.

Training data: derived/annotation_complete_labeled.csv (1,200 SEC-filing passages). Labels are Claude-generated
(label_source=claude_blind_*) and review_status=unreviewed; the AK/TA coder_id values are NOT human coders.
Nothing here is validated on earnings calls, so treat outputs as a pilot, not a result.

Split is by company (tickers never shared across train/val/test) to limit boilerplate leakage.
Outputs: out/ft_metrics.json, out/ec_passage_labels.csv (per call passage), out/tenk_item1a_ai_labels.csv.
"""
import json
import os
import random
import sys

import numpy as np
import pandas as pd
import torch
from sklearn.metrics import f1_score, roc_auc_score
from transformers import AutoModelForSequenceClassification, AutoTokenizer

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common

MODEL = "ProsusAI/finbert"
LABELS = ["ai_opportunity", "ai_risk"]
SEED, MAX_LEN, EPOCHS, LR, BATCH = 7, 256, 4, 3e-5, 16


def seed_all():
    random.seed(SEED); np.random.seed(SEED); torch.manual_seed(SEED)


def predict(texts, tok, model, device, batch=64):
    order = np.argsort([len(t) for t in texts])
    res = np.zeros((len(texts), len(LABELS)))
    model.eval()
    for i in range(0, len(texts), batch):
        idx = order[i:i + batch]
        enc = tok([texts[j] for j in idx], padding=True, truncation=True, max_length=MAX_LEN, return_tensors="pt").to(device)
        with torch.no_grad():
            res[idx] = torch.sigmoid(model(**enc).logits).cpu().numpy()
    return res


def main():
    seed_all()
    device = common.get_device()
    df = pd.read_csv(os.path.join(common.ROOT, "derived", "annotation_complete_labeled.csv"))
    df = df[["passage_id", "ticker", "text"] + LABELS].dropna()

    tickers = sorted(df.ticker.unique())
    rng = random.Random(SEED); rng.shuffle(tickers)
    n = len(tickers)
    test_t, val_t = set(tickers[: n // 5]), set(tickers[n // 5: 2 * (n // 5)])
    split = df.ticker.map(lambda t: "test" if t in test_t else ("val" if t in val_t else "train"))
    tr, va, te = df[split == "train"], df[split == "val"], df[split == "test"]
    print(f"train {len(tr)} val {len(va)} test {len(te)} | held-out tickers val={sorted(val_t)} test={sorted(test_t)}")

    tok = AutoTokenizer.from_pretrained(MODEL)
    model = AutoModelForSequenceClassification.from_pretrained(
        MODEL, num_labels=len(LABELS), problem_type="multi_label_classification", ignore_mismatched_sizes=True).to(device)
    opt = torch.optim.AdamW(model.parameters(), lr=LR, weight_decay=0.01)
    steps = EPOCHS * ((len(tr) + BATCH - 1) // BATCH)
    sched = torch.optim.lr_scheduler.LinearLR(opt, start_factor=1.0, end_factor=0.0, total_iters=steps)
    loss_fn = torch.nn.BCEWithLogitsLoss()

    best, best_state = 1e9, None
    for ep in range(EPOCHS):
        model.train()
        idx = np.random.permutation(len(tr))
        for i in range(0, len(idx), BATCH):
            b = tr.iloc[idx[i:i + BATCH]]
            enc = tok(b.text.tolist(), padding=True, truncation=True, max_length=MAX_LEN, return_tensors="pt").to(device)
            y = torch.tensor(b[LABELS].values, dtype=torch.float32, device=device)
            loss = loss_fn(model(**enc).logits, y)
            loss.backward(); torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
            opt.step(); sched.step(); opt.zero_grad()
        pv = predict(va.text.tolist(), tok, model, device)
        vl = float(loss_fn(torch.logit(torch.tensor(pv).clamp(1e-6, 1 - 1e-6)), torch.tensor(va[LABELS].values, dtype=torch.float32)))
        print(f"epoch {ep + 1} val loss {vl:.4f}", flush=True)
        if vl < best:
            best, best_state = vl, {k: v.detach().cpu().clone() for k, v in model.state_dict().items()}
    model.load_state_dict(best_state)

    # Thresholds picked on validation companies; metrics reported on untouched test companies.
    pv, pt = predict(va.text.tolist(), tok, model, device), predict(te.text.tolist(), tok, model, device)
    metrics = {"split": {"train": len(tr), "val": len(va), "test": len(te), "val_tickers": sorted(val_t), "test_tickers": sorted(test_t)},
               "label_source_note": "Claude-generated, unreviewed; not human gold", "labels": {}}
    thr = {}
    for j, lab in enumerate(LABELS):
        grid = np.linspace(0.1, 0.9, 33)
        f1s = [f1_score(va[lab], pv[:, j] >= g, zero_division=0) for g in grid]
        thr[lab] = float(grid[int(np.argmax(f1s))])
        yt = te[lab].values
        metrics["labels"][lab] = {
            "threshold": thr[lab], "test_positive_rate": float(yt.mean()),
            "test_auc": float(roc_auc_score(yt, pt[:, j])) if 0 < yt.sum() < len(yt) else None,
            "test_f1": float(f1_score(yt, pt[:, j] >= thr[lab], zero_division=0)),
            "test_f1_always_positive_baseline": float(f1_score(yt, np.ones(len(yt)), zero_division=0)),
        }
    json.dump(metrics, open(os.path.join(common.OUT, "ft_metrics.json"), "w"), indent=2)
    print(json.dumps(metrics["labels"], indent=2))

    # Score earnings-call passages (anchor sentence + same-turn context), keyed to the anchor sentence.
    p = pd.read_csv(os.path.join(common.CANON, "earnings_call_labeling_passages.csv"), usecols=["anchor_sentence_id", "text"])
    pr = predict(p.text.tolist(), tok, model, device)
    out = pd.DataFrame({"anchor_sentence_id": p.anchor_sentence_id, **{f"p_{l}": pr[:, j] for j, l in enumerate(LABELS)}})
    for l in LABELS:
        out[l] = (out[f"p_{l}"] >= thr[l]).astype(int)
    out.to_csv(os.path.join(common.OUT, "ec_passage_labels.csv"), index=False)

    tk = os.path.join(common.OUT, "tenk_item1a_ai_tone.csv")
    if os.path.exists(tk):
        t = pd.read_csv(tk, usecols=["ticker", "filing_date", "text"])
        tr_ = predict(t.text.tolist(), tok, model, device)
        o = t.copy()
        for j, l in enumerate(LABELS):
            o[f"p_{l}"] = tr_[:, j]; o[l] = (tr_[:, j] >= thr[l]).astype(int)
        o.to_csv(os.path.join(common.OUT, "tenk_item1a_ai_labels.csv"), index=False)
    print("done")


if __name__ == "__main__":
    main()
