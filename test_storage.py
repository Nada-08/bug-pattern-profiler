from pathlib import Path

from packages.ingestion.storage.local_store import save_json, load_json


test_path = Path("data/raw/test/example.json")

sample_data = {
    "name": "bug-pattern-profiler",
    "source": "test",
    "count": 1
}

save_json(test_path, sample_data)

loaded_data = load_json(test_path)

print("Saved file:", test_path)
print("Loaded data:", loaded_data)