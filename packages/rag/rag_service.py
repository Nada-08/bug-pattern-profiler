from packages.retrieval.search_service import SearchService
from packages.generation.generation_service import GenerationService

class RAGService: 
    def __init__(self):
        self.search_service = SearchService()
        self.generation_service = GenerationService()

    def answer(self, query: str, top_k: int = 5, namespace: str | None = None) -> dict:
        contexts = self.search_service.search(query=query, top_k=top_k, namespace=namespace)

        answer  = self.generation_service.generate_answer(
            query=query,
            contexts=contexts
        )

        return {
            "query": query,
            "answer": answer,
            "sources": contexts
        }