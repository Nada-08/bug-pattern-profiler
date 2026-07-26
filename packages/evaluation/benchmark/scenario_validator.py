from __future__ import annotations

import json
from pathlib import Path

from packages.evaluation.benchmark.matcher import matches
from packages.ingestion.storage.local_store import load_jsonl

SCENARIO_FILES = {
    "fused": Path("packages/evaluation/benchmark/benchmark_fused_scenarios.json"),
    "nvd": Path("packages/evaluation/benchmark/benchmark_nvd_scenarios.json"),
}

CORPORA = {
    "fused": Path("data/chunks/fused/kev_nvd.chunks.jsonl"),
    "nvd": Path("data/chunks/nvd/nvd_combined.chunks.jsonl"),
}


def main():
    for namespace in ("fused", "nvd"):
        with SCENARIO_FILES[namespace].open("r", encoding="utf-8") as f:
            scenarios = json.load(f)

        documents = list(load_jsonl(CORPORA[namespace]))

        print("\n" + "=" * 70)
        print(f"Scenario Validation ({namespace.upper()})")
        print("=" * 70)

        passed = 0

        for scenario in scenarios:
            count = sum(
                1
                for doc in documents
                if matches(doc, scenario["filters"])
            )

            status = "✓" if count > 0 else "✗"

            print(
                f"{status} "
                f"{scenario['id']:<20}"
                f"{count:>5} matches"
            )

            if count > 0:
                passed += 1

        print("=" * 70)
        print(f"Passed : {passed}")
        print(f"Failed : {len(scenarios) - passed}")
        print("=" * 70)


if __name__ == "__main__":
    main()