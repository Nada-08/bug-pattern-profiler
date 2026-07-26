from __future__ import annotations
import numpy as np

from pathlib import Path
from datetime import datetime

from packages.evaluation.retrieval.results import (
    EvaluationResult,
    EvaluationSummary,
    QueryMetrics,
    QueryResult,
)
from packages.ingestion.storage.local_store import load_json
from packages.evaluation.retrieval.metrics import (
    ndcg_at_k,
    precision_at_k,
    recall_at_k,
    reciprocal_rank,
    r_precision,
)
from packages.retrieval.search_service import SearchService
from packages.retrieval.models import SearchResult


BENCHMARK_FILES = {
    "fused": Path("packages/evaluation/benchmark/benchmark_fused.json"),
    "nvd": Path("packages/evaluation/benchmark/benchmark_nvd.json"),
}

QUERY_FILES = {
    "fused": Path("packages/evaluation/benchmark/benchmark_fused_queries.json"),
    "nvd": Path("packages/evaluation/benchmark/benchmark_nvd_queries.json"),
}


def compute_bucket_thresholds(gt_counts: list[int]) -> tuple[float, float]:
    p33, p66 = np.percentile(gt_counts, [33, 66])
    return p33, p66


def bucket_for(gt_count: int, p33: float, p66: float) -> str:
    if gt_count <= p33:
        return "narrow"
    elif gt_count <= p66:
        return "medium"
    return "broad"

