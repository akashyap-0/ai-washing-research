"""Figs 10-11: does earnings-call talk line up with AI releases (models, products, chips, agents)?

Fig 10: for 15 named models/products, mentions per 1,000 call sentences by quarter with their release dates marked
        (searches ALL call sentences, not only the AI-filtered ones, so chip names like Blackwell are counted).
Fig 11: vocabulary-wide scan. For every word/bigram in AI sentences, correlate its quarter-to-quarter change in share with
        the number of releases of each type whose launch falls just before that quarter's calls. A permutation test over all
        words tells us whether any word beats chance.
Release dates: V = checked by web search in this session, M = from the analyst's memory (not verified). Descriptive only;
the release list was assembled after seeing the data, which biases the test toward finding alignments.
"""
import datetime as dt
import glob
import importlib.util
import math
import os
import re
import sys
from importlib import import_module

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.stats import spearmanr
from sklearn.feature_extraction.text import CountVectorizer, ENGLISH_STOP_WORDS

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common

D = dt.date
CATS = {"model": ("Model release", "#0072B2"), "product": ("Product / platform", "#E69F00"),
        "chip": ("Chip", "#009E73"), "agent": ("Agent", "#D55E00")}
# (name, date, category, verified)
EVENTS = [
    ("ChatGPT", D(2022, 11, 30), "product", True), ("Bard / Bing Chat", D(2023, 2, 6), "product", False),
    ("Llama 1", D(2023, 2, 24), "model", True), ("GPT-4", D(2023, 3, 14), "model", True),
    ("Microsoft 365 Copilot", D(2023, 3, 16), "product", False), ("Claude 2", D(2023, 7, 11), "model", True),
    ("Llama 2", D(2023, 7, 18), "model", False), ("Gemini 1.0", D(2023, 12, 6), "model", True),
    ("Claude 3", D(2024, 3, 4), "model", False), ("Nvidia Blackwell", D(2024, 3, 18), "chip", False),
    ("Llama 3", D(2024, 4, 18), "model", False), ("GPT-4o", D(2024, 5, 13), "model", True),
    ("Apple Intelligence", D(2024, 6, 10), "product", True), ("Claude 3.5 Sonnet", D(2024, 6, 20), "model", False),
    ("Llama 3.1", D(2024, 7, 23), "model", False), ("OpenAI o1-preview", D(2024, 9, 12), "model", False),
    ("MCP", D(2024, 11, 25), "agent", True), ("DeepSeek V3", D(2024, 12, 26), "model", False),
    ("DeepSeek R1", D(2025, 1, 20), "model", True), ("OpenAI Operator", D(2025, 1, 23), "agent", True),
    ("o3-mini", D(2025, 1, 31), "model", True), ("GPT-4.5", D(2025, 2, 27), "model", False),
    ("Alexa+", D(2025, 2, 26), "product", False), ("Gemini 2.5 Pro", D(2025, 3, 25), "model", False),
    ("Llama 4", D(2025, 4, 5), "model", True), ("o3 / o4-mini", D(2025, 4, 16), "model", True),
    ("Claude 4", D(2025, 5, 22), "model", True), ("Claude Code GA", D(2025, 5, 22), "agent", True),
    ("GPT-5", D(2025, 8, 7), "model", True), ("Claude Sonnet 4.5", D(2025, 9, 29), "model", True),
    ("OpenClaw (as Warelay)", D(2025, 11, 24), "agent", True), ("Gemini 3", D(2025, 11, 18), "model", True),
    ("Claude Cowork", D(2026, 1, 12), "agent", True), ("Hermes Agent", D(2026, 2, 25), "agent", True),
    ("GPT-5.5", D(2026, 4, 23), "model", True),
]
# (panel title, regex, [(label, date, verified)])
FAMILIES = [
    ("ChatGPT", r"chat ?GPT", [("ChatGPT", D(2022, 11, 30), True)]),
    ("GPT-4 / GPT-4o", r"GPT[- ]?4", [("GPT-4", D(2023, 3, 14), True), ("GPT-4o", D(2024, 5, 13), True)]),
    ("GPT-5", r"GPT[- ]?5", [("GPT-5", D(2025, 8, 7), True), ("GPT-5.5", D(2026, 4, 23), True)]),
    ("Reasoning models (o1/o3)", r"\bo1\b|\bo3\b|reasoning model", [("o1*", D(2024, 9, 12), False), ("o3", D(2025, 4, 16), True)]),
    ("Llama", r"llama", [("L1", D(2023, 2, 24), True), ("L2*", D(2023, 7, 18), False), ("L3*", D(2024, 4, 18), False), ("L4", D(2025, 4, 5), True)]),
    ("Gemini", r"gemini", [("Gemini 1", D(2023, 12, 6), True), ("Gemini 3", D(2025, 11, 18), True)]),
    ("Bard", r"\bbard\b", [("Bard*", D(2023, 2, 6), False)]),
    ("Claude / Anthropic", r"claude|anthropic", [("Claude 3*", D(2024, 3, 4), False), ("Claude 4", D(2025, 5, 22), True)]),
    ("DeepSeek", r"deepseek", [("R1", D(2025, 1, 20), True)]),
    ("Copilot", r"copilot", [("M365 Copilot*", D(2023, 3, 16), False)]),
    ("Blackwell", r"blackwell", [("Blackwell*", D(2024, 3, 18), False)]),
    ("Rubin", r"\brubin\b", [("Vera Rubin*", D(2025, 3, 18), False)]),
    ("Apple Intelligence", r"apple intelligence", [("announced", D(2024, 6, 10), True), ("launch*", D(2024, 10, 28), False)]),
    ("Alexa", r"\balexa\b", [("Alexa+*", D(2025, 2, 26), False)]),
    ("Grok / xAI", r"\bgrok\b|\bxAI\b", []),
]
EXTRA_STOP = set("""thank thanks think know going want look like just really kind lot sort said say says question questions quarter quarters
year years time ll ve don didn doesn isn re let make get got way see also well yes yeah okay one two three first second new much
million billion percent next said call""".split())
COMPANY_WORDS = set("""alphabet google youtube meta facebook instagram whatsapp microsoft azure amazon aws apple nvidia tesla amazon.com
satya nadella sundar pichai mark zuckerberg jensen huang elon musk tim cook andy jassy susan li amy hood colette kress""".split())
plt.rcParams.update({"font.family": "DejaVu Sans", "axes.spines.top": False, "axes.spines.right": False})


