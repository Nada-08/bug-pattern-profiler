from __future__ import annotations

from math import log2


def recall_at_k(
    retrieved: list[str],
    relevant: list[str],
    k: int,
) -> float:
    """
    Recall@K = relevant retrieved / total relevant
    """

    if not relevant:
        return 0.0

    retrieved_k = set(retrieved[:k])
    relevant = set(relevant)

    return len(retrieved_k & relevant) / len(relevant)


def precision_at_k(
    retrieved: list[str],
    relevant: list[str],
    k: int,
) -> float:
    """
    Precision@K = relevant retrieved / retrieved count
    """

    if k <= 0:
        return 0.0

    retrieved_k = set(retrieved[:k])
    relevant = set(relevant)

    denominator = min(k, len(retrieved))

    if denominator == 0:
        return 0.0

    return len(retrieved_k & relevant) / denominator


def reciprocal_rank(
    retrieved: list[str],
    relevant: list[str],
) -> float:
    """
    Reciprocal Rank = 1 / rank of first relevant result
    """

    relevant = set(relevant)

    for rank, cve in enumerate(retrieved, start=1):
        if cve in relevant:
            return 1.0 / rank

    return 0.0


def dcg_at_k(
    retrieved: list[str],
    relevant: list[str],
    k: int,
) -> float:
    """
    Discounted Cumulative Gain
    """

    relevant = set(relevant)

    score = 0.0

    for rank, cve in enumerate(retrieved[:k], start=1):
        if cve in relevant:
            score += 1 / log2(rank + 1)

    return score


def ndcg_at_k(
    retrieved: list[str],
    relevant: list[str],
    k: int,
) -> float:
    """
    Normalized Discounted Cumulative Gain
    """

    ideal_hits = min(len(relevant), k)

    if ideal_hits == 0:
        return 0.0

    ideal_dcg = sum(
        1 / log2(rank + 1)
        for rank in range(1, ideal_hits + 1)
    )

    actual_dcg = dcg_at_k(retrieved, relevant, k)

    return actual_dcg / ideal_dcg


def r_precision(
    retrieved: list[str],
    relevant: list[str],
) -> float:
    """
    R-Precision = relevant retrieved in top-R / R, where R = total relevant

    Normalizes for ground-truth size so queries with vastly different
    |relevant| are comparable (unlike Recall@fixed-k, which is capped
    at k / |relevant| for large ground truths).
    """

    if not relevant:
        return 0.0

    r = len(relevant)
    retrieved_r = set(retrieved[:r])
    relevant = set(relevant)

    return len(retrieved_r & relevant) / r