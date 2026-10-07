"""
Build the canonical structured earnings-call dataset (Gate 3, corrected in Gate 4).

Source of truth: the sentence-level AI filter, filter_earnings_calls.py. Its parsing,
sentence splitting and classification code is imported and re-run, read-only, on the
current raw transcripts in earnings_calls/. This is a *distinct current extraction
version* (see EXTRACTION_VERSION); it is not the committed earnings_calls_ai_only/
Markdown output, which is read only to report drift. Nothing in earnings_calls/ or
earnings_calls_ai_only/ is written.

Canonical-only corrections on top of the filter (Gate 4, every change is audited in
speaker_attribution_audit.csv by earnings_calls_canonical/gate4_validate.py):
  1. msft / alphabet formats: a `NAME, Firm:` speaker label the filter's parser left inside
     a turn starts a new turn for that speaker; the label text is removed from the unit,
     exactly as the parser removes the labels it does recognise.
  2. all labelled formats: a bare speaker name gets the descriptor the same transcript gives
     that name elsewhere, only when exactly one labelled speaker matches.
No other change to units, text or classification.

Writes <out>/ (default earnings_calls_canonical/)
  earnings_call_sentences.csv          one row per candidate AI unit (the measurement unit)
  earnings_call_labeling_passages.csv  one same-speaker-turn context passage per AI unit (annotation input only)
  earnings_call_borderline_review.csv  automation/robotics and infrastructure-only units (review route)
  earnings_call_call_units.csv         one row per present call: denominators and counts
  build_validation.json                coverage, counts, integrity checks, hashes

No semantic labels are created. Deterministic: same inputs -> byte-identical outputs.

Usage:
  python build_earnings_call_canonical.py
  python build_earnings_call_canonical.py --out <empty dir>   # e.g. for a clean-rebuild check
  python build_earnings_call_canonical.py --verify            # build twice in memory, compare, no writes
"""

import argparse
import csv
import difflib
import hashlib
import html
import io
import json
import platform
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path

import nltk

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
import earnings_call_scope as S          # noqa: E402
import filter_earnings_calls as F        # noqa: E402

OUT = ROOT / "earnings_calls_canonical"
COMMITTED = ROOT / "earnings_calls_ai_only"
BUILD_VERSION = "canonical-v2"

CONTEXT_RULE_VERSION = "ctx-v2-same-turn-pm1"
CONTEXT_RULE = ("anchor plus the immediately previous and next parsed unit of the same speaker turn "
                "(same speaker, same section, same call); never crosses a speaker change, the "
                "prepared-remarks/Q&A boundary or the transcript boundary; no neighbour -> anchor only. "
                "In caption/Whisper files the whole section is one unlabelled turn, so speaker "
                "continuity there is unverified (context_speaker_continuity says so).")

SECTION_CODE = {F.PREPARED: "prepared_remarks", F.QA: "qa"}

SENTENCE_FIELDS = [
    "sentence_id", "call_id", "company", "ticker", "period_label", "calendar_year", "calendar_quarter",
    "fiscal_or_calendar_label", "call_date", "call_date_source", "source_file", "source_url",
    "source_type", "parser_format", "unit_type", "section", "section_method", "speaker",
    "speaker_role", "speaker_status", "speaker_status_reason", "speaker_correction_rule",
    "turn_order_in_call", "sentence_order_in_call", "sentence_order_in_section", "text_verbatim",
    "word_count", "trigger_terms", "core_terms", "weak_terms", "is_uncertain", "is_safe_harbor",
    "is_context_dependent", "is_long", "call_parse_flags", "in_committed_filter_output",
    "extraction_version",
]
PASSAGE_FIELDS = [
    "passage_id", "anchor_sentence_id", "context_rule_version", "context_sentence_ids",
    "context_unit_kinds", "n_units", "text", "context_word_count", "context_before_text",
    "anchor_text", "context_after_text", "context_speaker_continuity", "call_id", "company",
    "ticker", "period_label", "calendar_year", "calendar_quarter", "call_date", "source_file",
    "source_type", "unit_type", "section", "anchor_speaker", "anchor_speaker_role",
    "anchor_speaker_status", "anchor_sentence_order_in_call", "trigger_terms", "is_uncertain",
    "is_safe_harbor", "is_context_dependent", "is_long", "passage_role", "extraction_version",
]
BORDERLINE_FIELDS = [
    "borderline_id", "unit_id", "call_id", "company", "ticker", "period_label", "calendar_year",
    "calendar_quarter", "source_file", "source_type", "unit_type", "section", "speaker",
    "speaker_role", "speaker_status", "sentence_order_in_call", "borderline_type", "matched_terms",
    "text_verbatim", "review_route", "extraction_version",
]
CALL_FIELDS = [
    "call_id", "company", "ticker", "period_label", "calendar_year", "calendar_quarter",
    "fiscal_or_calendar_label", "call_date", "call_date_source", "source_file", "source_sha256",
    "source_url", "source_type", "acquisition_status", "parser_format", "unit_type",
    "section_method", "units_comparable_to_sentences", "total_units", "total_units_prepared",
    "total_units_qa", "ai_units", "ai_units_prepared", "ai_units_qa", "ai_uncertain",
    "ai_context_dependent", "ai_safe_harbor", "ai_long", "borderline_automation",
    "borderline_infrastructure", "units_speaker_corrected", "units_text_changed_by_correction",
    "ai_units_speaker_unresolved", "ai_units_speaker_unverified", "call_parse_flags",
    "committed_filter_output", "committed_drift", "extraction_version",
]


