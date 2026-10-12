from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.core.rbac import require_role, UserRole, TokenPayload
from app.services.analytics_service import analytics_service
from app.schemas.analytics import CommercialOverviewKPIs, TerritoryMetric

router = APIRouter(prefix="/analytics", tags=["Analytics"])

@router.get("/commercial", response_model=CommercialOverviewKPIs)
async def get_commercial_kpis(
    db: AsyncSession = Depends(get_db),
    current_user: TokenPayload = Depends(require_role(UserRole.STANDARD_USER)),
):
    return await analytics_service.get_overview_kpis(db)

@router.get("/territories", response_model=List[TerritoryMetric])
async def get_territory_metrics(
    db: AsyncSession = Depends(get_db),
    current_user: TokenPayload = Depends(require_role(UserRole.STANDARD_USER)),
):
    return await analytics_service.get_territory_analytics(db)
