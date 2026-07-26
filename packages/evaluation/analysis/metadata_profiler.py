from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

class MetadataProfiler:
    def __init__(self, jsonl_path: str | Path):
        self.jsonl_path = Path(jsonl_path)

        self.total_docs = 0
        self.source_counts = Counter()

        self.vendor_counter = Counter()
        self.product_counter = Counter()
        self.cwe_counter = Counter()
        self.severity_counter = Counter()
        self.year_counter = Counter()

        self.unique_cves = set()

        self.field_presence = defaultdict(int)

    def profile(self) -> dict[str, Any]:
        with self.jsonl_path.open("r", encoding="utf-8") as f:
            for line in f:
                if not line.strip():
                    continue

                doc = json.loads(line)
                self.total_docs += 1

                self.source_counts[doc.get("source_name", "Unknown")] += 1

                self._process_document(doc)

        return self._build_report()

    def _process_document(self, doc: dict):

        if doc.get("cve_id"):
            self.unique_cves.add(doc["cve_id"])
            self.field_presence["cve_id"] += 1

        for vendor in doc.get("vendor", []):
            if vendor:
                self.vendor_counter[vendor] += 1
        if doc.get("vendor"):
            self.field_presence["vendor"] += 1

        for product in doc.get("product", []):
            if product:
                self.product_counter[product] += 1
        if doc.get("product"):
            self.field_presence["product"] += 1

        for cwe in doc.get("cwe_ids", []):
            if cwe:
                self.cwe_counter[cwe] += 1
        if doc.get("cwe_ids"):
            self.field_presence["cwe_ids"] += 1

        severity = doc.get("severity")
        if severity:
            self.severity_counter[severity] += 1
            self.field_presence["severity"] += 1
        else:
            self.severity_counter["UNKNOWN"] += 1

        published = doc.get("published_at")
        if published:
            year = published[:4]
            self.year_counter[year] += 1
            self.field_presence["published_at"] += 1

        for field in [
            "cvss_score",
            "attack_vector",
            "attack_complexity",
            "privileges_required",
            "exploitability_score",
            "impact_score",
            "due_date",
            "required_action",
            "known_ransomware_use",
            "notes",
        ]:
            if doc.get(field) not in (None, "", []):
                self.field_presence[field] += 1

    def _build_report(self):

        return {
            "corpus": {
                "total_documents": self.total_docs,
                "unique_cves": len(self.unique_cves),
                "sources": dict(self.source_counts),
            },
            "top_vendors": self.vendor_counter.most_common(30),
            "top_products": self.product_counter.most_common(30),
            "top_cwes": self.cwe_counter.most_common(30),
            "severity_distribution": dict(self.severity_counter),
            "publication_years": dict(sorted(self.year_counter.items())),
            "metadata_completeness": {
                field: {
                    "count": count,
                    "percent": round(count / self.total_docs * 100, 2),
                }
                for field, count in sorted(self.field_presence.items())
            },
        }