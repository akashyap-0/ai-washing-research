"""
Gate 4: mechanical validation and filter reconciliation for the canonical earnings-call corpus.

Every check here is performed by code. Nothing in this script is a human validation.

Reads   earnings_calls/ (raw transcripts, manifest, Tanush's ai_passages.csv / call_summary.csv)
        earnings_calls_canonical/ (outputs of build_earnings_call_canonical.py)
        git history (legacy _validation.json versions, the previous canonical sentence file)
Writes  earnings_calls_canonical/gate4_validation.json
        earnings_calls_canonical/speaker_attribution_audit.csv
        earnings_calls_canonical/filter_comparison.csv
        earnings_calls_canonical/manual_review_sample.csv
Nothing else is written, except temporary directories under the system temp folder
(clean-rebuild check, legacy snapshot), which are deleted.

Usage (after `python build_earnings_call_canonical.py`):
  python earnings_calls_canonical/gate4_validate.py
  python earnings_calls_canonical/gate4_validate.py --skip-legacy-snapshot   # faster; omits B4 re-run
"""

import argparse
import csv
import html
import io
import json
import random
import re
import shutil
import subprocess
import sys
import tarfile
import tempfile
from collections import Counter, defaultdict
from pathlib import Path

CANON = Path(__file__).resolve().parent
ROOT = CANON.parent
sys.path.insert(0, str(ROOT))
import build_earnings_call_canonical as B   # noqa: E402
import earnings_call_scope as S             # noqa: E402
import filter_earnings_calls as F           # noqa: E402

GATE4_VERSION = "gate4-v1"
SEED = 20261006
SAMPLE_N = 150
GENERATED = ["earnings_call_sentences.csv", "earnings_call_labeling_passages.csv",
             "earnings_call_borderline_review.csv", "earnings_call_call_units.csv", "build_validation.json"]


def read_csv(path_or_text, text=False):
    f = io.StringIO(path_or_text) if text else open(path_or_text, encoding="utf-8", newline="")
    with f:
        return list(csv.DictReader(f))


def write_csv(path, rows, fields):
    with open(path, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields, lineterminator="\n")
        w.writeheader()
        w.writerows(rows)


def git(*args):
    return subprocess.run(["git", *args], cwd=ROOT, capture_output=True, check=True).stdout.decode("utf-8")


def pct(a, b):
    return round(100 * a / b, 1) if b else None


# ---------------------------------------------------------------------------
# 4. Clean rebuild into an empty directory
# ---------------------------------------------------------------------------

def rebuild_check():
    tmp = Path(tempfile.mkdtemp(prefix="canon_rebuild_"))
    try:
        assert not any(tmp.iterdir())
        subprocess.run([sys.executable, str(ROOT / "build_earnings_call_canonical.py"), "--out", str(tmp)],
                       cwd=ROOT, check=True, capture_output=True)
        res = {}
        for name in GENERATED:
            a, b = (CANON / name).read_bytes(), (tmp / name).read_bytes()
            res[name] = {"byte_identical": a == b, "bytes": len(a)}
        ids_a = [r["sentence_id"] for r in read_csv(CANON / "earnings_call_sentences.csv")]
        ids_b = [r["sentence_id"] for r in read_csv(tmp / "earnings_call_sentences.csv")]
        return {"method": "build_earnings_call_canonical.py --out <new empty temp dir>, byte comparison "
                          "with earnings_calls_canonical/",
                "files": res, "all_byte_identical": all(v["byte_identical"] for v in res.values()),
                "sentence_ids_identical_and_same_order": ids_a == ids_b,
                "timestamp_exceptions": "none: outputs embed no timestamps, temp paths or git HEAD"}
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


# ---------------------------------------------------------------------------
# Verbatim helpers
# ---------------------------------------------------------------------------

_TS = re.compile(r"\[\d+:\d{2}(?::\d{2})?\]")
_TAG = re.compile(r"\[(?:Music|music|Applause|applause|Laughter|laughter|clears throat|__)\]|>>|&gt;&gt;")


def norm_ws(s):
    return re.sub(r"\s+", " ", s).strip()


def norm_source(body):
    """Documented normalization only: HTML entities decoded, timestamps and caption tags removed,
    whitespace collapsed."""
    return norm_ws(_TAG.sub(" ", _TS.sub(" ", html.unescape(body))))


