"""Filter earnings-call transcripts down to AI-related passages.

Reads earnings_calls/<company>/*.md and writes:
  ai_passages.csv        one row per AI passage (keyword hit +/- 1 sentence of context)
  call_summary.csv       one row per call: sentence counts, AI sentence share
Speaker and section (prepared vs Q&A) are best-effort heuristics; see columns.
"""
import csv, glob, html, os, re

ROOT = os.path.dirname(os.path.abspath(__file__))

# Terms that unambiguously mean AI. Case-sensitive entries are handled separately.
STRONG_CI = [
    r"artificial intelligence", r"machine learning", r"deep learning", r"neural net(?:work)?s?",
    r"large language models?", r"\bLLMs?\b", r"\bgenerative\b", r"\bgen ?AI\b", r"chat ?GPT",
    r"\bGPT[- ]?\d?", r"open ?AI", r"\banthropic\b", r"\bcopilot", r"\bgemini\b", r"\bbard\b",
    r"\bllama\b", r"\bagentic\b", r"foundation models?", r"apple intelligence",
    r"\bbedrock\b", r"\btrainium\b", r"\binferentia\b", r"\bsagemaker\b", r"\bvertex\b",
]
# Adjacent infrastructure / autonomy terms: flagged but not counted as AI on their own.
WEAK_CI = [
    r"\bGPUs?\b", r"accelerated computing", r"\binference\b", r"\bblackwell\b", r"\bhopper\b", r"\bCUDA\b",
    r"\bTPUs?\b", r"\bFSD\b", r"full self[- ]driving", r"\boptimus\b", r"robotaxi", r"\bautonomy\b",
    r"\bdojo\b", r"data cent(?:er|re)s?",
]
RE_STRONG_CS = re.compile(r"\bA\.?I\.?(?![A-Za-z])")
RE_STRONG_CI = re.compile("|".join(STRONG_CI), re.I)
RE_WEAK = re.compile("|".join(WEAK_CI), re.I)

QA_PATTERNS = re.compile(
    r"first question|questions? (?:and|&) answers?:?|question[- ]and[- ]answer session (?:begins|will begin)"
    r"|we.ll (?:now )?(?:go|move|turn|open)[^.]{0,40}(?:Q&A|questions?)|let.s (?:go|start|begin)[^.]{0,30}(?:questions|Q&A)",
    re.I,
)


def cal_quarter(company, period):
    """Map a file's period label to the calendar quarter the fiscal quarter ends in."""
    if company in ("microsoft", "apple", "nvidia"):
        m = re.match(r"FY(\d\d)_Q(\d)", period)
        n, q = 2000 + int(m[1]), int(m[2])
        if company == "microsoft":
            return {1: (n - 1, 3), 2: (n - 1, 4), 3: (n, 1), 4: (n, 2)}[q]
        if company == "apple":
            return {1: (n - 1, 4), 2: (n, 1), 3: (n, 2), 4: (n, 3)}[q]
        return (n - 1, q)  # nvidia FYn Qq ends in calendar year n-1 (Q4 FYn = Oct-Jan)
    y, q = period.split("_")
    return (int(y), int(q[1]))


def source_type(header):
    # Check the specific sources first: Fool/caption headers also contain the phrase "official transcript".
    if "Motley Fool" in header:
        return "fool"
    if "YouTube" in header:
        return "caption"
    if "faster-whisper" in header:
        return "whisper"
    if "official transcript" in header.lower():
        return "official"
    return "unknown"


def mark_speakers(text, company, stype):
    """Insert marker tokens ⟦speaker⟧ where a speaker label is detectable (best effort)."""
    if company == "microsoft":
        who = r"[A-Z][A-Z\.\-']+(?: [A-Z][A-Z\.\-']+){0,2}(?:, [A-Za-z&\.\- ]{2,40})?"
        text = re.sub(rf"(?m)^({who}):", lambda m: f"\n⟦{m[1].title()}⟧ ", text)
        text = re.sub(rf"(?<=[\.\?\!] )({who}):", lambda m: f"⟦{m[1].title()}⟧ ", text)
    elif stype == "fool":
        text = re.sub(r"(?m)^\s*([A-Z][^\n]{2,60}?) -- ([^\n]{2,80})$", lambda m: f"\n⟦{m[1].strip()} ({m[2].strip()})⟧ ", text)
        text = re.sub(r"(?m)^\s*Operator\s*$", "\n⟦Operator⟧ ", text)
    elif company == "meta":
        text = re.sub(r"(?m)^([A-Z][\w\.\-' ]{2,40}), ([A-Z][^\n.]{2,70})$", lambda m: f"\n⟦{m[1]} ({m[2]})⟧ ", text)
        text = re.sub(r"(?m)^([A-Z][\w\.\-']+(?: [A-Z][\w\.\-']+){1,2}|Operator):\s", lambda m: f"\n⟦{m[1]}⟧ ", text)
    elif company == "alphabet":
        flat = re.sub(r"\s+", " ", text)
        flat = re.sub(
            r"(?<=[\.\?\!\*\"”\d]) ((?:Operator)|(?:[A-Z][\w\.\-']+(?: [A-Z][\w\.\-']+){1,3})(?:, [A-Za-z ,&]{3,50}| \([A-Za-z &\.,]{2,40}\))?): ",
            lambda m: f" ⟦{m[1]}⟧ ", flat)
        flat = re.sub(r"^(Operator|[A-Z][\w\.\-']+(?: [A-Z][\w\.\-']+){1,3}(?:, [A-Za-z ,&]{3,50})?): ", lambda m: f"⟦{m[1]}⟧ ", flat.strip())
        text = flat
    return text


