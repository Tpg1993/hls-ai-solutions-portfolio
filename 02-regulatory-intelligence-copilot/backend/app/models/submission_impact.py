from sqlalchemy import Column, String, Text, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.models.base import TimestampMixin

class SubmissionImpact(Base, TimestampMixin):
    __tablename__ = "submission_impacts"

    id = Column(String(50), primary_key=True, index=True)
    guidance_id = Column(String(50), ForeignKey("guidance_documents.id"), nullable=False, index=True)
    product_name = Column(String(100), nullable=False, index=True)  # e.g., OncoVax-7, CardioStat-Alpha
    ind_nda_number = Column(String(50), nullable=False)            # e.g., IND-148291, NDA-219482
    development_phase = Column(String(30), nullable=False)         # Phase 1, Phase 2, Phase 3, Post-Marketing
    therapeutic_area = Column(String(100), nullable=False)
    impact_level = Column(String(20), default="High", nullable=False) # Critical, High, Moderate, Advisory
    impact_summary = Column(Text, nullable=False)
    action_required = Column(Text, nullable=False)
    compliance_deadline = Column(Date, nullable=True)

    guidance = relationship("GuidanceDocument", back_populates="submission_impacts")
