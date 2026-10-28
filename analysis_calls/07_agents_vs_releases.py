"""Fig 7: did the rise in "AI agents" talk line up with the releases of OpenClaw and Hermes Agent?

Top: % of each quarter's AI sentences that mention agents (same pattern as the 'AI agents' topic in 04_network.py),
with release dates drawn on the call timeline. Bottom: agent sentences per company. Markers show the calls that
actually name OpenClaw or Hermes. Release dates come from web search (Wikipedia and news trackers), not from this repo.
Descriptive only: this shows timing, not cause.
"""
import datetime as dt
import glob
import os
import re
import sys
from importlib import import_module

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common

COLORS = import_module("01_timeseries").COLORS
AGENT_RX = r"agentic|AI agents?|\bagents\b"
NAME_RX = re.compile(r"open ?claw|clawdbot|moltbot|warelay|hermes", re.I)
# (label, date, color). Dates from web search; the rename/viral day is approximate ("late January 2026").
EVENTS = [("OpenClaw first released\n(as 'Warelay'), Nov 24 2025", dt.date(2025, 11, 24), "#7B3FBF"),
          ("Renamed OpenClaw,\nlate Jan 2026", dt.date(2026, 1, 28), "#B22222"),
          ("Hermes Agent\nreleased, Feb 25 2026", dt.date(2026, 2, 25), "#E69F00")]
plt.rcParams.update({"font.family": "DejaVu Sans", "axes.spines.top": False, "axes.spines.right": False})


def x_of(date):
    """Place a calendar date on the quarter axis. Calls are held ~35 days after the quarter they report, and a quarter's key is its start."""
    d = date - dt.timedelta(days=35)
    return d.year + (d.timetuple().tm_yday - 1) / 365.0 - 0.25


def name_mentions():
    """Calls whose transcript names OpenClaw/Hermes: {quarter_key: [(company, n_lines)]}"""
    spec = __import__("importlib.util").util.spec_from_file_location("fap", os.path.join(common.ROOT, "earnings_calls", "filter_ai_passages.py"))
    fap = __import__("importlib.util").util.module_from_spec(spec); spec.loader.exec_module(fap)
    out = {}
    for path in sorted(glob.glob(os.path.join(common.ROOT, "earnings_calls", "*", "*.md"))):
        company = os.path.basename(os.path.dirname(path))
        period = re.sub(rf"^{company}_|\\.md$", "", os.path.basename(path)).replace(".md", "")
        n = sum(1 for ln in open(path, encoding="utf-8") if NAME_RX.search(ln))
        if n:
            y, q = fap.cal_quarter(company, period)
            out.setdefault(common.qkey(y, q), []).append((company, n))
    return out


def main():
    s = pd.read_csv(os.path.join(common.CANON, "earnings_call_sentences.csv"),
                    usecols=["company", "calendar_year", "calendar_quarter", "text_verbatim"])
    s["q"] = [common.qkey(y, q) for y, q in zip(s.calendar_year, s.calendar_quarter)]
    s["agent"] = s.text_verbatim.str.contains(AGENT_RX, case=False, regex=True)
    tot = s.groupby("q").size()
    pct = (s[s.agent].groupby("q").size().reindex(tot.index).fillna(0) / tot * 100)
    by_co = s[s.agent].groupby(["q", "company"]).size().unstack(fill_value=0).reindex(tot.index).fillna(0)
    lo = common.qkey(2023, 4)
    pct, by_co = pct[pct.index >= lo], by_co[by_co.index >= lo]
    names = name_mentions()

    fig, (ax, ax2) = plt.subplots(2, 1, figsize=(13.5, 9.2), sharex=True, gridspec_kw={"height_ratios": [1.55, 1], "hspace": 0.08})
    last = pct.index.max()
    ax.plot(pct.index, pct.values, color="#009E73", lw=3.4, marker="o", ms=7, zorder=4)
    for q, v in pct.items():
        ax.text(q, v + 0.9, f"{v:.0f}%", ha="center", fontsize=9, color="#006b4f")
    # where the climb started
    ax.annotate("Climb starts mid-2024,\nover a year before OpenClaw", xy=(2024.5, pct.loc[2024.5]), xytext=(2023.85, 9.2),
                fontsize=11.5, fontweight="bold", color="#222222", arrowprops=dict(arrowstyle="-|>", color="#222222", lw=1.4))
    from matplotlib.lines import Line2D
    handles = []
    for label, d, color in EVENTS:
        x = x_of(d)
        for a in (ax, ax2):
            a.axvline(x, color=color, lw=2, ls="--", zorder=3)
        handles.append(Line2D([], [], color=color, lw=2.5, ls="--", label=label.replace("\n", " ")))
    handles.append(Line2D([], [], color="#222222", marker="D", ms=10, ls="", mfc="none", mew=2, label="Quarter whose calls name OpenClaw or Hermes"))
    ax.legend(handles=handles, loc="upper left", fontsize=10.5, frameon=True, framealpha=0.95, edgecolor="#dddddd", title="Releases and mentions", title_fontsize=10.5)
    for q, lst in names.items():
        if q in pct.index:
            ax.scatter([q], [pct.loc[q]], s=260, marker="D", facecolors="none", edgecolors="#222222", linewidths=2, zorder=5)
    ax.set_ylim(0, 23); ax.set_ylabel("% of AI sentences that mention agents", fontsize=11); ax.grid(axis="y", color="#e6e6e6")
    ax.set_title("Did the rise in 'AI agents' talk line up with the OpenClaw and Hermes Agent releases?", fontsize=17,
                 fontweight="bold", loc="left", pad=16)

    bottom = np.zeros(len(by_co))
    for c in common.COMPANY_ORDER:
        if c in by_co:
            ax2.bar(by_co.index, by_co[c].values, width=0.2, bottom=bottom, color=COLORS[c], label=c.title())
            bottom += by_co[c].values
    ax2.legend(ncol=3, fontsize=9.5, frameon=False, loc="upper left")
    ax2.set_ylabel("Agent sentences (count)", fontsize=11)
    xt = list(pct.index)[::2]
    ax2.set_xticks(xt); ax2.set_xticklabels([f"{int(q)} Q{int(round((q % 1) * 4)) + 1}" for q in xt], fontsize=10)
    ax2.set_xlim(lo - 0.2, last + 0.55); ax2.grid(axis="y", color="#e6e6e6")
    ax2.set_xlabel("Calendar quarter reported (calls are held in the following 4 to 6 weeks)", fontsize=10)
    fig.text(0.07, 0.012, "Release dates from web search (Wikipedia, news trackers); the late-January rename date is approximate. OpenClaw 2.0 (Aug 31, 2026) falls after our last "
             "call.\nShows timing, not cause: other agent launches in the same window (e.g. Claude Cowork, Codex) cannot be separated. 'Agents' pattern is broad "
             "(agentic, AI agent(s), agents).", fontsize=8.8, color="#555555")
    fig.tight_layout(rect=(0.0, 0.05, 1, 0.97))
    fig.savefig(os.path.join(common.FIG, "fig7_agents_vs_openclaw_hermes.png"), dpi=170)
    plt.close(fig)
    print(pct.round(1).to_dict()); print({k: v for k, v in names.items()})


if __name__ == "__main__":
    main()