def sha256_bytes(b):
    return hashlib.sha256(b).hexdigest()


def sha256_file(p):
    return sha256_bytes(Path(p).read_bytes())


def git_head():
    try:
        return subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, capture_output=True,
                              text=True, check=True).stdout.strip()
    except Exception:
        return "unavailable"


FILTER_SHA = sha256_file(ROOT / "filter_earnings_calls.py")
EXTRACTION_VERSION = f"filter_earnings_calls.py@sha256:{FILTER_SHA[:12]}/{BUILD_VERSION}"


# ---------------------------------------------------------------------------
# Speaker roles and statuses (no semantic labels; never guessed from outside the transcript)
# ---------------------------------------------------------------------------

TITLE_RX = re.compile(
    r"\b(?:CEO|CFO|COO|CTO|CBO|CAO|President|Chairman|Chairwoman|Officer|Chief|Director|VP|"
    r"Vice President|SVP|EVP|Head|Investor Relations|Treasurer|Counsel|Secretary|Founder|"
    r"Product Architect|Finance|Controller|Engineering|Autopilot)\b", re.I)


def speaker_role(speaker):
    """operator | unlabeled | unknown | analyst | company_representative | unresolved"""
    if speaker == "Operator":
        return "operator"
    if speaker == F.UNLABELED:
        return "unlabeled"
    if speaker.startswith("Unknown speaker"):
        return "unknown"
    _, sep, desc = speaker.partition(", ")
    if not sep:
        return "unresolved"
    if re.search(r"\bAnalyst\b", desc):
        return "analyst"
    if TITLE_RX.search(desc):
        return "company_representative"
    return "analyst"                     # descriptor is a firm (operator intro / roster / label)


META_LABEL_LOSS = ("Meta raw text from the original corpus can lack inline Q&A speaker labels "
                   "(verified for meta_2022_Q4 against the official PDF in Gate 2); this row's "
                   "speaker cannot be verified from the raw file and is not changed")


# Acquired raw files whose inline speaker labels were misplaced by the Gate 2 PDF extraction
# (pdftotext -layout). Found in Gate 4 by comparing label positions with pdftotext -raw of the
# cached official PDF (gate4_validate.py: B1b). Raw text may not be changed in Gate 4, so every
# labelled speaker in these calls is quarantined, not corrected. Sections were checked and are not affected.
RAW_LABEL_MISPLACEMENT = {
    "meta_2022_Q2": "15 label positions in the raw file are not in pdftotext -raw of the official PDF (12 missing)",
    "meta_2022_Q3": "13 label positions in the raw file are not in pdftotext -raw of the official PDF (10 missing)",
}


def speaker_status(speaker, corrected, company, section, acquisition_status, call_id=""):
    role = speaker_role(speaker)
    if role == "unlabeled":
        return "unlabeled_source", "caption/Whisper transcript has no speaker labels"
    if call_id in RAW_LABEL_MISPLACEMENT:
        return ("unverified_raw_label_misplacement",
                "Gate 2 PDF extraction (pdftotext -layout) misplaced inline speaker labels in this raw file: "
                + RAW_LABEL_MISPLACEMENT[call_id] + "; speaker not reliable until the raw file is re-extracted")
    if role == "unknown":
        return "unknown_speaker_in_source", "source transcript itself says 'Unknown speaker'"
    if role == "unresolved":
        return "unresolved_bare_name", "transcript gives no title or firm for this name anywhere"
    if (company == "meta" and section == F.QA and role != "operator"
            and acquisition_status == "already_present"):
        return "unverified_meta_label_loss_risk", META_LABEL_LOSS
    if role == "operator":
        return "operator", ""
    return ("resolved_corrected", "corrected from raw-text label (see audit)") if corrected \
        else ("resolved", "")


