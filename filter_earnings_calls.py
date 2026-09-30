"""
Filter earnings-call transcripts down to the sentences that are about AI.

Reads   earnings_calls/<company>/<company>_<period>.md   (never modified)
Writes  earnings_calls_ai_only/<company>/<company>_<period>_ai.md
        earnings_calls_ai_only/INDEX.md
        earnings_calls_ai_only/_stats.json        per-file counts (feeds INDEX)
        earnings_calls_ai_only/_validation.json   output of --validate

Pipeline per transcript:
  1. split off the metadata block (everything above the first '---' line)
  2. a format-specific parser strips noise (page numbers, running headers,
     footers, livestream chatter), re-flows broken lines, rejoins text split
     by page breaks, and attributes text to (section, speaker) turns
  3. split each turn into sentences with nltk Punkt + a custom abbreviation
     list (unpunctuated YouTube captions: one unit per caption segment)
  4. classify each sentence: AI / borderline-automation / borderline-infra / out
  5. render markdown grouped by section and speaker, original order kept

Formats (see detect_format):
  meta       Meta IR PDFs: "Name, Title" header lines, inline "Name:" in Q&A
  msft       Microsoft IR: "NAME:" labels
  factset    FactSet CallStreet PDFs (recent Nvidia)
  fool       Motley Fool transcripts (older Nvidia, most Tesla)
  alphabet   Alphabet IR PDFs, some extracted one word per line
  captions   Whisper (Amazon) or YouTube auto-captions (Apple, some Tesla)

Everything is deterministic and local; no network access. The rules in prose
are in earnings_calls_ai_only/FILTER_METHOD.md.

Usage:
  python filter_earnings_calls.py                      # all companies + INDEX
  python filter_earnings_calls.py --company meta       # one company
  python filter_earnings_calls.py --only meta_2024_Q1  # one file
  python filter_earnings_calls.py --validate           # QA checks on the output
"""

import argparse
import html
import json
import random
import re
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path

from nltk.tokenize import PunktTokenizer

ROOT = Path(__file__).resolve().parent
SRC_DIR = ROOT / "earnings_calls"
OUT_DIR = ROOT / "earnings_calls_ai_only"

COMPANIES = ["meta", "microsoft", "nvidia", "alphabet", "amazon", "apple", "tesla"]

PREPARED = "Prepared remarks"
QA = "Q&A"
UNLABELED = "Speaker not labeled"

LONG_WORDS = 150
SEED = 20260930


# ---------------------------------------------------------------------------
# Sentence splitting
# ---------------------------------------------------------------------------

# Abbreviations Punkt must not treat as sentence ends (lowercase, no final dot).
ABBREVIATIONS = {
    "u.s", "u.k", "inc", "vs", "mr", "mrs", "ms", "dr", "no", "e.g", "i.e",
    "approx", "a.i", "corp", "co", "ltd", "jr", "sr", "st", "dept", "fig",
    "est", "cf", "al", "p.m", "a.m", "jan", "feb", "mar", "apr", "jun", "jul",
    "aug", "sep", "sept", "oct", "nov", "dec",
}

_punkt = PunktTokenizer("english")
_punkt._params.abbrev_types.update(ABBREVIATIONS)


def split_sentences(text, unit_mode="punkt"):
    if unit_mode == "lines":
        return [s.strip() for s in text.split("\n") if s.strip()]
    return [s.strip() for s in _punkt.tokenize(text) if s.strip()]


# ---------------------------------------------------------------------------
# AI term lists
# ---------------------------------------------------------------------------

def _rx(pattern, cs=False):
    return re.compile(pattern, 0 if cs else re.IGNORECASE)


# Core terms: a hit puts the sentence in the AI set, no flag.
CORE_TERMS = [
    ("AI", _rx(r"(?<![A-Za-z])AIs?(?![A-Za-z])", cs=True)),
    ("A.I.", _rx(r"(?<![A-Za-z])A\.I\.")),
    ("artificial intelligence", _rx(r"\bartificial (?:general )?intelligence\b")),
    ("GenAI/OpenAI/xAI", _rx(r"\b(?:GenAI|OpenAI|xAI)\b", cs=True)),
    ("OpenAI/ChatGPT (any case)", _rx(r"\bopen ?ai\b|\bchat ?gpt\b")),
    ("Apple Intelligence", _rx(r"\bapple intelligence\b")),
    ("generative", _rx(r"\bgenerative\b")),
    ("agentic", _rx(r"\bagentic\b")),
    ("machine learning", _rx(r"\bmachine[- ]learning\b")),
    ("deep learning", _rx(r"\bdeep[- ]learning\b")),
    ("neural network", _rx(r"\bneural (?:net|nets|network|networks|engine|engines)\b")),
    ("LLM", _rx(r"\bLLMs?\b", cs=True)),
    ("language model", _rx(r"\b(?:large )?language models?\b")),
    ("ML model phrase", _rx(
        r"\b(?:foundation(?:al)?|frontier|reasoning|multimodal|diffusion|"
        r"open[- ]source|open[- ]weights?|ranking|recommendation|retrieval|"
        r"ML|trained|video[- ]generation|image[- ]generation|world)\s+models?\b")),
    ("training/inference compute", _rx(
        r"\b(?:training|inference)\s+(?:compute|clusters?|runs?|workloads?|"
        r"capacity|infrastructure|chips?|costs?|demand|tokens?|requests?)\b|"
        r"\bmodels?\s+(?:training|inference)\b|\btrain(?:ing|ed)?\s+(?:\w+\s+){0,3}models?\b")),
    ("parameter model", _rx(
        r"\bparameters?\s+models?\b|\b\d+(?:\.\d+)?\+?\s?(?:B|billion|trillion|T)\+?\s+parameters?\b")),
    ("superintelligence", _rx(r"\bsuperintelligen(?:ce|t)\b")),
    ("AGI", _rx(r"\bAGI\b", cs=True)),
    ("chatbot", _rx(r"\bchat ?bots?\b")),
    ("computer vision / NLP", _rx(r"\bcomputer vision\b|\bnatural language processing\b|\bNLP\b")),
    # Named AI products, models, labs, AI chips (case-sensitive).
    ("named AI product", _rx(
        r"\b(?:ChatGPT|Copilots?|Gemini|Gemma|Bard|Llama|Claude|Anthropic|"
        r"Bedrock|Trainium\d?|Inferentia\d?|TPUs?|Nova|Amazon Q|Q Developer|"
        r"DeepMind|DeepSeek|Grok|Mistral|Perplexity|NotebookLM|Imagen|Veo|"
        r"Midjourney|Stable Diffusion|Sora|Phi|Phi-\d|NIMs?|NeMo|TensorRT|GR00T|"
        r"MTIA|Maia|MAI|Emu|Movie Gen|Segment Anything|Stargate|AlphaFold|Dojo)\b|"
        r"\bTraining and Inference Accelerator\b", cs=True)),
    ("named AI product (any case)", _rx(r"\bcopilots?\b|\bgemini\b|\banthropic\b|\bdeepseek\b")),
]

