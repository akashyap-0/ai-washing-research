"""Graphs 3-4: tone of AI sentences on earnings calls vs in 10-K risk factors.

fig5: off-the-shelf FinBERT tone (P(pos) - P(neg)) of AI sentences, calls (prepared, Q&A) vs 10-K Item 1A.
fig6: EXPLORATORY fine-tuned labels (AI opportunity / AI risk), only drawn if out/ec_passage_labels.csv exists.
Both are descriptive pilots: no human validation, 10-K coverage is partial (Alphabet 2024+, Meta 2025+).
"""
import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common

SRC = {"calls_prepared": ("#1f77b4", "Earnings calls: prepared remarks"),
       "calls_qa": ("#2ca02c", "Earnings calls: Q&A"),
       "tenk_1a": ("#d62728", "10-K Item 1A risk factors")}
INV = {v: k for k, v in common.TICKER.items()}


def ci(x):
    x = np.asarray(x, float)
    return 1.96 * x.std(ddof=1) / np.sqrt(len(x)) if len(x) > 1 else np.nan


def load_calls():
    s = pd.read_csv(os.path.join(common.CANON, "earnings_call_sentences.csv"),
                    usecols=["sentence_id", "company", "calendar_year", "calendar_quarter", "section", "unit_type"])
    return s.rename(columns={"calendar_year": "year"})


def load_tenk(path):
    t = pd.read_csv(path)
    t["year"] = t.filing_date.str[:4].astype(int)
    t["company"] = t.ticker.map(INV)
    return t


def load_baselines():
    """Mean tone of NON-AI sentences per source (genre baseline), or None if not computed."""
    b = {}
    cp = os.path.join(common.OUT, "ec_nonai_baseline_tone.csv")
    tp = os.path.join(common.OUT, "tenk_item1a_nonai_baseline_tone.csv")
    if os.path.exists(cp):
        c = pd.read_csv(cp); c["tone"] = c.p_positive - c.p_negative
        b["calls_prepared"] = c[c.section == "prepared_remarks"].tone
        b["calls_qa"] = c[c.section == "qa"].tone
    if os.path.exists(tp):
        t = pd.read_csv(tp); b["tenk_1a"] = t.p_positive - t.p_negative
    return b


