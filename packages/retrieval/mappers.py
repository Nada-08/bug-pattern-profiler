from packages.retrieval.models import SearchResult

def pinecone_match_to_search_result(match: dict) -> SearchResult:
    metadata = match["metadata"]

    return SearchResult(
        score=match["score"],
        chunk_id=match["id"],
        **metadata,
    )