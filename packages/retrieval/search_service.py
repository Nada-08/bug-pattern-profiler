from packages.retrieval.embedder import Embedder
from packages.retrieval.vector_store import PineconeVectorStore

class SearchService:
    def __init__(self):
        self.embedder = Embedder()
        self.vector_store = PineconeVectorStore()

    def search(self, query: str, top_k: int = 5, namespace: str | None = None) -> list[dict]:
        query_embedding = self.embedder.embed_text(query)

        results = self.vector_store.query(
            vector=query_embedding,
            top_k=top_k,
            namespace=namespace
        )

        matches = []

        for match in results["matches"]:
            metadata = match["metadata"]

            matches.append({
                "score": match["score"],
                "chunk_id": match["id"],
                "doc_id": metadata.get("doc_id"),
                "cve_id": metadata.get("cve_id"),
                "title": metadata.get("title"),
                "text": metadata.get("text"),
                "source_type": metadata.get("source_type"),
                "source_name": metadata.get("source_name"),
                "vendor": metadata.get("vendor"),
                "product": metadata.get("product"),
                "published_at": metadata.get("published_at"),
                "tags": metadata.get("tags"),
                "severity": metadata.get("severity"),
                "cvss_score": metadata.get("cvss_score"),
                "cwe_ids": metadata.get("cwe_ids"),
                "attack_vector": metadata.get("attack_vector"),
                "attack_complexity": metadata.get("attack_complexity"),
                "privileges_required": metadata.get("privileges_required"),
                "exploitability_score": metadata.get("exploitability_score"),
                "impact_score": metadata.get("impact_score"),
            })
            
        return matches