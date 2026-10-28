"""Figs 8-9: (8) agent talk vs a timeline of agent launches; (9) which other words move with agent talk.

Fig 8: % of AI sentences mentioning agents per quarter, with ~13 agent launches placed on the call timeline.
       Dates marked * are from the analyst's memory, not verified in this session; the rest were checked via web search.
Fig 9: for every word/bigram in AI sentences that do NOT mention agents (so same-sentence co-occurrence cannot create the
       correlation), correlate its quarterly share with the agent share. Levels share a trend with almost everything, so we
       also report correlation of quarter-to-quarter changes and a permutation test of the strongest correlation.
Small sample: 14 quarters. Descriptive only.
"""
import datetime as dt
import os
import re
import sys
from importlib import import_module

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer, ENGLISH_STOP_WORDS

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common

COLORS = import_module("01_timeseries").COLORS
AGENT_RX = r"agentic|AI agents?|\bagents\b"
START = common.qkey(2023, 1)  # all seven firms present from here on, same sentence-based units except Amazon/caption calls
# (label, date, verified?)
LAUNCHES = [("Devin (Cognition)*", dt.date(2024, 3, 12), False), ("Agentforce GA*", dt.date(2024, 10, 25), False),
            ("MCP announced", dt.date(2024, 11, 25), True), ("Project Mariner*", dt.date(2024, 12, 11), False),
            ("OpenAI Operator", dt.date(2025, 1, 23), True), ("Claude Code preview", dt.date(2025, 2, 24), True),
            ("Manus", dt.date(2025, 3, 6), True), ("OpenAI Codex agent*", dt.date(2025, 5, 16), False),
            ("Claude Code GA", dt.date(2025, 5, 22), True), ("ChatGPT agent*", dt.date(2025, 7, 17), False),
            ("OpenClaw (as Warelay)", dt.date(2025, 11, 24), True), ("Claude Cowork", dt.date(2026, 1, 12), True),
            ("OpenClaw renamed (late Jan)", dt.date(2026, 1, 28), True), ("Hermes Agent", dt.date(2026, 2, 25), True)]
EXTRA_STOP = set("""thank thanks think know going want look like just really kind lot sort said say says question questions quarter quarters
year years time ll ve don didn doesn isn re let make get got way see also well yes yeah okay one two three first second new much
million billion percent next said call""".split())
COMPANY_WORDS = set("""alphabet google youtube meta facebook instagram whatsapp microsoft azure amazon aws apple nvidia tesla amazon.com
satya nadella sundar pichai mark zuckerberg jensen huang elon musk tim cook andy jassy susan li amy hood colette kress""".split())
plt.rcParams.update({"font.family": "DejaVu Sans", "axes.spines.top": False, "axes.spines.right": False})


def x_of(date):
    d = date - dt.timedelta(days=35)  # calls are held ~35 days after the quarter they report
    return d.year + (d.timetuple().tm_yday - 1) / 365.0 - 0.25


def load():
    s = pd.read_csv(os.path.join(common.CANON, "earnings_call_sentences.csv"),
                    usecols=["company", "calendar_year", "calendar_quarter", "text_verbatim"])
    s["q"] = [common.qkey(y, q) for y, q in zip(s.calendar_year, s.calendar_quarter)]
    s["agent"] = s.text_verbatim.str.contains(AGENT_RX, case=False, regex=True)
    return s[s.q >= START].reset_index(drop=True)