# Only for machine transcripts (Whisper / YouTube captions), where casing is
# unreliable: "ai"/"Ai" is AI. In official/human transcripts lowercase "ai"
# is logged as a false-positive candidate instead.
MACHINE_AI = _rx(r"(?<![A-Za-z])ai'?s?(?![A-Za-z])")

# Weak terms: a hit (with no core hit) includes the sentence with ⚑ uncertain.
MODEL_BARE = _rx(
    r"(?<!business )(?<!operating )(?<!financial )(?<!revenue )(?<!pricing )"
    r"(?<!subscription )(?<!economic )(?<!cost )(?<!delivery )(?<!hybrid )"
    r"(?<!partnership )(?<!retail )(?<!franchise )(?<!go-to-market )(?<!role )"
    r"(?<!licensing )(?<!monetization )(?<!consumption )(?<!distribution )"
    r"(?<!sales )(?<!service )(?<!services )(?<!margin )(?<!pricing )"
    r"\bmodels?\b(?!\s+(?:year|[3SXY]\b|lineup))")
WEAK_TERMS = [
    ("AI accelerator name", _rx(
        r"\b(?:Blackwell|Hopper|Rubin|GB[23]00|[AHB]100|H20|H200|DGX|HGX|NVLink|CUDA)\b", cs=True)),
    ("AI platform name", _rx(
        r"\b(?:Foundry|Fairwater|Omniverse|Cosmos|Isaac|Dynamo|Siri|Private Cloud Compute)\b", cs=True)),
    ("Meta ads-model name", _rx(r"\b(?:GEM|Andromeda|Lattice)\b", cs=True)),
    ("agent", _rx(r"\bagents?\b")),
    ("inference", _rx(r"\binferenc\w*")),
    ("tokens", _rx(r"\btokens?\b")),
    ("algorithm", _rx(r"\balgorithm\w*")),
    ("recommendation system", _rx(r"\brecommendation (?:systems?|engines?)\b")),
    ("model architecture/performance", _rx(
        r"\bmodels?\s+(?:architecture|performance|capabilit\w+|weights|parameters)\b")),
    ("model (bare)", MODEL_BARE),
    ("Alexa", _rx(r"\bAlexa\b", cs=True)),
    ("autonomous driving", _rx(
        r"\bWaymo\b|\bself[- ]driving\b|\bautonom\w+|\bFSD\b|\bAutopilot\b|"
        r"\brobo[- ]?taxi\w*|\bCybercab\b")),
]
# Weak terms switched off per company because they mean something else there.
WEAK_OFF = {"tesla": {"model (bare)"}, "apple": {"model (bare)"}}   # car / device models

AUTOMATION_TERMS = _rx(r"\bautomat\w*|\brobot\w*|\bOptimus\b|\bhumanoid\w*")
INFRA_TERMS = _rx(
    r"\bGPUs?\b|\bdata ?cent(?:er|re)s?\b|\bcap ?ex\b|\bcapital expenditures?\b|"
    r"\baccelerated computing\b|\bcompute\b|\bservers?\b|\bsupercomput\w+|"
    r"\baccelerators?\b|\binfrastructure\b")

# Lowercase/mixed-case "ai" tokens that the case-sensitive AI rule rejects;
# counted as false positives. Titles before "Ai" (a surname) likewise.
FALSE_POSITIVE_AI = _rx(r"(?<![A-Za-z])(?:ai|Ai|aI)s?(?![A-Za-z])", cs=True)
SURNAME_AI = _rx(r"\b(?:Mr|Ms|Mrs|Dr)\.\s+Ai\b", cs=True)

SAFE_HARBOR = _rx(
    r"forward[‐-]looking statements?|safe harbor|undertake no obligation|"
    r"could cause (?:actual )?results to differ|differ materially")

CONTEXT_DEPENDENT = _rx(
    r"^(?:(?:And|So|But|Now|Well|Yes|Yeah|Okay|OK)[,]?\s+)?"
    r"(?:It|It's|It’s|This|That|That's|That’s|These|Those|They|They're|They’re|Them|Which)\b"
    r"(?!\s+(?:month|year|quarter|week|morning|afternoon|time|fall|spring|summer|winter)\b)",
    cs=True)


@dataclass
class Verdict:
    kind: str                      # "ai" | "auto" | "infra" | "out"
    terms: list = field(default_factory=list)
    flags: list = field(default_factory=list)
    false_positive_ai: int = 0


def classify(sentence, machine=False, company=""):
    scrubbed = SURNAME_AI.sub(" ", sentence)
    fp = len(SURNAME_AI.findall(sentence))
    core = [name for name, rx in CORE_TERMS if rx.search(scrubbed)]
    if machine:
        if MACHINE_AI.search(scrubbed) and "AI" not in core:
            core.append("AI (machine transcript, any case)")
    else:
        fp += len(FALSE_POSITIVE_AI.findall(scrubbed))
    off = WEAK_OFF.get(company, set())
    weak = [name for name, rx in WEAK_TERMS if name not in off and rx.search(scrubbed)]
    flags = []
    if core or weak:
        if not core:
            flags.append("uncertain")
        if SAFE_HARBOR.search(sentence):
            flags.append("uncertain: safe-harbor")
        if CONTEXT_DEPENDENT.search(sentence):
            flags.append("context-dependent")
        if len(sentence.split()) > LONG_WORDS:
            flags.append("long")
        return Verdict("ai", core + weak, flags, fp)
    if AUTOMATION_TERMS.search(sentence):
        return Verdict("auto", false_positive_ai=fp)
    if INFRA_TERMS.search(sentence):
        return Verdict("infra", false_positive_ai=fp)
    return Verdict("out", false_positive_ai=fp)


# ---------------------------------------------------------------------------
# Shared parsing helpers
# ---------------------------------------------------------------------------

@dataclass
class Turn:
    section: str
    speaker: str
    text: str
    unit_mode: str = "punkt"       # "punkt" or "lines" (one unit per line)


TERMINAL = re.compile(r"[.?!][\"'”’)\]]*$")
HYPHEN_END = re.compile(r"[A-Za-z][-‐]$")
PAGE_NUMBER = re.compile(r"^\s*\d{1,3}\s*$")


def join_lines(lines):
    """Join wrapped lines into one string. A line ending in a single hyphen
    (PDF wrap inside a compound word) is joined with no space; everything
    else is joined with one space."""
    parts = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        if parts and HYPHEN_END.search(parts[-1]) and not parts[-1].endswith("--"):
            parts[-1] += line
        else:
            parts.append(line)
    return " ".join(parts)


