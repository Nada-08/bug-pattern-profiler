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

OUTPUT_FILES = {
    "fused": Path("packages/evaluation/benchmark/benchmark_fused.json"),
    "nvd": Path("packages/evaluation/benchmark/benchmark_nvd.json"),
}


def main():
    for namespace in ("fused", "nvd"):
        print(f"\nGenerating benchmark for '{namespace}' namespace...")

        # Load scenarios
        with SCENARIO_FILES[namespace].open("r", encoding="utf-8") as f:
            scenarios = json.load(f)

        # Load corpus
        documents = list(load_jsonl(CORPORA[namespace]))

        benchmark = []

        for scenario in scenarios:
            ground_truth = sorted({
                doc["cve_id"]
                for doc in documents
                if matches(doc, scenario["filters"])
            })

            benchmark.append({
                **scenario,
                "ground_truth": ground_truth,
                "num_relevant": len(ground_truth),
            })

            print(
                f"{scenario['id']:<20}"
                f"{len(ground_truth):>5} relevant CVEs"
            )

        # Ensure output directory exists
        OUTPUT_FILES[namespace].parent.mkdir(parents=True, exist_ok=True)

        # Save benchmark
        with OUTPUT_FILES[namespace].open("w", encoding="utf-8") as f:
            json.dump(benchmark, f, indent=2)

        print(f"\n✓ Benchmark saved to: {OUTPUT_FILES[namespace]}")


if __name__ == "__main__":
    main()