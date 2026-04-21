import httpx

from packages.common.settings import settings
from packages.ingestion.storage.local_store import save_json

def fetch_cisa_kev():
    response = httpx.get(
        settings.cisa_kev_url,
        timeout=settings.request_timeout_seconds
    )
    response.raise_for_status()

    data = response.json()

    output_path = settings.raw_dir / "cisa_kev" / "known_exploited_vulnerabilities.json"
    save_json(output_path, data)

    return output_path