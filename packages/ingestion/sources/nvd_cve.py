from pathlib import Path
import httpx

from packages.common.settings import settings
from packages.ingestion.storage.local_store import save_json

def fetch_nvd_page(
    start_index: int = 0,
    results_per_page: int = 100,
) -> tuple[Path, int | None]:

    output_path = settings.raw_dir / "nvd" / f"nvd_page_{start_index}.json"

    # Already downloaded -> skip API call
    if output_path.exists():
        # print(f"Skipping start_index={start_index} (already exists)")
        return output_path, None

    params = {
        "startIndex": start_index,
        "resultsPerPage": results_per_page,
    }

    response = httpx.get(
        settings.nvd_api_base,
        params=params,
        timeout=settings.request_timeout_seconds,
    )
    response.raise_for_status()

    data = response.json()

    save_json(output_path, data)

    return output_path, data["totalResults"]