from pathlib import Path
from time import perf_counter
from datetime import timedelta

from packages.ingestion.storage.local_store import load_jsonl
from packages.retrieval.embedder import Embedder
from packages.retrieval.vector_store import PineconeVectorStore


BATCH_SIZE = 100

def format_duration(seconds: float) -> str:
    return str(timedelta(seconds=round(seconds, 2)))


# Start overall timer
overall_start = perf_counter()


chunk_path = Path("data/chunks/cisa_kev/cisa_kev.chunks.jsonl")

chunks = load_jsonl(chunk_path)

embedder = Embedder()
store = PineconeVectorStore()

print("Total chunks:", len(chunks))

for i in range(0, len(chunks), BATCH_SIZE):
    batch_start = perf_counter()

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
                "vendor": chunk["vendor"],
                "product": chunk["product"],
                "published_at": chunk["published_at"],
                "tags": chunk["tags"],
            }
        })

    store.upsert_vectors(vectors)

    batch_end = perf_counter()
    batch_duration = batch_end - batch_start

    print(
        f"Uploaded batch {i // BATCH_SIZE + 1} "
        f"({len(vectors)} vectors) "
        f"in {format_duration(batch_duration)}"
    )

overall_end = perf_counter()
overall_duration = overall_end - overall_start

print()
print("Finished uploading all KEV chunks.")
print(f"Total execution time: {format_duration(overall_duration)}")
print(f"Started at: {overall_start:.4f}")
print(f"Finished at: {overall_end:.4f}")