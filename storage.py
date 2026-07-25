"""File-based storage: dedup + grouped CSV/JSON export.

No external database. Each source_type ("10-K", "10-Q", "8-K",
challenger_report, earnings_call_snippet) is kept in its own pair of
CSV/JSON files under config.EXPORT_DIR. Dedup works by re-reading whatever
group files already exist at the start of a run and skipping any doc_id
already present, so re-running is safe without a separate index/service.

Upload the resulting EXPORT_DIR to Drive with gdrive.upload_export_dir().
"""
import csv
import hashlib
import json
import os
from datetime import datetime, timezone

import config

_EXPORT_FIELDS = ["doc_id", "company", "ticker", "source_type", "filing_date",
                  "section", "url", "text", "retrieved_at"]


def make_doc_id(document):
    """Deterministic id so re-pulling the same source doesn't duplicate rows.

    Dedup keys on source_type + company + url + section, since a single
    filing URL can legitimately yield multiple distinct documents (e.g.
    Item 1A and Item 7 of one 10-K share a URL) and those shouldn't
    collide or overwrite each other.
    """
    basis = "|".join([
        str(document.get("source_type", "")),
        str(document.get("company", "")),
        str(document.get("url", "")),
        str(document.get("section", "")),
    ])
    return hashlib.sha256(basis.encode("utf-8")).hexdigest()[:16]


def _group_key(document):
    return document.get("source_type") or "unknown"


def _group_paths(group, export_dir):
    safe = group.replace("/", "_").replace("\\", "_")
    return (
        os.path.join(export_dir, f"ai_washing_{safe}.csv"),
        os.path.join(export_dir, f"ai_washing_{safe}.json"),
    )


class Dataset:
    """Holds one collection run's documents, grouped by source_type.

    Existing group files are lazily loaded (once per group) the first time
    that group is touched, so save_document() can tell new docs from ones
    already exported on a prior run.
    """

    def __init__(self, export_dir=None):
        self.export_dir = export_dir or config.EXPORT_DIR
        self._groups = {}       # group -> {doc_id: doc}
        self._loaded = set()    # groups already loaded from disk

    def _ensure_loaded(self, group):
        if group in self._loaded:
            return
        self._loaded.add(group)
        _, json_path = _group_paths(group, self.export_dir)
        docs = {}
        if os.path.exists(json_path):
            with open(json_path, encoding="utf-8") as f:
                for d in json.load(f):
                    doc_id = d.get("doc_id")
                    if doc_id:
                        docs[doc_id] = d
        self._groups[group] = docs

    def save_document(self, document):
        """Add doc_id + retrieved_at and store unless already present.

        Returns (doc_id, is_new). Existing documents are left untouched.
        """
        doc = dict(document)
        doc_id = make_doc_id(doc)
        doc["doc_id"] = doc_id
        doc.setdefault("retrieved_at", datetime.now(timezone.utc).isoformat())

        group = _group_key(doc)
        self._ensure_loaded(group)
        existing = self._groups[group]
        is_new = doc_id not in existing
        if is_new:
            existing[doc_id] = doc
        return doc_id, is_new

    def get_all_documents(self):
        return [d for docs in self._groups.values() for d in docs.values()]

    def export(self):
        """Write each group to its own CSV + JSON file.

        Returns {group: (csv_path, json_path, doc_count)}.
        """
        os.makedirs(self.export_dir, exist_ok=True)
        results = {}
        for group, docs in self._groups.items():
            csv_path, json_path = _group_paths(group, self.export_dir)
            docs_list = list(docs.values())
            # utf-8-sig: adds a BOM so Excel (the likely way these get
            # opened on Windows) detects UTF-8 instead of defaulting to the
            # system codepage and mangling curly quotes/dashes into '?'.
            with open(csv_path, "w", newline="", encoding="utf-8-sig") as f:
                writer = csv.DictWriter(f, fieldnames=_EXPORT_FIELDS,
                                        extrasaction="ignore")
                writer.writeheader()
                for d in docs_list:
                    writer.writerow(d)
            with open(json_path, "w", encoding="utf-8") as f:
                json.dump(docs_list, f, indent=2, ensure_ascii=False)
            results[group] = (csv_path, json_path, len(docs_list))
        return results