# ---------------------------------------------------------------------------
# Canonical speaker corrections
# ---------------------------------------------------------------------------

_TOK = r"(?:[A-Z][a-zA-Z'’-]+)"
LABEL_FIX = {
    # MICROSOFT: "KEITH WEISS, Morgan Stanley: ..." at a line start (ALL-CAPS name)
    "msft": re.compile(r"(?:^|(?<=\n))([A-Z][A-Z.'’-]+(?: [A-Z][A-Z.'’-]+){1,3}), ([A-Z][^:\n]{1,60}?):\s"),
    # ALPHABET: "Brian Nowak, Morgan Stanley: ..." (two-token name, optional middle initial)
    "alphabet": re.compile(r"(?<![\w.'’-])(" + _TOK + r"(?: [A-Z]\.)? " + _TOK + r"), "
                           r"([A-Z][^:?!\n]{1,60}?):\s"),
}


def correct_turns(turns, fmt):
    """Returns (turns, info). info[i] = dict(orig_turn, rule, evidence) for each new turn."""
    rx = LABEL_FIX.get(fmt)
    new, info = [], []
    for ti, t in enumerate(turns):
        if not rx:
            new.append(F.Turn(t.section, t.speaker, t.text, t.unit_mode))
            info.append(dict(orig_turn=ti, rule="", evidence=""))
            continue
        last, spk, rule, ev = 0, t.speaker, "", ""
        for m in rx.finditer(t.text):
            chunk = t.text[last:m.start()]
            if chunk.strip():
                new.append(F.Turn(t.section, spk, chunk.strip(), t.unit_mode))
                info.append(dict(orig_turn=ti, rule=rule, evidence=ev))
            spk = f"{F.display_name(m.group(1))}, {m.group(2).strip()}"
            rule, ev = f"{fmt}_name_comma_firm_label", m.group(0).strip()
            last = m.end()
        chunk = t.text[last:]
        if chunk.strip():
            new.append(F.Turn(t.section, spk, chunk.strip() if last else chunk, t.unit_mode))
            info.append(dict(orig_turn=ti, rule=rule, evidence=ev))

    # bare names -> the unique labelled variant of the same name in this transcript
    labelled = sorted({t.speaker for t in new if ", " in t.speaker})
    for t, inf in zip(new, info):
        s = t.speaker
        if ", " in s or s in ("Operator", F.UNLABELED) or s.startswith("Unknown speaker"):
            continue
        cands = sorted({L for L in labelled if F.names_match(L.split(", ")[0], s)})
        if len(cands) == 1:
            t.speaker = cands[0]
            inf["rule"] = inf["rule"] or "same_transcript_name_propagation"
            inf["evidence"] = inf["evidence"] or f"bare label '{s}'; same transcript labels '{cands[0]}'"
    return new, info


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def unit_type(fmt, unit_mode, whisper):
    if fmt != "captions":
        return "sentence"
    if whisper:
        return "whisper_unit"
    return "caption_segment" if unit_mode == "lines" else "caption_sentence"


def section_method(fmt, body, flags):
    if any("Q&A start not detected" in f for f in flags):
        return "not_detected_all_prepared"
    if fmt == "factset":
        return "explicit_section_header"
    if fmt == "fool":
        return ("explicit_section_header" if re.search(r"^\s*Questions (?:&|and) Answers:\s*$", body, re.M)
                else "transition_phrase_heuristic")
    if fmt in ("meta", "alphabet"):
        return "first_operator_turn_after_management"
    return "transition_phrase_heuristic"


def committed_ai_units(company, stem):
    """Multiset of (section, text) in the committed *_ai.md main AI sections, or None."""
    p = COMMITTED / company / f"{stem}_ai.md"
    if not p.exists():
        return None
    out, section = Counter(), None
    for line in p.read_text(encoding="utf-8").splitlines():
        if line.startswith("## "):
            section = {"## Prepared remarks": F.PREPARED, "## Q&A": F.QA}.get(line.strip())
            continue
        m = re.match(r"^\d+\. (.*)$", line)
        if section and m:
            out[(section, m.group(1).split(" ⚑ ")[0])] += 1
    return out


def unit_id(company, period, order, text):
    return f"{company}_{period}_u{order:04d}_{sha256_bytes(text.encode('utf-8'))[:10]}"


sentence_id = unit_id