class RetrievalEvaluator:

    def __init__(
        self,
        search_service: SearchService,
        namespace: str,
        ks: list[int] = [10, 50, 100],
        experiment_name: str = "baseline",
        retrieval_method: str = "dense",
        embedding_model: str = "BAAI/bge-small-en-v1.5",
    ):
        self.search_service = search_service
        self.namespace = namespace
        self.ks = ks
        self.experiment_name = experiment_name
        self.retrieval_method = retrieval_method
        self.embedding_model = embedding_model

        self.benchmark = load_json(BENCHMARK_FILES[self.namespace])
        self.query_sets = load_json(QUERY_FILES[self.namespace])

    def evaluate(self) -> EvaluationResult:
        benchmark_lookup = {item["id"]: item for item in self.benchmark}

        # First pass: collect all ground truths per query so we can compute thresholds
        all_queries = []
        for scenario in self.query_sets:
            scenario_id = scenario["scenario_id"]
            ground_truth = benchmark_lookup[scenario_id]["ground_truth"]
            for query in scenario["queries"]:
                all_queries.append((scenario_id, query, ground_truth))

        gt_counts = [len(gt) for _, _, gt in all_queries]
        p33, p66 = compute_bucket_thresholds(gt_counts)

        query_results = []
        ground_truth_sizes = []

        for scenario_id, query, ground_truth in all_queries:
            gt_count = len(ground_truth)

            ground_truth_sizes.append({
                "scenario_id": scenario_id,
                "query": query,
                "ground_truth_count": gt_count,
            })

            results = self.search_service.search(
                query=query,
                namespace=self.namespace,
                top_k=max(self.ks),
            )

            retrieved = self._extract_cve_ids(results)

            metrics = QueryMetrics(
                recall={str(k): recall_at_k(retrieved, ground_truth, k) for k in self.ks},
                precision={str(k): precision_at_k(retrieved, ground_truth, k) for k in self.ks},
                ndcg={str(k): ndcg_at_k(retrieved, ground_truth, k) for k in self.ks},
                reciprocal_rank=reciprocal_rank(retrieved, ground_truth),
                r_precision=r_precision(retrieved, ground_truth),
            )

            query_results.append(
                QueryResult(
                    scenario_id=scenario_id,
                    query=query,
                    ground_truth=ground_truth,
                    retrieved=retrieved,
                    metrics=metrics,
                    bucket=bucket_for(gt_count, p33, p66),
                )
            )

        self._inspect_ground_truth_sizes(ground_truth_sizes)

        print(f"\nBucket thresholds (namespace='{self.namespace}'): "
            f"narrow ≤ {p33:.1f}, medium ≤ {p66:.1f}, broad > {p66:.1f}")

        summary, by_bucket = self._summarize(query_results)

        return EvaluationResult(
            namespace=self.namespace,
            ks=self.ks,
            num_queries=len(query_results),
            created_at=datetime.now().isoformat(),
            experiment_name=self.experiment_name,
            retrieval_method=self.retrieval_method,
            embedding_model=self.embedding_model,
            summary=summary,
            query_results=query_results,
            by_bucket=by_bucket,
        )

    @staticmethod
    def _extract_cve_ids(results: list[SearchResult]) -> list[str]:
        return [result.cve_id for result in results]

    def _summarize(self, query_results):
        if not query_results:
            return EvaluationSummary(recall=0.0, precision=0.0, mrr=0.0, ndcg=0.0, r_precision=0.0), {}

        scenario_metrics = {}
        buckets = {"narrow": [], "medium": [], "broad": []}

        for result in query_results:
            scenario_metrics.setdefault(result.scenario_id, []).append(result.metrics)
            buckets[result.bucket].append(result)

        self._print_scenario_metrics(scenario_metrics)

        overall = self._aggregate_at_10(query_results)

        by_bucket = {
            b: {"num_queries": len(results), **self._aggregate_at_10(results)}
            for b, results in buckets.items()
            if results
        }

        self._print_bucket_summary(by_bucket)

        summary = EvaluationSummary(
            recall=overall["recall@10"],
            precision=overall["precision@10"],
            ndcg=overall["ndcg@10"],
            mrr=overall["mrr"],
            r_precision=overall["r_precision"],
        )

        return summary, by_bucket

    @staticmethod
    def _aggregate_at_10(results: list[QueryResult]) -> dict:
        recall_10 = [r.metrics.recall["10"] for r in results]
        precision_10 = [r.metrics.precision["10"] for r in results]
        ndcg_10 = [r.metrics.ndcg["10"] for r in results]
        rr = [r.metrics.reciprocal_rank for r in results]
        rp = [r.metrics.r_precision for r in results]
        n = len(results)
        return {
            "recall@10": round(sum(recall_10) / n, 4),
            "precision@10": round(sum(precision_10) / n, 4),
            "ndcg@10": round(sum(ndcg_10) / n, 4),
            "mrr": round(sum(rr) / n, 4),
            "r_precision": round(sum(rp) / n, 4),
        }

    def _print_bucket_summary(self, by_bucket):
        print("\nBucketed Metrics (by ground-truth size) — @10")
        print("-" * 70)
        for b in ("narrow", "medium", "broad"):
            if b not in by_bucket:
                continue
            m = by_bucket[b]
            print(f"{b:<8} n={m['num_queries']:<4} "
                  f"recall@10={m['recall@10']:.4f}  "
                  f"precision@10={m['precision@10']:.4f}  "
                  f"ndcg@10={m['ndcg@10']:.4f}  "
                  f"mrr={m['mrr']:.4f}  "
                  f"r_precision={m['r_precision']:.4f}")

    def _inspect_ground_truth_sizes(self, sizes):

        print("\nGround Truth Size Distribution")
        print("-" * 50)

        counts = [
            item["ground_truth_count"]
            for item in sizes
        ]

        print(f"Queries: {len(counts)}")
        print(f"Average GT size: {sum(counts)/len(counts):.2f}")
        print(f"Min GT size: {min(counts)}")
        print(f"Max GT size: {max(counts)}")

        print("\nLargest queries:")
        
        for item in sorted(
            sizes,
            key=lambda x: x["ground_truth_count"],
            reverse=True
        )[:10]:
            print(
                f"{item['ground_truth_count']:>4} | {item['query']}"
            )

    def _print_scenario_metrics(self, scenario_metrics):

        print("\nScenario Metrics")
        print("-" * 70)

        for scenario, metrics in scenario_metrics.items():

            print(f"\n{scenario}")

            print(
                "Recall@10:",
                sum(
                    m.recall["10"]
                    for m in metrics
                ) / len(metrics)
            )

            print(
                "MRR:",
                sum(
                    m.reciprocal_rank
                    for m in metrics
                ) / len(metrics)
            )

            print(
                "R-Precision:",
                sum(
                    m.r_precision
                    for m in metrics
                ) / len(metrics)
            )