def diagnose(text, src_norm):
    toks = text.split()
    best = 0
    for k in range(len(toks), 0, -1):
        if norm_ws(" ".join(toks[:k])) in src_norm:
            best = k
            break
    return f"first {best} of {len(toks)} words found contiguous in source; break before '{' '.join(toks[best:best+4])}'"


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--skip-legacy-snapshot", action="store_true")
    args = ap.parse_args()

    sentences = read_csv(CANON / "earnings_call_sentences.csv")
    passages = read_csv(CANON / "earnings_call_labeling_passages.csv")
    borderline = read_csv(CANON / "earnings_call_borderline_review.csv")
    calls = read_csv(CANON / "earnings_call_call_units.csv")
    manifest = {(r["company"], r["period_label"]): r for r in S.manifest_rows(parse=False)}
    V = {"gate4_version": GATE4_VERSION, "extraction_version": B.EXTRACTION_VERSION,
         "validation_type": "mechanical checks run by code; NOT human validation",
         "supersedes_for_current_corpus": ["earnings_calls_ai_only/_validation.json",
                                            "earnings_calls_ai_only/FILTER_METHOD.md (Validation section)"]}

    # ---- 1. scope coverage -------------------------------------------------
    expected = list(S.expected_calls())
    present = [(c, p) for c, p, _, _ in expected if S.raw_path(c, p).exists()]
    missing = [dict(company=c, period_label=p, calendar=f"{cy}Q{cq}",
                    acquisition_status=manifest[(c, p)]["acquisition_status"],
                    availability_status=manifest[(c, p)]["availability_status"])
               for c, p, cy, cq in expected if not S.raw_path(c, p).exists()]
    V["1_scope_coverage"] = {"expected": len(expected), "present": len(present), "missing": len(missing),
                             "missing_by_status": dict(Counter(m["acquisition_status"] for m in missing)),
                             "missing_calls": missing, "pass": len(expected) == 133 and len(present) + len(missing) == 133}

    # ---- 2. source / output coverage --------------------------------------
    exp_paths = {S.raw_path(c, p).relative_to(ROOT).as_posix() for c, p, _, _ in expected}
    on_disk = sorted(p.relative_to(ROOT).as_posix() for c in S.COMPANIES for p in (S.CALLS / c).glob("*.md"))
    extra = [p for p in on_disk if p not in exp_paths]
    stems_ci = Counter(Path(p).stem.lower() for p in on_disk)
    sent_calls = Counter(r["call_id"] for r in sentences)
    pass_calls = Counter(r["call_id"] for r in passages)
    present_ids = {f"{c}_{p}" for c, p in present}
    V["2_source_output_coverage"] = {
        "raw_files_on_disk": len(on_disk), "raw_files_outside_expected_set": extra,
        "duplicate_file_stems_case_insensitive": [k for k, v in stems_ci.items() if v > 1],
        "calls_in_call_units_file": len(calls),
        "present_calls_without_sentence_rows": sorted(present_ids - set(sent_calls)),
        "present_calls_without_passage_rows": sorted(present_ids - set(pass_calls)),
        "output_calls_not_in_present_set": sorted((set(sent_calls) | set(pass_calls) | {c["call_id"] for c in calls})
                                                  - present_ids),
    }
    V["2_source_output_coverage"]["pass"] = not (extra or V["2_source_output_coverage"]["duplicate_file_stems_case_insensitive"]
                                                 or V["2_source_output_coverage"]["present_calls_without_sentence_rows"]
                                                 or V["2_source_output_coverage"]["present_calls_without_passage_rows"]
                                                 or V["2_source_output_coverage"]["output_calls_not_in_present_set"]
                                                 or len(calls) != len(present))

    # ---- 3. field completeness and no-fabrication checks --------------------
    by_design_blank = {"speaker_status_reason": "blank when status is resolved/operator",
                       "speaker_correction_rule": "blank when the speaker was not corrected",
                       "core_terms": "blank for weak-term-only (uncertain) rows",
                       "weak_terms": "blank for core-only rows",
                       "call_parse_flags": "blank when the filter raised no file flag"}
    fields = list(sentences[0].keys())
    blank = {f: sum(1 for r in sentences if not r[f].strip()) for f in fields}
    required_missing = {f: n for f, n in blank.items() if f not in B.ALLOWED_BLANK and f not in by_design_blank}
    # call dates must be re-derivable from the file itself; URLs must appear in the file's metadata
    date_bad, url_bad = [], []
    for m in manifest.values():
        if not m["raw_file_path"]:
            continue
        meta, body = S.read_metadata(ROOT / m["raw_file_path"])
        d, src = S.call_date(m["company"], int(m["calendar_year"]), int(m["calendar_quarter"]), meta, body)
        if (d, src) != (m["call_date"], m["call_date_source"]):
            date_bad.append(m["raw_file_path"])
        if m["source_url"] and m["source_url"] not in meta:
            url_bad.append(m["raw_file_path"])
    row_date_mismatch = sum(1 for r in sentences
                            if r["call_date"] != manifest[(r["company"], r["period_label"])]["call_date"])
    V["3_field_completeness"] = {
        "fields_checked": len(fields),
        "required_field_missing_counts": required_missing,
        "required_field_missing_total": sum(required_missing.values()),
        "legitimately_unavailable": {f: {"rows": blank[f], "reason": why} for f, why in B.ALLOWED_BLANK.items()},
        "blank_by_design": {f: {"rows": blank[f], "reason": why} for f, why in by_design_blank.items()},
        "call_dates_not_rederivable_from_source_file": date_bad,
        "source_urls_not_present_in_file_metadata": url_bad,
        "sentence_rows_with_call_date_differing_from_manifest": row_date_mismatch,
        "pass": not (sum(required_missing.values()) or date_bad or url_bad or row_date_mismatch),
    }

    # ---- 4. IDs and reproducibility ----------------------------------------
    sids = [r["sentence_id"] for r in sentences]
    pids = [r["passage_id"] for r in passages]
    sidset = set(sids)
    unit_ids_known = sidset | {r["unit_id"] for r in borderline}
    id_rx = re.compile(r"^(?P<call>.+)_u(?P<ord>\d{4})_(?P<h>[0-9a-f]{10})$")
    id_formula_bad = [r["sentence_id"] for r in sentences
                      if r["sentence_id"] != B.unit_id(r["company"], r["period_label"],
                                                       int(r["sentence_order_in_call"]), r["text_verbatim"])]
    ctx_ids = [i for p in passages for i in p["context_sentence_ids"].split()]
    ctx_kinds = [k for p in passages for k in p["context_unit_kinds"].split()]
    ctx_unresolvable_ai = sum(1 for i, k in zip(ctx_ids, ctx_kinds) if k == "ai" and i not in sidset)
    ctx_unresolvable_bl = sum(1 for i, k in zip(ctx_ids, ctx_kinds) if k.startswith("borderline") and i not in unit_ids_known)
    V["4_ids_reproducibility"] = {
        "duplicate_sentence_ids": len(sids) - len(sidset),
        "duplicate_passage_ids": len(pids) - len(set(pids)),
        "duplicate_borderline_ids": len(borderline) - len({r["borderline_id"] for r in borderline}),
        "orphaned_anchor_sentence_ids": sum(1 for p in passages if p["anchor_sentence_id"] not in sidset),
        "sentences_without_passage": len(sidset - {p["anchor_sentence_id"] for p in passages}),
        "sentence_ids_not_matching_formula": len(id_formula_bad),
        "context_ids_total": len(ctx_ids),
        "context_ids_kind_counts": dict(Counter(ctx_kinds)),
        "context_ai_ids_not_in_sentence_file": ctx_unresolvable_ai,
        "context_borderline_ids_not_in_borderline_file": ctx_unresolvable_bl,
        "context_non_ai_ids_note": ("non-AI, non-borderline context units are not stored as rows; their text is in "
                                    "the passage and their ID follows the same formula"),
        "clean_rebuild": rebuild_check(),
    }

    # ---- per-call re-extraction (for verbatim, section/speaker, audit, legacy) ----
    extracted = {}
    for c, p in present:
        extracted[f"{c}_{p}"] = B.extract_call(c, p)

    # ---- 5. verbatim -------------------------------------------------------
    def verbatim_rows(rows, id_key):
        t1 = t2 = 0
        fails = []
        src_cache = {}
        for r in rows:
            cid = r["call_id"]
            if cid not in src_cache:
                body = extracted[cid]["body"]
                src_cache[cid] = (norm_source(body), html.unescape(body))
            sn, raw_unesc = src_cache[cid]
            if norm_ws(r["text_verbatim"]) in sn:
                t1 += 1
            elif F.verbatim_found(r["text_verbatim"], raw_unesc):
                t2 += 1
            else:
                fails.append({id_key: r[id_key], "diagnostic": diagnose(r["text_verbatim"], sn),
                              "text": r["text_verbatim"][:160]})
        return {"checked": len(rows), "tier1_exact_after_whitespace_normalization": t1,
                "tier2_only_with_filter_noise_tolerance": t2, "failures": len(fails), "failure_rows": fails}

    all_units = [dict(call_id=cid, text_verbatim=u["text"], unit_id=u["uid"], kind=u["kind"])
                 for cid, c in extracted.items() for u in c["units"]]
    V["5_verbatim"] = {
        "method": ("tier 1: unit text, whitespace-collapsed, is a substring of the raw body after the documented "
                   "normalization (HTML entities decoded, [mm:ss] timestamps and caption tags removed, whitespace "
                   "collapsed). Tier 2 (only if tier 1 fails): filter_earnings_calls.verbatim_found, which also "
                   "allows the filter's deleted noise (page numbers, FactSet headers, hyphen line-wraps) between "
                   "words. Run by code, not by a human."),
        "canonical_sentences": verbatim_rows(sentences, "sentence_id"),
        "borderline_rows": verbatim_rows(borderline, "borderline_id"),
        "all_parsed_units_including_non_ai": verbatim_rows(all_units, "unit_id"),
    }
    fails_all = V["5_verbatim"]["all_parsed_units_including_non_ai"]["failure_rows"]
    for f in fails_all:
        f["kind"] = next(u["kind"] for u in all_units if u["unit_id"] == f["unit_id"])

    # ---- 6. section and speaker checks + audit -------------------------------
    sec = Counter(r["section"] for r in sentences)
    status = Counter(r["speaker_status"] for r in sentences)
    single = []
    for cid, c in extracted.items():
        units = c["units"]
        spk = {u["speaker"] for u in units}
        secs = {u["section"] for u in units}
        lacks = all(u["speaker"] == F.UNLABELED for u in units)
        if len(secs) < 2 or (len(spk) < 2 and not lacks):
            single.append({"call_id": cid, "sections": len(secs), "speakers": len(spk)})
    unlabeled_single = sorted(cid for cid, c in extracted.items()
                              if {u["speaker"] for u in c["units"]} == {F.UNLABELED})

    audit = []
    for cid, c in extracted.items():
        company, period = cid.split("_", 1)
        acq = manifest[(company, period)]["acquisition_status"]
        for u in c["units"]:
            r = u.get("ref")
            st, why = B.speaker_status(u["speaker"], u["speaker_changed"], company, u["section"], acq, cid)
            base = dict(sentence_id=u["uid"], old_sentence_id=r["uid"] if r else "",
                        id_changed=int(bool(r) and r["uid"] != u["uid"]), unit_kind=u["kind"],
                        in_sentence_file=int(u["kind"] == "ai"), company=company, period_label=period,
                        section=B.SECTION_CODE[u["section"]], sentence_order_in_call=u["order"],
                        old_speaker=r["speaker"] if r else "", new_speaker=u["speaker"],
                        old_role=B.speaker_role(r["speaker"]) if r else "", new_role=B.speaker_role(u["speaker"]))
            if u["speaker_changed"]:
                audit.append(dict(base, audit_status="corrected", parsing_rule=u["rule"],
                                  confidence="high" if u["rule"].endswith("_label") else "medium",
                                  source_text_evidence=u["evidence"],
                                  reason=("explicit 'NAME, Firm:' label in the raw text starts this speaker's turn"
                                          if u["rule"].endswith("_label") else
                                          "same transcript labels this exact name with a firm; unique match")))
            elif u["kind"] == "ai" and st not in ("resolved", "resolved_corrected", "operator"):
                audit.append(dict(base, audit_status={"unresolved_bare_name": "unresolved",
                                                      "unverified_meta_label_loss_risk": "unverified",
                                                      "unverified_raw_label_misplacement": "unverified",
                                                      "unlabeled_source": "unresolved_source_has_no_labels",
                                                      "unknown_speaker_in_source": "unresolved"}[st],
                                  parsing_rule="none_applied", confidence="n/a",
                                  source_text_evidence=f"speaker as parsed: '{u['speaker']}'", reason=why))
    audit_fields = ["sentence_id", "old_sentence_id", "id_changed", "unit_kind", "in_sentence_file", "company",
                    "period_label", "section", "sentence_order_in_call", "old_speaker", "new_speaker", "old_role",
                    "new_role", "audit_status", "parsing_rule", "confidence", "source_text_evidence", "reason"]
    write_csv(CANON / "speaker_attribution_audit.csv", audit, audit_fields)

    # remaining unrecognised labels after correction (should be none)
    leftovers = []
    for cid, c in extracted.items():
        rx = B.LABEL_FIX.get(c["fmt"])
        if rx:
            leftovers += [u["uid"] for u in c["units"] if rx.search(u["text"])]
    ai_corr = sum(1 for a in audit if a["audit_status"] == "corrected" and a["unit_kind"] == "ai")
    V["6_section_speaker"] = {
        "sections_ai_rows": dict(sec), "unknown_section_rows": sum(1 for r in sentences
                                                                  if r["section"] not in ("prepared_remarks", "qa")),
        "speaker_status_ai_rows": dict(sorted(status.items())),
        "resolved_ai_rows": status["resolved"] + status["resolved_corrected"] + status["operator"],
        "unresolved_ai_rows": status["unresolved_bare_name"] + status["unknown_speaker_in_source"],
        "unverified_meta_ai_rows": status["unverified_meta_label_loss_risk"],
        "unverified_raw_label_misplacement_ai_rows": status["unverified_raw_label_misplacement"],
        "acquired_pdf_label_placement_check": acquired_label_check(),
        "unlabeled_source_ai_rows": status["unlabeled_source"],
        "corrections_this_task": {
            "all_units_speaker_changed": sum(1 for a in audit if a["audit_status"] == "corrected"),
            "ai_rows_speaker_changed": ai_corr,
            "units_text_changed_label_removed": sum(1 for cid, c in extracted.items() for u in c["units"]
                                                    if u["text_changed"]),
            "ai_rows_id_changed": sum(1 for a in audit if a["audit_status"] == "corrected" and a["unit_kind"] == "ai"
                                      and a["id_changed"]),
            "by_rule": dict(Counter(a["parsing_rule"] for a in audit if a["audit_status"] == "corrected")),
            "unrecognised_labels_remaining_after_correction": len(leftovers),
        },
        "unresolved_bare_names": dict(Counter(f"{r['company']}: {r['speaker']}" for r in sentences
                                              if r["speaker_status"] == "unresolved_bare_name").most_common()),
        "calls_with_one_section_or_one_speaker": single,
        "calls_with_one_speaker_because_source_has_no_labels": unlabeled_single,
    }

    # previous canonical sentence file (git HEAD) vs current: only documented changes allowed
    try:
        old = read_csv(git("show", "HEAD:earnings_calls_canonical/earnings_call_sentences.csv"), text=True)
        old_by = {r["sentence_id"]: r for r in old}
        new_by = {r["sentence_id"]: r for r in sentences}
        changed_cols = Counter()
        for i in set(old_by) & set(new_by):
            for k in set(old_by[i]) & set(new_by[i]):
                if old_by[i][k] != new_by[i][k]:
                    changed_cols[k] += 1
        audited_old = {a["old_sentence_id"] for a in audit if a["id_changed"]}
        only_old = set(old_by) - set(new_by)
        V["6b_change_vs_previous_canonical"] = {
            "previous": "git HEAD:earnings_calls_canonical/earnings_call_sentences.csv (canonical-v1)",
            "rows_previous": len(old), "rows_current": len(sentences),
            "ids_only_in_previous": len(only_old), "ids_only_in_current": len(set(new_by) - set(old_by)),
            "ids_only_in_previous_explained_by_audit": len(only_old & audited_old),
            "columns_changed_on_common_ids": dict(changed_cols),
            "columns_removed": sorted(set(old[0]) - set(sentences[0])),
            "columns_added": sorted(set(sentences[0]) - set(old[0])),
            "text_verbatim_changed_on_common_ids": changed_cols.get("text_verbatim", 0),
        }
    except subprocess.CalledProcessError:
        V["6b_change_vs_previous_canonical"] = {"previous": "not available in git"}

    # ---- 7. flags ------------------------------------------------------------
    def by(rows, key, flag=None, val="1"):
        return dict(sorted(Counter(r[key] for r in rows if flag is None or r[flag] == val).items()))
    V["7_flags"] = {
        "totals": {"uncertain": sum(int(r["is_uncertain"]) for r in sentences),
                   "context_dependent": sum(int(r["is_context_dependent"]) for r in sentences),
                   "long": sum(int(r["is_long"]) for r in sentences),
                   "safe_harbor": sum(int(r["is_safe_harbor"]) for r in sentences),
                   "borderline_automation_robotics": sum(r["borderline_type"].startswith("automation") for r in borderline),
                   "borderline_infrastructure": sum(r["borderline_type"].startswith("infrastructure") for r in borderline)},
        "by_company": {f: by(sentences, "company", f) for f in ("is_uncertain", "is_context_dependent", "is_long")},
        "by_source_type": {f: by(sentences, "source_type", f) for f in ("is_uncertain", "is_context_dependent", "is_long")},
        "borderline_by_company": {t: by(borderline, "company", "borderline_type", t)
                                  for t in ("automation_robotics_no_ai_term", "infrastructure_no_ai_term")},
        "borderline_by_source_type": {t: by(borderline, "source_type", "borderline_type", t)
                                      for t in ("automation_robotics_no_ai_term", "infrastructure_no_ai_term")},
    }

    # ---- 8. unit comparability ----------------------------------------------
    V["8_unit_comparability"] = {
        "ai_rows_by_unit_type": by(sentences, "unit_type"),
        "all_units_by_unit_type": dict(Counter(u["unit_type"] for c in extracted.values() for u in c["units"])),
        "calls_by_unit_type": dict(Counter(c["unit_type"] for c in calls)),
        "caption_segment_calls": sorted(c["call_id"] for c in calls if "caption_segment" in c["unit_type"]),
        "whisper_calls": sorted(c["call_id"] for c in calls if "whisper_unit" in c["unit_type"]),
        "statement": ("Unpunctuated caption segments (~30 s of speech) and Whisper units are not sentences. Counts "
                      "and shares built on them are NOT directly comparable to true-sentence counts and must be "
                      "reported separately or adjusted by a documented method; never pooled silently."),
    }

    # ---- B3. filter comparison ----------------------------------------------
    V["B3_filter_comparison"] = compare_filters(sentences, calls, manifest, expected)

    # ---- B4. legacy reconstruction ------------------------------------------
    V["B4_legacy"] = legacy(extracted, skip_snapshot=args.skip_legacy_snapshot)

    # ---- B5. manual review sample -------------------------------------------
    V["B5_manual_review_sample"] = review_sample(sentences, passages)

    (CANON / "gate4_validation.json").write_text(json.dumps(V, indent=2, ensure_ascii=False) + "\n",
                                                 encoding="utf-8")
    summary = {k: V[k].get("pass") for k in V if isinstance(V[k], dict) and "pass" in V[k]}
    print(json.dumps(summary, indent=1))


