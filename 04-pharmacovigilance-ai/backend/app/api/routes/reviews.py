from typing import List
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from app.core.database import get_db
from app.core.security import require_role
from app.models.safety import SafetyReview, SafetySignal, AuditEvent
from app.schemas.safety import SafetyReviewCreate, SafetyReviewResponse

router = APIRouter()

@router.post("", response_model=SafetyReviewResponse)
async def submit_safety_review(
    payload: SafetyReviewCreate,
    current_user: dict = Depends(require_role("SAFETY_REVIEWER")),
    db: AsyncSession = Depends(get_db)
):
    sig_result = await db.execute(select(SafetySignal).where(SafetySignal.id == payload.signal_id))
    signal = sig_result.scalars().first()
    if not signal:
        raise HTTPException(status_code=404, detail="Safety signal not found")

    # Update Signal Status based on decision
    if payload.decision == "ESCALATE_LABEL_UPDATE":
        signal.signal_status = "ESCALATED_LABEL_UPDATE"
    elif payload.decision == "DISMISS_SIGNAL":
        signal.signal_status = "CLOSED"
    else:
        signal.signal_status = "INVESTIGATING"

    review = SafetyReview(
        signal_id=signal.id,
        reviewer_username=current_user.get("sub", "safety_reviewer"),
        decision=payload.decision,
        comments=payload.comments,
        snapshot_prr=signal.prr,
        created_at=datetime.now(timezone.utc)
    )
    db.add(review)

    # Immutable Audit Log
    audit = AuditEvent(
        user_username=current_user.get("sub", "safety_reviewer"),
        action=f"SAFETY_DECISION_{payload.decision}",
        entity_type="SafetySignal",
        entity_id=str(signal.id),
        payload={
            "drug": signal.drug_name,
            "event": signal.adverse_event,
            "prr": signal.prr,
            "decision": payload.decision,
            "comments": payload.comments
        }
    )
    db.add(audit)
    await db.commit()
    await db.refresh(review)
    return review

@router.get("", response_model=List[SafetyReviewResponse])
async def list_reviews(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(SafetyReview).order_by(desc(SafetyReview.id)))
    return result.scalars().all()

@router.get("/audit")
async def list_audit_trail(
    current_user: dict = Depends(require_role("AUDITOR")),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(AuditEvent).order_by(desc(AuditEvent.id)).limit(100))
    events = result.scalars().all()
    return [
        {
            "id": e.id,
            "user": e.user_username,
            "action": e.action,
            "entity": f"{e.entity_type} #{e.entity_id}",
            "payload": e.payload,
            "timestamp": e.timestamp.isoformat() if e.timestamp else None
        }
        for e in events
    ]
