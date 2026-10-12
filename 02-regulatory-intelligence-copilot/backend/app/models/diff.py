from sqlalchemy import Column, String, Text, ForeignKey
from app.core.database import Base
from app.models.base import TimestampMixin

class GuidanceVersionDiff(Base, TimestampMixin):
    __tablename__ = "guidance_version_diffs"

    id = Column(String(50), primary_key=True, index=True)
    baseline_doc_id = Column(String(50), ForeignKey("guidance_documents.id"), nullable=False, index=True)
    comparison_doc_id = Column(String(50), ForeignKey("guidance_documents.id"), nullable=False, index=True)
    section_number = Column(String(50), nullable=False)
    section_title = Column(String(255), nullable=False)
    change_type = Column(String(50), nullable=False)  # ADDITION, DELETION, MODIFICATION, CLARIFICATION
    old_text = Column(Text, nullable=True)
    new_text = Column(Text, nullable=True)
    semantic_impact = Column(Text, nullable=False)   # LLM synthesized impact summary
    impact_severity = Column(String(20), default="MEDIUM", nullable=False) # CRITICAL, HIGH, MEDIUM, LOW
