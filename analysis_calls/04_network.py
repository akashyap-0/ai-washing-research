"""Graphs 3-4: which AI topics does each company talk about, and how did the topics change?

fig3_company_topic_map.png      companies (left) linked to AI topics (right), three periods side by side.
                                A link = the topic is at least 4% of that company's AI sentences (and 3+ sentences);
                                link width = that share. Same positions in every panel so changes are visible.
fig4a_topic_storyline.png       five lines: how the main AI concepts rise and fall.
fig4b_topic_heatmap.png         every topic by quarter, numbers in the cells.
Also writes out/topic_first_appearance.csv. 06_obsidian_vault.py reuses TOPICS, PERIODS, load, period_graph.

Caveats: counts are per AI sentence. Caption segments and Whisper lines are not sentences, so Amazon (Whisper)
and a few Apple/Tesla calls inflate or deflate per-unit counts. 17 early calls are missing. Topics come from the
hand-written dictionary below.
"""
import os
import re
import sys
from importlib import import_module

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pandas as pd
from matplotlib.patches import PathPatch
from matplotlib.path import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common

COLORS = import_module("01_timeseries").COLORS
INK, GRID, LAUNCH = "#222222", "#e6e6e6", "#B22222"

# (label, kind, regex). kind: concept = generic AI idea, product = named model/product/chip/stack.
TOPICS = [
    ("generative AI", "concept", r"generative|gen[- ]?AI|genai"),
    ("AI agents", "concept", r"agentic|AI agents?|\bagents\b"),
    ("LLMs / foundation models", "concept", r"large language model|\bLLMs?\b|language models?|foundation models?|frontier models?"),
    ("machine learning", "concept", r"machine learning|deep learning|neural net"),
    ("AGI / superintelligence", "concept", r"\bAGI\b|superintelligence|general intelligence"),
    ("training & inference compute", "concept", r"\binference\b|AI training|training (?:and|&) inference|training clusters?|compute"),
    ("AI chatbots / assistants", "concept", r"chatbots?|AI assistants?|virtual assistants?"),
    ("Copilot", "product", r"copilot"),
    ("Gemini", "product", r"gemini"),
    ("OpenAI / ChatGPT", "product", r"open ?AI|chat ?GPT|\bGPT[- ]?\d"),
    ("Llama / Meta AI", "product", r"llama|meta AI"),
    ("Apple Intelligence / Siri", "product", r"apple intelligence|siri"),
    ("AWS AI stack (Bedrock, Trainium, Nova...)", "product", r"bedrock|trainium|inferentia|sagemaker|\bnova\b|amazon q\b|alexa"),
    ("NVIDIA stack (Blackwell, Hopper, CUDA...)", "product", r"blackwell|hopper|\bH100|\bH200|\bCUDA|nvlink|\bGPUs?\b|\bRubin"),
    ("Tesla autonomy (FSD, Optimus, robotaxi...)", "product", r"\bFSD\b|full self[- ]driving|optimus|robotaxi|\bdojo\b|cybercab|autopilot"),
    ("xAI / Grok", "product", r"\bxAI\b|grok"),
    ("Anthropic / Claude", "product", r"anthropic|\bclaude\b"),
    ("DeepSeek", "product", r"deepseek"),
    ("Google AI Overviews / AI Mode", "product", r"AI overviews?|AI mode\b"),
]
SHORT = {  # readable one-line labels for the figures
    "training & inference compute": "Training & inference compute",
    "AWS AI stack (Bedrock, Trainium, Nova...)": "AWS AI (Bedrock, Trainium, Nova)",
    "NVIDIA stack (Blackwell, Hopper, CUDA...)": "NVIDIA (Blackwell, Hopper, CUDA)",
    "Tesla autonomy (FSD, Optimus, robotaxi...)": "Tesla (FSD, Optimus, robotaxi)",
    "Google AI Overviews / AI Mode": "Google AI Overviews / Mode",
    "machine learning": "Machine learning", "generative AI": "Generative AI",
    "AI chatbots / assistants": "Chatbots / assistants",
}
PERIODS = [("Before ChatGPT\n(calls 2021 Q4 - 2022 Q3)", (2021, 4), (2022, 3)),
           ("2023", (2023, 1), (2023, 4)),
           ("2024 - 2026 Q2", (2024, 1), (2026, 2))]
plt.rcParams.update({"font.family": "DejaVu Sans", "axes.spines.top": False, "axes.spines.right": False})


def short(label):
    return SHORT.get(label, label)


