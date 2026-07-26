from pathlib import Path

from packages.ingestion.storage.local_store import load_json
from packages.retrieval.query_parser import QueryParser


QUERY_FILES = {
    "fused": Path("packages/evaluation/benchmark/benchmark_fused_queries.json"),
    "nvd": Path("packages/evaluation/benchmark/benchmark_nvd_queries.json"),
}

def analyze(namespace: str):

    parser = QueryParser()

    queries = load_json(
        QUERY_FILES[namespace]
    )

    total = 0
    success = 0

    print("\n" + "=" * 70)
    print(f"Analyzing parser: {namespace}")
    print("=" * 70)

    for scenario in queries:

        scenario_id = scenario["scenario_id"]

        for query in scenario["queries"]:

            total += 1

            entities = parser.parse(query)

            has_filter = any(
                value is not None
                for value in entities.__dict__.values()
            )

            if has_filter:
                success += 1
            else:
                print("\nFAILED")
                print("Scenario:", scenario_id)
                print("Query:", query)
                print("Entities:", entities)

    print("\nSummary")
    print("-" * 50)
    print("Queries:", total)
    print("Extracted:", success)
    print(
        "Coverage:",
        f"{success / total:.2%}"
    )


if __name__ == "__main__":

    analyze("fused")
    analyze("nvd")