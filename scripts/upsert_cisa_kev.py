from pathlib import Path
from datetime import datetime

from packages.ingestion.storage.local_store import load_jsonl
from packages.retrieval.embedder import Embedder
from packages.retrieval.vector_store import PineconeVectorStore


BATCH_SIZE = 100

chunk_path = Path("data/chunks/fused/kev_nvd.chunks.jsonl")

chunks = load_jsonl(chunk_path)

embedder = Embedder()
store = PineconeVectorStore()

print("Total NVD chunks:", len(chunks))

start_time = datetime.now()

for i in range(0, len(chunks), BATCH_SIZE):
    batch_start = datetime.now()

    batch = chunks[i:i + BATCH_SIZE]
    texts = [chunk["text"] for chunk in batch]

    embeddings = embedder.embed_batch(texts)

    vectors = []

    for chunk, embedding in zip(batch, embeddings):
        vectors.append({
            "id": chunk["chunk_id"],
            "values": embedding,
            "metadata": {
                "doc_id": chunk["doc_id"],
                "source_type": chunk["source_type"],
                "source_name": chunk["source_name"],
                "title": chunk["title"],
                "text": chunk["text"],
                "cve_id": chunk["cve_id"],
                "cwe_ids": chunk.get("cwe_ids", []),
                "vendor": chunk.get("vendor", []),
                "product": chunk.get("product", []),
                "severity": chunk.get("severity"),
                "published_at": chunk.get("published_at"),
                "tags": chunk.get("tags", []),
            }
        })

    store.upsert_vectors(vectors, namespace="fused")

    batch_end = datetime.now()
    print(
        f"Uploaded batch {i // BATCH_SIZE + 1} "
        f"({len(vectors)} vectors) in {batch_end - batch_start}"
    )

end_time = datetime.now()

print()
print("Finished uploading all NVD chunks.")
print("Total execution time:", end_time - start_time)