from sqlalchemy import Column, String, Date, Text, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.models.base import TimestampMixin

class GuidanceDocument(Base, TimestampMixin):
    __tablename__ = "guidance_documents"

    id = Column(String(50), primary_key=True, index=True)
    authority = Column(String(50), nullable=False, index=True)  # FDA, EMA, PMDA, ICH, WHO
    title = Column(String(255), nullable=False, index=True)
    document_number = Column(String(100), nullable=True)
    therapeutic_area = Column(String(100), nullable=False, index=True)  # Oncology, Cell/Gene Therapy, Digital Health
    doc_type = Column(String(50), default="Guidance", nullable=False)   # Draft Guidance, Final Guidance, Guideline
    status = Column(String(30), default="Final", nullable=False)       # Draft, Final, Superseded
    publication_date = Column(Date, nullable=False, index=True)
    version = Column(String(20), default="1.0", nullable=False)
    summary = Column(Text, nullable=True)
    pdf_source_url = Column(String(255), nullable=True)

    sections = relationship("GuidanceSection", back_populates="document", cascade="all, delete-orphan")
    submission_impacts = relationship("SubmissionImpact", back_populates="guidance", cascade="all, delete-orphan")

class GuidanceSection(Base, TimestampMixin):
    __tablename__ = "guidance_sections"

    id = Column(String(50), primary_key=True, index=True)
    document_id = Column(String(50), ForeignKey("guidance_documents.id"), nullable=False, index=True)
    section_number = Column(String(50), nullable=False)  # e.g., "Section 3.2"
    section_title = Column(String(255), nullable=False)
    page_number = Column(Integer, nullable=False)
    chunk_text = Column(Text, nullable=False)
    keywords = Column(String(255), nullable=True)

    document = relationship("GuidanceDocument", back_populates="sections")
