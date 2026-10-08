"""Build an Obsidian vault of the AI knowledge graph (same data and edge rule as fig3).

Notes: one per company, AI topic/product and study period. [[Wikilinks]] are the edges, so Obsidian's graph view
draws the network. An edge exists when a company has 3+ AI sentences on a topic in a period (same rule as fig3).
Obsidian does not weight edges, but it sizes nodes by link count, so widely shared topics look bigger.
Re-run this script to regenerate (it overwrites the generated notes, not other files in the vault).
"""
import json
import os
import sys
from importlib import import_module

import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common

net = import_module("04_network")
VAULT = os.path.join(common.ROOT, "obsidian_vault")
SECTOR = {"alphabet": "Communication Services", "amazon": "Consumer Discretionary", "apple": "Information Technology",
          "meta": "Communication Services", "microsoft": "Information Technology", "nvidia": "Information Technology",
          "tesla": "Consumer Discretionary"}
PERIOD_NAMES = ["Period - Before ChatGPT (2021Q4-2022Q3)", "Period - 2023", "Period - 2024 to 2026Q2"]


def topic_name(label):
    return label.split(" (")[0].replace(" / ", " - ")


def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)


def main():
    s = net.load()
    graphs = [net.period_graph(s, lo, hi) for _, lo, hi in net.PERIODS]
    kind = {lab: k for lab, k, _ in net.TOPICS}
    fa = pd.read_csv(os.path.join(common.OUT, "topic_first_appearance.csv")).set_index("topic") \
        if os.path.exists(os.path.join(common.OUT, "topic_first_appearance.csv")) else net.first_appearance(s).set_index("topic")

    def weight(pi, c, label):
        G = graphs[pi][0]
        return G[c][label]["weight"] if G.has_edge(c, label) else 0

    # Companies
    for c in common.COMPANY_ORDER:
        lines = [f"---\ntags: [company]\nticker: {common.TICKER[c]}\nsector: {SECTOR[c]}\n---",
                 f"# {c.title()} ({common.TICKER[c]})", "",
                 "AI sentences in earnings calls by period (canonical dataset):", ""]
        for pi, (title, _, _) in enumerate(net.PERIODS):
            G = graphs[pi][0]
            n = G.nodes[c]["size"] if c in G else 0
            lines.append(f"- [[{PERIOD_NAMES[pi]}]]: {n:,} AI sentences")
        lines += ["", "## Topics linked to this company", "",
                  "Counts are AI sentences mentioning the topic (an edge needs 3+ in a period).", "",
                  "| Topic | Before ChatGPT | 2023 | 2024-26 | Total |", "|---|---:|---:|---:|---:|"]
        rows = []
        for label, _, _ in net.TOPICS:
            w = [weight(pi, c, label) for pi in range(3)]
            if sum(w):
                rows.append((sum(w), label, w))
        for tot, label, w in sorted(rows, reverse=True):
            lines.append(f"| [[{topic_name(label)}]] | {w[0] or ''} | {w[1] or ''} | {w[2] or ''} | {tot} |")
        lines += ["", f"Source rows: `earnings_calls_canonical/earnings_call_sentences.csv` (company = {c}).", ""]
        write(os.path.join(VAULT, "Companies", f"{c.title()}.md"), "\n".join(lines))

    # Topics
    for label, k, _ in net.TOPICS:
        row = fa.loc[label] if label in fa.index else None
        lines = [f"---\ntags: [{k}]\nkind: {k}\n"
                 + (f"first_quarter: {row['first_quarter_with_3plus_mentions']}\ntotal_mentions: {int(row['total_mentions'])}\n" if row is not None else "")
                 + "---", f"# {topic_name(label)}", "",
                 f"Type: **{'named product / stack' if k == 'product' else 'AI concept'}**." + (f" Pattern: `{label}`." if label != topic_name(label) else ""), ""]
        if row is not None:
            lines.append(f"First quarter with 3+ mentions: **{row['first_quarter_with_3plus_mentions']}** "
                         f"({row['companies_that_quarter']}). Total mentions across calls: {int(row['total_mentions'])}.\n")
        lines += ["## Who talks about it", "", "| Company | Before ChatGPT | 2023 | 2024-26 |", "|---|---:|---:|---:|"]
        for c in common.COMPANY_ORDER:
            w = [weight(pi, c, label) for pi in range(3)]
            if sum(w):
                lines.append(f"| [[{c.title()}]] | {w[0] or ''} | {w[1] or ''} | {w[2] or ''} |")
        lines.append("")
        write(os.path.join(VAULT, "Topics", f"{topic_name(label)}.md"), "\n".join(lines))

    # Periods
    for pi, ((title, lo, hi), (G, n)) in enumerate(zip(net.PERIODS, graphs)):
        comps = [c for c in common.COMPANY_ORDER if c in G]
        tops = sorted((x for x in G if G.nodes[x]["kind"] != "company"), key=lambda x: -G.nodes[x]["size"])
        lines = ["---\ntags: [period]\n---", f"# {PERIOD_NAMES[pi]}", "",
                 f"Calls reporting calendar {common.qlabel(*lo)} to {common.qlabel(*hi)}; {n:,} AI sentences.", "",
                 "## Companies active", ""] + [f"- [[{c.title()}]] ({G.nodes[c]['size']:,} AI sentences)" for c in comps] \
            + ["", "## Topics with a 3+ sentence link to at least one company", ""] \
            + [f"- [[{topic_name(t)}]] ({G.nodes[t]['size']} mentions)" for t in tops] + [""]
        write(os.path.join(VAULT, f"{PERIOD_NAMES[pi]}.md"), "\n".join(lines))

    start = """---
tags: [index]
---
# AI diffusion across the Mag 7: knowledge graph

How AI talk spreads across Alphabet, Amazon, Apple, Meta, Microsoft, Nvidia and Tesla earnings calls
(calls reporting Q4 2021 to Q2 2026). This vault is the same graph as `figures_calls/fig3_ai_knowledge_graph.png`.

**Open the graph view** (Ctrl/Cmd+G). Blue = company, grey = AI concept, orange = named product/stack,
green = study period. Click a note to see counts. Use the graph's Filters to hide period nodes for a cleaner view.

- Periods: [[Period - Before ChatGPT (2021Q4-2022Q3)]], [[Period - 2023]], [[Period - 2024 to 2026Q2]]
- Companies: """ + ", ".join(f"[[{c.title()}]]" for c in common.COMPANY_ORDER) + """

## Read this first
- An edge means a company had **3+ AI sentences** mentioning the topic in that period. Counts are sentences from the
  canonical dataset (`earnings_calls_canonical/`, built by Advik). Topics come from a hand-written pattern list
  in `analysis_calls/04_network.py`.
- Descriptive only: the AI-sentence filter has not been human-validated, 17 of 133 calls are missing (mostly before
  2022Q4), and Amazon/caption calls use units that are not sentences. No causal claims.
- Obsidian does not weight edges. Edge counts are in the tables inside each note.
- Regenerate with `python3 analysis_calls/06_obsidian_vault.py`.
"""
    write(os.path.join(VAULT, "00 Start here.md"), start)

    graph = {"collapse-filter": False, "search": "", "showTags": False, "showAttachments": False, "hideUnresolved": False,
             "showOrphans": True, "collapse-color-groups": False,
             "colorGroups": [{"query": "tag:#company", "color": {"a": 1, "rgb": 2201331}},
                             {"query": "tag:#concept", "color": {"a": 1, "rgb": 10066329}},
                             {"query": "tag:#product", "color": {"a": 1, "rgb": 16750848}},
                             {"query": "tag:#period", "color": {"a": 1, "rgb": 5025616}}],
             "collapse-display": False, "showArrow": False, "textFadeMultiplier": 0, "nodeSizeMultiplier": 1.3,
             "lineSizeMultiplier": 1, "collapse-forces": False, "centerStrength": 0.5, "repelStrength": 12,
             "linkStrength": 1, "linkDistance": 220, "scale": 1, "close": True}
    write(os.path.join(VAULT, ".obsidian", "graph.json"), json.dumps(graph, indent=2))
    n_files = sum(len(f) for _, _, f in os.walk(VAULT))
    print(f"vault written to {VAULT} ({n_files} files)")


if __name__ == "__main__":
    main()
