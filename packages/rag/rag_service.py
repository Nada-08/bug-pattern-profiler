from packages.retrieval.search_service import SearchService
from packages.generation.generation_service import AnswerGenerationService
from packages.retrieval.vector_store import PineconeVectorStore
from packages.retrieval.embedder import Embedder

class RAGService: 
    def __init__(self):
        self.search_service = SearchService(embedder=Embedder(), vector_store=PineconeVectorStore())
        self.generation_service = AnswerGenerationService()

    def answer(self, query: str, top_k: int = 5, namespace: str | str = "fused") -> dict:
        # contexts = self.search_service.search(query=query, top_k=top_k, namespace=namespace)

        contexts = self.search_service.search_multi_source(
            query=query,
            top_k=top_k
        )

        answer  = self.generation_service.generate_answer(
            query=query,
            contexts=contexts
        )
        
        return {
            "query": query,
            "answer": answer,
            "sources": contexts
        }