def split_metadata(raw):
    lines = raw.splitlines()
    for i, line in enumerate(lines):
        if line.strip() == "---":
            return "\n".join(lines[:i]).rstrip(), lines[i + 1:]
    raise ValueError("no '---' separator after metadata block")


def names_match(a, b):
    """'Ken Dorell' ~ 'Kenneth Dorell', 'Doug Anmuth' ~ 'Douglas Anmuth'."""
    pa, pb = a.lower().split(), b.lower().split()
    if not pa or not pb or pa[-1] != pb[-1]:
        return False
    fa, fb = pa[0], pb[0]
    return fa.startswith(fb) or fb.startswith(fa)


def display_name(name):
    """Title-case ALL-CAPS names (Microsoft); leave everything else alone."""
    if name.isupper() and name != "Q&A":
        return " ".join(w.capitalize() if not re.match(r"^[A-Z]\.$", w) else w
                        for w in name.split())
    return name


class SpeakerBook:
    """Maps bare speaker names to 'Name, Title' / 'Name, Firm' labels using
    only information present in the same transcript."""

    def __init__(self):
        self.labels = {}           # full name -> descriptor

    def add(self, name, descriptor):
        self.labels.setdefault(name, descriptor.strip().rstrip(",;"))

    def label(self, name):
        if name in ("Operator", UNLABELED):
            return name
        for known, desc in self.labels.items():
            if known.lower() == name.lower() or names_match(known, name):
                return f"{display_name(name)}, {desc}"
        return display_name(name)


OPERATOR_INTRO = re.compile(
    r"(?:from the line of|comes from|question is from|question from)\s+(?:[a-z]+\s+){0,3}"
    r"([A-Z][\w.'’‐-]+(?:\s+[A-Z][\w.'’‐-]+){0,3})\s+(?:from|with|of|at)\s+"
    r"(.+?)(?:\.\s+(?:Please|Your|Go|Thank|The|Mr|Ms)\b|\.?\s*$|,\s+please|\.\s)")

# Phrases that open the Q&A inside a turn; the section switches at the start
# of the sentence that contains the match.
QA_MARKERS = {
    "msft": _rx(r"(?:let['’]s|we['’]ll|we will|now)\s+(?:now\s+)?(?:go|move|turn|open)\w*\s+"
                r"(?:over\s+|on\s+)?(?:to\s+)?(?:the\s+)?Q&A"),
    "fool": _rx(r"(?:go|move|head|moving|going|start|begin)\w*\s+(?:on\s+|over\s+|through\s+|with\s+)?"
                r"(?:to\s+)?(?:the\s+)?(?:investor|say\.com|analyst|retail)\s+(?:questions|Q&A)|"
                r"(?:let['’]s|we['’]ll|we will)\s+(?:now\s+)?(?:go|move|open)\w*\s+(?:on\s+|over\s+)?"
                r"(?:to\s+)?(?:the\s+)?(?:Q&A|questions)"),
    "apple": _rx(r"may we (?:have|take|get) the (?:the |first )?question|"
                 r"(?:our|the) (?:first|next) question (?:is|comes) from"),
    "nvidia": _rx(r"first question|question comes from|question is from"),
    "tesla": _rx(r"(?:go|move|head|moving|going|start|begin)\w*\s+(?:on\s+|over\s+|through\s+|with\s+)?"
                 r"(?:to\s+)?(?:the\s+)?(?:investor|say\.com|analyst|retail)\s+(?:questions|Q&A)|"
                 r"covers? (?:uh )?the say\.com questions|questions on say\.com relate"),
    "amazon": _rx(r"first question|question comes from|question is from"),
}


def split_qa(turns, marker):
    """Everything from the first marker onward becomes Q&A. Returns (turns, found)."""
    for ti, t in enumerate(turns):
        m = marker.search(t.text)
        if not m:
            continue
        if t.unit_mode == "lines":
            cut = m.start()                        # may split one caption segment in two
        else:
            cut = max(t.text.rfind(p, 0, m.start()) for p in (". ", "? ", "! ", ".\n"))
            cut = 0 if cut < 0 else cut + 2
        before, after = t.text[:cut].strip(), t.text[cut:].strip()
        out = turns[:ti]
        if before:
            out.append(Turn(PREPARED, t.speaker, before, t.unit_mode))
        out.append(Turn(QA, t.speaker, after, t.unit_mode))
        out += [Turn(QA, x.speaker, x.text, x.unit_mode) for x in turns[ti + 1:]]
        return out, True
    return turns, False


def append_turn(turns, section, speaker, text, unit_mode="punkt"):
    text = text.strip()
    if not text:
        return
    if turns and turns[-1].speaker == speaker and turns[-1].section == section:
        turns[-1].text += "\n" + text
    else:
        turns.append(Turn(section, speaker, text, unit_mode))


# ---------------------------------------------------------------------------
# Meta: "Name, Title" header lines (prepared) and inline "Name:" (Q&A)
# ---------------------------------------------------------------------------

META_HEADER = re.compile(
    r"^([A-Z][\w.'’‐-]+(?: [A-Z][\w.'’‐-]+){0,3}), (.*(?:CEO|CFO|COO|CTO|President|"
    r"Director|VP|Vice President|Investor Relations|Finance|Officer|Chief|Head).*)$")
META_INLINE = re.compile(
    r"^\s*(Operator|[A-Z][\w.'’‐-]+(?: [A-Z][\w.'’‐-]+){1,3}):\s+(.*)$")


def parse_meta(body_lines, company):
    notes = {"page_numbers_removed": 0, "page_break_joins": 0, "title_block_paragraphs": 0}

    # 1. paragraphs; an inline "Name:" line after a finished sentence starts a new one
    paragraphs, cur = [], []
    for line in body_lines:
        if not line.strip():
            if cur:
                paragraphs.append(cur)
                cur = []
            continue
        if cur and META_INLINE.match(line) and TERMINAL.search(cur[-1].strip()):
            paragraphs.append(cur)
            cur = []
        cur.append(line)
    if cur:
        paragraphs.append(cur)

    # 2. drop page numbers; rejoin a paragraph that the page break cut mid-sentence
    merged = []
    after_page_break = False
    for para in paragraphs:
        if len(para) == 1 and PAGE_NUMBER.match(para[0]):
            notes["page_numbers_removed"] += 1
            after_page_break = True
            continue
        text = join_lines(para)
        if (after_page_break and merged and not TERMINAL.search(merged[-1])
                and not META_INLINE.match(para[0]) and not META_HEADER.match(text)):
            sep = "" if HYPHEN_END.search(merged[-1]) else " "
            merged[-1] = merged[-1] + sep + text
            notes["page_break_joins"] += 1
        else:
            merged.append(text)
        after_page_break = False

    # 3. attribute paragraphs to speakers and sections
    book = SpeakerBook()
    turns, speaker, section = [], None, PREPARED
    non_operator_spoke = False
    for text in merged:
        m_head = META_HEADER.match(text)
        if m_head and not TERMINAL.search(text) and len(text.split()) <= 10:
            speaker = m_head.group(1)
            book.add(speaker, m_head.group(2))
            non_operator_spoke = True
            continue
        m_in = META_INLINE.match(text)
        if m_in:
            speaker, text = m_in.group(1), m_in.group(2)
            if speaker == "Operator":
                if non_operator_spoke:
                    section = QA
                for name, firm in OPERATOR_INTRO.findall(text):
                    book.add(name, firm)
            else:
                non_operator_spoke = True
        if speaker is None:
            notes["title_block_paragraphs"] += 1   # "Meta Platforms, Inc. (META)" etc.
            continue
        append_turn(turns, section, speaker, text)

    for t in turns:
        t.speaker = book.label(t.speaker)
    return turns, notes, []


