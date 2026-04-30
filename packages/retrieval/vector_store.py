from pinecone import Pinecone

from packages.common.settings import settings

class PineconeVectorStore:
    def __init__(self):
        if not settings.pinecone_api_key:
            raise ValueError("PINECONE_API_KEY is missing. Add it to your .env file.")
        
        self.pc = Pinecone(api_key=settings.pinecone_api_key)
        self.index = self.pc.Index(settings.pinecone_index_name)

    def upsert_vectors(self, vectors: list[dict]): # uploads vectors into Pinecone.
        self.index.upsert(vectors=vectors)

    def query(self, vector: list[float], top_k: int = 5):
        return self.index.query(
            vector=vector,
            top_k=top_k,
            include_metadata=True
        )