def clean_text(text, stype):
    text = html.unescape(text)
    text = re.sub(r"\[(?:Music|Applause|Laughter|Inaudible)[^\]]*\]", " ", text, flags=re.I)
    if stype in ("caption", "whisper"):
        text = re.sub(r"(?m)^\[\d\d:\d\d\]\s*", "", text)
        text = text.replace(">>", " ")
    text = re.sub(r"(?m)^\s*\d{1,3}\s*$", "", text)  # stray page numbers
    return text


SENT_SPLIT = re.compile(r"(?<=[\.\?\!])\s+(?=[A-Z⟦\"“(])|\n{2,}")
# Whisper segments are often unpunctuated, so every timestamped line is its own unit.
LINE_SPLIT = re.compile(r"\n+")


def process(path):
    company = os.path.basename(os.path.dirname(path))
    period = re.sub(rf"^{company}_|\.md$", "", os.path.basename(path))
    raw = open(path, encoding="utf-8").read()
    header, _, body = raw.partition("\n---\n")
    stype = source_type(header)
    body = clean_text(body, stype)
    body = mark_speakers(body, company, stype)

    # Section boundary: Fool pages carry an explicit header; otherwise first Q&A cue after 8% of the call.
    qa_at, qa_method = None, "none"
    m = re.search(r"Questions (?:and|&) Answers:?", body)
    if stype == "fool" and m and m.start() > len(body) * 0.05:
        qa_at, qa_method = m.start(), "header"
    else:
        floor = int(len(body) * 0.08)
        for m in QA_PATTERNS.finditer(body):
            if m.start() >= floor:
                qa_at, qa_method = m.start(), "cue"
                break

    sents, pos, speaker = [], 0, ""
    for chunk in (LINE_SPLIT if stype == "whisper" else SENT_SPLIT).split(body):
        if not chunk or not chunk.strip():
            continue
        start = body.find(chunk, pos)
        pos = start + len(chunk) if start >= 0 else pos
        while True:  # consume speaker markers at the head of the chunk
            mm = re.match(r"\s*⟦([^⟧]+)⟧\s*", chunk)
            if not mm:
                break
            speaker, chunk = mm[1], chunk[mm.end():]
        chunk = re.sub(r"⟦[^⟧]*⟧", " ", chunk)
        chunk = re.sub(r"\s+", " ", chunk).strip()
        if len(chunk) < 3:
            continue
        section = "unknown" if qa_at is None else ("qa" if start >= qa_at else "prepared")
        sents.append((chunk, section, speaker))
    return company, period, stype, qa_method, sents


def main():
    passages, summary, pid = [], [], 0
    for path in sorted(glob.glob(os.path.join(ROOT, "*", "*.md"))):
        company, period, stype, qa_method, sents = process(path)
        strong, weak = [], []
        for i, (s, sec, spk) in enumerate(sents):
            kw = set(x.group(0).strip() for x in RE_STRONG_CS.finditer(s))
            kw |= set(x.group(0).strip().lower() for x in RE_STRONG_CI.finditer(s))
            kw.discard("")
            strong.append(sorted(kw))
            weak.append(sorted(set(x.group(0).strip().lower() for x in RE_WEAK.finditer(s))))
        hit = [bool(k) for k in strong]
        # Passages = hit sentences with +/-1 sentence of context; adjacent windows merge.
        i, n = 0, len(sents)
        cy, cq = cal_quarter(company, period)
        while i < n:
            if not hit[i]:
                i += 1
                continue
            a, b = max(0, i - 1), i
            j = i
            while j + 1 < n and (hit[j + 1] or (j + 2 < n and hit[j + 2])):
                j += 1
            b = min(n - 1, j + 1)
            idx = range(a, b + 1)
            kws = sorted({k for t in range(a, b + 1) for k in strong[t]})
            secs = [sents[t][1] for t in range(i, j + 1) if hit[t]] or [sents[i][1]]
            spks = [sents[t][2] for t in range(i, j + 1) if hit[t] and sents[t][2]]
            pid += 1
            passages.append({
                "passage_id": f"{company}-{period}-{pid:05d}", "company": company, "period": period,
                "cal_year": cy, "cal_quarter": cq, "source_type": stype, "section": secs[0],
                "speaker": spks[0] if spks else "", "n_hit_sentences": sum(hit[i:j + 1]),
                "keywords": "; ".join(kws), "text": " ".join(sents[t][0] for t in idx),
            })
            i = b + 1
        n_hit = sum(hit)
        weak_only = sum(1 for k, w in zip(strong, weak) if not k and w)
        summary.append({
            "company": company, "period": period, "cal_year": cy, "cal_quarter": cq, "source_type": stype,
            "qa_boundary": qa_method, "sentences": n, "ai_sentences": n_hit,
            "ai_share": round(n_hit / n, 4) if n else 0, "weak_only_sentences": weak_only,
            "passages": sum(1 for p in passages if p["company"] == company and p["period"] == period),
        })

    with open(os.path.join(ROOT, "ai_passages.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(passages[0].keys()))
        w.writeheader(); w.writerows(passages)
    with open(os.path.join(ROOT, "call_summary.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(summary[0].keys()))
        w.writeheader(); w.writerows(summary)
    print(f"{len(summary)} calls, {len(passages)} AI passages")


if __name__ == "__main__":
    main()