# ---------------------------------------------------------------------------
# B1b: label placement in the Gate 2 PDF acquisitions (local cached originals only)
# ---------------------------------------------------------------------------

_LBL = re.compile(r"(?:^|(?<=[.?!] )|(?<=\s))(Operator|[A-Z][\w.'’-]+(?: [A-Z][\w.'’-]+){1,3}(?:, [^:\n]{2,60})?):"
                  r"\s+(\S+(?: \S+){0,5})")


def acquired_label_check():
    """Each inline label plus its next four words, from the committed raw file vs pdftotext -raw
    of the cached official PDF. Uses only cache/earnings_call_sources/ (no download)."""
    res = {"method": ("label + next 4 words multiset, committed raw file (pdftotext -layout) vs "
                      "pdftotext -raw of cache/earnings_call_sources/<call>.pdf"), "calls": {}}
    exe = shutil.which("pdftotext")
    for stem in ("alphabet_2022_Q1", "alphabet_2022_Q2", "alphabet_2022_Q3", "meta_2021_Q4", "meta_2022_Q1",
                 "meta_2022_Q2", "meta_2022_Q3"):
        pdf = ROOT / "cache" / "earnings_call_sources" / f"{stem}.pdf"
        if not exe or not pdf.exists():
            res["calls"][stem] = "not checked: cached PDF or pdftotext unavailable"
            continue
        raw = subprocess.run([exe, "-raw", "-enc", "UTF-8", str(pdf), "-"], capture_output=True).stdout.decode()
        _, body = S.read_metadata(S.raw_path(*stem.split("_", 1)))

        def seq(t):
            return Counter((m.group(1), " ".join(m.group(2).split()[:4])) for m in _LBL.finditer(norm_ws(t)))
        a, b = seq(raw), seq(body)
        res["calls"][stem] = {"labels_pdf_raw_mode": sum(a.values()), "labels_raw_file": sum(b.values()),
                              "in_pdf_not_in_file": sum((a - b).values()), "in_file_not_in_pdf": sum((b - a).values()),
                              "quarantined_in_canonical": stem in B.RAW_LABEL_MISPLACEMENT}
    bad = sorted(k for k, v in res["calls"].items() if isinstance(v, dict) and (v["in_pdf_not_in_file"] or
                                                                              v["in_file_not_in_pdf"]))
    res["calls_with_misplaced_labels"] = bad
    res["all_misplaced_calls_quarantined"] = set(bad) <= set(B.RAW_LABEL_MISPLACEMENT)
    return res


