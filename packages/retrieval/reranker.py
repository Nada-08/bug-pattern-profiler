from sentence_transformers import CrossEncoder
from packages.retrieval.models import SearchResult


class Reranker:

    def __init__(
        self,
        model_name: str = "cross-encoder/ms-marco-MiniLM-L-6-v2"
    ):
        self.model = CrossEncoder(
            model_name
        )


    def rerank(
        self,
        query: str,
        documents: list[SearchResult],
        top_k: int = 5
    ) -> list[SearchResult]:

        if not documents:
            return []


        pairs = [
            (
                query,
                self._build_document_text(doc)
            )
            for doc in documents
        ]


        scores = self.model.predict(
            pairs
        )


        ranked = sorted(
            zip(documents, scores),
            key=lambda x: x[1],
            reverse=True
        )


        results = []

        for doc, score in ranked[:top_k]:
            doc.score = float(score)
            results.append(doc)


        return results



    def _build_document_text(
        self,
        doc: SearchResult
    ) -> str:

        return f"""
        CVE: {doc.cve_id}

        Title:
        {doc.title}

        Description:
        {doc.text}

        Severity:
        {doc.severity}

        Source:
        {doc.source_type}
        """