def fig_launches(s):
    tot = s.groupby("q").size()
    pct = s[s.agent].groupby("q").size().reindex(tot.index).fillna(0) / tot * 100
    fig, (ax, ax2) = plt.subplots(2, 1, figsize=(15, 10), sharex=True, gridspec_kw={"height_ratios": [1.5, 1.1], "hspace": 0.04})
    ax.plot(pct.index, pct.values, color="#009E73", lw=3.4, marker="o", ms=7, zorder=4)
    for q, v in pct.items():
        ax.text(q, v + 0.8, f"{v:.0f}%", ha="center", fontsize=9, color="#006b4f")
    ax.set_ylabel("% of AI sentences that mention agents", fontsize=11); ax.set_ylim(0, 19); ax.grid(axis="y", color="#e6e6e6")
    ax.set_title("Agent talk on earnings calls vs a timeline of agent launches", fontsize=17, fontweight="bold", loc="left", pad=14)
    levels = [0.95, 0.80, 0.65, 0.50, 0.35, 0.20, 0.08]
    for i, (name, d, verified) in enumerate(LAUNCHES):
        x = x_of(d)
        color = "#333333" if verified else "#8a8a8a"
        ax.axvline(x, color=color, lw=1.1, ls=":", alpha=0.8, zorder=1)
        y = levels[i % len(levels)]
        ax2.plot([x, x], [0, y], color=color, lw=1.2)
        ax2.scatter([x], [0], color=color, s=40, zorder=3)
        ax2.text(x + 0.012, y, name, fontsize=9.5, color=color, va="center", ha="left", fontweight="bold" if verified else "normal")
    ax2.set_ylim(-0.08, 1.05); ax2.set_yticks([]); ax2.spines["left"].set_visible(False)
    qs = list(pct.index)
    ax2.set_xticks(qs[::2]); ax2.set_xticklabels([f"{int(q)} Q{int(round((q % 1) * 4)) + 1}" for q in qs[::2]], fontsize=10)
    ax2.set_xlim(START - 0.2, qs[-1] + 0.9)
    ax2.set_xlabel("Calendar quarter reported (calls are held in the following 4 to 6 weeks)", fontsize=10)
    fig.text(0.06, 0.012, "* date from memory, not verified here; other dates checked via web search. Launches are placed on the call timeline (a launch after a quarter's calls shows up in the next "
             "quarter).\nThe list was assembled after the fact and is concentrated in 2024-25, and many launches cluster together, so timing cannot isolate any one of them.",
             fontsize=8.8, color="#555555")
    fig.tight_layout(rect=(0, 0.03, 1, 1))
    fig.savefig(os.path.join(common.FIG, "fig8_agent_launch_timeline.png"), dpi=170)
    plt.close(fig)
    # launches per quarter vs change in agent share
    xs = np.array([x_of(d) for _, d, _ in LAUNCHES])
    rows = []
    for q in qs[1:]:
        n = int(((xs > q - 0.25) & (xs <= q)).sum())
        rows.append((q, n, pct.loc[q] - pct.loc[q - 0.25]))
    t = pd.DataFrame(rows, columns=["q", "launches_before_these_calls", "change_in_agent_share_pts"])
    t.to_csv(os.path.join(common.OUT, "agent_launches_vs_change.csv"), index=False)
    from scipy.stats import spearmanr
    r, p = spearmanr(t.launches_before_these_calls, t.change_in_agent_share_pts)
    print(t.round(1).to_string(index=False)); print(f"Spearman(launches, change) = {r:.2f}, p = {p:.2f}, n = {len(t)}")
    return pct, r, p


def word_correlations(s, pct):
    non = s[~s.agent].reset_index(drop=True)
    stops = list(ENGLISH_STOP_WORDS | EXTRA_STOP | COMPANY_WORDS)
    cv = CountVectorizer(binary=True, ngram_range=(1, 2), min_df=40, stop_words=stops, token_pattern=r"(?u)\b[a-zA-Z][a-zA-Z\-]{2,}\b")
    X = cv.fit_transform(non.text_verbatim)
    words = np.array(cv.get_feature_names_out())
    qs = sorted(non.q.unique())
    M = np.vstack([np.asarray(X[(non.q == q).values].mean(axis=0)).ravel() * 100 for q in qs])  # quarters x words (% of non-agent AI sentences)
    a = pct.reindex(qs).values
    keep = (M.std(axis=0) > 0) & ~np.array([any(t in ("agent", "agents", "agentic") for t in w.split()) for w in words])
    M, words = M[:, keep], words[keep]
    def corr(A, b):
        A = (A - A.mean(0)) / (A.std(0) + 1e-12); b = (b - b.mean()) / (b.std() + 1e-12)
        return (A * b[:, None]).mean(0)
    r_lvl = corr(M, a)
    r_dif = corr(np.diff(M, axis=0), np.diff(a))
    # permutation test on the strongest change-correlation: shuffle the agent changes, record max |r| over all words
    rng = np.random.default_rng(0); d_a = np.diff(a); dM = np.diff(M, axis=0)
    null = np.array([np.abs(corr(dM, rng.permutation(d_a))).max() for _ in range(1500)])
    thr = float(np.percentile(null, 95))
    out = pd.DataFrame({"word": words, "r_levels": r_lvl, "r_changes": r_dif, "total_docs": np.asarray(X[:, keep].sum(axis=0)).ravel(),
                        "first_q_share": M[0], "last_q_share": M[-1]})
    out["passes_perm_95"] = out.r_changes.abs() > thr
    out = out.sort_values("r_levels", ascending=False)
    out.to_csv(os.path.join(common.OUT, "agent_word_correlations.csv"), index=False)
    print(f"{len(words)} words; permutation 95th percentile of max|r_changes| = {thr:.2f}; words above it: {int(out.passes_perm_95.sum())}")
    return out, M, words, qs, a, thr


