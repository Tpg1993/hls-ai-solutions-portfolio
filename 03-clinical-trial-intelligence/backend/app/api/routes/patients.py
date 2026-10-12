from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.core.rbac import require_role, UserRole, TokenPayload
from app.models.patient import Patient
from app.schemas.patient import PatientListItem, PatientDetail

router = APIRouter(prefix="/patients", tags=["Patient Cohort"])

@router.get("", response_model=List[PatientListItem])
async def list_patients(
    diagnosis: Optional[str] = Query(None),
    stage: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_db),
    current_user: TokenPayload = Depends(require_role(UserRole.STANDARD_USER)),
):
    stmt = select(Patient)
    if diagnosis:
        stmt = stmt.where(Patient.primary_diagnosis.ilike(f"%{diagnosis}%"))
    if stage:
        stmt = stmt.where(Patient.stage.ilike(f"%{stage}%"))

    res = await db.execute(stmt)
    return res.scalars().all()

@router.get("/{patient_id}", response_model=PatientDetail)
async def get_patient_detail(
    patient_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: TokenPayload = Depends(require_role(UserRole.STANDARD_USER)),
):
    stmt = select(Patient).where(Patient.id == patient_id).options(
        selectinload(Patient.labs),
        selectinload(Patient.biomarkers),
    )
    res = await db.execute(stmt)
    patient = res.scalar_one_or_none()
    if not patient:
        raise HTTPException(status_code=404, detail=f"Patient '{patient_id}' not found")
    return patient
