from pydantic import BaseModel, Field
from dataclasses import dataclass
from typing import Optional


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


@dataclass
class QueryEntities:
    cve_id: Optional[str] = None
    cwe_ids: list[str] = None

    vendor: Optional[str] = None
    vendor_confidence: float = 0.0

    product: Optional[str] = None
    product_confidence: float = 0.0
    
    severity: Optional[str] = None

    attack_vector: Optional[str] = None
    attack_complexity: Optional[str] = None
    privileges_required: Optional[str] = None

    # new
    published_year: Optional[int] = None
    published_after: Optional[int] = None

    cvss_min: Optional[float] = None

    known_ransomware_use: Optional[bool] = None

    required_action: Optional[str] = None

    patch_due_before: Optional[str] = None

    def has_filters(self) -> bool:
        return any([
            self.cve_id,
            self.cwe_ids,
            self.vendor,
            self.product,
            self.severity,
            self.attack_vector,
            self.attack_complexity,
            self.privileges_required,
        ])

@dataclass
class VendorProductMatch:
    vendor: str | None = None
    vendor_confidence: float = 0.0

    product: str | None = None
    product_confidence: float = 0.0