def qtick(q):
    return f"{int(q)} Q{int(round((q % 1) * 4)) + 1}"


def load():
    s = pd.read_csv(os.path.join(common.CANON, "earnings_call_sentences.csv"),
                    usecols=["sentence_id", "company", "calendar_year", "calendar_quarter", "section", "text_verbatim"])
    s["q"] = [common.qkey(y, q) for y, q in zip(s.calendar_year, s.calendar_quarter)]
    for label, _, rx in TOPICS:
        s[label] = s.text_verbatim.str.contains(rx, flags=re.IGNORECASE, regex=True)
    return s


def period_graph(s, lo, hi, min_edge=3):
    """Company-topic graph with raw sentence counts (used by the Obsidian vault builder)."""
    d = s[(s.q >= common.qkey(*lo)) & (s.q <= common.qkey(*hi))]
    G = nx.Graph()
    for c in common.COMPANY_ORDER:
        n = int((d.company == c).sum())
        if n:
            G.add_node(c, kind="company", size=n)
    for label, kind, _ in TOPICS:
        for c in common.COMPANY_ORDER:
            w = int(d.loc[d.company == c, label].sum())
            if w >= min_edge:
                G.add_node(label, kind=kind, size=0)
                G.add_edge(c, label, weight=w)
    for label, kind, _ in TOPICS:
        if label in G:
            G.nodes[label]["size"] = sum(G[label][c]["weight"] for c in G[label])
    G.remove_nodes_from([n for n in list(G) if G.degree(n) == 0])
    return G, len(d)


def first_appearance(s):
    rows = []
    for label, kind, _ in TOPICS:
        d = s[s[label]]
        if d.empty:
            continue
        by_q = d.groupby("q").size()
        qual = by_q[by_q >= 3]
        fq = qual.index.min() if len(qual) else by_q.index.min()
        first_co = d[d.q == fq].company.value_counts()
        row = {"topic": label, "kind": kind, "first_quarter_with_3plus_mentions": f"{int(fq)}Q{int(round((fq % 1) * 4)) + 1}",
               "companies_that_quarter": "; ".join(f"{c}:{n}" for c, n in first_co.items()), "total_mentions": len(d)}
        for c in common.COMPANY_ORDER:
            row[c] = int((d.company == c).sum())
        rows.append(row)
    out = pd.DataFrame(rows).sort_values("first_quarter_with_3plus_mentions")
    out.to_csv(os.path.join(common.OUT, "topic_first_appearance.csv"), index=False)
    return out


# ---------------------------------------------------------------- fig3
def curve(ax, p0, p1, color, lw, alpha, z=1):
    (x0, y0), (x1, y1) = p0, p1
    xm = (x0 + x1) / 2
    path = Path([(x0, y0), (xm, y0), (xm, y1), (x1, y1)], [Path.MOVETO, Path.CURVE4, Path.CURVE4, Path.CURVE4])
    ax.add_patch(PathPatch(path, facecolor="none", edgecolor=color, lw=lw, alpha=alpha, zorder=z, capstyle="round"))


