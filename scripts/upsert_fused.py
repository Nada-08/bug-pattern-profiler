from pathlib import Path
from datetime import datetime

from sympy import pprint

from packages.ingestion.storage.local_store import load_jsonl
from packages.retrieval.embedder import Embedder
from packages.retrieval.vector_store import PineconeVectorStore

BATCH_SIZE = 100

embedder = Embedder()
store = PineconeVectorStore()

def upsert_chunks(chunk_path: Path, namespace: str):
    chunks = load_jsonl(chunk_path)

    print(f"\nUploading {len(chunks)} chunks to namespace '{namespace}'")

    start_time = datetime.now()

    START_INDEX = 0

    for i in range(START_INDEX, len(chunks), BATCH_SIZE):
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
                    "cvss_score": chunk.get("cvss_score"),

                    "attack_vector": chunk.get("attack_vector"),
                    "attack_complexity": chunk.get("attack_complexity"),
                    "privileges_required": chunk.get("privileges_required"),
                    "exploitability_score": chunk.get("exploitability_score"),
                    "impact_score": chunk.get("impact_score"),

                    "published_at": chunk.get("published_at"),
                    "tags": chunk.get("tags", []),

                    # KEV-specific fields
                    "due_date": chunk.get("due_date"),
                    "required_action": chunk.get("required_action"),
                    "known_ransomware_use": chunk.get("known_ransomware_use"),
                    "notes": chunk.get("notes"),
                }
            })

        
        store.upsert_vectors(vectors, namespace=namespace)

        print(
            f"Batch {i // BATCH_SIZE + 1} "
            f"({len(vectors)} vectors)"
        )

    print(f"Finished uploading '{namespace}' in {datetime.now() - start_time}")


if __name__ == "__main__":
    # upsert_chunks(
    #     Path("data/chunks/nvd/nvd_combined.chunks.jsonl"),
    #     namespace="nvd",
    # )

    upsert_chunks(
        Path("data/chunks/fused/kev_nvd.chunks.jsonl"),
        namespace="fused",
    )