def split_units(turns, fmt, company, machine, whisper):
    units = []
    for ti, turn in enumerate(turns):
        text = turn.text if turn.unit_mode == "lines" else F.join_lines(turn.text.split("\n"))
        for sent in F.split_sentences(text, turn.unit_mode):
            v = F.classify(sent, machine=machine, company=company)
            units.append(dict(turn=ti, section=turn.section, speaker=turn.speaker, text=sent,
                              kind=v.kind, terms=v.terms, flags=v.flags,
                              unit_type=unit_type(fmt, turn.unit_mode, whisper)))
    for i, u in enumerate(units, 1):
        u["order"] = i
    return units


# ---------------------------------------------------------------------------
# Per-call extraction
# ---------------------------------------------------------------------------

def extract_call(company, period):
    path = S.raw_path(company, period)
    raw = path.read_text(encoding="utf-8")
    metadata, body_lines = F.split_metadata(raw)
    turns, notes, file_flags, fmt = F.parse(company, metadata, body_lines)
    machine = fmt in F.MACHINE_FORMATS
    whisper = "whisper" in metadata.lower()

    # 1. the filter's own result, unchanged (reference for drift and for the audit)
    ref = split_units(turns, fmt, company, machine, whisper)
    _, stats, pf = F.process_file(path, company)
    if [(r["section"], r["speaker"], r["text"], r["kind"]) for r in pf] != \
       [(u["section"], u["speaker"], u["text"], u["kind"]) for u in ref]:
        raise RuntimeError(f"{path.name}: extraction differs from filter_earnings_calls.process_file")

    # 2. canonical: corrected turns
    cturns, info = correct_turns(turns, fmt)
    units = split_units(cturns, fmt, company, machine, whisper)
    for u in units:
        u["rule"], u["evidence"], u["orig_turn"] = (info[u["turn"]]["rule"], info[u["turn"]]["evidence"],
                                                    info[u["turn"]]["orig_turn"])

    # align canonical units to filter units (same text, or text with the label removed)
    sm = difflib.SequenceMatcher(None, [r["text"] for r in ref], [u["text"] for u in units], autojunk=False)
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal" or (tag == "replace" and i2 - i1 == j2 - j1):
            for a, b in zip(range(i1, i2), range(j1, j2)):
                units[b]["ref"] = ref[a]
        else:
            for b in range(j1, j2):
                units[b]["ref"] = None
    for u in units:
        r = u.get("ref")
        u["speaker_changed"] = bool(r) and r["speaker"] != u["speaker"]
        u["text_changed"] = not r or r["text"] != u["text"]

    sec_order = Counter()
    for u in units:
        sec_order[u["section"]] += 1
        u["order_in_section"] = sec_order[u["section"]]
        u["uid"] = unit_id(company, period, u["order"], u["text"])
    for r in ref:
        r["uid"] = unit_id(company, period, r["order"], r["text"])

    body = "\n".join(body_lines)
    flags = list(stats["parse_flags"])
    return dict(path=path, raw=raw, metadata=metadata, body=body, fmt=fmt, flags=flags,
                stats=stats, units=units, ref=ref, section_method=section_method(fmt, body, flags))


# ---------------------------------------------------------------------------
# Build
# ---------------------------------------------------------------------------