def fig_company_topic_map(s, min_share=0.04, min_count=3):
    concepts = [t for t in TOPICS if t[1] == "concept"]
    products = [t for t in TOPICS if t[1] == "product"]
    topic_order = [t[0] for t in concepts] + [None] + [t[0] for t in products]  # None = gap between groups
    comp_order = ["microsoft", "alphabet", "meta", "amazon", "apple", "nvidia", "tesla"]
    kind_of = {a: b for a, b, _ in TOPICS}
    n_rows = len(topic_order)
    ty = {t: -i for i, t in enumerate(topic_order) if t}
    top, bot = 0.0, -(n_rows - 1)
    cy = {c: top + (bot - top) * (i + 0.5) / len(comp_order) for i, c in enumerate(comp_order)}

    fig, axes = plt.subplots(1, 3, figsize=(25, 11.5))
    for ax, (title, lo, hi) in zip(axes, PERIODS):
        d = s[(s.q >= common.qkey(*lo)) & (s.q <= common.qkey(*hi))]
        ncomp = d.groupby("company").size()
        for t, y in ty.items():
            cnt = int(d[t].sum())
            prod = kind_of[t] == "product"
            ax.scatter([1.0], [y], s=60, marker="s" if prod else "o", color="#E8A33D" if prod else "#8a8a8a", zorder=4)
            ax.text(1.04, y, short(t), va="center", fontsize=11, color=INK if cnt else "#bbbbbb")
        ax.text(1.04, ty["generative AI"] + 0.95, "AI CONCEPTS", fontsize=9, color="#777777", fontweight="bold")
        ax.text(1.04, ty["Copilot"] + 0.95, "NAMED PRODUCTS / STACKS", fontsize=9, color="#E8A33D", fontweight="bold")
        links = []
        for c in comp_order:
            n = int(ncomp.get(c, 0))
            if not n:
                continue
            for t in ty:
                k = int(d.loc[d.company == c, t].sum())
                if k >= min_count and k / n >= min_share:
                    links.append((k / n, c, t, k))
        for share, c, t, k in sorted(links):  # thick first so thin links stay visible
            curve(ax, (0.0, cy[c]), (1.0, ty[t]), COLORS[c], lw=1.0 + share * 38, alpha=0.62)
        top_topic = {}
        for share, c, t, k in sorted(links):
            top_topic[c] = (short(t).split(" (")[0], share)
        for c in comp_order:
            n = int(ncomp.get(c, 0))
            has = n > 0
            ax.scatter([0.0], [cy[c]], s=(200 + 12 * np.sqrt(n)) if has else 140, color=COLORS[c] if has else "#e0e0e0",
                       edgecolors="white", linewidths=1.5, zorder=4)
            ax.text(-0.11, cy[c] + 0.30, c.title(), ha="right", va="center", fontsize=13, fontweight="bold", color=COLORS[c] if has else "#bbbbbb")
            ax.text(-0.11, cy[c] - 0.12, f"{n:,} AI sentences" if has else "no calls in data", ha="right", va="center",
                    fontsize=9, color="#666666" if has else "#bbbbbb")
            if c in top_topic:
                ax.text(-0.11, cy[c] - 0.50, f"top: {top_topic[c][0]} ({top_topic[c][1] * 100:.0f}%)", ha="right", va="center",
                        fontsize=9, color=COLORS[c], fontweight="bold")
        ax.set_title(f"{title}\n{len(d):,} AI sentences in {d.company.nunique()} companies' calls", fontsize=14, fontweight="bold", loc="left")
        ax.set_xlim(-0.95, 1.85); ax.set_ylim(bot - 0.9, top + 1.2); ax.axis("off")
    fig.suptitle("Which AI topics does each company talk about?", fontsize=22, fontweight="bold", x=0.02, ha="left", y=0.995)
    fig.text(0.02, 0.945, "A line means the topic makes up at least 4% of that company's AI talk in the period. Thicker line = bigger share "
             "(each company's biggest topic and its share is written under its name). Positions are identical in the three panels, so you can watch links appear.",
             fontsize=11.5, color="#444444")
    fig.text(0.02, 0.012, "Counts are AI sentences from the canonical earnings-call dataset; a sentence can mention several topics. "
             f"Amazon and some Apple/Tesla calls use caption or machine-audio units, not sentences; {common.missing_note()}.",
             fontsize=9, color="#555555")
    fig.tight_layout(rect=(0, 0.03, 1, 0.93))
    fig.savefig(os.path.join(common.FIG, "fig3_company_topic_map.png"), dpi=140)
    plt.close(fig)


# ---------------------------------------------------------------- fig4
def shares_by_quarter(s):
    ai = s.groupby("q").size()
    mat = pd.DataFrame({lab: s[s[lab]].groupby("q").size() for lab, _, _ in TOPICS}).fillna(0)
    return (mat.div(ai, axis=0) * 100).reindex(ai.index), ai


