from typing import List, Optional
from datetime import date
from pydantic import BaseModel

class GuidanceSectionItem(BaseModel):
    id: str
    section_number: str
    section_title: str
    page_number: int
    chunk_text: str
    keywords: Optional[str] = None

class SubmissionImpactItem(BaseModel):
    id: str
    product_name: str
    ind_nda_number: str
    development_phase: str
    therapeutic_area: str
    impact_level: str
    impact_summary: str
    action_required: str
    compliance_deadline: Optional[date] = None

class GuidanceSummary(BaseModel):
    id: str
    authority: str
    title: str
    document_number: Optional[str] = None
    therapeutic_area: str
    doc_type: str
    status: str
    publication_date: date
    version: str
    summary: Optional[str] = None

class GuidanceDetail(GuidanceSummary):
    sections: List[GuidanceSectionItem] = []
    submission_impacts: List[SubmissionImpactItem] = []
