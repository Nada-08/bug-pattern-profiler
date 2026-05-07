from pathlib import Path

from packages.ingestion.sources.nvd_cve import fetch_nvd_page
from packages.ingestion.sources.cisa_kev import fetch_cisa_kev

from packages.ingestion.normalize.schema import NormalizedDocument
from packages.ingestion.normalize.nvd_normalizer import normalize_nvd_file
from packages.ingestion.normalize.cisa_kev_normalizer import normalize_cisa_kev_file

from packages.ingestion.fusion.kev_nvd_fuser import fuse_kev_with_nvd

from packages.ingestion.chunking.chunker import chunk_document
from packages.ingestion.storage.local_store import save_jsonl, load_jsonl


def run_ingest_local():
    print("Fetching NVD...")
    print("Fetching NVD pages...")

    nvd_raw_paths = []
    results_per_page = 100
    max_results = 1000

    for start_index in range(0, max_results, results_per_page):
        print(f"Fetching NVD start_index={start_index}...")
        path = fetch_nvd_page(
            start_index=start_index,
            results_per_page=results_per_page
        )
        nvd_raw_paths.append(path)
    
    print("Fetching CISA KEV...")
    cisa_raw_path = fetch_cisa_kev()

    print("Normalizing NVD...")
    nvd_docs = []

    for path in nvd_raw_paths:
        nvd_docs.extend(normalize_nvd_file(path))

    nvd_normalized_path = Path("data/normalized/nvd/nvd_combined.normalized.jsonl")
    save_jsonl(nvd_normalized_path, [doc.model_dump() for doc in nvd_docs])

    print("Chunking NVD...")
    nvd_chunks = []
    for doc in nvd_docs:
        nvd_chunks.extend(chunk_document(doc))
    nvd_chunks_path = Path("data/chunks/nvd/nvd_combined.chunks.jsonl")
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

    print("Fusing KEV + NVD...")
    fused_normalized_path = Path("data/normalized/fused/kev_nvd.normalized.jsonl")

    fuse_kev_with_nvd(
        kev_path=cisa_normalized_path,
        nvd_path=nvd_normalized_path,
        output_path=fused_normalized_path,
    )

    print("Loading fused docs...")
    fused_docs = load_jsonl(fused_normalized_path)

    print("Chunking fused KEV + NVD...")
    fused_chunks = []

    for doc_dict in fused_docs:
        doc = NormalizedDocument(**doc_dict)
        fused_chunks.extend(chunk_document(doc))

    fused_chunks_path = Path("data/chunks/fused/kev_nvd.chunks.jsonl")
    save_jsonl(fused_chunks_path, [chunk.model_dump() for chunk in fused_chunks])

    print()
    print("Done.")
    print(f"NVD docs: {len(nvd_docs)}")
    print(f"NVD chunks: {len(nvd_chunks)}")
    print(f"CISA KEV docs: {len(cisa_docs)}")
    print(f"CISA KEV chunks: {len(cisa_chunks)}")
    print(f"Fused docs: {len(fused_docs)}")
    print(f"Fused chunks: {len(fused_chunks)}")


if __name__ == "__main__":
    run_ingest_local()