def fig_storyline(s):
    mat, ai = shares_by_quarter(s)
    lines = [("machine learning", "#7F7F7F", "Machine learning"), ("generative AI", "#D55E00", "Generative AI"),
             ("LLMs / foundation models", "#0072B2", "LLMs / foundation models"), ("AI agents", "#009E73", "AI agents"),
             ("training & inference compute", "#CC79A7", "Training & inference compute")]
    fig, ax = plt.subplots(figsize=(13, 6.2))
    lx = common.qkey(*common.FIRST_POST_QUARTER) - 0.125
    ax.axvspan(lx, mat.index.max() + 0.3, color="#fdecea", zorder=0)
    ax.axvline(lx, color=LAUNCH, lw=2)
    ax.text(lx - 0.05, 0.97, "ChatGPT\nlaunches", color=LAUNCH, ha="right", va="top", fontsize=11, fontweight="bold",
            transform=ax.get_xaxis_transform())
    ys = []
    for lab, color, name in lines:
        ax.plot(mat.index, mat[lab], color=color, lw=3.2, marker="o", ms=5)
        ys.append((mat[lab].iloc[-3:].mean(), name, color))
    ys.sort()
    last = mat.index.max()
    placed = []
    for y, name, color in ys:  # de-overlap the direct labels
        yy = max(y, placed[-1] + 1.4) if placed else y
        placed.append(yy)
        ax.text(last + 0.12, yy, name, color=color, fontsize=12, fontweight="bold", va="center")
    qs = list(mat.index)
    ax.set_xticks(qs[::2]); ax.set_xticklabels([qtick(q) for q in qs[::2]], fontsize=10)
    ax.set_xlim(min(qs) - 0.2, last + 2.2); ax.set_ylim(0, None)
    ax.grid(axis="y", color=GRID)
    ax.set_ylabel("% of that quarter's AI sentences that mention the topic", fontsize=11)
    fig.suptitle("What 'AI' means on earnings calls keeps changing: ML, then generative AI, then agents",
                 fontsize=17, fontweight="bold", x=0.04, ha="left", y=0.985)
    ax.set_title("All seven companies pooled. " + ("Before the launch only some firms' calls are in our data, so early quarters are noisier."
                 if "missing" in common.missing_note() else "Every firm's calls are included in every quarter."),
                 fontsize=10.5, loc="left", color="#444444")
    fig.tight_layout(rect=(0, 0, 1, 0.94))
    fig.savefig(os.path.join(common.FIG, "fig4a_topic_storyline.png"), dpi=170)
    plt.close(fig)


def fig_topic_heatmap(s):
    mat, ai = shares_by_quarter(s)
    fa = first_appearance(s).set_index("topic")
    kind = {l: k for l, k, _ in TOPICS}
    groups = []
    for k, name in (("concept", "AI CONCEPTS"), ("product", "NAMED PRODUCTS / STACKS")):
        labs = sorted([l for l in mat.columns if kind[l] == k],
                      key=lambda l: (fa.loc[l, "first_quarter_with_3plus_mentions"], -fa.loc[l, "total_mentions"]))
        groups.append((name, labs))
    rows = [l for _, labs in groups for l in labs]
    M = mat[rows].T
    fig, ax = plt.subplots(figsize=(16, 9))
    ax.imshow(M.values, aspect="auto", cmap="Blues", vmin=0, vmax=12)
    for i in range(M.shape[0]):
        for j in range(M.shape[1]):
            v = M.values[i, j]
            if v >= 1:
                ax.text(j, i, f"{v:.0f}", ha="center", va="center", fontsize=8.5, color="white" if v > 6 else INK)
    ax.set_yticks(range(len(rows))); ax.set_yticklabels([short(r) for r in rows], fontsize=11)
    qs = list(M.columns)
    ax.set_xticks(range(len(qs))); ax.set_xticklabels([qtick(q) for q in qs], rotation=45, ha="right", fontsize=9)
    x = [k for k, q in enumerate(qs) if q >= common.qkey(*common.FIRST_POST_QUARTER) - 0.125][0] - 0.5
    ax.axvline(x, color=LAUNCH, lw=3)
    ax.text(x + 0.1, -1.0, "ChatGPT launch  →", color=LAUNCH, fontsize=11, fontweight="bold")
    ax.axhline(len(groups[0][1]) - 0.5, color="white", lw=6)
    for sp in ax.spines.values():
        sp.set_visible(False)
    ax.set_title("Each cell = % of that quarter's AI sentences that mention the topic (blank = under 1%). Darker = more.",
                 fontsize=12, loc="left", pad=26)
    fig.suptitle("The topic map of AI talk, quarter by quarter", fontsize=18, fontweight="bold", x=0.02, ha="left", y=0.995)
    fig.text(0.02, 0.012, "Concepts on top, named products below; rows ordered by when the topic first appears. A sentence can mention several "
             "topics, so rows are independent (columns do not sum to 100%).", fontsize=9, color="#555555")
    fig.tight_layout(rect=(0, 0.03, 1, 0.95))
    fig.savefig(os.path.join(common.FIG, "fig4b_topic_heatmap.png"), dpi=170)
    plt.close(fig)


if __name__ == "__main__":
    for old in ("fig3_ai_knowledge_graph.png", "fig4_topic_diffusion_heatmap.png"):
        p = os.path.join(common.FIG, old)
        if os.path.exists(p):
            os.remove(p)
    s = load()
    fig_company_topic_map(s)
    fig_storyline(s)
    fig_topic_heatmap(s)
    print("done")
