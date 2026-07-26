from __future__ import annotations

import random
from pathlib import Path

from packages.ingestion.storage.local_store import load_jsonl

CORPUS = Path("data/chunks/nvd/nvd_combined.chunks.jsonl")


def main():
    documents = list(load_jsonl(CORPUS))

    cves = sorted({
        doc["cve_id"]
        for doc in documents
        if doc.get("cve_id")
    })

    random.seed(42)  # reproducible
    sample = random.sample(cves, min(50, len(cves)))

    print("Sampled CVEs:\n")
    for cve in sorted(sample):
        print(cve)


if __name__ == "__main__":
    main()