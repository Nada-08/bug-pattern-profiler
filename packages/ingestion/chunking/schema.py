from pydantic import BaseModel, Field

class ChunkRecord(BaseModel):
    chunk_id: str
    doc_id: str
    source_type: str
    source_name: str
    title: str
    text: str
    sequence: int

    cve_id: str | None = None
    cwe_ids: list[str] = Field(default_factory=list)
    vendor: list[str] = Field(default_factory=list)
    product: list[str] = Field(default_factory=list)

    severity: str | None = None
    published_at: str | None = None
    tags: list[str] = Field(default_factory=list)