def fig_tone(calls, tenk):
    calls = calls.copy(); calls["tone"] = calls.p_positive - calls.p_negative
    tenk = tenk.copy(); tenk["tone"] = tenk.p_positive - tenk.p_negative
    comp = calls[calls.unit_type.isin(["sentence", "caption_sentence"])]  # sentence-like units only
    base = load_baselines()
    INKC, GREY = "#222222", "#9a9a9a"
    plt.rcParams.update({"font.family": "DejaVu Sans", "axes.spines.top": False, "axes.spines.right": False})

    src = [("calls_prepared", "Earnings calls:\nprepared remarks", comp[(comp.section == "prepared_remarks") & (comp.year >= 2023)].tone, "#0072B2"),
           ("calls_qa", "Earnings calls:\nQ&A with analysts", comp[(comp.section == "qa") & (comp.year >= 2023)].tone, "#009E73"),
           ("tenk_1a", "10-K risk factors\n(Item 1A)", tenk[tenk.year >= 2023].tone, "#D55E00")]
    fig, axes = plt.subplots(1, 2, figsize=(16, 6.2), gridspec_kw={"width_ratios": [1.1, 1]})
    ax = axes[0]
    for i, (key, name, ai, color) in enumerate(src):
        y = len(src) - 1 - i
        b = base[key].mean()
        ax.plot([b, ai.mean()], [y, y], color=color, lw=5, alpha=0.35, solid_capstyle="round", zorder=1)
        ax.scatter([b], [y], s=190, facecolors="white", edgecolors=color, linewidths=2.5, zorder=3)
        ax.errorbar([ai.mean()], [y], xerr=[ci(ai)], fmt="o", ms=13, color=color, capsize=4, lw=2, zorder=4)
        right = ai.mean() >= b
        ax.text(b - 0.02 if right else b + 0.02, y + 0.27, f"{b:+.2f}", ha="right" if right else "left", fontsize=10, color="#555555")
        ax.text(ai.mean() + 0.02 if right else ai.mean() - 0.02, y + 0.27, f"{ai.mean():+.2f}", ha="left" if right else "right",
                fontsize=11, color=color, fontweight="bold")
        ax.text(0.99, y, f"AI vs other: {ai.mean() - b:+.2f}", transform=ax.get_yaxis_transform(), ha="right", va="center", fontsize=11,
                color=INKC, fontweight="bold")
    ax.set_yticks(range(len(src))); ax.set_yticklabels([n for _, n, _, _ in src][::-1], fontsize=12)
    ax.axvline(0, color=GREY, lw=1)
    ax.set_xlim(-0.45, 0.78); ax.set_ylim(-0.6, 2.7)
    ax.set_xlabel("Tone  (negative  ←  0  →  positive)", fontsize=11)
    ax.set_title("Hollow dot = ordinary sentences in that source   |   filled dot = AI sentences (95% CI)", fontsize=10.5, loc="left", color="#444444")
    ax.text(-0.43, -0.45, "Reading: the big gap between sources is mostly genre (risk factors are always gloomy).\n"
            "The AI-specific effect is the small gap between the hollow and filled dot.", fontsize=9.5, color="#555555", va="bottom")

    ax = axes[1]
    post_c, post_k = comp[comp.year >= 2023], tenk[tenk.year >= 2023]
    cos = [c for c in common.COMPANY_ORDER if c in set(post_k.company)]
    order = sorted(cos, key=lambda c: -(post_c[(post_c.company == c) & (post_c.section == "prepared_remarks")].tone.mean()
                                         if c in set(post_c.company) else -9))
    for i, c in enumerate(order):
        y = len(order) - 1 - i
        pts = []
        for key, name, color, d in [("prep", "calls: prepared", "#0072B2", post_c[(post_c.company == c) & (post_c.section == "prepared_remarks")].tone),
                                    ("qa", "calls: Q&A", "#009E73", post_c[(post_c.company == c) & (post_c.section == "qa")].tone),
                                    ("k", "10-K risk factors", "#D55E00", post_k[post_k.company == c].tone)]:
            if len(d) >= 5:
                pts.append(d.mean())
                ax.errorbar([d.mean()], [y], xerr=[ci(d)], fmt="o", ms=10, color=color, capsize=3, lw=1.6, zorder=3,
                            label=name if i == 0 else None)
        if len(pts) > 1:
            ax.plot([min(pts), max(pts)], [y, y], color="#cccccc", lw=3, zorder=1)
    ax.set_yticks(range(len(order))); ax.set_yticklabels([c.title() for c in order][::-1], fontsize=12)
    ax.axvline(0, color=GREY, lw=1)
    ax.set_xlabel("Tone of AI sentences  (negative  ←  0  →  positive)", fontsize=11)
    ax.set_title("Same pattern at every company (AI sentences, 2023 onward)", fontsize=10.5, loc="left", color="#444444")
    ax.legend(loc="lower right", fontsize=10, frameon=False)
    if "amazon" in order:
        ax.text(0.02, 0.02, "Amazon: no call dots (audio-only call, not comparable units)", transform=ax.transAxes, fontsize=8.5, color="#777777")
    fig.suptitle("Executives sound upbeat about AI on calls and gloomy in risk factors, but most of that gap is just genre",
                 fontsize=16, fontweight="bold", x=0.02, ha="left", y=0.995)
    fig.text(0.02, 0.01, "Tone = FinBERT P(positive) - P(negative), off-the-shelf model (not fine-tuned). 'Ordinary sentences' = random samples of "
             "non-AI sentences from the same sources. 10-K coverage is partial (Alphabet from 2024, Meta from 2025).", fontsize=9, color="#555555")
    fig.tight_layout(rect=(0, 0.03, 1, 0.95))
    fig.savefig(os.path.join(common.FIG, "fig5_tone_calls_vs_10k.png"), dpi=170)
    plt.close(fig)

    rows = []
    for key, d in [("calls_prepared", comp[comp.section == "prepared_remarks"]), ("calls_qa", comp[comp.section == "qa"]), ("tenk_1a", tenk)]:
        for lab, dd in [("2021-2022", d[d.year <= 2022]), ("2023-2026", d[d.year >= 2023])]:
            rows.append({"source": key, "period": lab, "n": len(dd), "mean_tone": dd.tone.mean(),
                         "share_negative_gt_0.5": (dd.p_negative > 0.5).mean(), "share_positive_gt_0.5": (dd.p_positive > 0.5).mean()})
    for key, ser in base.items():
        rows.append({"source": key + "_NONAI_baseline", "period": "all", "n": len(ser), "mean_tone": ser.mean(),
                     "share_negative_gt_0.5": np.nan, "share_positive_gt_0.5": np.nan})
    out = pd.DataFrame(rows)
    out.to_csv(os.path.join(common.OUT, "tone_summary.csv"), index=False)
    print(out.round(3).to_string(index=False))


