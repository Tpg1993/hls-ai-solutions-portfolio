from typing import List, Optional
from pydantic import BaseModel

class CriterionItem(BaseModel):
    id: str
    criterion_type: str
    category: str
    description: str
    min_numeric_value: Optional[float] = None
    max_numeric_value: Optional[float] = None
    required_biomarker: Optional[str] = None

class TrialListItem(BaseModel):
    id: str
    nct_id: str
    title: str
    phase: str
    condition: str
    therapeutic_area: str
    target_enrollment: int
    current_enrollment: int
    status: str
    protocol_summary: Optional[str] = None

class TrialDetail(TrialListItem):
    criteria: List[CriterionItem] = []