def build():
    manifest = {(r["company"], r["period_label"]): r for r in S.manifest_rows(parse=False)}
    sentences, passages, borderline, calls_out, changes = [], [], [], [], []
    drift, verbatim_fail, verbatim_checked = {}, [], 0
    source_hashes = {}
    core_names = {n for n, _ in F.CORE_TERMS} | {"AI (machine transcript, any case)"}

    for company, period, cy, cq in S.expected_calls():
        m = manifest[(company, period)]
        if not S.raw_path(company, period).exists():
            continue
        c = extract_call(company, period)
        stem = call_id = f"{company}_{period}"
        source_file = c["path"].relative_to(ROOT).as_posix()
        source_hashes[source_file] = sha256_bytes(c["raw"].encode("utf-8"))
        units = c["units"]
        utypes = sorted({u["unit_type"] for u in units})
        common = dict(call_id=call_id, company=company, ticker=S.TICKER[company], period_label=period,
                      calendar_year=cy, calendar_quarter=cq)
        flags_str = "; ".join(c["flags"])

        # drift: the filter's own (uncorrected) AI units vs the committed Markdown
        committed = committed_ai_units(company, stem)
        ref_ai = Counter((r["section"], r["text"]) for r in c["ref"] if r["kind"] == "ai")
        if committed is None:
            drift[stem] = {"status": "no_committed_file", "filter_ai_units": sum(ref_ai.values())}
        else:
            only_new, only_old = ref_ai - committed, committed - ref_ai
            drift[stem] = {"status": "match" if not only_new and not only_old else "differs",
                           "filter_ai_units": sum(ref_ai.values()), "committed_ai_units": sum(committed.values()),
                           "only_in_current_filter_run": sum(only_new.values()),
                           "only_in_committed": sum(only_old.values()),
                           "examples_only_in_committed": [t[:160] for (_, t) in list(only_old)[:3]]}

        src_for_verbatim = html.unescape(c["body"])
        for u in units:
            sec = SECTION_CODE[u["section"]]
            role = speaker_role(u["speaker"])
            st, why = speaker_status(u["speaker"], u["speaker_changed"], company, u["section"],
                                     m["acquisition_status"], call_id)
            u.update(role=role, status=st, status_reason=why, sec=sec)
            if u["speaker_changed"] or u["text_changed"]:
                r = u.get("ref")
                changes.append(dict(
                    sentence_id=u["uid"], old_sentence_id=r["uid"] if r else "", call_id=call_id,
                    company=company, period_label=period, kind=u["kind"], section=sec,
                    old_speaker=r["speaker"] if r else "", new_speaker=u["speaker"],
                    old_role=speaker_role(r["speaker"]) if r else "", new_role=role,
                    old_text=r["text"] if r else "", new_text=u["text"],
                    rule=u["rule"], evidence=u["evidence"], new_status=st))
            if u["kind"] in ("auto", "infra"):
                bterms = (F.AUTOMATION_TERMS if u["kind"] == "auto" else F.INFRA_TERMS).findall(u["text"])
                borderline.append(dict(
                    borderline_id=u["uid"].replace("_u", "_b", 1), unit_id=u["uid"], **common,
                    source_file=source_file, source_type=m["source_type"], unit_type=u["unit_type"],
                    section=sec, speaker=u["speaker"], speaker_role=role, speaker_status=st,
                    sentence_order_in_call=u["order"],
                    borderline_type="automation_robotics_no_ai_term" if u["kind"] == "auto"
                    else "infrastructure_no_ai_term",
                    matched_terms="; ".join(sorted(set(t.lower() for t in bterms))),
                    text_verbatim=u["text"], review_route="gate5_human_uncertainty_review",
                    extraction_version=EXTRACTION_VERSION))

        by_order = {u["order"]: u for u in units}
        for u in units:
            if u["kind"] != "ai":
                continue
            verbatim_checked += 1
            if not F.verbatim_found(u["text"], src_for_verbatim):
                verbatim_fail.append({"sentence_id": u["uid"], "text": u["text"][:200]})
            r = u.get("ref")
            in_committed = ("no_committed_file" if committed is None else
                            "yes" if r and committed.get((r["section"], r["text"])) else "no")
            row = dict(
                sentence_id=u["uid"], **common, fiscal_or_calendar_label=m["fiscal_or_calendar_label"],
                call_date=m["call_date"], call_date_source=m["call_date_source"], source_file=source_file,
                source_url=m["source_url"], source_type=m["source_type"], parser_format=c["fmt"],
                unit_type=u["unit_type"], section=u["sec"], section_method=c["section_method"],
                speaker=u["speaker"], speaker_role=u["role"], speaker_status=u["status"],
                speaker_status_reason=u["status_reason"],
                speaker_correction_rule=u["rule"] if u["speaker_changed"] else "",
                turn_order_in_call=u["turn"] + 1, sentence_order_in_call=u["order"],
                sentence_order_in_section=u["order_in_section"], text_verbatim=u["text"],
                word_count=len(u["text"].split()), trigger_terms="; ".join(u["terms"]),
                core_terms="; ".join(t for t in u["terms"] if t in core_names),
                weak_terms="; ".join(t for t in u["terms"] if t not in core_names),
                is_uncertain=int("uncertain" in u["flags"]),
                is_safe_harbor=int("uncertain: safe-harbor" in u["flags"]),
                is_context_dependent=int("context-dependent" in u["flags"]),
                is_long=int("long" in u["flags"]), call_parse_flags=flags_str,
                in_committed_filter_output=in_committed, extraction_version=EXTRACTION_VERSION)
            sentences.append(row)

            # context passage: same speaker turn, previous and next unit only
            prev_u = by_order.get(u["order"] - 1)
            next_u = by_order.get(u["order"] + 1)
            before = [prev_u] if prev_u and prev_u["turn"] == u["turn"] else []
            after = [next_u] if next_u and next_u["turn"] == u["turn"] else []
            ctx = before + [u] + after
            if not before and not after:
                cont = "anchor_only_no_same_turn_neighbour"
            elif u["status"] == "unlabeled_source":
                cont = "same_turn_unlabelled_source_speaker_unverified"
            elif u["status"] == "unverified_meta_label_loss_risk":
                cont = "same_turn_meta_label_loss_risk"
            elif u["status"] == "unverified_raw_label_misplacement":
                cont = "same_turn_raw_label_misplacement_risk"
            else:
                cont = "same_labelled_speaker_turn"
            text = " ".join(x["text"] for x in ctx)
            kinds = {"ai": "ai", "auto": "borderline_automation", "infra": "borderline_infrastructure",
                     "out": "non_ai"}
            passages.append(dict(
                passage_id="P2_" + u["uid"], anchor_sentence_id=u["uid"],
                context_rule_version=CONTEXT_RULE_VERSION,
                context_sentence_ids=" ".join(x["uid"] for x in ctx),
                context_unit_kinds=" ".join(kinds[x["kind"]] for x in ctx), n_units=len(ctx),
                text=text, context_word_count=len(text.split()),
                context_before_text=" ".join(x["text"] for x in before), anchor_text=u["text"],
                context_after_text=" ".join(x["text"] for x in after), context_speaker_continuity=cont,
                **common, call_date=m["call_date"], source_file=source_file, source_type=m["source_type"],
                unit_type=u["unit_type"], section=u["sec"], anchor_speaker=u["speaker"],
                anchor_speaker_role=u["role"], anchor_speaker_status=u["status"],
                anchor_sentence_order_in_call=u["order"], trigger_terms=row["trigger_terms"],
                is_uncertain=row["is_uncertain"], is_safe_harbor=row["is_safe_harbor"],
                is_context_dependent=row["is_context_dependent"], is_long=row["is_long"],
                passage_role="annotation_input_only; map labels back to anchor_sentence_id",
                extraction_version=EXTRACTION_VERSION))

        st_ = c["stats"]
        ai_units = [u for u in units if u["kind"] == "ai"]
        fc = Counter(f for u in ai_units for f in u["flags"])
        sec_count = Counter(u["section"] for u in units)
        ai_sec = Counter(u["section"] for u in ai_units)
        calls_out.append(dict(
            **common, fiscal_or_calendar_label=m["fiscal_or_calendar_label"], call_date=m["call_date"],
            call_date_source=m["call_date_source"], source_file=source_file,
            source_sha256=source_hashes[source_file], source_url=m["source_url"],
            source_type=m["source_type"], acquisition_status=m["acquisition_status"], parser_format=c["fmt"],
            unit_type="; ".join(utypes), section_method=c["section_method"],
            units_comparable_to_sentences=int(utypes == ["sentence"] or utypes == ["caption_sentence"]),
            total_units=len(units), total_units_prepared=sec_count[F.PREPARED], total_units_qa=sec_count[F.QA],
            ai_units=len(ai_units), ai_units_prepared=ai_sec[F.PREPARED], ai_units_qa=ai_sec[F.QA],
            ai_uncertain=fc.get("uncertain", 0), ai_context_dependent=fc.get("context-dependent", 0),
            ai_safe_harbor=fc.get("uncertain: safe-harbor", 0), ai_long=fc.get("long", 0),
            borderline_automation=sum(u["kind"] == "auto" for u in units),
            borderline_infrastructure=sum(u["kind"] == "infra" for u in units),
            units_speaker_corrected=sum(u["speaker_changed"] for u in units),
            units_text_changed_by_correction=sum(u["text_changed"] for u in units),
            ai_units_speaker_unresolved=sum(u["status"] == "unresolved_bare_name" for u in ai_units),
            ai_units_speaker_unverified=sum(u["status"].startswith("unverified") for u in ai_units),
            call_parse_flags=flags_str,
            committed_filter_output="present" if committed is not None else "absent",
            committed_drift=drift[stem]["status"], extraction_version=EXTRACTION_VERSION))
        # filter totals vs canonical totals (corrections may only move label text)
        c["delta"] = (st_["total"], len(units), st_["ai"], len(ai_units))

    validation = make_validation(manifest, sentences, passages, borderline, calls_out, drift,
                                 verbatim_checked, verbatim_fail, source_hashes, changes)
    return sentences, passages, borderline, calls_out, validation, changes


