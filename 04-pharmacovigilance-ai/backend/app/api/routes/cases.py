import random
from typing import List, Optional
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from app.core.database import get_db
from app.core.security import require_role
from app.models.safety import SafetyCase, AuditEvent
from app.schemas.safety import SafetyCaseResponse, SafetyCaseCreate
from app.ai.extractor import extract_safety_entities

router = APIRouter()

@router.get("", response_model=List[SafetyCaseResponse])
async def list_cases(
    drug: Optional[str] = None,
    severity: Optional[str] = None,
    limit: int = Query(50, le=200),
    db: AsyncSession = Depends(get_db)
):
    query = select(SafetyCase)
    if drug:
        query = query.where(SafetyCase.suspect_drug.ilike(f"%{drug}%"))
    if severity:
        query = query.where(SafetyCase.severity == severity)
    query = query.order_by(desc(SafetyCase.id)).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()

@router.get("/{case_id}", response_model=SafetyCaseResponse)
async def get_case_by_id(case_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(SafetyCase).where(SafetyCase.case_id == case_id))
    case = result.scalars().first()
    if not case:
        raise HTTPException(status_code=404, detail="Safety case not found")
    return case

@router.post("/extract", response_model=SafetyCaseResponse)
async def extract_and_create_case(
    payload: SafetyCaseCreate,
    current_user: dict = Depends(require_role("ANALYST")),
    db: AsyncSession = Depends(get_db)
):
    entities = extract_safety_entities(payload.narrative)
    
    new_case_id = f"ICSR-2026-{random.randint(9000, 9999)}"
    new_case = SafetyCase(
        case_id=new_case_id,
        age=entities["age"],
        sex=entities["sex"],
        suspect_drug=payload.suspect_drug or entities["suspect_drug"],
        dosage="50mg daily",
        adverse_event=payload.adverse_event or entities["adverse_event"],
        meddra_soc=entities["meddra_soc"],
        severity=entities["severity"],
        outcome=entities["outcome"],
        country=payload.country or "US",
        date_received=datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        narrative_raw=payload.narrative,
        narrative_scrubbed=entities["scrubbed_narrative"]
    )
    db.add(new_case)

    # Log audit event
    audit = AuditEvent(
        user_username=current_user.get("sub", "analyst"),
        action="EXTRACT_CASE_NARRATIVE",
        entity_type="SafetyCase",
        entity_id=new_case_id,
        payload={"redactions_count": entities["pii_redactions_count"]}
    )
    db.add(audit)
    await db.commit()
    await db.refresh(new_case)
    return new_case
