from pathlib import Path

from packages.ingestion.storage.local_store import load_json
from packages.ingestion.normalize.schema import NormalizedDocument

def get_english_description(descriptions: list[dict]) -> str:
    for item in descriptions:
        if item.get("lang") == "en":
            return item.get("value", "")
    return ""

def extract_cvss_metrics(cve: dict) -> dict:
    metrics = cve.get("metrics", {})

    # Prefer newer CVSS versions first
    if metrics.get("cvssMetricV31"):
        metric = metrics["cvssMetricV31"][0]
        cvss_data = metric.get("cvssData", {})

        return {
            "cvss_score": cvss_data.get("baseScore"),
            "severity": cvss_data.get("baseSeverity"),
            "cvss_version": cvss_data.get("version"),
            "attack_vector": cvss_data.get("attackVector"),
            "attack_complexity": cvss_data.get("attackComplexity"),
            "privileges_required": cvss_data.get("privilegesRequired"),
            "exploitability_score": metric.get("exploitabilityScore"),
            "impact_score": metric.get("impactScore"),
        }

    if metrics.get("cvssMetricV30"):
        metric = metrics["cvssMetricV30"][0]
        cvss_data = metric.get("cvssData", {})

        return {
            "cvss_score": cvss_data.get("baseScore"),
            "severity": cvss_data.get("baseSeverity"),
            "cvss_version": cvss_data.get("version"),
            "attack_vector": cvss_data.get("attackVector"),
            "attack_complexity": cvss_data.get("attackComplexity"),
            "privileges_required": cvss_data.get("privilegesRequired"),
            "exploitability_score": metric.get("exploitabilityScore"),
            "impact_score": metric.get("impactScore"),
        }

    if metrics.get("cvssMetricV2"):
        metric = metrics["cvssMetricV2"][0]
        cvss_data = metric.get("cvssData", {})

        return {
            "cvss_score": cvss_data.get("baseScore"),
            "severity": metric.get("baseSeverity"),
            "cvss_version": cvss_data.get("version"),
            "attack_vector": cvss_data.get("accessVector"),
            "attack_complexity": cvss_data.get("accessComplexity"),
            "privileges_required": cvss_data.get("authentication"),
            "exploitability_score": metric.get("exploitabilityScore"),
            "impact_score": metric.get("impactScore"),
        }

    return {}


def extract_cwe_ids(cve: dict) -> list[str]:
    weaknesses = cve.get("weaknesses", [])

    cwe_ids = []

    for weakness in weaknesses:
        for description in weakness.get("description", []):
            value = description.get("value", "")

            if value.startswith("CWE-"):
                cwe_ids.append(value)

    return list(set(cwe_ids))

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

        cvss = extract_cvss_metrics(cve)

        cwe_ids = extract_cwe_ids(cve)

        content=f"""
CVE: {cve_id}

Severity: {cvss.get("severity")}
CVSS Score: {cvss.get("cvss_score")}
CVSS Version: {cvss.get("cvss_version")}

Attack Vector: {cvss.get("attack_vector")}
Attack Complexity: {cvss.get("attack_complexity")}
Privileges Required: {cvss.get("privileges_required")}

CWEs: {", ".join(cwe_ids) if cwe_ids else "None"}

Description:
{description}
""".strip()

        doc = NormalizedDocument(
            doc_id=f"cve:{cve_id}",
            source_type="cve",
            source_name="NVD",
            title=cve_id,
            summary=description,
            content=content,
            cve_id=cve_id,
            published_at=cve.get("published"),
            updated_at=cve.get("lastModified"),
            raw_source_path=str(raw_path),
            severity=cvss.get("severity"),
            cvss_score=cvss.get("cvss_score"),
            cvss_version=cvss.get("cvss_version"),
            attack_vector=cvss.get("attack_vector"),
            attack_complexity=cvss.get("attack_complexity"),
            privileges_required=cvss.get("privileges_required"),
            exploitability_score=cvss.get("exploitability_score"),
            impact_score=cvss.get("impact_score"),
            cwe_ids=cwe_ids,
        )

        normalized_docs.append(doc)

    return normalized_docs