REQUIRED_NONEMPTY = ["sentence_id", "call_id", "company", "ticker", "period_label", "calendar_year",
                     "calendar_quarter", "fiscal_or_calendar_label", "call_date_source", "source_file",
                     "source_type", "parser_format", "unit_type", "section", "section_method", "speaker",
                     "speaker_role", "speaker_status", "turn_order_in_call", "sentence_order_in_call",
                     "sentence_order_in_section", "text_verbatim", "word_count", "trigger_terms",
                     "is_uncertain", "is_safe_harbor", "is_context_dependent", "is_long",
                     "in_committed_filter_output", "extraction_version"]
ALLOWED_BLANK = {"call_date": "not stated in the source file (never inferred)",
                 "source_url": "raw-file metadata gives no URL (Nvidia FY26 Q1 - FY27 Q2)"}


def make_validation(manifest, sentences, passages, borderline, calls_out, drift,
                    verbatim_checked, verbatim_fail, source_hashes, changes):
    def count(rows, key):
        return dict(sorted(Counter(str(r[key]) for r in rows).items()))

    ids = [r["sentence_id"] for r in sentences]
    idset = set(ids)
    pids = [r["passage_id"] for r in passages]
    bids = [r["borderline_id"] for r in borderline]
    missing_req = {f: sum(1 for r in sentences if str(r[f]).strip() == "") for f in REQUIRED_NONEMPTY}
    blanks = {f: {"rows": sum(1 for r in sentences if not str(r[f]).strip()),
                  "calls": sorted({r["call_id"] for r in sentences if not str(r[f]).strip()}),
                  "reason": why} for f, why in ALLOWED_BLANK.items()}
    filter_files = sorted(p.relative_to(ROOT).as_posix() for c in S.COMPANIES
                          for p in (S.CALLS / c).glob(f"{c}_*.md"))
    committed_files = sorted(p.relative_to(ROOT).as_posix() for c in S.COMPANIES
                             for p in (COMMITTED / c).glob(f"{c}_*_ai.md"))
    sent_per_call = Counter(r["call_id"] for r in sentences)
    pass_per_call = Counter(r["call_id"] for r in passages)
    coverage = {r["call_id"]: {"source_file": r["source_file"], "ai_rows": sent_per_call.get(r["call_id"], 0),
                               "passage_rows": pass_per_call.get(r["call_id"], 0),
                               "total_units": r["total_units"], "committed_filter_output": r["committed_filter_output"]}
                for r in calls_out}
    missing_periods = [{k: m[k] for k in ("company", "period_label", "calendar_year", "calendar_quarter",
                                          "availability_status", "acquisition_status")}
                       for m in manifest.values() if not m["raw_file_path"]]
    orphans = [p["passage_id"] for p in passages if p["anchor_sentence_id"] not in idset]
    flags = {f: sum(int(r[f]) for r in sentences)
             for f in ("is_uncertain", "is_safe_harbor", "is_context_dependent", "is_long")}
    return {
        "build_version": BUILD_VERSION,
        "extraction_version": EXTRACTION_VERSION,
        "status_note": ("Build integrity checks only, run by code. Not a human validation and not a recall/"
                        "precision validation of the AI filter. Gate 4 results: gate4_validation.json."),
        "counts": {
            "source_raw_transcript_files_found": len(filter_files),
            "committed_sentence_filter_files_found": len(committed_files),
            "calls_processed": len(calls_out),
            "canonical_sentence_rows": len(sentences),
            "canonical_passage_rows": len(passages),
            "borderline_review_rows": len(borderline),
            "total_parsed_units_all_calls": sum(r["total_units"] for r in calls_out),
        },
        "by_company": count(sentences, "company"),
        "by_calendar_quarter": dict(sorted(Counter(f"{r['calendar_year']}Q{r['calendar_quarter']}"
                                                   for r in sentences).items())),
        "by_company_period": count(sentences, "call_id"),
        "by_section": count(sentences, "section"),
        "by_source_type": count(sentences, "source_type"),
        "by_unit_type": count(sentences, "unit_type"),
        "by_speaker_role": count(sentences, "speaker_role"),
        "by_speaker_status": count(sentences, "speaker_status"),
        "by_section_method": count(sentences, "section_method"),
        "passages_by_context_continuity": count(passages, "context_speaker_continuity"),
        "passages_by_n_units": count(passages, "n_units"),
        "flag_counts": flags,
        "borderline_by_type": count(borderline, "borderline_type"),
        "speaker_corrections": {
            "units_changed_any_kind": len(changes),
            "units_speaker_changed": sum(1 for c in changes if c["old_speaker"] != c["new_speaker"]),
            "units_text_changed_label_removed": sum(1 for c in changes if c["old_text"] != c["new_text"]),
            "ai_rows_speaker_changed": sum(1 for c in changes if c["kind"] == "ai"
                                           and c["old_speaker"] != c["new_speaker"]),
            "by_rule": dict(sorted(Counter(c["rule"] for c in changes).items())),
        },
        "integrity": {
            "duplicate_sentence_ids": len(ids) - len(idset),
            "duplicate_passage_ids": len(pids) - len(set(pids)),
            "duplicate_borderline_ids": len(bids) - len(set(bids)),
            "orphaned_passage_anchors": len(orphans),
            "one_passage_per_sentence": len(passages) == len(sentences) and not orphans,
            "missing_required_field_counts": missing_req,
            "missing_required_field_total": sum(missing_req.values()),
            "allowed_blank_fields": blanks,
            "semantic_label_columns_present": False,
            "filter_reference_rows_match_process_file": True,
            "verbatim_check": {"method": "filter_earnings_calls.verbatim_found against the raw body",
                               "checked_ai_rows": verbatim_checked, "failures": len(verbatim_fail),
                               "failure_examples": verbatim_fail[:25]},
        },
        "source_file_to_output_coverage": coverage,
        "calls_with_zero_ai_rows": sorted(k for k, v in coverage.items() if v["ai_rows"] == 0),
        "committed_output_drift": {"summary": dict(Counter(d["status"] for d in drift.values())),
                                   "differs": {k: v for k, v in drift.items() if v["status"] == "differs"},
                                   "no_committed_file": sorted(k for k, v in drift.items()
                                                               if v["status"] == "no_committed_file")},
        "missing_or_unavailable_periods": missing_periods,
        "manifest_counts": dict(Counter(m["acquisition_status"] for m in manifest.values())),
        "reproducibility": {
            "command": "python build_earnings_call_canonical.py",
            "python": platform.python_version(),
            "nltk": nltk.__version__,
            "filter_earnings_calls.py_sha256": FILTER_SHA,
            "build_earnings_call_canonical.py_sha256": sha256_file(Path(__file__)),
            "earnings_call_scope.py_sha256": sha256_file(ROOT / "earnings_call_scope.py"),
            "source_file_sha256": source_hashes,
            "context_rule_version": CONTEXT_RULE_VERSION,
            "context_rule": CONTEXT_RULE,
            "sentence_id_rule": "<company>_<period_label>_u<4-digit order in call>_<first 10 hex of sha256(text_verbatim)>",
            "note": "git HEAD is deliberately not embedded so outputs do not change with unrelated commits",
        },
    }