# ---------------------------------------------------------------------------
# B3: canonical sentence filter vs Tanush's passage filter
# ---------------------------------------------------------------------------

def tnorm(s):
    return re.sub(r"\s+", " ", re.sub(r"[^0-9a-z]+", " ", html.unescape(s).lower())).strip()


NGRAM = 6


def grams(norm_text):
    t = norm_text.split()
    return {tuple(t[i:i + NGRAM]) for i in range(len(t) - NGRAM + 1)}


def shingle_match(unit_norm, gram_set, text_blob):
    g = grams(unit_norm)
    if not g:                                       # unit shorter than 6 tokens: containment
        return bool(unit_norm) and unit_norm in text_blob
    return len(g & gram_set) / len(g) >= 0.5


def compare_filters(sentences, calls, manifest, expected):
    tp = read_csv(S.CALLS / "ai_passages.csv")
    ts = {(r["company"], r["period"]): r for r in read_csv(S.CALLS / "call_summary.csv")}
    t_by = defaultdict(list)
    for r in tp:
        t_by[(r["company"], r["period"])].append(r)
    c_by = defaultdict(list)
    for r in sentences:
        c_by[(r["company"], r["period_label"])].append(r)
    call_by = {(c["company"], c["period_label"]): c for c in calls}
    method = ("normalization: lowercase, every non-alphanumeric run -> one space. (a) strict containment: a "
              "canonical AI unit overlaps if its normalized text is a substring of any Tanush passage of the same "
              "company-period. (b) shingle overlap (primary): a canonical unit overlaps if >=50% of its word "
              "6-grams occur in that call's Tanush passages (units under 6 words: containment); a Tanush passage "
              "overlaps if some canonical AI unit of the call has >=50% of its 6-grams in that passage. (b) "
              "tolerates different unit boundaries (Whisper segments, Tanush's line splits and digit-line removal)")
    rows, tot = [], Counter()
    no_canon_examples = []
    for company, period, _, _ in expected:
        key = (company, period)
        cr, trs = c_by.get(key, []), t_by.get(key, [])
        call = call_by.get(key)
        m = manifest[key]
        in_canon, in_t = call is not None, key in ts
        canon_cov = ("present: canonical rows from current raw file" if in_canon else
                     f"absent: raw call not in repo ({m['acquisition_status']})")
        if in_t:
            t_cov = "present: Tanush ran on this raw file (2026-10-01)"
        elif in_canon:
            t_cov = "absent: call acquired 2026-10-06 (Gate 2), after Tanush's filter ran"
        else:
            t_cov = f"absent: raw call not in repo ({m['acquisition_status']})"
        res, diff = "", ""
        if in_canon and in_t:
            tnorms = [tnorm(t["text"]) for t in trs]
            blob = " | ".join(tnorms)
            tgrams = [grams(t) for t in tnorms]
            all_tgrams = set().union(*tgrams) if tgrams else set()
            cnorms = [tnorm(r["text_verbatim"]) for r in cr]
            strict = [r for r, cn in zip(cr, cnorms) if cn and cn in blob]
            covered = [r for r, cn in zip(cr, cnorms) if shingle_match(cn, all_tgrams, blob)]
            core = [r for r in cr if r["is_uncertain"] == "0"]
            unc = [r for r in cr if r["is_uncertain"] == "1"]
            core_cov = sum(1 for r in covered if r["is_uncertain"] == "0")
            unc_cov = sum(1 for r in covered if r["is_uncertain"] == "1")
            cgrams = [(cn, grams(cn)) for cn in cnorms if cn]
            t_hit = [i for i, (t, tg) in enumerate(zip(tnorms, tgrams))
                     if any((len(g & tg) / len(g) >= 0.5) if g else cn in t for cn, g in cgrams)]
            hit_set = set(t_hit)
            no_canon = [trs[i] for i in range(len(trs)) if i not in hit_set]
            for t in no_canon[:2]:
                if len(no_canon_examples) < 40:
                    no_canon_examples.append({"call": f"{company}_{period}", "passage_id": t["passage_id"],
                                              "keywords": t["keywords"], "text": t["text"][:240]})
            tot.update(canon=len(cr), strict=len(strict), covered=len(covered), core=len(core), core_cov=core_cov,
                       unc=len(unc), unc_cov=unc_cov, tpass=len(trs), thit=len(t_hit))
            res = (f"shingle: {len(covered)}/{len(cr)} canonical units overlap a Tanush passage "
                   f"({pct(len(covered), len(cr))}%; core {core_cov}/{len(core)}, uncertain {unc_cov}/{len(unc)}); "
                   f"{len(t_hit)}/{len(trs)} Tanush passages overlap a canonical unit; "
                   f"strict containment {len(strict)}/{len(cr)}")
            notes = []
            if unc:
                notes.append(f"{len(unc) - unc_cov} canonical weak-term (uncertain) units not in Tanush (weak terms "
                             f"are excluded from Tanush passages by design)")
            if core and core_cov < len(core):
                notes.append(f"{len(core) - core_cov} canonical core-term units not in any Tanush passage")
            if no_canon:
                notes.append(f"{len(no_canon)} Tanush passages contain no canonical AI unit")
            if ts[key]["qa_boundary"] == "none":
                notes.append("Tanush found no Q&A boundary")
            diff = "; ".join(notes) or "no material difference at unit level"
        elif in_canon:
            diff = "only canonical covers this call"
        else:
            diff = "neither source covers this call"
        tsec = Counter(t["section"] for t in trs)
        rows.append(dict(
            company=company, period_label=period, canonical_ai_sentences=len(cr) if in_canon else "",
            tanush_passages=len(trs) if in_t else "", canonical_source_coverage=canon_cov,
            tanush_source_coverage=t_cov,
            section_metadata_available_canonical=("yes: prepared_remarks/qa on every row "
                                                  f"({call['section_method']})" if in_canon else ""),
            section_metadata_available_tanush=(f"{tsec['prepared'] + tsec['qa']}/{len(trs)} passages prepared/qa; "
                                               f"boundary={ts[key]['qa_boundary']}" if in_t else ""),
            speaker_metadata_available_canonical=(
                f"{sum(1 for r in cr if r['speaker_status'] in ('resolved', 'resolved_corrected', 'operator'))}/"
                f"{len(cr)} rows resolved" if in_canon else ""),
            speaker_metadata_available_tanush=(f"{sum(1 for t in trs if t['speaker'].strip())}/{len(trs)} passages "
                                               f"with a speaker" if in_t else ""),
            overlap_method=method if in_canon and in_t else "not computed: call missing from one or both sources",
            overlap_result=res, major_difference=diff,
            recommended_use=("canonical = primary measurement unit; Tanush = auxiliary audit/context only"
                             if in_canon and in_t else
                             "canonical = primary measurement unit; no Tanush passages to audit against" if in_canon
                             else "no data for either source")))
    fields = ["company", "period_label", "canonical_ai_sentences", "tanush_passages", "canonical_source_coverage",
              "tanush_source_coverage", "section_metadata_available_canonical", "section_metadata_available_tanush",
              "speaker_metadata_available_canonical", "speaker_metadata_available_tanush", "overlap_method",
              "overlap_result", "major_difference", "recommended_use"]
    write_csv(CANON / "filter_comparison.csv", rows, fields)
    both = sum(1 for r in rows if r["overlap_result"])
    return {
        "method": method, "rows": len(rows), "calls_in_both": both,
        "calls_only_canonical": [f"{r['company']}_{r['period_label']}" for r in rows
                                 if r["canonical_ai_sentences"] != "" and r["tanush_passages"] == ""],
        "calls_only_tanush": [f"{r['company']}_{r['period_label']}" for r in rows
                              if r["canonical_ai_sentences"] == "" and r["tanush_passages"] != ""],
        "calls_in_neither": sum(1 for r in rows if r["canonical_ai_sentences"] == "" and r["tanush_passages"] == ""),
        "pooled_over_calls_in_both": {
            "canonical_units": tot["canon"], "canonical_units_in_tanush": tot["covered"],
            "pct": pct(tot["covered"], tot["canon"]),
            "strict_containment_units": tot["strict"], "strict_containment_pct": pct(tot["strict"], tot["canon"]),
            "core_units": tot["core"], "core_in_tanush": tot["core_cov"], "core_pct": pct(tot["core_cov"], tot["core"]),
            "uncertain_units": tot["unc"], "uncertain_in_tanush": tot["unc_cov"],
            "uncertain_pct": pct(tot["unc_cov"], tot["unc"]),
            "tanush_passages": tot["tpass"], "tanush_passages_with_canonical_unit": tot["thit"],
            "tanush_pct": pct(tot["thit"], tot["tpass"])},
        "tanush_total_passages_file": len(tp),
        "examples_tanush_passages_without_canonical_unit": no_canon_examples,
        "roles": {"canonical": "primary measurement source: sentence order, flags, prepared/Q&A split, stable IDs",
                  "tanush": "auxiliary audit/context source; never merged with or substituted for canonical rows"},
    }


