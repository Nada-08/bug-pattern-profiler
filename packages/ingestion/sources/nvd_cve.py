from pathlib import Path
import httpx

from packages.common.settings import settings
from packages.ingestion.storage.local_store import save_json

def fetch_nvd_page(start_index: int = 0, results_per_page: int = 10) -> Path:
    # startIndex=0 -> start from the beginning
    # resultsPerPage=10 -> fetch only 10 CVEs for now
    params = {
        "startIndex": start_index,
        "resultsPerPage": results_per_page,
    }

    response = httpx.get(
        settings.nvd_api_base,
        params=params,
        timeout=settings.request_timeout_seconds
    )
    response.raise_for_status()

    data = response.json()

    output_path = settings.raw_dir / "nvd" / f"nvd_page_{start_index}.json"
    save_json(output_path, data)


    return output_path
