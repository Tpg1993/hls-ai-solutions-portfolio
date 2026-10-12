from typing import List, Optional, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from app.core.database import get_db
from app.core.security import require_role
from app.models.safety import SafetySignal, EvidenceDocument, SafetyCase
from app.schemas.safety import SafetySignalResponse, EvidenceDocumentResponse
from app.statistics.disproportionality import calculate_disproportionality_metrics
from app.ai.router import llm_router

router = APIRouter()

@router.get("", response_model=List[SafetySignalResponse])
async def list_signals(
    risk_level: Optional[str] = None,
    status: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    query = select(SafetySignal)
    if risk_level:
        query = query.where(SafetySignal.risk_level == risk_level)
    if status:
        query = query.where(SafetySignal.signal_status == status)
    query = query.order_by(desc(SafetySignal.prr))
    result = await db.execute(query)
    return result.scalars().all()

@router.get("/{signal_id}", response_model=SafetySignalResponse)
async def get_signal(signal_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(SafetySignal).where(SafetySignal.id == signal_id))
    signal = result.scalars().first()
    if not signal:
        raise HTTPException(status_code=404, detail="Safety signal not found")
    return signal

@router.get("/{signal_id}/evidence", response_model=List[EvidenceDocumentResponse])
async def get_signal_evidence(signal_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(SafetySignal).where(SafetySignal.id == signal_id))
    signal = result.scalars().first()
    if not signal:
        raise HTTPException(status_code=404, detail="Safety signal not found")

    docs_result = await db.execute(
        select(EvidenceDocument).where(EvidenceDocument.drug_name == signal.drug_name)
    )
    return docs_result.scalars().all()

@router.post("/{signal_id}/summary")
async def generate_investigator_summary(
    signal_id: int,
    current_user: dict = Depends(require_role("ANALYST")),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(SafetySignal).where(SafetySignal.id == signal_id))
    signal = result.scalars().first()
    if not signal:
        raise HTTPException(status_code=404, detail="Safety signal not found")

    system_prompt = (
        "You are an expert Pharmacovigilance Safety Scientist and Medical Reviewer. "
        "Synthesize evidence for the safety signal objectively. Never fabricate case counts. "
        "Explicitly remind that final regulatory disposition is a human investigator responsibility."
    )
    user_prompt = (
        f"Generate an investigator summary for signal: {signal.drug_name} and {signal.adverse_event}. "
        f"Observed cases: {signal.observed_cases}, Expected: {signal.expected_cases}, "
        f"PRR: {signal.prr} (95% CI: {signal.prr_ci_lower}-{signal.prr_ci_upper}), "
        f"Chi-square: {signal.chi_square}, Risk level: {signal.risk_level}."
    )

    grounded_context = {
        "drug": signal.drug_name,
        "event": signal.adverse_event,
        "prr": signal.prr,
        "cases": signal.observed_cases
    }

    response, fallback = await llm_router.generate_completion(
        system_prompt=system_prompt,
        user_prompt=user_prompt,
        grounded_context=grounded_context
    )

    return {
        "signal_id": signal.id,
        "drug_name": signal.drug_name,
        "adverse_event": signal.adverse_event,
        "summary": response.content,
        "provider": response.provider,
        "fallback_triggered": fallback
    }
