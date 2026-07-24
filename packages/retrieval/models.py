from pydantic import BaseModel, Field


class SearchResult(BaseModel):
    score: float
    chunk_id: str

    doc_id: str | None = None
    cve_id: str | None = None
    title: str | None = None
    text: str | None = None

    source_type: str | None = None
    source_name: str | None = None

    vendor: list[str] = Field(default_factory=list)
    product: list[str] = Field(default_factory=list)

    published_at: str | None = None
    tags: list[str] = Field(default_factory=list)

    severity: str | None = None
    cvss_score: float | None = None

    cwe_ids: list[str] = Field(default_factory=list)

    attack_vector: str | None = None
    attack_complexity: str | None = None
    privileges_required: str | None = None

    exploitability_score: float | None = None
    impact_score: float | None = None

    due_date: str | None = None
    required_action: str | None = None
    known_ransomware_use: str | None = None

    patch_status: str | None = None
    days_overdue: int | None = None