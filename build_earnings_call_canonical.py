"""
Build the canonical structured earnings-call dataset (Gate 3).

Source of truth: the sentence-level AI filter, filter_earnings_calls.py. Its parsing,
sentence splitting and classification code is imported and re-run, read-only, on the
current raw transcripts in earnings_calls/. Nothing in earnings_calls/ or
earnings_calls_ai_only/ is written. The committed *_ai.md outputs are read only to report
drift between them and today's raw files.

Writes earnings_calls_canonical/
  earnings_call_sentences.csv          one row per candidate AI unit (the measurement unit)
  earnings_call_labeling_passages.csv  one bounded-context passage per AI unit (for annotation only)
  earnings_call_borderline_review.csv  automation/robotics and infrastructure-only units (review route)
  earnings_call_call_units.csv         one row per present call: denominators and counts
  build_validation.json                coverage, counts, integrity checks, hashes

No semantic labels are created. Deterministic: same inputs -> byte-identical outputs.

Usage:
  python build_earnings_call_canonical.py
  python build_earnings_call_canonical.py --verify   # build twice in memory, compare, no writes
"""

import argparse
import csv
import hashlib
import html
import io
import json
import platform
import re
import subprocess
import sys
from collections import Counter, defaultdict
from pathlib import Path

import nltk

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
import earnings_call_scope as S          # noqa: E402
import filter_earnings_calls as F        # noqa: E402

OUT = ROOT / "earnings_calls_canonical"
COMMITTED = ROOT / "earnings_calls_ai_only"
BUILD_VERSION = "canonical-v1"

K_BEFORE, K_AFTER = 2, 1                 # passage context rule (units, same call + same section)
CONTEXT_RULE = (f"up to {K_BEFORE} preceding and {K_AFTER} following parsed units of the same call "
                f"and same section, in call order; may cross a speaker turn (flagged); never crosses "
                f"the prepared-remarks/Q&A boundary")

SECTION_CODE = {F.PREPARED: "prepared_remarks", F.QA: "qa"}

