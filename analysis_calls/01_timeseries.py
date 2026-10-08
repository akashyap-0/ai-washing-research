"""Graphs 1-2: how much AI talk is there in Mag 7 earnings calls over time, and does it jump after ChatGPT?

Source: earnings_calls_canonical/earnings_call_call_units.csv (counts only, no model).
AI share = AI units / all valid parsed units in the call (Advik's primary denominator).
Calls whose units are not sentences (YouTube caption segments, Whisper lines) are drawn hollow and left out of
pooled lines, because their shares are not comparable to sentence-based calls (EARNINGS_CALL_SCOPE.md section 4).

Outputs: fig1_headline_ai_talk.png (the one-chart answer), fig1b_ai_talk_by_company.png (small multiples),
fig2_ai_share_heatmap.png (company x quarter grid with the numbers in the cells).
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

# Colour-blind-safe (Okabe-Ito) so no two firms share a hue.
COLORS = {"alphabet": "#0072B2", "amazon": "#E69F00", "apple": "#7F7F7F", "meta": "#CC79A7",
          "microsoft": "#56B4E9", "nvidia": "#009E73", "tesla": "#D55E00"}
INK, GRID, LAUNCH = "#222222", "#e6e6e6", "#B22222"
plt.rcParams.update({"font.family": "DejaVu Sans", "axes.spines.top": False, "axes.spines.right": False,
                     "axes.edgecolor": "#888888", "axes.labelcolor": INK, "xtick.color": INK, "ytick.color": INK})


def qtick(q):
    return f"{int(q)} Q{int(round((q % 1) * 4)) + 1}"


def load():
    cu = pd.read_csv(os.path.join(common.CANON, "earnings_call_call_units.csv"))
    cu["q"] = [common.qkey(y, q) for y, q in zip(cu.calendar_year, cu.calendar_quarter)]
    cu["share"] = cu.ai_units / cu.total_units * 100
    cu["comparable"] = cu.units_comparable_to_sentences == 1
    return cu


def launch_x():
    return common.qkey(*common.FIRST_POST_QUARTER) - 0.125


def balanced_firms(cu):
    """Firms with at least 3 sentence-comparable calls both before and after the launch: a fixed-composition panel."""
    comp = cu[cu.comparable]
    post = comp.q >= common.qkey(*common.FIRST_POST_QUARTER)
    pre_n, post_n = comp[~post].groupby("company").size(), comp[post].groupby("company").size()
    return sorted(c for c in pre_n.index if pre_n[c] >= 3 and post_n.get(c, 0) >= 3)


def fig_headline(cu):
    bal = balanced_firms(cu)
    d = cu[cu.comparable & cu.company.isin(bal)]
    g = d.groupby("q").share.mean()
    pre, post = g[g.index < launch_x()], g[g.index >= launch_x()]
    qs = sorted(cu.q.unique())

    fig, ax = plt.subplots(figsize=(13, 6.2))
    ax.axvspan(launch_x(), max(qs) + 0.3, color="#fdecea", zorder=0)
    ax.axvline(launch_x(), color=LAUNCH, lw=2)
    for c in bal:
        dc = d[d.company == c].sort_values("q")
        ax.plot(dc.q, dc.share, color=COLORS[c], lw=1.4, alpha=0.55, marker="o", ms=4)
        ax.text(dc.q.iloc[-1] + 0.08, dc.share.iloc[-1], c.title(), color=COLORS[c], fontsize=10, va="center", fontweight="bold")
    ax.plot(g.index, g.values, color=INK, lw=4, marker="o", ms=8, zorder=5, label="Average of the three firms")
    ax.legend(loc="lower right", fontsize=11, frameon=False)
    ax.annotate(f"{pre.mean():.0f}% of the call\nbefore ChatGPT", xy=(pre.index[len(pre) // 2], pre.mean()), xytext=(2021.9, 24),
                fontsize=13, color=INK, ha="left", arrowprops=dict(arrowstyle="-|>", color=INK, lw=1.4))
    ax.annotate(f"{post.mean():.0f}% of the call\nafter ChatGPT", xy=(post.index[len(post) // 2], post.mean()), xytext=(2023.6, 6),
                fontsize=13, color=INK, ha="left", arrowprops=dict(arrowstyle="-|>", color=INK, lw=1.4))
    ax.text(launch_x() - 0.05, 42, "ChatGPT launches\nNov 30, 2022", color=LAUNCH, fontsize=11, ha="right", fontweight="bold")
    ax.set_xticks(qs[::2]); ax.set_xticklabels([qtick(q) for q in qs[::2]], rotation=0, fontsize=10)
    ax.set_xlim(min(qs) - 0.2, max(qs) + 1.15); ax.set_ylim(0, 46)
    ax.set_ylabel("Share of the earnings call that is about AI (%)", fontsize=12)
    ax.set_xlabel("Calendar quarter reported", fontsize=11)
    ax.grid(axis="y", color=GRID)
    fig.suptitle("AI went from a side topic to a core topic on earnings calls right after ChatGPT",
                 fontsize=17, fontweight="bold", x=0.05, ha="left", y=0.985)
    ax.set_title(f"Same three firms the whole way ({', '.join(c.title() for c in bal)}). Each dot is one earnings call.",
                 fontsize=11, loc="left", color="#444444")
    fig.text(0.05, 0.01, "Why only these three? They are the only firms with several comparable calls both before and after the launch "
             "(17 of 133 early calls are missing). Share = AI sentences / all sentences in the call.", fontsize=8.5, color="#555555")
    fig.tight_layout(rect=(0.0, 0.04, 1, 0.95))
    fig.savefig(os.path.join(common.FIG, "fig1_headline_ai_talk.png"), dpi=170)
    plt.close(fig)


def fig_by_company(cu):
    qs = sorted(cu.q.unique())
    order = list(cu[cu.comparable & (cu.q >= launch_x())].groupby("company").share.mean().sort_values(ascending=False).index)
    order += [c for c in common.COMPANY_ORDER if c not in order]
    fig, axes = plt.subplots(2, 4, figsize=(16, 7.4), sharex=True, sharey=True)
    for ax, c in zip(axes.flat, order):
        d = cu[cu.company == c].sort_values("q")
        ax.axvspan(launch_x(), max(qs) + 0.3, color="#fdecea", zorder=0)
        ax.plot(d.q, d.share, color=COLORS[c], lw=2.4, zorder=2)
        ax.scatter(d.q[d.comparable], d.share[d.comparable], color=COLORS[c], s=26, zorder=3)
        ax.scatter(d.q[~d.comparable], d.share[~d.comparable], facecolors="white", edgecolors=COLORS[c], s=34, lw=1.5, zorder=3)
        last = d[d.q >= max(qs) - 1].share.mean()
        ax.set_title(c.title(), fontsize=14, fontweight="bold", color=COLORS[c], loc="left")
        ax.text(0.98, 0.96, f"now ~{last:.0f}%", transform=ax.transAxes, ha="right", va="top", fontsize=11, color=INK)
        ax.set_xticks([2022, 2023, 2024, 2025, 2026]); ax.set_xticklabels(["'22", "'23", "'24", "'25", "'26"])
        ax.grid(axis="y", color=GRID); ax.set_ylim(0, 60)
    for ax in axes.flat[len(order):]:
        ax.axis("off")
    last_ax = axes.flat[len(order)]
    last_ax.text(0.02, 0.95, "How to read", fontsize=12, fontweight="bold", va="top", transform=last_ax.transAxes)
    last_ax.text(0.02, 0.82, "Line = % of each call that is about AI.\nPink area = after ChatGPT launched.\n"
                 "Hollow dots = calls where the transcript\nis not split into sentences (captions or\nmachine audio), so the number is\nless comparable.", fontsize=10, va="top", color="#333333", transform=last_ax.transAxes)
    axes[0, 0].set_ylabel("% of call about AI"); axes[1, 0].set_ylabel("% of call about AI")
    fig.suptitle("Every company talks about AI far more than before, but at very different levels", fontsize=17, fontweight="bold",
                 x=0.04, ha="left", y=0.995)
    fig.tight_layout(rect=(0, 0, 1, 0.95))
    fig.savefig(os.path.join(common.FIG, "fig1b_ai_talk_by_company.png"), dpi=170)
    plt.close(fig)


def fig_heatmap(cu):
    piv = cu.pivot_table(index="company", columns="q", values="share")
    comp = cu.pivot_table(index="company", columns="q", values="comparable", aggfunc="first")
    order = list(cu[cu.q >= launch_x()].groupby("company").share.mean().sort_values(ascending=False).index)
    piv, comp = piv.reindex(order), comp.reindex(order)
    cols = list(piv.columns)
    fig, ax = plt.subplots(figsize=(16, 5.6))
    cmap = plt.get_cmap("YlGnBu").copy(); cmap.set_bad("#f0f0f0")
    ax.imshow(np.ma.masked_invalid(piv.values), cmap=cmap, vmin=0, vmax=45, aspect="auto")
    for i in range(piv.shape[0]):
        for j in range(piv.shape[1]):
            v = piv.values[i, j]
            if np.isnan(v):
                ax.text(j, i, "n/a", ha="center", va="center", fontsize=8, color="#aaaaaa")
            else:
                ok = comp.values[i, j] in (True, 1)
                ax.text(j, i, f"{v:.0f}" + ("" if ok else "*"), ha="center", va="center", fontsize=10,
                        color="white" if v > 24 else INK, fontweight="bold" if ok else "normal")
    ax.set_xticks(range(len(cols))); ax.set_xticklabels([qtick(q) for q in cols], rotation=45, ha="right", fontsize=9)
    ax.set_yticks(range(len(order))); ax.set_yticklabels([c.title() for c in order], fontsize=12)
    x = [k for k, q in enumerate(cols) if q >= launch_x()][0] - 0.5
    ax.axvline(x, color=LAUNCH, lw=3)
    ax.text(x + 0.1, -0.62, "ChatGPT launch  →", color=LAUNCH, fontsize=11, fontweight="bold", va="bottom")
    for sp in ax.spines.values():
        sp.set_visible(False)
    ax.set_title("Each cell = % of that company's earnings call that is about AI (darker = more AI talk)", fontsize=12, loc="left", pad=34)
    fig.suptitle("When did each company start talking about AI, and how much?", fontsize=17, fontweight="bold", x=0.02, ha="left", y=0.995)
    fig.text(0.02, 0.01, "n/a = call not in our data.   * = transcript not split into proper sentences (captions / machine audio), so compare with care.   "
             "Rows ordered by AI share since 2023.", fontsize=9, color="#555555")
    fig.tight_layout(rect=(0, 0.04, 1, 0.94))
    fig.savefig(os.path.join(common.FIG, "fig2_ai_share_heatmap.png"), dpi=170)
    plt.close(fig)


def summary(cu):
    comp = cu[cu.comparable].copy()
    comp["post"] = comp.q >= launch_x()
    rows = []
    for c in common.COMPANY_ORDER:
        d = comp[comp.company == c]
        pre, post = d[~d.post], d[d.post]
        rows.append({"company": c, "pre_calls": len(pre), "pre_mean_pct": pre.share.mean() if len(pre) else np.nan,
                     "post_calls": len(post), "post_mean_pct": post.share.mean()})
    out = pd.DataFrame(rows)
    out.to_csv(os.path.join(common.OUT, "ai_share_pre_post.csv"), index=False)
    print(out.round(2).to_string(index=False))


if __name__ == "__main__":
    for old in ("fig1_ai_talk_over_time.png",):
        p = os.path.join(common.FIG, old)
        if os.path.exists(p):
            os.remove(p)
    cu = load()
    fig_headline(cu)
    fig_by_company(cu)
    fig_heatmap(cu)
    summary(cu)
    print("figures written to", common.FIG)