# ---------------------------------------------------------------------------
# Microsoft: "NAME:" labels, alone on a line or inline
# ---------------------------------------------------------------------------

MSFT_LABEL = re.compile(r"^\s*([A-Z][A-Z.'’-]+(?: [A-Z][A-Z.'’-]+){0,3}):\s*(.*)$")
INTRO_TITLE = re.compile(
    r"([A-Z][a-z]+(?: [A-Z][a-z]+){1,2}), ((?:[a-z]+ ){0,5}(?:officer|president|secretary|"
    r"counsel|relations|treasurer)(?: [a-z]+){0,6}?)(?=,| and [A-Z]|\.|;)")


def parse_msft(body_lines, company):
    notes = {"title_block_lines": 0}
    book = SpeakerBook()
    turns, speaker = [], None
    for line in body_lines:
        if line.strip() == "END":
            break
        if not line.strip():
            continue
        m = MSFT_LABEL.match(line)
        if m and m.group(1) not in ("Q&A",) and len(m.group(1)) > 3:
            speaker, line = m.group(1), m.group(2)
        if speaker is None:
            notes["title_block_lines"] += 1        # "Transcript", call title, names, date
            continue
        if speaker == "OPERATOR":
            for name, firm in OPERATOR_INTRO.findall(line):
                book.add(name, firm)
        append_turn(turns, PREPARED, speaker, line)
    if turns:                                      # titles stated in the IR opening
        for name, title in INTRO_TITLE.findall(turns[0].text):
            book.add(name, title)
    turns, found = split_qa(turns, QA_MARKERS["msft"])
    flags = [] if found else ["Q&A start not detected"]
    for t in turns:
        t.speaker = "Operator" if t.speaker == "OPERATOR" else book.label(t.speaker)
    return turns, notes, flags


# ---------------------------------------------------------------------------
# FactSet CallStreet (Nvidia FY26+)
# ---------------------------------------------------------------------------

FACTSET_NOISE = [re.compile(p) for p in (
    r"^\s*NVIDIA Corp\.\s*\(NVDA\s*\)\s*$", r"^\s*Q\d \d{4} Earnings Call\s*$",
    r"^\s*Corrected Transcript\s*$", r"^\s*\d{1,2}\s*-[A-Za-z]{3}\s*-\d{4}\s*$",
    r"1-877-FACTSET", r"^\s*\d{1,3}\s*$", r"^\s*Copyright ©", r"^\s*Total Pages:",
)]
DOTTED = re.compile(r"^\s*\.{20,}\s*$")


def parse_factset(body_lines, company):
    notes = {"noise_lines_removed": 0}
    book = SpeakerBook()
    turns, speaker, section = [], None, None
    expect = None                                  # "name" -> "title" -> None
    for line in body_lines:
        s = line.strip()
        s = re.sub(r"\s+", " ", s)
        if s == "MANAGEMENT DISCUSSION SECTION":
            section = PREPARED
            continue
        if s == "QUESTION AND ANSWER SECTION":
            section = QA
            continue
        if s == "Disclaimer":
            break
        if section is None:
            continue                               # cover page + participant list
        if any(rx.search(line) for rx in FACTSET_NOISE):
            notes["noise_lines_removed"] += 1
            continue
        if DOTTED.match(line):
            expect = "name"
            continue
        if not s:
            continue
        if s.startswith("Operator:"):
            speaker, expect = "Operator", None
            append_turn(turns, section, speaker, s[len("Operator:"):])
            continue
        if expect == "name":
            speaker, expect = s, "title"
            continue
        if expect == "title":
            book.add(speaker, re.sub(r"\s+[QA]$", "", s))
            expect = None
            continue
        if speaker == "Operator":
            for name, firm in OPERATOR_INTRO.findall(s):
                book.add(name, firm)
        append_turn(turns, section, speaker, line)
    for t in turns:
        t.speaker = book.label(t.speaker)
    return turns, notes, []


# ---------------------------------------------------------------------------
# Motley Fool (Nvidia FY23-FY25, Tesla)
# ---------------------------------------------------------------------------

FOOL_SPEAKER = re.compile(
    r"^\s*((?:[A-Z][\w.'’-]*)(?: (?:[A-Z][\w.'’-]*|de|van|von|da)){1,4}) -- (.{2,120}?)\s*$")
FOOL_STOP = re.compile(r"^\s*(?:Duration:|Call participants:|More [A-Z]+ analysis)")


def parse_fool(body_lines, company):
    notes = {"lines_after_call_dropped": 0}
    turns, speaker, section = [], None, None
    labels = {}
    in_roster = False
    for line in body_lines:                        # names seen anywhere with a title,
        s = line.strip()                           # plus the closing participant roster
        if s == "Call participants:":
            in_roster = True
            continue
        if in_roster:
            if not s:
                break
            name, _, title = s.partition(" -- ")
            labels.setdefault(name.strip(), title.replace(" -- ", ", ").strip())
            continue
        m = FOOL_SPEAKER.match(line)
        if m and not TERMINAL.search(s):
            labels.setdefault(m.group(1), m.group(2).replace(" -- ", ", "))
    explicit_qa = False
    for i, line in enumerate(body_lines):
        s = line.strip()
        if FOOL_STOP.match(line):
            notes["lines_after_call_dropped"] = len(body_lines) - i
            break
        if s == "Prepared Remarks:":
            section = PREPARED
            continue
        if s in ("Questions & Answers:", "Questions and Answers:"):
            section, explicit_qa = QA, True
            continue
        if section is None or not s:
            continue
        if s == "Operator" or s in labels:        # bare name line, no title
            speaker = s
            continue
        m = FOOL_SPEAKER.match(line)
        if m and not TERMINAL.search(s):
            speaker = m.group(1)
            labels.setdefault(speaker, m.group(2).replace(" -- ", ", "))
            continue
        if speaker is None:
            continue
        append_turn(turns, section, speaker, s)
    flags = []
    if not explicit_qa:
        turns, found = split_qa(turns, QA_MARKERS["fool"])
        if not found:
            flags.append("Q&A start not detected")
    for t in turns:
        if labels.get(t.speaker):
            t.speaker = f"{t.speaker}, {labels[t.speaker]}"
    return turns, notes, flags


