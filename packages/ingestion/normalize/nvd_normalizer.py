from pathlib import Path

from packages.ingestion.storage.local_store import load_json
from packages.ingestion.normalize.schema import NormalizedDocument

def get_english_description(descriptions: list[dict]) -> str:
    for item in descriptions:
        if item.get("lang") == "en":
            return item.get("value", "")
    return ""


def normalize_nvd_file(raw_path: Path) -> list[NormalizedDocument]:
    data = load_json(raw_path)
    vulnerabilities = data.get("vulnerabilities", [])

    normalized_docs = []

    for item in vulnerabilities:
        cve = item.get("cve", {})

        cve_id = cve.get("id")
        if not cve_id:
            continue

        description = get_english_description(cve.get("descriptions", []))

        doc = NormalizedDocument(
            doc_id=f"cve:{cve_id}",
            source_type="cve",
            source_name="NVD",
            title=cve_id,
            summary=description,
            content=description,
            cve_id=cve_id,
            published_at=cve.get("published"),
            updated_at=cve.get("lastModified"),
            raw_source_path=str(raw_path)
        )

        normalized_docs.append(doc)

    return normalized_docs