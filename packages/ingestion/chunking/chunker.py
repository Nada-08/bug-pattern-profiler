from packages.ingestion.normalize.schema import NormalizedDocument
from packages.ingestion.chunking.schema import ChunkRecord

def chunk_document(doc: NormalizedDocument) -> list[ChunkRecord]:
    chunk = ChunkRecord(
        chunk_id=f"{doc.doc_id}:chunk:0001",
        doc_id=doc.doc_id,
        source_type=doc.source_type,
        source_name=doc.source_name,
        title=doc.title,
        text=doc.content,
        sequence=1,
        cve_id=doc.cve_id,
        cwe_ids=doc.cwe_ids,
        vendor=doc.vendor,
        product=doc.product,
        severity=doc.severity,
        published_at=doc.published_at,
        tags=doc.tags
    )

    return [chunk]