# ---------------------------------------------------------------------------
# Alphabet: inline "Name, Title:" / "Name (Firm):" labels; some files are
# one word per line, some with a blank line after every word
# ---------------------------------------------------------------------------

_UNIT_NEXT = re.compile(
    r"^(?:million|billion|trillion|thousand|hundred|percent|%|x|times|years?|months?|days?|"
    r"weeks?|quarters?|hours?|minutes?|seconds?|points?|basis|and|or|to|of|-|–|through|plus|out)\b")
_PROD_PREV = re.compile(
    r"^(?:Gemini|Imagen|Veo|Gemma|Llama|Genie|Pixel|Q|Phase|version|Chapter|Android|iOS|Lyria|"
    r"Claude|GPT|top|Tier|Level|No\.|number|Nest|Tensor|Ironwood|Trillium|TPU|v|Pro|Flash)$", re.I)


def _page_score(toks, i):
    prev = toks[i - 1] if i else ""
    nxt = toks[i + 1] if i + 1 < len(toks) else ""
    if _PROD_PREV.match(prev) or nxt in ("Pro", "Flash", "Ultra", "Nano"):
        return None
    s = 0
    if TERMINAL.search(prev) or prev.endswith(":"):
        s += 2
    if nxt[:1].isupper():
        s += 1
    if _UNIT_NEXT.match(nxt):
        s -= 1
    if prev.startswith("$") and prev[-1] not in ".,;":
        s -= 2
    return s


def find_inline_pages(toks, lo=150, hi=900):
    """Page numbers in word-per-line PDF extractions carry no layout cue. They
    are the integers 1, 2, 3, ... in order, a few hundred words apart. For page
    n, take the best-scoring bare token 'n' in the window after page n-1."""
    pages, n, last = [], 1, 0
    while True:
        cands = [(_page_score(toks, i), i) for i in range(last + lo, min(len(toks), last + hi))
                 if toks[i] == str(n)]
        cands = [(s, i) for s, i in cands if s is not None and s >= -1]
        if not cands:
            return pages
        _, i = max(cands, key=lambda c: (c[0], -c[1]))
        pages.append(i)
        last, n = i, n + 1


_NAME_TOK = r"(?:[A-Z]\.|[A-Z][\w'’-]+)"            # no trailing period except initials
ALPHA_NAME = _NAME_TOK + r"(?: " + _NAME_TOK + r"){1,3}"
ALPHA_LABEL = re.compile(
    r"(?:^|(?<=[.?!] )|(?<=[.?!][\"”’)] ))"
    r"(Operator|(" + ALPHA_NAME + r")(?:(, [^:.?!]{2,90}?)|( \([^)]{2,60}\)))):\s")
TITLE_KW = re.compile(r"CEO|CFO|COO|CBO|President|Director|VP|Officer|Chief|Head|"
                      r"Investor Relations|Finance")


def parse_alphabet(body_lines, company):
    notes = {}
    nonblank = [l for l in body_lines if l.strip()]
    single = sum(len(l.split()) == 1 for l in nonblank) / max(1, len(nonblank))
    blanks = len(body_lines) - len(nonblank)
    if single > 0.8 and blanks > 0.4 * len(nonblank):
        notes["layout"] = "one word per line, blank line after every word"
        toks = [l.strip() for l in nonblank]
        pages = set(find_inline_pages(toks))
        notes["page_numbers_removed"] = len(pages)
        notes["page_numbers_method"] = "inline sequence detector"
        text = join_lines(t for i, t in enumerate(toks) if i not in pages)
    else:
        notes["layout"] = "one word per line" if single > 0.8 else "wrapped lines"
        keep, pages = [], 0
        for i, l in enumerate(body_lines):
            if PAGE_NUMBER.match(l) and (i + 1 == len(body_lines) or not body_lines[i + 1].strip()):
                pages += 1
                continue
            keep.append(l)
        notes["page_numbers_removed"] = pages
        notes["page_numbers_method"] = "digit-only line followed by blank line"
        text = join_lines(keep)

    # pass 1: well-formed labels; pass 2: the same labels with no sentence end before them
    found = {}
    for m in ALPHA_LABEL.finditer(text):
        if m.group(1) == "Operator" or m.group(4) or TITLE_KW.search(m.group(3) or ""):
            found[m.group(1)] = m
    known = sorted(found, key=len, reverse=True)
    label_rx = re.compile(r"(?:^|(?<=\s))(" + "|".join(re.escape(k) for k in known) + r"):\s")
    marks = list(label_rx.finditer(text))
    if not marks:
        return [], notes, ["PARSE FAILED: no speaker labels"]
    notes["title_block_chars"] = marks[0].start()
    turns, section, mgmt_spoke = [], PREPARED, False
    for k, m in enumerate(marks):
        label = m.group(1)
        chunk = text[m.end(): marks[k + 1].start() if k + 1 < len(marks) else len(text)]
        if label == "Operator":
            if mgmt_spoke:
                section = QA
            speaker = "Operator"
        else:
            mgmt_spoke = True
            name, rest = re.match(r"(" + ALPHA_NAME + r")(.*)", label).groups()
            rest = rest.strip()
            rest = rest[1:-1] if rest.startswith("(") else rest.lstrip(", ")
            speaker = f"{name}, {rest}"
        append_turn(turns, section, speaker, chunk)
    return turns, notes, []


# ---------------------------------------------------------------------------
# Machine transcripts: Whisper (Amazon) and YouTube auto-captions (Apple, Tesla)
# ---------------------------------------------------------------------------

SEGMENT = re.compile(r"^\s*\[(\d+:\d{2}(?::\d{2})?)\]\s?(.*)$")
CAPTION_NOISE = re.compile(
    r"\bforeign\s*(?=\[Music\])|\[(?:Music|music|Applause|applause|Laughter|laughter|"
    r"clears throat|__)\]|>>|&gt;&gt;")
CALL_START = _rx(
    r"(?:good (?:afternoon|day|evening)[^.]{0,30}?)?welcome to (?:the )?(?:apple|tesla|amazon|nvidia)|"
    r"my name is (?:suhasini|travis)|conference is now being recorded|"
    r"speaking first today is apple|be followed by CFO|thank you for standing by")
