from __future__ import annotations

from dataclasses import asdict, dataclass

@dataclass(slots=True)
class QueryMetrics:
    recall: dict[str, float]
    precision: dict[str, float]
    ndcg: dict[str, float]
    reciprocal_rank: float
    r_precision: float


@dataclass(slots=True)
class QueryResult:
    scenario_id: str
    query: str
    ground_truth: list[str]
    retrieved: list[str]
    metrics: QueryMetrics
    bucket: str


@dataclass(slots=True)
class EvaluationSummary:
    recall: float
    precision: float
    mrr: float
    ndcg: float
    r_precision: float


@dataclass(slots=True)
class EvaluationResult:
    namespace: str
    ks: list[int]
    num_queries: int
    created_at: str

    experiment_name: str
    embedding_model: str
    retrieval_method: str

    summary: EvaluationSummary
    query_results: list[QueryResult]

    by_bucket: dict

    def to_dict(self) -> dict:
        return asdict(self)