from pathlib import Path
from packages.ingestion.normalize.nvd_normalizer import normalize_nvd_file

docs = normalize_nvd_file(Path("data/raw/nvd/nvd_page_0.json"))

for doc in docs:
    print(doc)