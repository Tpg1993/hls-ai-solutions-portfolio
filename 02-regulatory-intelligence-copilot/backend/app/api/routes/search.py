from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.core.rbac import require_role, UserRole, TokenPayload
from app.ai.agents.regulatory_team import run_regulatory_agent_team
from app.schemas.search import SearchRequest, SearchResponse
from app.models.audit import AuditEvent

router = APIRouter(prefix="/search", tags=["Regulatory Search & Hybrid RAG"])

@router.post("", response_model=SearchResponse)
async def execute_regulatory_search(
    request: SearchRequest,
    db: AsyncSession = Depends(get_db),
    current_user: TokenPayload = Depends(require_role(UserRole.STANDARD_USER)),
):
    try:
        result = await run_regulatory_agent_team(
            db=db,
            query=request.query,
            authority=request.authority,
            therapeutic_area=request.therapeutic_area,
        )

        # Audit log
        import uuid
        audit = AuditEvent(
            id=str(uuid.uuid4()),
            user_id=current_user.sub,
            user_role=current_user.role.value,
            action="REGULATORY_INQUIRY_SEARCH",
            resource_type="GuidanceQuery",
            resource_id=request.query[:50],
            details={
                "provider": result["provider_used"],
                "citations_count": len(result["citations"]),
                "latency_ms": result["latency_ms"],
            },
        )
        db.add(audit)
        await db.commit()

        return SearchResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Regulatory agent search failure: {str(e)}")
