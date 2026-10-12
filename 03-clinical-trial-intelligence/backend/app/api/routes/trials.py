from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.core.rbac import require_role, UserRole, TokenPayload
from app.models.trial import ClinicalTrial
from app.schemas.trial import TrialListItem, TrialDetail

router = APIRouter(prefix="/trials", tags=["Clinical Trials"])

@router.get("", response_model=List[TrialListItem])
async def list_trials(
    phase: Optional[str] = Query(None),
    condition: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_db),
    current_user: TokenPayload = Depends(require_role(UserRole.STANDARD_USER)),
):
    stmt = select(ClinicalTrial)
    if phase:
        stmt = stmt.where(ClinicalTrial.phase == phase)
    if condition:
        stmt = stmt.where(ClinicalTrial.condition.ilike(f"%{condition}%"))
    if status:
        stmt = stmt.where(ClinicalTrial.status == status)

    res = await db.execute(stmt)
    return res.scalars().all()

@router.get("/{trial_id}", response_model=TrialDetail)
async def get_trial_detail(
    trial_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: TokenPayload = Depends(require_role(UserRole.STANDARD_USER)),
):
    stmt = select(ClinicalTrial).where(ClinicalTrial.id == trial_id).options(
        selectinload(ClinicalTrial.criteria)
    )
    res = await db.execute(stmt)
    trial = res.scalar_one_or_none()
    if not trial:
        raise HTTPException(status_code=404, detail=f"Trial '{trial_id}' not found")
    return trial
