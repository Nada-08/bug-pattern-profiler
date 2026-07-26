from pinecone import Pinecone

from packages.common.settings import settings

class PineconeVectorStore:
    def __init__(self):
        if not settings.pinecone_api_key:
            raise ValueError(
                "PINECONE_API_KEY is missing. Add it to your .env file."
            )

        self.pc = Pinecone(api_key=settings.pinecone_api_key)
        self.index = self.pc.Index(settings.pinecone_index_name)

    def _clean_metadata(self, metadata: dict) -> dict:
        cleaned = {}

        for key, value in metadata.items():
            # skip None values
            if value is None:
                continue

            # Pinecone supports lists of strings
            if isinstance(value, list):
                cleaned[key] = [
                    str(item)
                    for item in value
                    if item is not None
                ]

            # supported primitive types
            elif isinstance(value, (str, int, float, bool)):
                cleaned[key] = value

            # fallback conversion
            else:
                cleaned[key] = str(value)

        return cleaned

    def upsert_vectors(self, vectors: list[dict],namespace: str | None = None): # insert if not exists, update if exists
        # clean metadata before upload
        for vector in vectors:
            if "metadata" in vector:
                vector["metadata"] = self._clean_metadata(
                    vector["metadata"]
                )

        self.index.upsert(
            vectors=vectors,
            namespace=namespace
        )

    def query(self, vector: list[float], top_k: int = 5, namespace: str | None = None, filter: dict | None = None) -> dict:

        result = self.index.query(
            vector=vector,
            top_k=top_k,
            filter=filter,
            include_metadata=True,
            namespace=namespace
        )

        return result
    
    def delete_namespace(self, namespace: str):
        self.index.delete(delete_all=True, namespace=namespace)