def x_of(date):
    d = date - dt.timedelta(days=35)  # calls are held ~35 days after the quarter they report
    return d.year + (d.timetuple().tm_yday - 1) / 365.0 - 0.25


def q_attr(date):
    """Quarter key whose calls are the first to follow this date."""
    return math.ceil(round(x_of(date) * 4, 6)) / 4.0


def qlab(q):
    return f"{int(q)}Q{int(round((q % 1) * 4)) + 1}"


# ---------------------------------------------------------------- data
def all_sentences():
    spec = importlib.util.spec_from_file_location("fap", os.path.join(common.ROOT, "earnings_calls", "filter_ai_passages.py"))
    fap = importlib.util.module_from_spec(spec); spec.loader.exec_module(fap)
    calls_dir = os.environ.get("CALLS_DIR", os.path.join(common.ROOT, "earnings_calls"))
    rows = []
    for path in sorted(glob.glob(os.path.join(calls_dir, "*", "*.md"))):
        company = os.path.basename(os.path.dirname(path))
        period = os.path.basename(path)[len(company) + 1:-3]
        _, _, _, _, sents = fap.process(path)
        y, q = fap.cal_quarter(company, period)
        rows += [(company, common.qkey(y, q), t) for t, _, _ in sents]
    return pd.DataFrame(rows, columns=["company", "q", "text"])


# ---------------------------------------------------------------- fig 10
def fig_models(allS):
    tot = allS.groupby("q").size()
    qs = list(tot.index)
    fig, axes = plt.subplots(4, 4, figsize=(21, 14.5), sharex=True)
    rows = []
    for ax, (title, rx, rels) in zip(axes.flat, FAMILIES):
        hit = allS[allS.text.str.contains(rx, case=False, regex=True)]
        cnt = hit.groupby("q").size().reindex(qs).fillna(0)
        rate = cnt / tot * 1000
        ax.bar(qs, rate.values, width=0.2, color="#56B4E9", alpha=0.8, zorder=2)
        first = next((q for q in qs if cnt.loc[q] >= 3), None)
        for lbl, d, ver in rels:
            x = x_of(d)
            ax.axvline(x, color="#B22222" if ver else "#999999", lw=2, ls="--", zorder=3)
            ax.text(x, ax.get_ylim()[1] * 0.0 + rate.max() * 1.0 if rate.max() > 0 else 1, lbl, rotation=90, fontsize=8.5,
                    color="#B22222" if ver else "#777777", va="top", ha="right")
            qa = q_attr(d)
            rows.append({"family": title, "release": lbl, "release_date": d, "verified": ver, "release_quarter_calls": qlab(qa),
                         "first_quarter_3plus_mentions": qlab(first) if first else "", "lag_quarters": (first - qa) * 4 if first else np.nan,
                         "total_mentions": int(cnt.sum())})
        ax.set_title(title, fontsize=12.5, fontweight="bold", loc="left")
        note = f"first 3+ mentions: {qlab(first)}" if first else "rarely mentioned"
        ax.text(0.02, 0.95, note, transform=ax.transAxes, fontsize=9.5, va="top", color="#333333")
        ax.grid(axis="y", color="#eeeeee"); ax.set_xticks(qs[::4]); ax.set_xticklabels([qlab(q) for q in qs[::4]], fontsize=8.5, rotation=45)
    for ax in axes.flat[len(FAMILIES):]:
        ax.axis("off")
    last = axes.flat[len(FAMILIES)]
    last.text(0.0, 0.95, "How to read", fontsize=13, fontweight="bold", va="top")
    last.text(0.0, 0.82, "Bars = sentences mentioning the model or\nproduct, per 1,000 call sentences, by quarter.\n"
              "Red dashed line = release (verified via web search).\nGrey dashed = date from memory (*), unverified.\n\n"
              "Calls are held ~5 weeks after a quarter ends, so a\nrelease just before a quarter's calls shows up in\nthat quarter's bar.", fontsize=10.5, va="top", color="#333333")
    fig.suptitle("Do earnings calls start talking about a model right after it is released?", fontsize=20, fontweight="bold", x=0.02, ha="left", y=0.995)
    fig.supylabel("mentions per 1,000 call sentences", fontsize=11)
    fig.tight_layout(rect=(0.01, 0, 1, 0.965))
    fig.savefig(os.path.join(common.FIG, "fig10_model_mentions_vs_releases.png"), dpi=150)
    plt.close(fig)
    out = pd.DataFrame(rows)
    out.to_csv(os.path.join(common.OUT, "model_first_mention_vs_release.csv"), index=False)
    return out


