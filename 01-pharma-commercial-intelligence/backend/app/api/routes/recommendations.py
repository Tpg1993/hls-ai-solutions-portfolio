from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.core.rbac import require_role, UserRole, TokenPayload
from app.services.recommendation_service import recommendation_service
from app.services.audit_service import audit_service
from app.schemas.recommendation import RecommendationItem, BatchGenerateResponse

router = APIRouter(prefix="/recommendations", tags=["Recommendations"])

@router.get("", response_model=List[RecommendationItem])
async def list_recommendations(
    territory_id: Optional[str] = Query(None),
    priority_tier: Optional[str] = Query(None),
    specialty: Optional[str] = Query(None),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db),
    current_user: TokenPayload = Depends(require_role(UserRole.STANDARD_USER)),
):
    return await recommendation_service.list_recommendations(
        db=db,
        territory_id=territory_id,
        priority_tier=priority_tier,
        specialty=specialty,
        limit=limit,
        offset=offset,
    )

@router.post("/generate", response_model=BatchGenerateResponse)
async def generate_recommendations(
    batch_limit: int = Query(500, ge=10, le=5000),
    db: AsyncSession = Depends(get_db),
    current_user: TokenPayload = Depends(require_role(UserRole.ADMIN)),
):
    result = await recommendation_service.generate_batch_recommendations(db, batch_limit=batch_limit)
    await audit_service.log_event(
        db=db,
        user_id=current_user.sub,
        user_role=current_user.role.value,
        action="BATCH_RECOMMENDATION_GENERATION",
        resource_type="Recommendation",
        details={"processed": result.total_processed, "generated": result.recommendations_generated},
    )
    return result
