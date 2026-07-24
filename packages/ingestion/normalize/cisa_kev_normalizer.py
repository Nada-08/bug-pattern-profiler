from pathlib import Path

from packages.ingestion.storage.local_store import load_json
from packages.ingestion.normalize.schema import NormalizedDocument

def build_kev_content(item: dict) -> str:
    parts = [
        f"CVE: {item.get('cveID', '')}",
        f"Vendor: {item.get('vendorProject', '')}",
        f"Product: {item.get('product', '')}",
        f"Name: {item.get('vulnerabilityName', '')}",
        f"Description: {item.get('shortDescription', '')}",
        f"Required Action: {item.get('requiredAction', '')}",
        f"Due Date: {item.get('dueDate', '')}",
        f"Known Ransomware Use: {item.get('knownRansomwareCapaignUse', '')}",
        f"Notes: {item.get('notes', '')}",
    ]

    return "\n".join(parts)


def normalize_cisa_kev_file(raw_path: Path) -> list[NormalizedDocument]:
    data = load_json(raw_path)
    vulnerabilities = data.get("vulnerabilities", [])

    normalized_docs = []

    for item in vulnerabilities:
        cve_id = item.get("cveID")
        if not cve_id:
            continue

        doc = NormalizedDocument(
            doc_id=f"kev:{cve_id}",
            source_type="kev",
            source_name="CISA-KEV",
            title=item.get("vulnerabilityName", cve_id),
            summary=item.get("shortDescription", ""),
            content=build_kev_content(item),
            cve_id=cve_id,
            cwe_ids=item.get("cwes", []),
            vendor=[item["vendorProject"]] if item.get("vendorProject") else [],
            product=[item["product"]] if item.get("product") else [],
            published_at=item.get("dateAdded"),
            updated_at=None,
            references=[],
            tags=["known_exploited"],
            raw_source_path=str(raw_path),
            extra={
                "required_action": item.get("requiredAction"),
                "due_date": item.get("dueDate"),
                "known_ransomware_campaign_use": item.get("knownRansomwareCampaignUse"),
                "notes": item.get("notes")
            },
        )

        normalized_docs.append(doc)

    return normalized_docs