CALL_END = {
    "tesla": _rx(r"(?:that's|that is) all the time we have|look forward to talking to you next quarter|"
                 r"see you (?:again )?(?:next quarter|in three months)|thank you very much and goodbye"),
    "apple": _rx(r"this does conclude today's conference"),
    "amazon": _rx(r"(?:this|that) concludes (?:today's|the|our) (?:call|conference|teleconference)"),
}


def parse_captions(body_lines, company, meta_text):
    notes = {}
    flags = []
    segs = []
    for line in body_lines:
        m = SEGMENT.match(line)
        if m:
            txt = CAPTION_NOISE.sub(" ", html.unescape(m.group(2)))
            txt = re.sub(r"\s+", " ", txt).strip()
            segs.append(txt)
    notes["segments"] = len(segs)
    whisper = "whisper" in meta_text.lower()
    flags.append("machine transcript (Whisper), no speaker labels" if whisper
                 else "YouTube auto-captions, no speaker labels")

    # trim to the call itself
    start = next(((i, m.start()) for i, s in enumerate(segs) for m in [CALL_START.search(s)] if m), None)
    if start is None:
        flags.append("call opening not detected: source may start mid-call")
        start = (0, 0)
    si, sp = start
    notes["pre_call_segments_dropped"] = si
    if si > 3:
        flags.append(f"{si} pre-call livestream segments dropped")
    segs = segs[si:]
    segs[0] = segs[0][sp:]
    end_rx = CALL_END.get(company)
    if end_rx:
        ends = [i for i, s in enumerate(segs) if end_rx.search(s)]
        if ends:
            notes["post_call_segments_dropped"] = len(segs) - ends[-1] - 1
            segs = segs[: ends[-1] + 1]
        else:
            notes["post_call_segments_dropped"] = 0
            if company == "tesla":
                flags.append("call end not detected")
    segs = [s for s in segs if s]

    words = sum(len(s.split()) for s in segs)
    punct = sum(len(re.findall(r"[.?!]", s)) for s in segs)
    notes["punct_per_100_words"] = round(100 * punct / max(1, words), 2)
    if punct / max(1, words) < 0.01:
        mode = "lines"
        flags.append("unpunctuated captions: units are ~30s caption segments, not sentences")
        text = "\n".join(segs)
    elif whisper:
        # Whisper segments rarely end in punctuation. Start a new unit where
        # the previous segment has no final punctuation and the next segment
        # starts with a capital letter; then Punkt-split inside each unit.
        mode = "lines"
        units, cur = [], []
        for s in segs:
            if cur and not TERMINAL.search(cur[-1]) and s[:1].isupper():
                units.append(join_lines(cur))
                cur = []
            cur.append(s)
        if cur:
            units.append(join_lines(cur))
        notes["whisper_segment_boundaries_used"] = len(units)
        text = "\n".join(sent for u in units for sent in split_sentences(u))
    else:
        mode = "punkt"
        text = join_lines(segs)
    turns = [Turn(PREPARED, UNLABELED, text, mode)]
    turns, found = split_qa(turns, QA_MARKERS[company if company in QA_MARKERS else "fool"])
    if not found:
        flags.append("Q&A start not detected: all text under Prepared remarks")
    return turns, notes, flags


# ---------------------------------------------------------------------------
# Format dispatch
# ---------------------------------------------------------------------------

def detect_format(company, meta_text, body_lines):
    body = "\n".join(body_lines[:400])
    if company == "meta":
        return "meta"
    if company == "microsoft":
        return "msft"
    if company == "alphabet":
        return "alphabet"
    if "callstreet" in body.lower():
        return "factset"
    if "Motley Fool" in meta_text or "Prepared Remarks:" in body:
        return "fool"
    if any(SEGMENT.match(l) for l in body_lines[:20]):
        return "captions"
    raise ValueError(f"unknown transcript format for {company}")


MACHINE_FORMATS = {"captions"}


def parse(company, meta_text, body_lines):
    fmt = detect_format(company, meta_text, body_lines)
    if fmt == "meta":
        turns, notes, flags = parse_meta(body_lines, company)
    elif fmt == "msft":
        turns, notes, flags = parse_msft(body_lines, company)
    elif fmt == "factset":
        turns, notes, flags = parse_factset(body_lines, company)
    elif fmt == "fool":
        turns, notes, flags = parse_fool(body_lines, company)
    elif fmt == "alphabet":
        turns, notes, flags = parse_alphabet(body_lines, company)
    else:
        turns, notes, flags = parse_captions(body_lines, company, meta_text)
    notes["format"] = fmt
    return turns, notes, flags, fmt


# ---------------------------------------------------------------------------
# Rendering
# ---------------------------------------------------------------------------

def fmt_flags(flags):
    return "".join(f" ⚑ {f}" for f in flags)


def render(metadata, rows, total, file_flags):
    ai = [r for r in rows if r["kind"] == "ai"]
    auto = [r for r in rows if r["kind"] == "auto"]
    infra = [r for r in rows if r["kind"] == "infra"]
    out = [metadata, "- **Filter:** AI-sentence extraction, see FILTER_METHOD.md", "", "---", ""]
    out.append(f"**{len(ai)} AI sentences of {total} total**")
    out.append(f"(Borderline, listed at the end: {len(auto)} automation/robotics, "
               f"{len(infra)} infrastructure, none containing an AI term.)")
    if file_flags:
        out.append("")
        out.append("Source/parse flags: " + "; ".join(file_flags) + ".")
    out.append("")
    for section in (PREPARED, QA):
        sec_rows = [r for r in ai if r["section"] == section]
        out.append(f"## {section}")
        if not sec_rows:
            out.append("")
            out.append("_No AI sentences in this section._")
            out.append("")
            continue
        last_turn = None
        for n, r in enumerate(sec_rows, 1):
            if r["turn"] != last_turn:
                out.append("")
                out.append(f"### {r['speaker']}")
                last_turn = r["turn"]
            out.append(f"{n}. {r['text']}{fmt_flags(r['flags'])}")
        out.append("")
    for title, group in (("automation/robotics without an AI term", auto),
                         ("infrastructure without an AI term", infra)):
        out.append(f"## Borderline: {title}")
        out.append("")
        if not group:
            out.append("_None._")
        for n, r in enumerate(group, 1):
            out.append(f"{n}. [{r['section']} · {r['speaker']}] {r['text']}")
        out.append("")
    return "\n".join(out).rstrip() + "\n"


# ---------------------------------------------------------------------------
# Driver
# ---------------------------------------------------------------------------