# ---------------------------------------------------------------- fig 11
def load_ai():
    s = pd.read_csv(os.path.join(common.CANON, "earnings_call_sentences.csv"), usecols=["calendar_year", "calendar_quarter", "text_verbatim"])
    s["q"] = [common.qkey(y, q) for y, q in zip(s.calendar_year, s.calendar_quarter)]
    return s[s.q >= common.qkey(2022, 4)].reset_index(drop=True)


def alignment(ai):
    stops = list(ENGLISH_STOP_WORDS | EXTRA_STOP | COMPANY_WORDS)
    cv = CountVectorizer(binary=True, ngram_range=(1, 2), min_df=40, stop_words=stops, token_pattern=r"(?u)\b[a-zA-Z][a-zA-Z\-]{2,}\b")
    X = cv.fit_transform(ai.text_verbatim); words = np.array(cv.get_feature_names_out())
    qs = sorted(ai.q.unique())
    M = np.vstack([np.asarray(X[(ai.q == q).values].mean(axis=0)).ravel() * 100 for q in qs])
    dM = np.diff(M, axis=0); trans = qs[1:]
    totdocs = np.asarray(X.sum(axis=0)).ravel()
    loads = {"any release": lambda e: True, "model release": lambda e: e[2] == "model", "product / chip launch": lambda e: e[2] in ("product", "chip"),
             "agent launch": lambda e: e[2] == "agent"}
    qa_list = [q_attr(e[1]) for e in EVENTS]
    rng = np.random.default_rng(0)
    res = {}
    def rank_corr(A, b):
        from scipy.stats import rankdata
        Ar = np.apply_along_axis(rankdata, 0, A); br = rankdata(b)
        Ar = (Ar - Ar.mean(0)) / (Ar.std(0) + 1e-12); br = (br - br.mean()) / (br.std() + 1e-12)
        return (Ar * br[:, None]).mean(0)
    for name, sel in loads.items():
        L = np.array([sum(1 for e, qa in zip(EVENTS, qa_list) if sel(e) and abs(qa - q) < 1e-6) for q in trans], float)
        if L.std() == 0:
            continue
        r = rank_corr(dM, L)
        null = np.array([rank_corr(dM, rng.permutation(L)).max() for _ in range(1000)])
        thr = float(np.percentile(null, 95))
        order = np.argsort(-r)
        keep = [i for i in order if totdocs[i] >= 60][:6]
        res[name] = {"load": L, "thr": thr, "rows": [(words[i], float(r[i]), float((null >= r[i]).mean()), i) for i in keep]}
    return res, M, words, qs, trans


