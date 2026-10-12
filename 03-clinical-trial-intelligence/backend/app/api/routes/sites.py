from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.core.rbac import require_role, UserRole, TokenPayload
from app.models.site import TrialSite
from app.schemas.site import SiteListItem

router = APIRouter(prefix="/sites", tags=["Trial Sites & Risk Telemetry"])

@router.get("", response_model=List[SiteListItem])
async def list_sites(
    risk: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_db),
    current_user: TokenPayload = Depends(require_role(UserRole.STANDARD_USER)),
):
    stmt = select(TrialSite).options(selectinload(TrialSite.metric))
    res = await db.execute(stmt)
    sites = res.scalars().all()
    if risk:
        sites = [s for s in sites if s.metric and s.metric.predicted_risk.lower() == risk.lower()]
    return sites
