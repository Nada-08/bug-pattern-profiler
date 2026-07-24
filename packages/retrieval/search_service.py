from packages.retrieval.embedder import Embedder
from packages.retrieval.models import SearchResult
from packages.retrieval.vector_store import PineconeVectorStore
from packages.retrieval.mappers import pinecone_match_to_search_result


class SearchService:
    def __init__(
        self,
        embedder: Embedder | None = None,
        vector_store: PineconeVectorStore | None = None
    ):
        self.embedder = embedder
        self.vector_store = vector_store

    def search(
        self,
        query: str,
        top_k: int = 5,
        namespace: str | None = None,
    ) -> list[SearchResult]:

        query_embedding = self.embedder.embed_text(query)

        results = self.vector_store.query(
            vector=query_embedding,
            top_k=top_k,
            namespace=namespace,
        )

        return [
            pinecone_match_to_search_result(match)
            for match in results["matches"]
        ]