# ---------------------------------------------------------------------------
# B4: legacy QA records
# ---------------------------------------------------------------------------

def legacy(extracted, skip_snapshot=False):
    out = {"legacy_validation_json_versions": {}}
    for c in ("fb184fe", "c1dd6c6", "a33883b"):
        v = json.loads(git("show", f"{c}:earnings_calls_ai_only/_validation.json"))
        out["legacy_validation_json_versions"][c] = {
            "amazon_coverage": v["coverage"]["by_company"]["amazon"],
            "verbatim_checked": v["verbatim"]["checked_all"], "verbatim_failures": v["verbatim"]["failures_all"],
            "false_positive_ai_tokens": v["false_positive_ai_tokens"], "flag_totals": v["flag_totals"]}
    out["filter_method_md_claims"] = {"verbatim_checked": 48555, "verbatim_failures": 0,
                                      "false_positive_ai_tokens": 0, "uncertain": 2536, "context_dependent": 574,
                                      "tesla_split_claimed": "9 Motley Fool / 6 captions"}
    # current filter code on the current 105 original calls and on all 116
    orig = {cid for cid in extracted if not cid.startswith(("alphabet_2022_Q1", "alphabet_2022_Q2", "alphabet_2022_Q3",
                                                            "meta_2021_Q4", "meta_2022_Q1", "meta_2022_Q2",
                                                            "meta_2022_Q3", "microsoft_FY22", "microsoft_FY23_Q1"))}
    def stats(ids):
        st = [extracted[i]["stats"] for i in ids]
        ref_units = [u for i in ids for u in extracted[i]["ref"]]
        fails = sum(1 for i in ids for u in extracted[i]["ref"]
                    if not F.verbatim_found(u["text"], html.unescape(extracted[i]["body"])))
        return {"calls": len(ids), "units": sum(s["total"] for s in st), "ai": sum(s["ai"] for s in st),
                "uncertain": sum(s["flag_counts"].get("uncertain", 0) for s in st),
                "context_dependent": sum(s["flag_counts"].get("context-dependent", 0) for s in st),
                "false_positive_ai_tokens": sum(s["false_positive_ai_tokens"] for s in st),
                "verbatim_failures_all_filter_units": fails, "units_checked": len(ref_units)}
    out["current_filter_code_on_current_raw"] = {"original_105_calls": stats(sorted(orig)),
                                                 "all_116_calls": stats(sorted(extracted))}
    tesla = Counter(S.source_type(*S.read_metadata(S.raw_path("tesla", p))) for c, p, _, _ in S.expected_calls()
                    if c == "tesla" and S.raw_path(c, p).exists())
    a33 = sum(1 for f in git("ls-tree", "--name-only", "a33883b", "earnings_calls/tesla/").split()
              if "Motley Fool" in git("show", f"a33883b:{f}")[:1500])
    out["tesla_source_split"] = {"current": dict(tesla), "motley_fool_files_at_a33883b": a33}
    if not skip_snapshot:
        out["snapshot_4b47e6a_rerun"] = snapshot("4b47e6a")
    return out


