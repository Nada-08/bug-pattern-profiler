from fastapi import APIRouter, Depends

from apps.api.app.schemas.chat import (
    ChatRequest,
    ChatResponse,
    Source
)

from apps.api.app.dependencies import get_rag_service

from packages.rag.rag_service import RAGService


router = APIRouter(
    prefix="/chat",
    tags=["chat"]
)


@router.post("")
def chat(
    request: ChatRequest,
    rag_service: RAGService = Depends(get_rag_service)
):

    result = rag_service.answer(
        query=request.query,
        namespace="fused"
    )

    sources = [
        Source(
            cve_id=s.cve_id,
            title=s.title,

            vendor=s.vendor,
            product=s.product,

            severity=s.severity,
            cvss_score=s.cvss_score,

            score=s.score,
            source_type=s.source_type,

            published_at=s.published_at,

            required_action=s.required_action,
            patch_status=s.patch_status,
            days_overdue=s.days_overdue,
        )
        for s in result["sources"]
    ]


    return ChatResponse(
        answer=result["answer"],
        sources=sources
    )