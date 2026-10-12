from typing import List, Dict, Any, Optional
from pydantic import BaseModel

class CriterionBreakdownItem(BaseModel):
    criterion_id: Optional[str] = None
    criterion_type: str
    category: str
    description: str
    status: str # PASS, FAIL, UNKNOWN
    observed_evidence: str
    evaluation_reason: str

class MatchListItem(BaseModel):
    id: str
    patient_id: str
    trial_id: str
    eligibility_status: str # ELIGIBLE, INELIGIBLE, UNCERTAIN
    confidence_score: float
    review_status: str     # PENDING, APPROVED, REJECTED
    reviewer_notes: Optional[str] = None
    patient_mrn: Optional[str] = None
    trial_nct: Optional[str] = None
    trial_title: Optional[str] = None

class MatchDetail(MatchListItem):
    criteria_breakdown: List[CriterionBreakdownItem] = []
    ai_explanation: Optional[str] = None

class ReviewDecisionRequest(BaseModel):
    review_status: str # APPROVED, REJECTED
    reviewer_notes: str

class ScreenPatientRequest(BaseModel):
    patient_id: str
    trial_id: str
