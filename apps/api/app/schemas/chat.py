from typing import Any
from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    query: str
    top_k: int = 5
    namespace: str | None = None


class Source(BaseModel):
    cve_id: str | None = None
    title: str | None = None

    vendor: list[str] = Field(default_factory=list)
    product: list[str] = Field(default_factory=list)

    severity: str | None = None
    cvss_score: float | None = None

    score: float
    source_type: str | None = None

    published_at: str | None = None

    required_action: str | None = None
    patch_status: str | None = None
    days_overdue: int | None = None


class ChatResponse(BaseModel):
    answer: dict[str, Any]
    sources: list[Source]