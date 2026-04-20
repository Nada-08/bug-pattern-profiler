from packages.ingestion.sources.nvd_cve import fetch_nvd_page

path = fetch_nvd_page()

print("Saved NVD file to:", path)