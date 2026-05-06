from pathlib import Path

from packages.ingestion.storage.local_store import load_jsonl, save_jsonl

def fuse_kev_with_nvd(
    kev_path: Path,
    nvd_path: Path,
    output_path: Path,
):
    kev_docs = load_jsonl(kev_path)
    nvd_docs = load_jsonl(nvd_path)

    nvd_by_cve = {
        doc.get("cve_id"): doc
        for doc in nvd_docs
        if doc.get("cve_id")
    }

    fused_docs = []

    for kev_doc in kev_docs:
        cve_id = kev_doc.get("cve_id")
        nvd_doc = nvd_by_cve.get(cve_id)

        if not nvd_doc:
            fused_docs.append(kev_doc)
            continue

        fused_doc = {
            **kev_doc,

            "source_type": "kev+nvd",
            "source_name": "CISA-KEV + NVD",

            "severity": nvd_doc.get("severity"),
            "cvss_score": nvd_doc.get("cvss_score"),
            "attack_vector": nvd_doc.get("attack_vector"),
            "attack_complexity": nvd_doc.get("attack_complexity"),
            "privileges_required": nvd_doc.get("privileges_required"),
            "exploitability_score": nvd_doc.get("exploitability_score"),
            "impact_score": nvd_doc.get("impact_score"),
            "cwe_ids": nvd_doc.get("cwe_ids", []),

            "tags": list(set(
                kev_doc.get("tags", []) +
                nvd_doc.get("tags", []) +
                ["known_exploited", "nvd_enriched"]
            )),
        }

        fused_doc["content"] = "\n".join([
            f"CVE: {cve_id}",
            f"Title: {fused_doc.get('title')}",
            f"Severity: {fused_doc.get('severity')}",
            f"CVSS Score: {fused_doc.get('cvss_score')}",
            f"Attack Vector: {fused_doc.get('attack_vector')}",
            f"Attack Complexity: {fused_doc.get('attack_complexity')}",
            f"Privileges Required: {fused_doc.get('privileges_required')}",
            f"CWE: {', '.join(fused_doc.get('cwe_ids', []))}",
            "",
            f"Summary: {fused_doc.get('summary')}",
            "",
            "Known Exploited: Yes",
        ])

        fused_docs.append(fused_doc)

    save_jsonl(output_path, fused_docs)

    print(f"KEV docs: {len(kev_docs)}")
    print(f"NVD docs: {len(nvd_docs)}")
    print(f"Fused docs saved: {len(fused_docs)}")
    print(f"Output: {output_path}")