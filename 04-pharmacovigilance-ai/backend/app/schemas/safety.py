from pydantic import BaseModel, ConfigDict
from typing import Optional, List, Dict, Any
from datetime import datetime

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    role: str
    username: str

class UserLogin(BaseModel):
    username: str
    password: str

class SafetyCaseCreate(BaseModel):
    narrative: str
    suspect_drug: Optional[str] = None
    adverse_event: Optional[str] = None
    country: Optional[str] = "US"

class SafetyCaseResponse(BaseModel):
    id: int
    case_id: str
    age: Optional[int]
    sex: Optional[str]
    suspect_drug: str
    adverse_event: str
    meddra_soc: Optional[str]
    severity: str
    outcome: Optional[str]
    country: Optional[str]
    narrative_scrubbed: Optional[str]
    created_at: Optional[datetime]

    model_config = ConfigDict(from_attributes=True)

class SafetySignalResponse(BaseModel):
    id: int
    drug_name: str
    adverse_event: str
    meddra_soc: Optional[str]
    observed_cases: int
    expected_cases: float
    total_drug_cases: int
    total_event_cases: int
    prr: float
    prr_ci_lower: float
    prr_ci_upper: float
    ror: float
    ror_ci_lower: float
    ror_ci_upper: float
    chi_square: float
    risk_level: str
    signal_status: str

    model_config = ConfigDict(from_attributes=True)

class EvidenceDocumentResponse(BaseModel):
    id: int
    doc_type: str
    drug_name: str
    adverse_event: Optional[str]
    title: str
    section: Optional[str]
    citation: Optional[str]
    text_chunk: str
    relevance_score: float

    model_config = ConfigDict(from_attributes=True)

class SafetyReviewCreate(BaseModel):
    signal_id: int
    decision: str  # ESCALATE_LABEL_UPDATE, ROUTINE_SURVEILLANCE, REJECT
    comments: str

class SafetyReviewResponse(BaseModel):
    id: int
    signal_id: int
    reviewer_username: str
    decision: str
    comments: str
    snapshot_prr: float
    created_at: Optional[datetime]

    model_config = ConfigDict(from_attributes=True)

class NL2SQLRequest(BaseModel):
    question: str

class NL2SQLResponse(BaseModel):
    sql: str
    data: List[Dict[str, Any]]
    row_count: int
    explanation: Optional[str] = None
    error: Optional[str] = None