def to_csv(rows, fields):
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=fields, lineterminator="\n")
    w.writeheader()
    w.writerows(rows)
    return buf.getvalue()


def render(result):
    sentences, passages, borderline, calls_out, validation, _ = result
    files = {
        "earnings_call_sentences.csv": to_csv(sentences, SENTENCE_FIELDS),
        "earnings_call_labeling_passages.csv": to_csv(passages, PASSAGE_FIELDS),
        "earnings_call_borderline_review.csv": to_csv(borderline, BORDERLINE_FIELDS),
        "earnings_call_call_units.csv": to_csv(calls_out, CALL_FIELDS),
    }
    validation["output_sha256"] = {k: sha256_bytes(v.encode("utf-8")) for k, v in files.items()}
    files["build_validation.json"] = json.dumps(validation, indent=2, ensure_ascii=False) + "\n"
    return files


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--verify", action="store_true", help="build twice in memory and compare; no writes")
    ap.add_argument("--out", default=str(OUT), help="output directory (default earnings_calls_canonical/)")
    args = ap.parse_args()
    a = render(build())
    if args.verify:
        b = render(build())
        same = {k: a[k] == b[k] for k in a}
        print(json.dumps(same, indent=1))
        sys.exit(0 if all(same.values()) else 1)
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    for name, text in a.items():
        (out / name).write_text(text, encoding="utf-8", newline="")
    v = json.loads(a["build_validation.json"])
    print(json.dumps({"counts": v["counts"], "speaker_corrections": v["speaker_corrections"],
                      "integrity": {k: v["integrity"][k] for k in (
                          "duplicate_sentence_ids", "orphaned_passage_anchors", "missing_required_field_total")},
                      "verbatim_failures": v["integrity"]["verbatim_check"]["failures"],
                      "drift": v["committed_output_drift"]["summary"],
                      "passages": v["passages_by_context_continuity"]}, indent=1))


if __name__ == "__main__":
    main()