def snapshot(commit):
    """Re-run that commit's own filter + --validate on that commit's raw files, in a temp copy."""
    tmp = Path(tempfile.mkdtemp(prefix=f"snap_{commit}_"))
    try:
        tar = subprocess.run(["git", "archive", commit, "filter_earnings_calls.py", "earnings_calls",
                              "earnings_calls_ai_only"], cwd=ROOT, capture_output=True, check=True).stdout
        with tarfile.open(fileobj=io.BytesIO(tar)) as tf:
            tf.extractall(tmp, filter="data")
        subprocess.run([sys.executable, "filter_earnings_calls.py"], cwd=tmp, check=True, capture_output=True)
        subprocess.run([sys.executable, "filter_earnings_calls.py", "--validate"], cwd=tmp, check=True,
                       capture_output=True)
        v = json.loads((tmp / "earnings_calls_ai_only" / "_validation.json").read_text(encoding="utf-8"))
        return {"commit": commit, "amazon_files": v["coverage"]["by_company"]["amazon"],
                "verbatim_checked": v["verbatim"]["checked_all"], "verbatim_failures": v["verbatim"]["failures_all"],
                "false_positive_ai_tokens": v["false_positive_ai_tokens"], "flag_totals": v["flag_totals"]}
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


# ---------------------------------------------------------------------------
# B5: stratified review sample (no labels)
# ---------------------------------------------------------------------------