def fig_alignment(res, M, words, qs):
    groups = list(res.keys())
    n = sum(len(res[g]["rows"]) for g in groups)
    fig = plt.figure(figsize=(17, 13.5))
    gs = fig.add_gridspec(2, 1, height_ratios=[1, 5.2], hspace=0.06)
    ax0 = fig.add_subplot(gs[0]); ax = fig.add_subplot(gs[1], sharex=ax0)
    q0 = qs[0]
    col = lambda x: (x - q0) / 0.25
    # event strip
    levels = [0.95, 0.83, 0.71, 0.59, 0.47, 0.35, 0.23, 0.11]
    for i, (name, d, cat, ver) in enumerate(sorted(EVENTS, key=lambda e: e[1])):
        c = CATS[cat][1]; x = col(x_of(d))
        if x < -0.5:
            continue
        y = levels[i % 8]
        ax0.plot([x, x], [0, y], color=c, lw=1.4); ax0.scatter([x], [0], color=c, s=28, zorder=3)
        ax0.text(x + 0.05, y, name + ("" if ver else "*"), fontsize=7.6, color=c, va="center", fontweight="bold" if ver else "normal")
    ax0.set_ylim(-0.05, 1.05); ax0.set_yticks([]); ax0.spines["left"].set_visible(False); ax0.spines["bottom"].set_visible(False)
    ax0.tick_params(axis="x", labelbottom=False)
    from matplotlib.lines import Line2D
    ax0.legend(handles=[Line2D([], [], color=c, marker="o", ls="", label=l) for _, (l, c) in CATS.items()], loc="upper left", ncol=4, fontsize=9, frameon=False)
    # heatmap
    rows, labels, ypos, brk = [], [], [], []
    y = 0
    for g in groups:
        brk.append((y, g))
        for w, r, p, i in res[g]["rows"]:
            v = M[:, i]; z = (v - v.mean()) / (v.std() + 1e-12)
            rows.append(z); labels.append(f"{w}"); ypos.append((y, r, p)); y += 1
        y += 0.8
    for (yy, r, p), z in zip(ypos, rows):
        ax.imshow(z[None, :], extent=(-0.5, len(qs) - 0.5, yy + 0.45, yy - 0.45), aspect="auto", cmap="Blues", vmin=-1.6, vmax=2.6, origin="upper", interpolation="nearest")
        ax.text(len(qs) - 0.3, yy, f"r = {r:+.2f}   p = {p:.2f}", fontsize=9.5, va="center", color="#333333")
    ax.set_yticks([yy for yy, _, _ in ypos]); ax.set_yticklabels(labels, fontsize=10.5)
    for yy, g in brk:
        ax.text(-0.5, yy - 0.75, f"words that jump with: {g.upper()}  (n releases = {int(res[g]['load'].sum())})", fontsize=10.5, fontweight="bold", color="#222222", va="bottom")
    ax.set_ylim(y - 0.2, -1.3); ax.set_xlim(-0.5, len(qs) + 2.8)
    ax.set_xticks(range(0, len(qs), 2)); ax.set_xticklabels([qlab(q) for q in qs[::2]], fontsize=9.5, rotation=45)
    for sp in ("left",):
        ax.spines[sp].set_visible(False)
    ax.set_xlabel("Calendar quarter reported", fontsize=10)
    min_p = min(row[2] for g in groups for row in res[g]["rows"])
    fig.suptitle(f"Do any words jump when AI products are released?  Not reliably (best p = {min_p:.2f})", fontsize=19, fontweight="bold", x=0.02, ha="left", y=0.985)
    fig.text(0.02, 0.945, "Top timeline: releases placed on the call timeline (* = date from memory, unverified). Rows: the 6 best-matching words per release type, share of AI sentences containing the word, standardized "
             "per word (darker = higher). A real link would show p below 0.05. r = Spearman correlation of the word's quarter-to-quarter CHANGE with the number of releases of that type just before the calls.",
             fontsize=9.5, color="#444444", wrap=True)
    thr_txt = "; ".join(f"{g}: {res[g]['thr']:.2f}" for g in groups)
    fig.text(0.02, 0.012, f"p = chance that the best of ALL ~{len(words)} words would do this well on shuffled release timing (smaller = less likely luck). "
             f"95% permutation thresholds for r - {thr_txt}.  14 quarter-to-quarter changes only; the release list was assembled after seeing the data.",
             fontsize=8.8, color="#555555", wrap=True)
    fig.subplots_adjust(left=0.13, right=0.97, top=0.9, bottom=0.07)
    fig.savefig(os.path.join(common.FIG, "fig11_words_that_jump_with_releases.png"), dpi=160)
    plt.close(fig)


if __name__ == "__main__":
    allS = all_sentences()
    print("all call sentences:", len(allS))
    t = fig_models(allS)
    print(t[["family", "release", "verified", "release_quarter_calls", "first_quarter_3plus_mentions", "lag_quarters", "total_mentions"]].to_string(index=False))
    ai = load_ai()
    res, M, words, qs, trans = alignment(ai)
    for g, d in res.items():
        print(f"\n[{g}] 95% perm threshold r={d['thr']:.2f}; loads per transition: {d['load'].astype(int).tolist()}")
        for w, r, p, i in d["rows"]:
            print(f"   {w:28s} r={r:+.2f}  p(max)={p:.3f}")
    fig_alignment(res, M, words, qs)
