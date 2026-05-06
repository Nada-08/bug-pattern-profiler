from pathlib import Path
from pydantic import BaseModel
import os


class Settings(BaseModel):
    data_dir: Path = Path("data")
    raw_dir: Path = Path("data/raw")
    normalized_dir: Path = Path("data/normalized")
    chunks_dir: Path = Path("data/chunks")

    nvd_api_base: str = "https://services.nvd.nist.gov/rest/json/cves/2.0"
    cisa_kev_url: str = "https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json"

    nvd_api_key: str | None = os.getenv("NVD_API_KEY")
    request_timeout_seconds: int = 30

    pinecone_api_key: str | None = os.getenv("PINECONE_API_KEY")
    pinecone_index_name: str = os.getenv("PINECONE_INDEX_NAME", "bug-pattern-profiler")
    
    openrouter_api_key: str | None = os.getenv("OPENROUTER_API_KEY")
    openrouter_model: str = os.getenv(
        "OPENROUTER_MODEL",
        "qwen/qwen3-next-80b-a3b-instruct:free"
    )

    groq_api_key: str | None = os.getenv("GROQ_API_KEY")
    groq_model: str = os.getenv(
        "GROQ_MODEL",
        "llama3-70b-8192"
    )

settings = Settings()