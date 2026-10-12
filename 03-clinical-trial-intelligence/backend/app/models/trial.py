from sqlalchemy import Column, String, Integer, Float, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.models.base import TimestampMixin

class ClinicalTrial(Base, TimestampMixin):
    __tablename__ = "clinical_trials"

    id = Column(String(50), primary_key=True, index=True)
    nct_id = Column(String(50), unique=True, index=True, nullable=False)
    title = Column(String(255), nullable=False)
    phase = Column(String(30), nullable=False)  # Phase 1, Phase 2, Phase 3
    condition = Column(String(100), nullable=False, index=True) # NSCLC, Breast Cancer, etc.
    therapeutic_area = Column(String(100), nullable=False)
    target_enrollment = Column(Integer, nullable=False)
    current_enrollment = Column(Integer, default=0, nullable=False)
    status = Column(String(30), default="Recruiting", nullable=False)
    protocol_summary = Column(Text, nullable=True)

    criteria = relationship("TrialCriterion", back_populates="trial", cascade="all, delete-orphan")
    matches = relationship("PatientTrialMatch", back_populates="trial", cascade="all, delete-orphan")

class TrialCriterion(Base, TimestampMixin):
    __tablename__ = "trial_criteria"

    id = Column(String(50), primary_key=True, index=True)
    trial_id = Column(String(50), ForeignKey("clinical_trials.id"), nullable=False, index=True)
    criterion_type = Column(String(20), nullable=False)  # INCLUSION, EXCLUSION
    category = Column(String(50), nullable=False)        # AGE, ECOG, BIOMARKER, PRIOR_THERAPY, LAB
    description = Column(Text, nullable=False)
    required_biomarker = Column(String(50), nullable=True) # e.g. "EGFR_EXON_20"
    min_numeric_value = Column(Float, nullable=True)     # e.g. 18 for age, 100 for platelets
    max_numeric_value = Column(Float, nullable=True)     # e.g. 1 for ECOG

    trial = relationship("ClinicalTrial", back_populates="criteria")
