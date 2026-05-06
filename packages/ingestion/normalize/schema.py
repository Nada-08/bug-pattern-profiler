from pydantic import BaseModel, Field

class NormalizedDocument(BaseModel):
    doc_id: str
    source_type: str # what kind of source this came from (e.g. cve, kev)
    source_name: str

    title: str
    summary: str
    content: str # the full normalized text to be chuncked

    cve_id: str | None = None
    cwe_ids: list[str] = Field(default_factory=list) # list of weakness ids 

    # may not be fill these well from NVD, but keep them so format stays consistent
    vendor: list[str] = Field(default_factory=list)
    product: list[str] = Field(default_factory=list)
    affected_versions: list[str] = Field(default_factory=list)

    # useful for filtering and ranking later
    severity: str | None = None
    cvss_score: float | None = None
    cvss_version: str | None = None
    
    attack_vector: str | None = None
    attack_complexity: str | None = None
    privileges_required: str | None = None
    
    exploitability_score: float | None = None
    impact_score: float | None = None

    # dates from the source
    published_at: str | None = None
    updated_at: str | None = None

    references: list[str] = Field(default_factory=list) # links to advisories or related pages
    tags: list[str] = Field(default_factory=list) # extra labels, useful later

    raw_source_path: str # raw file this normalized document came from 
    extra: dict = Field(default_factory=dict) # store source-specific details we don’t want to lose.