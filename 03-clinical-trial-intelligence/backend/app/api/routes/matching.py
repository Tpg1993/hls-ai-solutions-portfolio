import uuid
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.core.rbac import require_role, UserRole, TokenPayload
from app.models.match import PatientTrialMatch
from app.models.patient import Patient
from app.models.trial import ClinicalTrial
from app.models.audit import AuditEvent
from app.schemas.match import (
    MatchListItem,
    MatchDetail,
    ScreenPatientRequest,
    ReviewDecisionRequest,
)
from app.ai.agents.trial_team import run_patient_screening_workflow

router = APIRouter(prefix="/matching", tags=["Patient-Trial Matching & Screening"])

@router.get("", response_model=List[MatchListItem])
async def list_matches(
    status: Optional[str] = Query(None), # ELIGIBLE, INELIGIBLE, UNCERTAIN
    review_status: Optional[str] = Query(None), # PENDING, APPROVED, REJECTED
    trial_id: Optional[str] = Query(None),
    patient_id: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_db),
    current_user: TokenPayload = Depends(require_role(UserRole.STANDARD_USER)),
):
    stmt = select(PatientTrialMatch).options(
        selectinload(PatientTrialMatch.patient),
        selectinload(PatientTrialMatch.trial),
    )
    if status:
        stmt = stmt.where(PatientTrialMatch.eligibility_status == status)
    if review_status:
        stmt = stmt.where(PatientTrialMatch.review_status == review_status)
    if trial_id:
        stmt = stmt.where(PatientTrialMatch.trial_id == trial_id)
    if patient_id:
        stmt = stmt.where(PatientTrialMatch.patient_id == patient_id)

    res = await db.execute(stmt)
    records = res.scalars().all()

    items = []
    for m in records:
        items.append(MatchListItem(
            id=m.id,
            patient_id=m.patient_id,
            trial_id=m.trial_id,
            eligibility_status=m.eligibility_status,
            confidence_score=m.confidence_score,
            review_status=m.review_status,
            reviewer_notes=m.reviewer_notes,
            patient_mrn=m.patient.synthetic_mrn if m.patient else None,
            trial_nct=m.trial.nct_id if m.trial else None,
            trial_title=m.trial.title if m.trial else None,
        ))
    return items

@router.get("/{match_id}", response_model=MatchDetail)
async def get_match_detail(
    match_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: TokenPayload = Depends(require_role(UserRole.STANDARD_USER)),
):
    stmt = select(PatientTrialMatch).where(PatientTrialMatch.id == match_id).options(
        selectinload(PatientTrialMatch.patient),
        selectinload(PatientTrialMatch.trial),
    )
    res = await db.execute(stmt)
    m = res.scalar_one_or_none()
    if not m:
        raise HTTPException(status_code=404, detail=f"Match '{match_id}' not found")

    return MatchDetail(
        id=m.id,
        patient_id=m.patient_id,
        trial_id=m.trial_id,
        eligibility_status=m.eligibility_status,
        confidence_score=m.confidence_score,
        review_status=m.review_status,
        reviewer_notes=m.reviewer_notes,
        patient_mrn=m.patient.synthetic_mrn if m.patient else None,
        trial_nct=m.trial.nct_id if m.trial else None,
        trial_title=m.trial.title if m.trial else None,
        criteria_breakdown=m.criteria_breakdown or [],
        ai_explanation=m.ai_explanation,
    )

@router.post("/screen")
async def execute_live_screening(
    req: ScreenPatientRequest,
    db: AsyncSession = Depends(get_db),
    current_user: TokenPayload = Depends(require_role(UserRole.STANDARD_USER)),
):
    """
    Executes live multi-agent screening via Sarvam AI 105B.
    """
    try:
        result = await run_patient_screening_workflow(
            db=db,
            patient_id=req.patient_id,
            trial_id=req.trial_id,
        )

        # Update or insert match record
        match_id = f"MATCH-{req.patient_id}-{req.trial_id}"
        stmt = select(PatientTrialMatch).where(PatientTrialMatch.id == match_id)
        res = await db.execute(stmt)
        match_record = res.scalar_one_or_none()

        if not match_record:
            match_record = PatientTrialMatch(
                id=match_id,
                patient_id=req.patient_id,
                trial_id=req.trial_id,
                eligibility_status=result["eligibility_status"],
                confidence_score=result["confidence_score"],
                criteria_breakdown=result["criteria_breakdown"],
                review_status="PENDING" if result["eligibility_status"] == "ELIGIBLE" else "REJECTED",
                reviewer_notes="Evaluated via Live AI Screening Workflow.",
                ai_explanation=result["ai_explanation"],
            )
            db.add(match_record)
        else:
            match_record.eligibility_status = result["eligibility_status"]
            match_record.confidence_score = result["confidence_score"]
            match_record.criteria_breakdown = result["criteria_breakdown"]
            match_record.ai_explanation = result["ai_explanation"]

        await db.commit()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Live screening failure: {str(e)}")

@router.post("/{match_id}/review")
async def submit_clinical_review(
    match_id: str,
    decision: ReviewDecisionRequest,
    db: AsyncSession = Depends(get_db),
    current_user: TokenPayload = Depends(require_role(UserRole.CLINICAL_REVIEWER)),
):
    """
    Human-in-the-loop review sign-off. Requires CLINICAL_REVIEWER role.
    """
    stmt = select(PatientTrialMatch).where(PatientTrialMatch.id == match_id)
    res = await db.execute(stmt)
    m = res.scalar_one_or_none()
    if not m:
        raise HTTPException(status_code=404, detail="Match record not found")

    if decision.review_status not in ["APPROVED", "REJECTED"]:
        raise HTTPException(status_code=400, detail="Review status must be APPROVED or REJECTED")

    m.review_status = decision.review_status
    m.reviewer_notes = decision.reviewer_notes

    # Immutable Audit Log
    audit = AuditEvent(
        id=str(uuid.uuid4()),
        user_id=current_user.sub,
        user_role=current_user.role.value,
        action=f"CLINICAL_MATCH_{decision.review_status}",
        resource_type="PatientTrialMatch",
        resource_id=match_id,
        details={
            "status": decision.review_status,
            "notes": decision.reviewer_notes,
            "patient_id": m.patient_id,
            "trial_id": m.trial_id,
        },
    )
    db.add(audit)
    await db.commit()

    return {
        "status": "success",
        "match_id": match_id,
        "review_status": m.review_status,
        "reviewer_notes": m.reviewer_notes,
        "signed_by": current_user.sub,
    }