SENTENCE_FIELDS = [
    "sentence_id", "call_id", "company", "ticker", "period_label", "calendar_year", "calendar_quarter",
    "fiscal_or_calendar_label", "call_date", "call_date_source", "source_file", "source_url",
    "source_type", "parser_format", "unit_type", "section", "section_method", "speaker",
    "speaker_role", "speaker_attribution_warning", "turn_order_in_call", "sentence_order_in_call",
    "sentence_order_in_section", "text_verbatim", "word_count", "trigger_terms", "core_terms",
    "weak_terms", "is_uncertain", "is_safe_harbor", "is_context_dependent", "is_long",
    "call_parse_flags", "in_committed_filter_output", "extraction_version",
]
PASSAGE_FIELDS = [
    "passage_id", "anchor_sentence_id", "call_id", "company", "ticker", "period_label",
    "calendar_year", "calendar_quarter", "call_date", "source_file", "source_type", "unit_type",
    "section", "anchor_speaker", "anchor_speaker_role", "speaker_attribution_warning",
    "anchor_sentence_order_in_call", "trigger_terms", "is_uncertain", "is_safe_harbor",
    "is_context_dependent", "is_long", "context_rule", "context_before_orders",
    "context_after_orders", "context_crosses_speaker_turn", "context_speakers",
    "context_before_text", "anchor_text", "context_after_text", "passage_text",
    "passage_word_count", "passage_role", "extraction_version",
]
BORDERLINE_FIELDS = [
    "borderline_id", "call_id", "company", "ticker", "period_label", "calendar_year",
    "calendar_quarter", "source_file", "source_type", "unit_type", "section", "speaker",
    "speaker_role", "sentence_order_in_call", "borderline_type", "matched_terms",
    "text_verbatim", "review_route", "extraction_version",
]
CALL_FIELDS = [
    "call_id", "company", "ticker", "period_label", "calendar_year", "calendar_quarter",
    "fiscal_or_calendar_label", "call_date", "call_date_source", "source_file", "source_sha256",
    "source_url", "source_type", "acquisition_status", "parser_format", "unit_type",
    "section_method", "units_comparable_to_sentences", "total_units", "total_units_prepared",
    "total_units_qa", "ai_units", "ai_units_prepared", "ai_units_qa", "ai_uncertain",
    "ai_context_dependent", "ai_safe_harbor", "ai_long", "borderline_automation",
    "borderline_infrastructure", "speaker_attribution_warning_units", "call_parse_flags",
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
# Row-level derivations (no semantic labels)
# ---------------------------------------------------------------------------

TITLE_RX = re.compile(
    r"\b(?:CEO|CFO|COO|CTO|CBO|CAO|President|Chairman|Chairwoman|Officer|Chief|Director|VP|"
    r"Vice President|SVP|EVP|Head|Investor Relations|Treasurer|Counsel|Secretary|Founder|"
    r"Product Architect|Finance|Controller|Engineering|Autopilot)\b", re.I)


def speaker_role(speaker):
    """Rule-based role from the speaker label the filter produced; never guessed from a bare name.
    operator | unlabeled | unknown | analyst | company_representative | unresolved"""
    if speaker == "Operator":
        return "operator"
    if speaker == F.UNLABELED:
        return "unlabeled"
    if speaker.startswith("Unknown speaker"):
        return "unknown"
    name, sep, desc = speaker.partition(", ")
    if not sep:
        return "unresolved"
    if re.search(r"\bAnalyst\b", desc):
        return "analyst"
    if TITLE_RX.search(desc):
        return "company_representative"
    return "analyst"                     # descriptor is a firm (operator intro / roster)


# Speaker labels left inside turn text because the format's parser did not recognise them.
UNRECOGNISED_LABEL = {
    "msft": re.compile(r"(?:^|(?<=\s))([A-Z][A-Z.'’-]+(?: [A-Z][A-Z.'’-]+){0,3}, [A-Z][^:\n]{1,60}):\s"),
    "alphabet": re.compile(r"(?:^|(?<=\s))([A-Z][\w.'’-]+(?: [A-Z][\w.'’-]+){1,3}, [^:.?!\n]{2,60}):\s"),
}


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


# ---------------------------------------------------------------------------
# Per-call extraction (mirrors filter_earnings_calls.process_file, keeps turn detail)
# ---------------------------------------------------------------------------

def extract_call(company, period, cy, cq, manifest_row):
    path = S.raw_path(company, period)
    raw = path.read_text(encoding="utf-8")
    metadata, body_lines = F.split_metadata(raw)
    turns, notes, file_flags, fmt = F.parse(company, metadata, body_lines)
    machine = fmt in F.MACHINE_FORMATS
    whisper = "whisper" in metadata.lower()
    units = []
    for ti, turn in enumerate(turns):
        text = turn.text if turn.unit_mode == "lines" else F.join_lines(turn.text.split("\n"))
        for sent in F.split_sentences(text, turn.unit_mode):
            v = F.classify(sent, machine=machine, company=company)
            units.append(dict(turn=ti, section=turn.section, speaker=turn.speaker, text=sent,
                              kind=v.kind, terms=v.terms, flags=v.flags,
                              unit_type=unit_type(fmt, turn.unit_mode, whisper)))

    # the filter's own driver must give the same units, or the build stops
    _, stats, ref = F.process_file(path, company)
    if [(r["section"], r["speaker"], r["text"], r["kind"]) for r in ref] != \
       [(u["section"], u["speaker"], u["text"], u["kind"]) for u in units]:
        raise RuntimeError(f"{path.name}: extraction differs from filter_earnings_calls.process_file")

    # speaker-attribution warnings: from an unrecognised label to the end of its turn
    rx = UNRECOGNISED_LABEL.get(fmt)
    open_label = {}
    for u in units:
        u["attr_warning"] = ""
        if not rx:
            continue
        if u["turn"] in open_label:
            u["attr_warning"] = open_label[u["turn"]]
        m = rx.search(u["text"])
        if m:
            msg = (f"unrecognised speaker label '{m.group(1)}' inside a turn attributed to "
                   f"'{u['speaker']}'; text from the label on is likely by that speaker")
            open_label[u["turn"]] = msg
            u["attr_warning"] = msg

    body = "\n".join(body_lines)
    flags = list(stats["parse_flags"])
    sec_method = section_method(fmt, body, flags)
    sec_order = Counter()
    for i, u in enumerate(units, 1):
        u["order"] = i
        sec_order[u["section"]] += 1
        u["order_in_section"] = sec_order[u["section"]]
    call = dict(path=path, raw=raw, metadata=metadata, body=body, fmt=fmt, flags=flags,
                stats=stats, units=units, section_method=sec_method, manifest=manifest_row)
    return call


def sentence_id(company, period, order, text):
    return f"{company}_{period}_u{order:04d}_{sha256_bytes(text.encode('utf-8'))[:10]}"


# ---------------------------------------------------------------------------
# Build
# ---------------------------------------------------------------------------

def build():
    manifest = {(r["company"], r["period_label"]): r for r in S.manifest_rows(parse=False)}
    sentences, passages, borderline, calls_out = [], [], [], []
    drift, verbatim_fail, verbatim_checked = {}, [], 0
    source_hashes = {}
    core_names = {n for n, _ in F.CORE_TERMS} | {"AI (machine transcript, any case)"}

    for company, period, cy, cq in S.expected_calls():
        m = manifest[(company, period)]
        if not S.raw_path(company, period).exists():
            continue
        c = extract_call(company, period, cy, cq, m)
        stem = f"{company}_{period}"
        call_id = stem
        source_file = c["path"].relative_to(ROOT).as_posix()
        source_hashes[source_file] = sha256_bytes(c["raw"].encode("utf-8"))
        utypes = sorted({u["unit_type"] for u in c["units"]})
        common = dict(call_id=call_id, company=company, ticker=S.TICKER[company], period_label=period,
                      calendar_year=cy, calendar_quarter=cq)
        flags_str = "; ".join(c["flags"])

        committed = committed_ai_units(company, stem)
        ai_units = [u for u in c["units"] if u["kind"] == "ai"]
        rebuilt = Counter((u["section"], u["text"]) for u in ai_units)
        if committed is None:
            drift[stem] = {"status": "no_committed_file", "rebuilt_ai_units": len(ai_units)}
        else:
            only_new = rebuilt - committed
            only_old = committed - rebuilt
            drift[stem] = {"status": "match" if not only_new and not only_old else "differs",
                           "rebuilt_ai_units": len(ai_units), "committed_ai_units": sum(committed.values()),
                           "only_in_rebuild": sum(only_new.values()), "only_in_committed": sum(only_old.values()),
                           "examples_only_in_committed": [t[:160] for (_, t) in list(only_old)[:3]]}

        src_for_verbatim = html.unescape(c["body"])
        by_order = {u["order"]: u for u in c["units"]}
        for u in c["units"]:
            sid = sentence_id(company, period, u["order"], u["text"])
            u["sid"] = sid
        for u in c["units"]:
            sec = SECTION_CODE[u["section"]]
            role = speaker_role(u["speaker"])
            if u["kind"] in ("auto", "infra"):
                bterms = (F.AUTOMATION_TERMS if u["kind"] == "auto" else F.INFRA_TERMS).findall(u["text"])
                borderline.append(dict(
                    borderline_id=u["sid"].replace("_u", "_b", 1), **common, source_file=source_file,
                    source_type=m["source_type"], unit_type=u["unit_type"], section=sec,
                    speaker=u["speaker"], speaker_role=role, sentence_order_in_call=u["order"],
                    borderline_type="automation_robotics_no_ai_term" if u["kind"] == "auto"
                    else "infrastructure_no_ai_term",
                    matched_terms="; ".join(sorted(set(t.lower() for t in bterms))),
                    text_verbatim=u["text"], review_route="gate5_human_uncertainty_review",
                    extraction_version=EXTRACTION_VERSION))
            if u["kind"] != "ai":
                continue
            verbatim_checked += 1
            if not F.verbatim_found(u["text"], src_for_verbatim):
                verbatim_fail.append({"sentence_id": u["sid"], "text": u["text"][:200]})
            in_committed = ("no_committed_file" if committed is None else
                            "yes" if committed.get((u["section"], u["text"])) else "no")
            row = dict(
                sentence_id=u["sid"], **common, fiscal_or_calendar_label=m["fiscal_or_calendar_label"],
                call_date=m["call_date"], call_date_source=m["call_date_source"], source_file=source_file,
                source_url=m["source_url"], source_type=m["source_type"], parser_format=c["fmt"],
                unit_type=u["unit_type"], section=sec, section_method=c["section_method"],
                speaker=u["speaker"], speaker_role=role, speaker_attribution_warning=u["attr_warning"],
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

            # bounded context passage
            before = [by_order[o] for o in range(u["order"] - 1, u["order"] - 1 - K_BEFORE, -1)
                      if o in by_order and by_order[o]["section"] == u["section"]]
            # stop at the first unit from another section (keeps the window contiguous)
            before = _contiguous(before)[::-1]
            after = _contiguous([by_order[o] for o in range(u["order"] + 1, u["order"] + 1 + K_AFTER)
                                 if o in by_order and by_order[o]["section"] == u["section"]])
            ctx = before + [u] + after
            ptxt = " ".join(x["text"] for x in ctx)
            passages.append(dict(
                passage_id="P_" + u["sid"], anchor_sentence_id=u["sid"], **{k: common[k] for k in common},
                call_date=m["call_date"], source_file=source_file, source_type=m["source_type"],
                unit_type=u["unit_type"], section=sec, anchor_speaker=u["speaker"], anchor_speaker_role=role,
                speaker_attribution_warning=u["attr_warning"], anchor_sentence_order_in_call=u["order"],
                trigger_terms=row["trigger_terms"], is_uncertain=row["is_uncertain"],
                is_safe_harbor=row["is_safe_harbor"], is_context_dependent=row["is_context_dependent"],
                is_long=row["is_long"], context_rule=CONTEXT_RULE,
                context_before_orders=" ".join(str(x["order"]) for x in before),
                context_after_orders=" ".join(str(x["order"]) for x in after),
                context_crosses_speaker_turn=int(any(x["turn"] != u["turn"] for x in ctx)),
                context_speakers=" | ".join(dict.fromkeys(x["speaker"] for x in ctx)),
                context_before_text=" ".join(x["text"] for x in before), anchor_text=u["text"],
                context_after_text=" ".join(x["text"] for x in after), passage_text=ptxt,
                passage_word_count=len(ptxt.split()),
                passage_role="annotation_context_only; measurement unit is anchor_sentence_id",
                extraction_version=EXTRACTION_VERSION))

        st = c["stats"]
        fc = Counter(f for u in ai_units for f in u["flags"])
        calls_out.append(dict(
            **common, fiscal_or_calendar_label=m["fiscal_or_calendar_label"], call_date=m["call_date"],
            call_date_source=m["call_date_source"], source_file=source_file,
            source_sha256=source_hashes[source_file], source_url=m["source_url"],
            source_type=m["source_type"], acquisition_status=m["acquisition_status"], parser_format=c["fmt"],
            unit_type="; ".join(utypes), section_method=c["section_method"],
            units_comparable_to_sentences=int(utypes == ["sentence"] or utypes == ["caption_sentence"]),
            total_units=st["total"], total_units_prepared=st["total_by_section"][F.PREPARED],
            total_units_qa=st["total_by_section"][F.QA], ai_units=st["ai"],
            ai_units_prepared=st["ai_by_section"][F.PREPARED], ai_units_qa=st["ai_by_section"][F.QA],
            ai_uncertain=fc.get("uncertain", 0), ai_context_dependent=fc.get("context-dependent", 0),
            ai_safe_harbor=fc.get("uncertain: safe-harbor", 0), ai_long=fc.get("long", 0),
            borderline_automation=st["borderline_auto"], borderline_infrastructure=st["borderline_infra"],
            speaker_attribution_warning_units=sum(1 for u in c["units"] if u["attr_warning"]),
            call_parse_flags=flags_str,
            committed_filter_output="present" if committed is not None else "absent",
            committed_drift=drift[stem]["status"], extraction_version=EXTRACTION_VERSION))

    validation = make_validation(manifest, sentences, passages, borderline, calls_out, drift,
                                 verbatim_checked, verbatim_fail, source_hashes)
    return sentences, passages, borderline, calls_out, validation


def _contiguous(units):
    """units are ordered outward from the anchor; keep them only while orders are consecutive."""
    out = []
    for x in units:
        if out and abs(x["order"] - out[-1]["order"]) != 1:
            break
        out.append(x)
    return out


REQUIRED_NONEMPTY = ["sentence_id", "call_id", "company", "ticker", "period_label", "calendar_year",
                     "calendar_quarter", "source_file", "source_type", "unit_type", "section",
                     "speaker", "speaker_role", "sentence_order_in_call", "text_verbatim",
                     "trigger_terms", "extraction_version"]
ALLOWED_BLANK = {"call_date": "not stated in the source file (never inferred)",
                 "source_url": "raw-file metadata gives no URL (Nvidia FY26 Q1 - FY27 Q2)"}


def make_validation(manifest, sentences, passages, borderline, calls_out, drift,
                    verbatim_checked, verbatim_fail, source_hashes):
    def count(rows, key):
        return dict(sorted(Counter(str(r[key]) for r in rows).items()))

    ids = [r["sentence_id"] for r in sentences]
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
    coverage = {r["call_id"]: {"source_file": r["source_file"], "ai_rows": sent_per_call.get(r["call_id"], 0),
                               "total_units": r["total_units"], "committed_filter_output": r["committed_filter_output"]}
                for r in calls_out}
    missing_periods = [{k: m[k] for k in ("company", "period_label", "calendar_year", "calendar_quarter",
                                          "availability_status", "acquisition_status")}
                       for m in manifest.values() if not m["raw_file_path"]]
    passage_ok = all(p["anchor_sentence_id"] in set(ids) for p in passages) and len(passages) == len(sentences)
    flags = {f: sum(int(r[f]) for r in sentences)
             for f in ("is_uncertain", "is_safe_harbor", "is_context_dependent", "is_long")}
    drift_summary = Counter(d["status"] for d in drift.values())
    return {
        "build_version": BUILD_VERSION,
        "extraction_version": EXTRACTION_VERSION,
        "status_note": ("Build integrity checks only. This is NOT a validation of the AI filter's recall or "
                        "precision (Gate 4). Do not describe the filter as validated."),
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
        "by_section_method": count(sentences, "section_method"),
        "flag_counts": flags,
        "speaker_attribution_warning_rows": sum(1 for r in sentences if r["speaker_attribution_warning"]),
        "borderline_by_type": count(borderline, "borderline_type"),
        "integrity": {
            "duplicate_sentence_ids": len(ids) - len(set(ids)),
            "duplicate_passage_ids": len(pids) - len(set(pids)),
            "duplicate_borderline_ids": len(bids) - len(set(bids)),
            "missing_required_field_counts": missing_req,
            "missing_required_field_total": sum(missing_req.values()),
            "allowed_blank_fields": blanks,
            "every_passage_has_valid_anchor_and_one_per_sentence": passage_ok,
            "semantic_label_columns_present": False,
            "rows_match_filter_process_file": True,
            "verbatim_check": {"method": "filter_earnings_calls.verbatim_found against the raw body",
                               "checked_ai_rows": verbatim_checked, "failures": len(verbatim_fail),
                               "failure_examples": verbatim_fail[:25]},
        },
        "source_file_to_output_coverage": coverage,
        "calls_with_zero_ai_rows": sorted(k for k, v in coverage.items() if v["ai_rows"] == 0),
        "committed_output_drift": {"summary": dict(drift_summary),
                                   "differs": {k: v for k, v in drift.items() if v["status"] == "differs"},
                                   "no_committed_file": sorted(k for k, v in drift.items()
                                                               if v["status"] == "no_committed_file")},
        "missing_or_unavailable_periods": missing_periods,
        "manifest_counts": dict(Counter(m["acquisition_status"] for m in manifest.values())),
        "reproducibility": {
            "command": "python build_earnings_call_canonical.py",
            "git_head": git_head(),
            "python": platform.python_version(),
            "nltk": nltk.__version__,
            "filter_earnings_calls.py_sha256": FILTER_SHA,
            "build_earnings_call_canonical.py_sha256": sha256_file(Path(__file__)),
            "earnings_call_scope.py_sha256": sha256_file(ROOT / "earnings_call_scope.py"),
            "source_file_sha256": source_hashes,
            "context_rule": CONTEXT_RULE,
            "sentence_id_rule": "<company>_<period_label>_u<4-digit order in call>_<first 10 hex of sha256(text_verbatim)>",
        },
    }


def to_csv(rows, fields):
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=fields, lineterminator="\n")
    w.writeheader()
    w.writerows(rows)
    return buf.getvalue()


def render(result):
    sentences, passages, borderline, calls_out, validation = result
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
    args = ap.parse_args()
    a = render(build())
    if args.verify:
        b = render(build())
        same = {k: a[k] == b[k] for k in a}
        print(json.dumps(same, indent=1))
        sys.exit(0 if all(same.values()) else 1)
    OUT.mkdir(exist_ok=True)
    for name, text in a.items():
        (OUT / name).write_text(text, encoding="utf-8", newline="")
    v = json.loads(a["build_validation.json"])
    print(json.dumps({"counts": v["counts"], "integrity": {k: v["integrity"][k] for k in (
        "duplicate_sentence_ids", "missing_required_field_total",
        "every_passage_has_valid_anchor_and_one_per_sentence")},
        "verbatim_failures": v["integrity"]["verbatim_check"]["failures"],
        "drift": v["committed_output_drift"]["summary"]}, indent=1))


if __name__ == "__main__":
    main()
