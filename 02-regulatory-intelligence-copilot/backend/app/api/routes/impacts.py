from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.core.rbac import require_role, UserRole, TokenPayload
from app.models.submission_impact import SubmissionImpact
from app.schemas.guidance import SubmissionImpactItem

router = APIRouter(prefix="/impacts", tags=["Submission Impacts"])

@router.get("", response_model=List[SubmissionImpactItem])
async def list_submission_impacts(
    impact_level: Optional[str] = Query(None),
    product_name: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_db),
    current_user: TokenPayload = Depends(require_role(UserRole.STANDARD_USER)),
):
    stmt = select(SubmissionImpact)
    filters = []
    if impact_level:
        filters.append(SubmissionImpact.impact_level == impact_level)
    if product_name:
        filters.append(SubmissionImpact.product_name.ilike(f"%{product_name}%"))

    if filters:
        stmt = stmt.where(and_(*filters))

    stmt = stmt.order_by(SubmissionImpact.compliance_deadline.asc())
    res = await db.execute(stmt)
    return res.scalars().all()
