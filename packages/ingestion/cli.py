from pathlib import Path
import time

from packages.ingestion.sources.nvd_cve import fetch_nvd_page
from packages.ingestion.sources.cisa_kev import fetch_cisa_kev

from packages.ingestion.normalize.schema import NormalizedDocument
from packages.ingestion.normalize.nvd_normalizer import normalize_nvd_file
from packages.ingestion.normalize.cisa_kev_normalizer import normalize_cisa_kev_file

from packages.ingestion.fusion.kev_nvd_fuser import fuse_kev_with_nvd

from packages.ingestion.chunking.chunker import chunk_document
from packages.ingestion.storage.local_store import save_jsonl, load_jsonl


RAW_NVD_DIR = Path("data/raw/nvd")
RAW_KEV_DIR = Path("data/raw/cisa_kev")

NORMALIZED_NVD_PATH = Path("data/normalized/nvd/nvd_combined.normalized.jsonl")
NORMALIZED_KEV_PATH = Path("data/normalized/cisa_kev/cisa_kev.normalized.jsonl")
NORMALIZED_FUSED_PATH = Path("data/normalized/fused/kev_nvd.normalized.jsonl")

NVD_CHUNKS_PATH = Path("data/chunks/nvd/nvd_combined.chunks.jsonl")
KEV_CHUNKS_PATH = Path("data/chunks/cisa_kev/cisa_kev.chunks.jsonl")
FUSED_CHUNKS_PATH = Path("data/chunks/fused/kev_nvd.chunks.jsonl")


def fetch_data():
    # print("Fetching NVD...")

    # results_per_page = 100
    # start_index = 0

    # while True:
    #     path, total_results = fetch_nvd_page(
    #         start_index=start_index,
    #         results_per_page=results_per_page,
    #     )

    #     print(f"Fetched {path.name}")

    #     start_index += results_per_page

    #     if start_index >= total_results:
    #         break

    #     time.sleep(10)

    print("Fetching CISA KEV...")
    fetch_cisa_kev()


def normalize_data():
    print("Normalizing NVD...")

    nvd_docs = []

    raw_paths = sorted(RAW_NVD_DIR.glob("*.json"))

    for path in raw_paths:
        print(f"Normalizing {path.name}")
        nvd_docs.extend(normalize_nvd_file(path))

    save_jsonl(
        NORMALIZED_NVD_PATH,
        [doc.model_dump() for doc in nvd_docs],
    )

    print(f"NVD documents: {len(nvd_docs)}")

    print("Normalizing CISA KEV...")

    kev_raw_path = next(RAW_KEV_DIR.glob("*.json"))

    kev_docs = normalize_cisa_kev_file(kev_raw_path)

    save_jsonl(
        NORMALIZED_KEV_PATH,
        [doc.model_dump() for doc in kev_docs],
    )

    print(f"KEV documents: {len(kev_docs)}")


def chunk_data():
    print("Chunking NVD...")

    nvd_docs = [
        NormalizedDocument(**doc)
        for doc in load_jsonl(NORMALIZED_NVD_PATH)
    ]

    nvd_chunks = []

    for doc in nvd_docs:
        nvd_chunks.extend(chunk_document(doc))

    save_jsonl(
        NVD_CHUNKS_PATH,
        [chunk.model_dump() for chunk in nvd_chunks],
    )

    print(f"NVD chunks: {len(nvd_chunks)}")

    print("Chunking CISA KEV...")

    kev_docs = [
        NormalizedDocument(**doc)
        for doc in load_jsonl(NORMALIZED_KEV_PATH)
    ]

    kev_chunks = []

    for doc in kev_docs:
        kev_chunks.extend(chunk_document(doc))

    save_jsonl(
        KEV_CHUNKS_PATH,
        [chunk.model_dump() for chunk in kev_chunks],
    )

    print(f"KEV chunks: {len(kev_chunks)}")


def fuse_data():
    print("Fusing KEV + NVD...")

    fuse_kev_with_nvd(
        kev_path=NORMALIZED_KEV_PATH,
        nvd_path=NORMALIZED_NVD_PATH,
        output_path=NORMALIZED_FUSED_PATH,
    )


def chunk_fused_data():
    print("Chunking fused documents...")

    fused_docs = [
        NormalizedDocument(**doc)
        for doc in load_jsonl(NORMALIZED_FUSED_PATH)
    ]

    fused_chunks = []

    for doc in fused_docs:
        fused_chunks.extend(chunk_document(doc))

    save_jsonl(
        FUSED_CHUNKS_PATH,
        [chunk.model_dump() for chunk in fused_chunks],
    )

    print(f"Fused chunks: {len(fused_chunks)}")


if __name__ == "__main__":
    # fetch_data()         
    normalize_data()        # Uses existing raw JSON files
    chunk_data()
    fuse_data()
    chunk_fused_data()