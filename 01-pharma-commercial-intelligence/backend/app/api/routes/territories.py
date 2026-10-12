from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.core.rbac import require_role, UserRole, TokenPayload
from app.models.territory import Territory

router = APIRouter(prefix="/territories", tags=["Territories"])

@router.get("")
async def list_territories(
    db: AsyncSession = Depends(get_db),
    current_user: TokenPayload = Depends(require_role(UserRole.STANDARD_USER)),
):
    res = await db.execute(select(Territory))
    territories = res.scalars().all()
    return [
        {
            "id": t.id,
            "name": t.name,
            "region": t.region,
            "quota": t.quota,
            "assigned_rep_name": t.assigned_rep_name,
            "assigned_rep_email": t.assigned_rep_email,
            "target_specialty": t.target_specialty,
        }
        for t in territories
    ]
