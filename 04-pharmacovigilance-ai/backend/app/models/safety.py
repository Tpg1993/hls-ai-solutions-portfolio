from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Float, DateTime, Text, JSON, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.core.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role = Column(String(50), default="SAFETY_REVIEWER", nullable=False)
    full_name = Column(String(100), nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

class SafetyCase(Base):
    __tablename__ = "safety_cases"

    id = Column(Integer, primary_key=True, index=True)
    case_id = Column(String(50), unique=True, index=True, nullable=False)
    age = Column(Integer, nullable=True)
    sex = Column(String(10), nullable=True)
    suspect_drug = Column(String(100), index=True, nullable=False)
    dosage = Column(String(50), nullable=True)
    adverse_event = Column(String(150), index=True, nullable=False)
    meddra_soc = Column(String(150), index=True, nullable=True) # System Organ Class
    severity = Column(String(50), index=True, nullable=False) # SERIOUS_HOSPITALIZATION, LIFE_THREATENING, NON_SERIOUS
    outcome = Column(String(50), nullable=True) # RECOVERED, NOT_RECOVERED, FATAL, UNKNOWN
    country = Column(String(10), nullable=True)
    date_received = Column(String(30), nullable=True)
    narrative_raw = Column(Text, nullable=True)
    narrative_scrubbed = Column(Text, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

class SafetySignal(Base):
    __tablename__ = "safety_signals"

    id = Column(Integer, primary_key=True, index=True)
    drug_name = Column(String(100), index=True, nullable=False)
    adverse_event = Column(String(150), index=True, nullable=False)
    meddra_soc = Column(String(150), nullable=True)
    observed_cases = Column(Integer, nullable=False)
    expected_cases = Column(Float, nullable=False)
    total_drug_cases = Column(Integer, nullable=False)
    total_event_cases = Column(Integer, nullable=False)
    prr = Column(Float, nullable=False)
    prr_ci_lower = Column(Float, nullable=False)
    prr_ci_upper = Column(Float, nullable=False)
    ror = Column(Float, nullable=False)
    ror_ci_lower = Column(Float, nullable=False)
    ror_ci_upper = Column(Float, nullable=False)
    chi_square = Column(Float, nullable=False)
    risk_level = Column(String(20), default="MEDIUM") # HIGH, MEDIUM, LOW
    signal_status = Column(String(50), default="OPEN") # OPEN, INVESTIGATING, CLOSED, ESCALATED_LABEL_UPDATE
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

class EvidenceDocument(Base):
    __tablename__ = "evidence_documents"

    id = Column(Integer, primary_key=True, index=True)
    doc_type = Column(String(50), nullable=False) # DRUG_LABEL, LITERATURE_PUBMED
    drug_name = Column(String(100), index=True, nullable=False)
    adverse_event = Column(String(150), index=True, nullable=True)
    title = Column(String(255), nullable=False)
    section = Column(String(100), nullable=True) # Warnings, Precautions, Section 5.1
    citation = Column(String(255), nullable=True)
    text_chunk = Column(Text, nullable=False)
    relevance_score = Column(Float, default=0.9)

class SafetyReview(Base):
    __tablename__ = "safety_reviews"

    id = Column(Integer, primary_key=True, index=True)
    signal_id = Column(Integer, ForeignKey("safety_signals.id"), nullable=False)
    reviewer_username = Column(String(50), nullable=False)
    decision = Column(String(100), nullable=False) # ESCALATE_LABEL_UPDATE, ROUTINE_SURVEILLANCE, REJECT
    comments = Column(Text, nullable=False)
    snapshot_prr = Column(Float, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

class AuditEvent(Base):
    __tablename__ = "audit_events"

    id = Column(Integer, primary_key=True, index=True)
    user_username = Column(String(50), nullable=False)
    action = Column(String(100), nullable=False)
    entity_type = Column(String(50), nullable=False)
    entity_id = Column(String(50), nullable=False)
    payload = Column(JSON, nullable=True)
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))
