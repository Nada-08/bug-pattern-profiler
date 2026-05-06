from pathlib import Path
from pprint import pprint

from packages.ingestion.storage.local_store import load_json


data = load_json(Path("data/raw/nvd/nvd_page_0.json"))

vulnerabilities = data.get("vulnerabilities", [])

for item in vulnerabilities:
    cve = item.get("cve", {})
    cve_id = cve.get("id")
    metrics = cve.get("metrics", {})

    print("=" * 80)
    print("CVE:", cve_id)
    print("Metric keys:", metrics.keys())
    pprint(metrics)
    break