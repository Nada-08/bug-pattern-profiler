from __future__ import annotations

from packages.evaluation.retrieval.report_writer import ReportWriter
from packages.evaluation.retrieval.retrieval_evaluator import RetrievalEvaluator
from packages.retrieval.embedder import Embedder
from packages.retrieval.search_service import SearchService
from packages.retrieval.vector_store import PineconeVectorStore


def build_search_service() -> SearchService:
    embedder = Embedder()

    vector_store = PineconeVectorStore()

    return SearchService(
        embedder=embedder,
        vector_store=vector_store,
    )


def evaluate_namespace(
    namespace: str,
    experiment_name: str,
):
    print("=" * 70)
    print(f"Evaluating namespace: {namespace}")
    print("=" * 70)

    search_service = build_search_service()

    evaluator = RetrievalEvaluator(
        search_service=search_service,
        namespace=namespace,
        ks = [10, 50, 100],
        experiment_name=experiment_name,
        retrieval_method="dense",
        embedding_model="BAAI/bge-small-en-v1.5"
    )

    result = evaluator.evaluate()

    report_path = ReportWriter().write(result)

    print("\nSummary (overall @10)")
    print("-" * 70)
    print(f"Recall@10    : {result.summary.recall:.4f}")
    print(f"Precision@10 : {result.summary.precision:.4f}")
    print(f"NDCG@10      : {result.summary.ndcg:.4f}")
    print(f"MRR          : {result.summary.mrr:.4f}")
    print(f"R-Precision  : {result.summary.r_precision:.4f}")

    print("\nSummary (by ground-truth-size bucket)")
    print("-" * 70)
    for bucket_name, metrics in result.by_bucket.items():
        print(f"\n{bucket_name} (n={metrics['num_queries']})")
        print(f"  Recall@10    : {metrics['recall@10']:.4f}")
        print(f"  Precision@10 : {metrics['precision@10']:.4f}")
        print(f"  NDCG@10      : {metrics['ndcg@10']:.4f}")
        print(f"  MRR          : {metrics['mrr']:.4f}")
        print(f"  R-Precision  : {metrics['r_precision']:.4f}")

    print(f"\nReport saved to:\n{report_path}")


def main():
    experiment_name = "reranker_hybrid_retrieval_evaluation"

    evaluate_namespace(
        namespace="fused",
        experiment_name=experiment_name,
    )

    evaluate_namespace(
        namespace="nvd",
        experiment_name=experiment_name,
    )


if __name__ == "__main__":
    main()