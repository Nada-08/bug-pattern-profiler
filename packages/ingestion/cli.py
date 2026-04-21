from pathlib import Path

from packages.ingestion.sources.nvd_cve import fetch_nvd_page
from packages.ingestion.sources.cisa_kev import fetch_cisa_kev

from packages.ingestion.normalize.nvd_normalizer import normalize_nvd_file
from packages.ingestion.normalize.cisa_kev_normalizer import normalize_cisa_kev_file

from packages.ingestion.chunking.chunker import chunk_document
from packages.ingestion.storage.local_store import save_jsonl


def run_ingest_local():
    print("Fetching NVD...")
    nvd_raw_path = fetch_nvd_page(start_index=0, results_per_page=10)

    print("Fetching CISA KEV...")
    cisa_raw_path = fetch_cisa_kev()

    print("Normalizing NVD...")
    nvd_docs = normalize_nvd_file(nvd_raw_path)
    nvd_normalized_path = Path("data/normalized/nvd/nvd_page_0.normalized.jsonl")
    save_jsonl(nvd_normalized_path, [doc.model_dump() for doc in nvd_docs])

    print("Chunking NVD...")
    nvd_chunks = []
    for doc in nvd_docs:
        nvd_chunks.extend(chunk_document(doc))
    nvd_chunks_path = Path("data/chunks/nvd/nvd_page_0.chunks.jsonl")
    save_jsonl(nvd_chunks_path, [chunk.model_dump() for chunk in nvd_chunks])

    print("Normalizing CISA KEV...")
    cisa_docs = normalize_cisa_kev_file(cisa_raw_path)
    cisa_normalized_path = Path("data/normalized/cisa_kev/cisa_kev.normalized.jsonl")
    save_jsonl(cisa_normalized_path, [doc.model_dump() for doc in cisa_docs])

    print("Chunking CISA KEV...")
    cisa_chunks = []
    for doc in cisa_docs:
        cisa_chunks.extend(chunk_document(doc))
    cisa_chunks_path = Path("data/chunks/cisa_kev/cisa_kev.chunks.jsonl")
    save_jsonl(cisa_chunks_path, [chunk.model_dump() for chunk in cisa_chunks])

    print()
    print("Done.")
    print(f"NVD docs: {len(nvd_docs)}")
    print(f"NVD chunks: {len(nvd_chunks)}")
    print(f"CISA KEV docs: {len(cisa_docs)}")
    print(f"CISA KEV chunks: {len(cisa_chunks)}")


if __name__ == "__main__":
    run_ingest_local()