from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    data_dir: Path = Path("data")
    raw_dir: Path = Path("data/raw")
    normalized_dir: Path = Path("data/normalized")
    chunks_dir: Path = Path("data/chunks")

    nvd_api_base: str = (
        "https://services.nvd.nist.gov/rest/json/cves/2.0"
    )

    cisa_kev_url: str = (
        "https://www.cisa.gov/sites/default/files/feeds/"
        "known_exploited_vulnerabilities.json"
    )

    nvd_api_key: str | None = None
    request_timeout_seconds: int = 30

    pinecone_api_key: str | None = None
    pinecone_index_name: str = "bug-pattern-profiler"

    openrouter_api_key: str | None = None
    openrouter_model: str = (
        "qwen/qwen3-next-80b-a3b-instruct:free"
    )

    groq_api_key: str | None = None
    groq_model: str = "llama3-70b-8192"


    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )


settings = Settings()