def cooccurrence(s):
    """Words over-represented INSIDE agent sentences vs other AI sentences (2024Q3 onward), by smoothed log-odds."""
    d = s[s.q >= common.qkey(2024, 3)]
    stops = list(ENGLISH_STOP_WORDS | EXTRA_STOP | COMPANY_WORDS)
    cv = CountVectorizer(binary=True, ngram_range=(1, 2), min_df=25, stop_words=stops, token_pattern=r"(?u)\b[a-zA-Z][a-zA-Z\-]{2,}\b")
    X = cv.fit_transform(d.text_verbatim); w = np.array(cv.get_feature_names_out())
    ag = d.agent.values
    ca, cn = np.asarray(X[ag].sum(0)).ravel(), np.asarray(X[~ag].sum(0)).ravel()
    lo = np.log((ca + 0.5) / (ag.sum() + 1)) - np.log((cn + 0.5) / ((~ag).sum() + 1))
    ok = (ca >= 25) & ~np.array([any(t in ("agent", "agents", "agentic") for t in x.split()) for x in w])
    df = pd.DataFrame({"word": w[ok], "log_odds": lo[ok], "in_agent_sentences": ca[ok], "in_other_ai_sentences": cn[ok]}).sort_values("log_odds", ascending=False)
    df.to_csv(os.path.join(common.OUT, "agent_cooccurring_words.csv"), index=False)
    return df


