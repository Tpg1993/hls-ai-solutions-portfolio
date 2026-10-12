from typing import List, Optional
from pydantic import BaseModel

class DiffItem(BaseModel):
    id: str
    section_number: str
    section_title: str
    change_type: str
    old_text: Optional[str] = None
    new_text: Optional[str] = None
    semantic_impact: str
    impact_severity: str

class DocBrief(BaseModel):
    id: str
    title: str
    authority: str
    version: str

class DiffResponse(BaseModel):
    baseline_doc: DocBrief
    comparison_doc: DocBrief
    total_changes: int
    critical_changes: int
    high_priority_changes: int
    changes: List[DiffItem]
    analysis_latency_ms: float