def process_file(path, company):
    raw = path.read_text(encoding="utf-8")
    metadata, body = split_metadata(raw)
    turns, notes, file_flags, fmt = parse(company, metadata, body)
    machine = fmt in MACHINE_FORMATS
    rows = []
    for ti, turn in enumerate(turns):
        text = turn.text if turn.unit_mode == "lines" else join_lines(turn.text.split("\n"))
        for sent in split_sentences(text, turn.unit_mode):
            v = classify(sent, machine=machine, company=company)
            rows.append({"turn": ti, "section": turn.section, "speaker": turn.speaker,
                         "text": sent, "kind": v.kind, "terms": v.terms,
                         "flags": v.flags, "fp_ai": v.false_positive_ai})
    total = len(rows)
    ai_rows = [r for r in rows if r["kind"] == "ai"]
    flag_counts = Counter(f for r in ai_rows for f in r["flags"])

    parse_flags = list(file_flags)
    speakers = {t.speaker for t in turns}
    sections = {r["section"] for r in rows}
    if total == 0:
        parse_flags.append("PARSE FAILED: zero sentences")
    if not machine and not speakers - {UNLABELED, "Operator"}:
        parse_flags.append("no speaker labels found")
    if total and len(sections) < 2 and not any("Q&A start" in f for f in parse_flags):
        parse_flags.append("only one section detected")
    if total and not 400 <= total <= 900:
        parse_flags.append(f"{total} units, outside the typical 400-900")

    stats = {
        "company": company, "file": path.name, "period": path.stem.split("_", 1)[1],
        "format": fmt, "total": total, "ai": len(ai_rows),
        "ai_by_section": {s: sum(r["section"] == s for r in ai_rows) for s in (PREPARED, QA)},
        "total_by_section": {s: sum(r["section"] == s for r in rows) for s in (PREPARED, QA)},
        "borderline_auto": sum(r["kind"] == "auto" for r in rows),
        "borderline_infra": sum(r["kind"] == "infra" for r in rows),
        "false_positive_ai_tokens": sum(r["fp_ai"] for r in rows),
        "flag_counts": dict(flag_counts), "parse_notes": notes, "parse_flags": parse_flags,
        "speakers": sorted(speakers),
    }
    return render(metadata, rows, total, parse_flags), stats, rows


def pct(a, b):
    return f"{100 * a / b:.1f}%" if b else "n/a"


