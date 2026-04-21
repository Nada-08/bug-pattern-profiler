from pathlib import Path

from packages.ingestion.normalize.nvd_normalizer import normalize_nvd_file


def test_nvd_normalizer_returns_docs():
    raw_path = Path("data/raw/nvd/nvd_page_0.json")

    docs = normalize_nvd_file(raw_path)

    assert len(docs) > 0


def test_nvd_normalizer_has_doc_id():
    raw_path = Path("data/raw/nvd/nvd_page_0.json")

    docs = normalize_nvd_file(raw_path)

    first = docs[0]

    assert first.doc_id.startswith("cve:")