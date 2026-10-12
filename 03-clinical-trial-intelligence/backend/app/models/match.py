from sqlalchemy import Column, String, Float, Text, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.models.base import TimestampMixin

class PatientTrialMatch(Base, TimestampMixin):
    __tablename__ = "patient_trial_matches"

    id = Column(String(50), primary_key=True, index=True)
    patient_id = Column(String(50), ForeignKey("patients.id"), nullable=False, index=True)
    trial_id = Column(String(50), ForeignKey("clinical_trials.id"), nullable=False, index=True)
    eligibility_status = Column(String(30), nullable=False) # ELIGIBLE, INELIGIBLE, UNCERTAIN
    confidence_score = Column(Float, nullable=False)        # 0.0 to 1.0
    criteria_breakdown = Column(JSON, nullable=False)       # List of criterion results (PASS/FAIL/UNKNOWN)
    review_status = Column(String(30), default="PENDING", nullable=False) # PENDING, APPROVED, REJECTED
    reviewer_notes = Column(Text, nullable=True)
    ai_explanation = Column(Text, nullable=True)

    patient = relationship("Patient", back_populates="matches")
    trial = relationship("ClinicalTrial", back_populates="matches")
