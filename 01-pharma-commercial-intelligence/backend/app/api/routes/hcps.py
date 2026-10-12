from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.core.rbac import require_role, UserRole, TokenPayload
from app.services.hcp_service import hcp_service
from app.schemas.hcp import HCPListItem, HCPDetailResponse

router = APIRouter(prefix="/hcps", tags=["HCPs"])

@router.get("", response_model=List[HCPListItem])
async def list_hcps(
    specialty: Optional[str] = Query(None),
    territory_id: Optional[str] = Query(None),
    decile_min: Optional[int] = Query(None),
    priority_tier: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db),
    current_user: TokenPayload = Depends(require_role(UserRole.STANDARD_USER)),
):
    items, total = await hcp_service.get_hcps(
        db=db,
        specialty=specialty,
        territory_id=territory_id,
        decile_min=decile_min,
        priority_tier=priority_tier,
        search=search,
        limit=limit,
        offset=offset,
    )
    return items

@router.get("/{hcp_id}", response_model=HCPDetailResponse)
async def get_hcp_detail(
    hcp_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: TokenPayload = Depends(require_role(UserRole.STANDARD_USER)),
):
    detail = await hcp_service.get_hcp_detail(db, hcp_id)
    if not detail:
        raise HTTPException(status_code=404, detail=f"HCP '{hcp_id}' not found")
    return detail