def fig_words(out, M, words, qs, a, thr, co):
    pos = out[(out.total_docs >= 60)].sort_values("r_levels", ascending=False).head(14)
    neg = out[(out.total_docs >= 60)].sort_values("r_levels").head(8)
    fig, axes = plt.subplots(1, 4, figsize=(25, 7.8), gridspec_kw={"width_ratios": [1, 0.7, 1, 1.35]})
    ax = axes[0]
    y = np.arange(len(pos))[::-1]
    ax.barh(y, pos.r_levels, color="#009E73", alpha=0.35, label="over time (levels)")
    ax.scatter(pos.r_changes, y, color="#D55E00", s=70, zorder=3, label="quarter-to-quarter changes")
    ax.set_yticks(y); ax.set_yticklabels(pos.word, fontsize=11); ax.set_xlim(-0.2, 1.02); ax.axvline(0, color="#888", lw=1)
    ax.axvline(thr, color="#D55E00", lw=1, ls=":")
    ax.text(thr - 0.01, 3.0, "95% permutation\nthreshold for\nthe best of all\nwords (changes)", fontsize=8, color="#D55E00", va="center", ha="right")
    ax.set_title("Words that rise alongside agent talk", fontsize=13, fontweight="bold", loc="left"); ax.legend(fontsize=9, loc="lower right", frameon=False)
    ax.set_xlabel("correlation with agent share (n = %d quarters)" % len(qs))
    ax = axes[1]
    y = np.arange(len(neg))[::-1]
    ax.barh(y, neg.r_levels, height=0.6, color="#7F7F7F", alpha=0.6)
    ax.set_yticks(y); ax.set_yticklabels(neg.word, fontsize=11); ax.axvline(0, color="#888", lw=1); ax.set_xlim(-1.02, 0.2)
    ax.set_title("Words that fade as agents rise", fontsize=13, fontweight="bold", loc="left"); ax.set_xlabel("correlation (levels)")
    ax = axes[2]
    top = co.head(14); y = np.arange(len(top))[::-1]
    ax.barh(y, top.log_odds, color="#56B4E9", alpha=0.8)
    ax.set_yticks(y); ax.set_yticklabels(top.word, fontsize=11)
    ax.set_title("Words used INSIDE agent sentences", fontsize=13, fontweight="bold", loc="left"); ax.set_xlabel("how over-represented (log odds), 2024 Q3 on")
    ax = axes[3]
    z = lambda v: (v - v.mean()) / (v.std() + 1e-12)
    ax.plot(qs, z(a), color="black", lw=4, label="AGENTS (share of AI sentences)", zorder=5)
    palette = ["#D55E00", "#0072B2", "#CC79A7", "#E69F00", "#56B4E9", "#7B3FBF"]
    idx = {w: i for i, w in enumerate(words)}
    for w, c in zip(list(pos.word.head(6)), palette):
        ax.plot(qs, z(M[:, idx[w]]), color=c, lw=1.8, alpha=0.9, label=w)
    ax.axhline(0, color="#ccc", lw=1)
    ax.set_xticks(qs[::2]); ax.set_xticklabels([f"{int(q)}Q{int(round((q % 1) * 4)) + 1}" for q in qs[::2]], fontsize=9, rotation=45)
    ax.set_ylabel("standardized (z-score)"); ax.legend(fontsize=9, frameon=False, loc="upper left")
    ax.set_title("The six most co-moving words vs agents", fontsize=13, fontweight="bold", loc="left")
    fig.suptitle("Which other words move with 'agents' on earnings calls?", fontsize=18, fontweight="bold", x=0.02, ha="left", y=0.995)
    fig.text(0.02, 0.935, "Computed on AI sentences that do NOT mention agents, so a word cannot correlate just by appearing in the same sentence. "
             "Almost every AI term trends up, so levels overstate the link; the orange dots (changes) are the stricter test.", fontsize=10.5, color="#444444")
    fig.text(0.02, 0.012, "Only 14 quarters and thousands of candidate words: treat as leads to read, not findings. 'Changes' = quarter-over-quarter differences. "
             "Pattern for agents: agentic, AI agent(s), agents.", fontsize=9, color="#555555")
    fig.tight_layout(rect=(0, 0.03, 1, 0.92))
    fig.savefig(os.path.join(common.FIG, "fig9_agent_word_correlations.png"), dpi=165)
    plt.close(fig)
    print("\nTOP positive (by levels):"); print(pos[["word", "r_levels", "r_changes", "total_docs", "first_q_share", "last_q_share"]].round(2).to_string(index=False))
    print("\nTOP negative (levels):"); print(neg[["word", "r_levels", "r_changes", "total_docs", "first_q_share", "last_q_share"]].round(2).to_string(index=False))
    # lead/lag for the top few
    print("\nlead/lag (corr of agent_t with word_{t-k}; k>0 means the word moves FIRST):")
    for w in list(pos.word.head(6)):
        v = M[:, idx[w]]
        res = {k: np.corrcoef(a[k:], v[:len(v) - k])[0, 1] if k >= 0 else np.corrcoef(a[:k], v[-k:])[0, 1] for k in range(-3, 4)}
        best = max(res, key=lambda k: res[k])
        print(f"  {w:28s} best lag {best:+d} (r={res[best]:.2f}); lag0 r={res[0]:.2f}")


if __name__ == "__main__":
    s = load()
    pct, r, p = fig_launches(s)
    out, M, words, qs, a, thr = word_correlations(s, pct)
    co = cooccurrence(s)
    print("\nINSIDE agent sentences (log-odds, 2024Q3+):"); print(co.head(16).round(2).to_string(index=False))
    fig_words(out, M, words, qs, a, thr, co)
