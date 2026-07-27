from packages.retrieval.embedder import Embedder
from packages.retrieval.models import SearchResult
from packages.retrieval.vector_store import PineconeVectorStore
from packages.retrieval.mappers import pinecone_match_to_search_result
from packages.retrieval.query_parser import QueryParser
from packages.retrieval.filter_builder import FilterBuilder
from packages.retrieval.reranker import Reranker


class SearchService:
    def __init__(
        self,
        embedder: Embedder | None = None,
        vector_store: PineconeVectorStore | None = None,
        reranker: Reranker | None = None,
        retrieval_k: int = 25,
    ):
        self.embedder = embedder
        self.vector_store = vector_store
        self.query_parser = QueryParser()
        self.filter_builder = FilterBuilder()
        self.reranker = reranker or Reranker()
        self.retrieval_k = retrieval_k

    def search(
        self,
        query: str,
        top_k: int = 5,
        namespace: str | None = None,
        rerank: bool = True,
    ) -> list[SearchResult]:

        entities = self.query_parser.parse(query)
        metadata_filter = self.filter_builder.build(entities)

        query_embedding = self.embedder.embed_text(query)

        retrieve_k = max(self.retrieval_k, top_k * 2)

        results = self.vector_store.query(
            vector=query_embedding,
            top_k=retrieve_k,
            namespace=namespace,
            filter=metadata_filter,
        )

        documents = [
            pinecone_match_to_search_result(match)
            for match in results["matches"]
        ]

        if rerank:
            documents = self.reranker.rerank(
                query=query,
                documents=documents,
                top_k=top_k,
            )

        return documents

    def search_multi_source(
        self,
        query: str,
        top_k: int = 5,
    ) -> list[SearchResult]:

        nvd_results = self.search(
            query=query,
            top_k=self.retrieval_k,
            namespace="nvd",
            rerank=False,
        )

        fused_results = self.search(
            query=query,
            top_k=self.retrieval_k,
            namespace="fused",
            rerank=False,
        )

        merged = self._merge_results(
            nvd_results,
            fused_results,
        )

        reranked = self.reranker.rerank(
            query=query,
            documents=merged,
            top_k=top_k,
        )

        return [
            r for r in reranked
            if r.source_type == "kev"
            or r.vendor
            or r.product
        ]

    def _merge_results(
        self,
        *result_sets,
    ) -> list[SearchResult]:

        merged: dict[str, SearchResult] = {}

        for results in result_sets:
            for item in results:

                if not item.cve_id:
                    continue

                if item.cve_id not in merged:
                    merged[item.cve_id] = item
                else:
                    merged[item.cve_id] = self._combine_results(
                        merged[item.cve_id],
                        item,
                    )

        return list(merged.values())

    def _combine_results(
        self,
        first: SearchResult,
        second: SearchResult,
    ) -> SearchResult:

        data = {}

        for field in SearchResult.model_fields:

            value1 = getattr(first, field)
            value2 = getattr(second, field)

            data[field] = (
                value1
                if value1 not in (None, "", [])
                else value2
            )

        for field in [
            "vendor",
            "product",
            "tags",
            "cwe_ids",
        ]:
            data[field] = list({
                *(getattr(first, field) or []),
                *(getattr(second, field) or []),
            })

        data["score"] = max(first.score, second.score)

        return SearchResult(**data)