def fig_labels(calls, tenk_lab):
    """EXPLORATORY fig6: share of AI sentences the fine-tuned FinBERT flags as AI-opportunity / AI-risk."""
    lab_path = os.path.join(common.OUT, "ec_passage_labels.csv")
    if not os.path.exists(lab_path):
        print("no fine-tuned labels yet; skipping fig6")
        return
    lab = pd.read_csv(lab_path).rename(columns={"anchor_sentence_id": "sentence_id"})
    d = calls.merge(lab, on="sentence_id")
    d["q"] = [common.qkey(y, q) for y, q in zip(d.year, d.calendar_quarter)]
    d = d[d.unit_type.isin(["sentence", "caption_sentence"])]
    plt.rcParams.update({"font.family": "DejaVu Sans", "axes.spines.top": False, "axes.spines.right": False})
    lx = common.qkey(*common.FIRST_POST_QUARTER) - 0.125
    fig, axes = plt.subplots(1, 2, figsize=(15, 6.4), sharey=True)
    for ax, col, title in [(axes[0], "ai_opportunity", "Flagged as AI OPPORTUNITY"), (axes[1], "ai_risk", "Flagged as AI RISK")]:
        ax.axvspan(lx, 2026.9, color="#fdecea", zorder=0)
        ax.axvline(lx, color="#B22222", lw=2)
        ends = []
        for sec, color, name in [("prepared_remarks", SRC["calls_prepared"][0], "Calls: prepared remarks"), ("qa", SRC["calls_qa"][0], "Calls: Q&A")]:
            g = d[d.section == sec].groupby("q")[col].agg(["mean", "count"])
            g = g[g["count"] >= 20]
            ax.plot(g.index, g["mean"] * 100, marker="o", ms=5, lw=2.6, color=color)
            ends.append((g["mean"].iloc[-1] * 100, name, color, g.index[-1]))
        if tenk_lab is not None:
            t = tenk_lab.copy()
            g = t.groupby("year")[col].agg(["mean", "count"]); g = g[g["count"] >= 15]
            ax.plot(g.index + 0.5, g["mean"] * 100, marker="s", ms=8, lw=2.6, ls="--", color=SRC["tenk_1a"][0])
            ends.append((g["mean"].iloc[-1] * 100, "10-K risk factors\n(by filing year)", SRC["tenk_1a"][0], g.index[-1] + 0.5))
        ends.sort()
        for i in range(1, len(ends)):
            ends[i] = (max(ends[i][0], ends[i - 1][0] + 7), *ends[i][1:])
        for y, name, color, xq in ends:
            ax.text(xq + 0.1, y, name, color=color, fontsize=10.5, fontweight="bold", va="center")
        ax.set_title(title, fontsize=14, fontweight="bold", loc="left")
        ax.set_xlim(2021.7, 2028.6); ax.set_ylim(0, 105); ax.grid(axis="y", color="#e6e6e6")
        ax.set_xticks([2022, 2023, 2024, 2025, 2026]); ax.set_xlabel("Calendar quarter (calls) / filing year (10-K)", fontsize=10)
    axes[0].set_ylabel("% of AI sentences flagged", fontsize=11)
    axes[0].text(lx + 0.06, 4, "ChatGPT launch", color="#B22222", ha="left", va="bottom", fontsize=10, fontweight="bold")
    fig.suptitle("EXPLORATORY: how often a fine-tuned FinBERT flags AI sentences as opportunity vs risk", fontsize=16,
                 fontweight="bold", x=0.02, ha="left", y=0.995)
    fig.text(0.02, 0.905, "Trained on 1,200 SEC-filing passages whose labels were generated by Claude and never human-reviewed. "
             "Not validated on earnings calls. Read the trends, not the absolute levels.", fontsize=10.5, color="#444444")
    fig.text(0.02, 0.012, "Caveats: the model flags most call sentences as opportunity (levels are saturated), and its risk flag partly detects risk-factor writing style\n"
             "(training risk labels come almost entirely from Item 1A). Decision thresholds were tuned on only 80 passages.",
             fontsize=9, color="#7a1f1f")
    fig.tight_layout(rect=(0, 0.07, 1, 0.89))
    fig.savefig(os.path.join(common.FIG, "fig6_exploratory_opportunity_vs_risk.png"), dpi=170)
    plt.close(fig)
    print(d.groupby("section")[["ai_opportunity", "ai_risk"]].mean().round(3))


if __name__ == "__main__":
    calls = load_calls().merge(pd.read_csv(os.path.join(common.OUT, "ec_sentence_tone.csv")), on="sentence_id")
    tenk = load_tenk(os.path.join(common.OUT, "tenk_item1a_ai_tone.csv"))
    fig_tone(calls, tenk)
    lp = os.path.join(common.OUT, "tenk_item1a_ai_labels.csv")
    tenk_lab = load_tenk(lp) if os.path.exists(lp) else None
    fig_labels(load_calls(), tenk_lab)