def write_index(all_stats):
    lines = ["# Earnings calls: AI-sentence extraction index", "",
             "One row per transcript. \"Total\" counts every sentence the parser kept after "
             "noise removal (for unpunctuated caption files, caption segments). \"AI\" counts "
             "sentences in the main AI sections (Prepared remarks + Q&A), excluding the "
             "Borderline sections. Method and validation: FILTER_METHOD.md.", ""]
    lines.append("| Company | Period | Format | Total | AI | % AI | AI in prepared / Q&A | "
                 "⚑ uncertain | Borderline auto / infra | Flags |")
    lines.append("|---|---|---|---:|---:|---:|---|---:|---|---|")
    totals = {}
    for company in COMPANIES:
        rows = sorted((s for s in all_stats.values() if s["company"] == company),
                      key=lambda s: s["file"])
        for s in rows:
            fc = s["flag_counts"]
            unc = fc.get("uncertain", 0)
            lines.append(
                f"| {company} | {s['period']} | {s['format']} | {s['total']} | {s['ai']} | "
                f"{pct(s['ai'], s['total'])} | {s['ai_by_section'][PREPARED]} / "
                f"{s['ai_by_section'][QA]} | {unc} | {s['borderline_auto']} / "
                f"{s['borderline_infra']} | {'; '.join(s['parse_flags']) or '-'} |")
            t = totals.setdefault(company, Counter())
            t.update(files=1, total=s["total"], ai=s["ai"], unc=unc,
                     auto=s["borderline_auto"], infra=s["borderline_infra"],
                     prep=s["ai_by_section"][PREPARED], qa=s["ai_by_section"][QA])
    lines += ["", "## Totals", "",
              "| Company | Files | Total | AI | % AI | AI in prepared / Q&A | ⚑ uncertain | "
              "Borderline auto / infra |",
              "|---|---:|---:|---:|---:|---|---:|---|"]
    grand = Counter()
    for company in COMPANIES:
        t = totals.get(company)
        if not t:
            continue
        grand.update(t)
        lines.append(f"| {company} | {t['files']} | {t['total']} | {t['ai']} | "
                     f"{pct(t['ai'], t['total'])} | {t['prep']} / {t['qa']} | {t['unc']} | "
                     f"{t['auto']} / {t['infra']} |")
    lines.append(f"| **all** | **{grand['files']}** | **{grand['total']}** | **{grand['ai']}** | "
                 f"**{pct(grand['ai'], grand['total'])}** | {grand['prep']} / {grand['qa']} | "
                 f"{grand['unc']} | {grand['auto']} / {grand['infra']} |")
    (OUT_DIR / "INDEX.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------

# Tokens the verbatim check may skip between two words of a sentence: things
# the parsers delete (page numbers, timestamps, caption tags, FactSet headers,
# speaker labels at a page/turn seam).
_SKIP = (r"(?:\s|\[\d+:\d{2}(?::\d{2})?\]|\[[A-Za-z_ ]+\]|>>|&gt;&gt;|\b\d{1,3}\b|"
         r"NVIDIA Corp\.\s*\(NVDA\s*\)|Q\d \d{4} Earnings Call|Corrected Transcript|"
         r"\d{1,2}\s*-[A-Za-z]{3}\s*-\d{4}|1-877-FACTSET\s+www\.callstreet\.com|"
         r"Copyright © \d{4}-\d{4} FactSet CallStreet, LLC)")


def verbatim_found(sentence, source):
    toks = sentence.split()
    parts = []
    for tok in toks:
        esc = re.escape(tok)
        esc = esc.replace(r"\-", r"-\s*").replace("‐", "‐\\s*")   # PDF hyphen wraps
        parts.append(esc)
    rx = re.compile(parts[0] + "".join(_SKIP + "+" + p for p in parts[1:]) if len(parts) > 1
                    else parts[0])
    return rx.search(source) is not None


RECALL_TERMS = [
    ("AI (uppercase token)", re.compile(r"(?<![A-Za-z])AIs?(?![A-Za-z])")),
    ("artificial intelligence", re.compile(r"artificial intelligence", re.I)),
    ("generative", re.compile(r"\bgenerative\b", re.I)),
    ("machine learning", re.compile(r"machine[- ]learning", re.I)),
    ("LLM", re.compile(r"\bLLMs?\b")),
    ("agentic", re.compile(r"\bagentic\b", re.I)),
    ("Copilot", re.compile(r"\bcopilots?\b", re.I)),
    ("Gemini", re.compile(r"\bGemini\b")),
    ("Llama", re.compile(r"\bLlama\b")),
    ("OpenAI", re.compile(r"\bopen ?ai\b", re.I)),
    ("Apple Intelligence", re.compile(r"apple intelligence", re.I)),
    ("Bedrock", re.compile(r"\bBedrock\b")),
]
RECALL_FILES = ["meta_2025_Q2", "microsoft_FY25_Q2", "nvidia_FY26_Q2", "nvidia_FY24_Q3",
                "alphabet_2025_Q1", "amazon_2023_Q4", "apple_FY25_Q2", "tesla_2024_Q2"]


def validate():
    results = {"seed": SEED}
    all_stats = json.loads((OUT_DIR / "_stats.json").read_text(encoding="utf-8"))

    # 1 + 5. coverage and time coverage
    missing, cov = [], {}
    for company in COMPANIES:
        src = sorted(p.stem for p in (SRC_DIR / company).glob(f"{company}_*.md"))
        out = sorted(p.stem[:-3] for p in (OUT_DIR / company).glob(f"{company}_*_ai.md"))
        cov[company] = {"source": len(src), "output": len(out)}
        missing += [s for s in src if s not in out]
    results["coverage"] = {"by_company": cov, "missing": missing}
    results["count_outliers"] = {k: s["total"] for k, s in all_stats.items()
                                 if not 400 <= s["total"] <= 900}
    results["parse_flags"] = {k: s["parse_flags"] for k, s in all_stats.items() if s["parse_flags"]}

    # parse everything once
    parsed = {}
    for company in COMPANIES:
        for path in sorted((SRC_DIR / company).glob(f"{company}_*.md")):
            _, stats, rows = process_file(path, company)
            parsed[path.stem] = (path, rows)

    # 2. recall: raw term hits in the transcript body vs hits inside AI sentences
    recall = {}
    for stem in RECALL_FILES:
        path, rows = parsed[stem]
        _, body = split_metadata(path.read_text(encoding="utf-8"))
        body_txt = html.unescape("\n".join(body))
        ai_txt = [r["text"] for r in rows if r["kind"] == "ai"]
        other = [r["text"] for r in rows if r["kind"] != "ai"]
        per = {}
        for name, rx in RECALL_TERMS:
            src_n = len(rx.findall(body_txt))
            if not src_n:
                continue
            out_n = sum(len(rx.findall(t)) for t in ai_txt)
            leaked = [t for t in other if rx.search(t)]
            per[name] = {"source": src_n, "in_ai_output": out_n,
                         "in_non_ai_output": len(leaked), "examples_not_ai": leaked[:3]}
        recall[stem] = per
    results["recall"] = recall

    # 3. precision sample (read by hand; judgments recorded in FILTER_METHOD.md)
    rng = random.Random(SEED)
    pool = [(stem, r) for stem, (_, rows) in parsed.items() for r in rows if r["kind"] == "ai"]
    sample = rng.sample(pool, 40)
    results["precision_sample"] = [{"file": s, "section": r["section"], "speaker": r["speaker"],
                                    "terms": r["terms"], "flags": r["flags"], "text": r["text"]}
                                   for s, r in sample]

    # 4. verbatim: every output sentence, plus the requested random 50
    src_cache = {stem: html.unescape(path.read_text(encoding="utf-8").split("\n---\n", 1)[1])
                 for stem, (path, _) in parsed.items()}
    fails, checked = [], 0
    for stem, (_, rows) in parsed.items():
        for r in rows:
            checked += 1
            if not verbatim_found(r["text"], src_cache[stem]):
                fails.append({"file": stem, "text": r["text"][:200]})
    every = [(stem, r) for stem, (_, rows) in parsed.items() for r in rows]
    s50 = random.Random(SEED + 1).sample(every, 50)
    s50_fail = [x for x in s50 if not verbatim_found(x[1]["text"], src_cache[x[0]])]
    results["verbatim"] = {"checked_all": checked, "failures_all": len(fails),
                           "failure_examples": fails[:25],
                           "sample50_failures": len(s50_fail)}

    # term / flag / false positive tallies
    results["flag_totals"] = dict(sum((Counter(s["flag_counts"]) for s in all_stats.values()),
                                      Counter()))
    results["false_positive_ai_tokens"] = sum(s["false_positive_ai_tokens"]
                                              for s in all_stats.values())
    fp_examples = [(stem, r["text"][:160]) for stem, (_, rows) in parsed.items()
                   for r in rows if r["fp_ai"]]
    results["false_positive_examples"] = fp_examples[:20]
    term_counter = Counter()
    for _, rows in parsed.values():
        for r in rows:
            if r["kind"] == "ai":
                term_counter.update(r["terms"])
    results["trigger_term_counts"] = dict(term_counter.most_common())
    only_weak = Counter()
    for _, rows in parsed.values():
        for r in rows:
            if r["kind"] == "ai" and "uncertain" in r["flags"]:
                only_weak.update(r["terms"])
    results["uncertain_trigger_counts"] = dict(only_weak.most_common())

    (OUT_DIR / "_validation.json").write_text(json.dumps(results, indent=2, ensure_ascii=False),
                                              encoding="utf-8")
    print(json.dumps({k: v for k, v in results.items() if k not in ("precision_sample", "recall")},
                     indent=1, ensure_ascii=False)[:6000])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--company", action="append", help="limit to company folder(s)")
    ap.add_argument("--only", help="process a single file stem, e.g. meta_2024_Q1")
    ap.add_argument("--validate", action="store_true", help="run the QA checks")
    args = ap.parse_args()
    if args.validate:
        validate()
        return

    companies = args.company or COMPANIES
    stats_path = OUT_DIR / "_stats.json"
    all_stats = json.loads(stats_path.read_text(encoding="utf-8")) if stats_path.exists() else {}

    for company in companies:
        for path in sorted((SRC_DIR / company).glob(f"{company}_*.md")):
            if args.only and path.stem != args.only:
                continue
            md, stats, _ = process_file(path, company)
            dest = OUT_DIR / company / f"{path.stem}_ai.md"
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_text(md, encoding="utf-8")
            all_stats[path.stem] = stats
            print(f"{path.stem:22s} {stats['format']:8s} total={stats['total']:4d} "
                  f"ai={stats['ai']:4d} (prep {stats['ai_by_section'][PREPARED]:3d} / "
                  f"qa {stats['ai_by_section'][QA]:3d}) unc={stats['flag_counts'].get('uncertain', 0):3d} "
                  f"auto={stats['borderline_auto']:3d} infra={stats['borderline_infra']:3d} "
                  f"{'; '.join(stats['parse_flags'])}")

    OUT_DIR.mkdir(exist_ok=True)
    stats_path.write_text(json.dumps(all_stats, indent=2, ensure_ascii=False), encoding="utf-8")
    write_index(all_stats)


if __name__ == "__main__":
    main()
