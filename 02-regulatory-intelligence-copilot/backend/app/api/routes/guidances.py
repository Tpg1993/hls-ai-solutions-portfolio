from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select, and_
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.core.rbac import require_role, UserRole, TokenPayload
from app.models.guidance import GuidanceDocument, GuidanceSection
from app.models.submission_impact import SubmissionImpact
from app.schemas.guidance import GuidanceSummary, GuidanceDetail

router = APIRouter(prefix="/guidances", tags=["Guidance Library"])

@router.get("", response_model=List[GuidanceSummary])
async def list_guidance_documents(
    authority: Optional[str] = Query(None),
    therapeutic_area: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db),
    current_user: TokenPayload = Depends(require_role(UserRole.STANDARD_USER)),
):
    stmt = select(GuidanceDocument)
    filters = []
    if authority:
        filters.append(GuidanceDocument.authority.ilike(f"%{authority}%"))
    if therapeutic_area:
        filters.append(GuidanceDocument.therapeutic_area.ilike(f"%{therapeutic_area}%"))
    if status:
        filters.append(GuidanceDocument.status == status)
    if search:
        filters.append(GuidanceDocument.title.ilike(f"%{search}%"))

    if filters:
        stmt = stmt.where(and_(*filters))

    stmt = stmt.order_by(GuidanceDocument.publication_date.desc()).limit(limit).offset(offset)
    res = await db.execute(stmt)
    docs = res.scalars().all()
    return docs

@router.get("/{doc_id}", response_model=GuidanceDetail)
async def get_guidance_detail(
    doc_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: TokenPayload = Depends(require_role(UserRole.STANDARD_USER)),
):
    stmt = select(GuidanceDocument).where(GuidanceDocument.id == doc_id).options(
        selectinload(GuidanceDocument.sections),
        selectinload(GuidanceDocument.submission_impacts),
    )
    res = await db.execute(stmt)
    doc = res.scalar_one_or_none()
    if not doc:
        raise HTTPException(status_code=404, detail=f"Guidance document '{doc_id}' not found")
    return doc