def review_sample(sentences, passages):
    rng = random.Random(SEED)
    pas = {p["anchor_sentence_id"]: p for p in passages}
    def key(r):
        return (int(r["calendar_year"]), int(r["calendar_quarter"]), r["sentence_id"])
    strata = defaultdict(list)
    for r in sentences:
        strata[(r["company"], r["section"], "uncertain" if r["is_uncertain"] == "1" else "core")].append(r)
    for v in strata.values():
        v.sort(key=key)
    CAPTION_SLOTS = 10
    base = (SAMPLE_N - CAPTION_SLOTS) // len(strata)           # 140 / 28 = 5
    alloc = {k: min(base, len(v)) for k, v in strata.items()}
    short = (SAMPLE_N - CAPTION_SLOTS) - sum(alloc.values())
    order = sorted(strata, key=lambda k: (-len(strata[k]), k))
    while short > 0:
        moved = False
        for k in order:
            if short and alloc[k] < len(strata[k]):
                alloc[k] += 1
                short -= 1
                moved = True
        if not moved:
            break

    def spread_pick(rows, k, taken):
        rows = [r for r in rows if r["sentence_id"] not in taken]
        if k >= len(rows):
            return rows
        out = []
        for i in range(k):                     # one draw per equal time-ordered chunk
            chunk = rows[i * len(rows) // k:(i + 1) * len(rows) // k]
            out.append(rng.choice(chunk))
        return out

    picked, reason, taken = [], {}, set()
    for k in sorted(strata):
        for r in spread_pick(strata[k], alloc[k], taken):
            picked.append(r)
            taken.add(r["sentence_id"])
            reason[r["sentence_id"]] = f"stratum {k[0]}/{k[1]}/{k[2]}"
    cap = sorted((r for r in sentences if r["unit_type"] == "caption_segment"), key=key)
    for r in spread_pick(cap, CAPTION_SLOTS, taken):
        picked.append(r)
        taken.add(r["sentence_id"])
        reason[r["sentence_id"]] = "caption_segment top-up"
    picked.sort(key=lambda r: (r["company"], key(r)))
    rows = []
    for i, r in enumerate(picked, 1):
        p = pas[r["sentence_id"]]
        rows.append(dict(
            review_id=f"G4R{i:03d}", sentence_id=r["sentence_id"], passage_id=p["passage_id"],
            company=r["company"], period_label=r["period_label"], calendar_year=r["calendar_year"],
            calendar_quarter=r["calendar_quarter"], call_date=r["call_date"], source_file=r["source_file"],
            source_url=r["source_url"], source_type=r["source_type"], unit_type=r["unit_type"],
            section=r["section"], speaker=r["speaker"], speaker_role=r["speaker_role"],
            speaker_status=r["speaker_status"], sentence_order_in_call=r["sentence_order_in_call"],
            match_type="uncertain" if r["is_uncertain"] == "1" else "core", trigger_terms=r["trigger_terms"],
            is_uncertain=r["is_uncertain"], is_context_dependent=r["is_context_dependent"], is_long=r["is_long"],
            text_verbatim=r["text_verbatim"], passage_text=p["text"],
            context_speaker_continuity=p["context_speaker_continuity"], selection=reason[r["sentence_id"]],
            reviewer_id="", review_date="", q_is_about_ai="", q_text_matches_source="", q_speaker_correct="",
            q_section_correct="", q_unit_boundary_ok="", reviewer_notes=""))
    write_csv(CANON / "manual_review_sample.csv", rows, list(rows[0].keys()))
    return {"seed": SEED, "n": len(rows), "strata": len(strata),
            "allocation": {"/".join(k): alloc[k] for k in sorted(strata)}, "caption_segment_top_up": CAPTION_SLOTS,
            "by_company": dict(Counter(r["company"] for r in rows)), "by_section": dict(Counter(r["section"] for r in rows)),
            "by_match_type": dict(Counter(r["match_type"] for r in rows)),
            "by_unit_type": dict(Counter(r["unit_type"] for r in rows)),
            "by_calendar_year": dict(sorted(Counter(r["calendar_year"] for r in rows).items())),
            "by_source_type": dict(Counter(r["source_type"] for r in rows)),
            "judgment_columns_blank": True,
            "note": "Review questions are mechanical (is it about AI, text/speaker/section/unit correct). "
                    "No opportunity/risk/efficiency/workforce or other substantive labels."}


if __name__ == "__main__":
    main()
