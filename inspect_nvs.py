from packages.ingestion.storage.local_store import load_json

from pathlib import Path

data = load_json(Path("data/raw/nvd/nvd_page_0.json"))

print("Top-level keys:")
print(data.keys())

vulnerabilities = data.get("vulnerabilities", [])
print("\nNumber of vulnerability records:", len(vulnerabilities))

first = vulnerabilities[0]
print("\nKeys in first vulnerability record:")
print(first.keys())

cve = first.get("cve", {})
print("\nKeys inside 'cve':")
print(cve.keys())

print("\nCVE ID:")
print(cve.get("id"))

print("\nPublished:")
print(cve.get("published"))

print("\nLast Modified:")
print(cve.get("lastModified"))

print("\nDescriptions:")
print(cve.get("descriptions"))