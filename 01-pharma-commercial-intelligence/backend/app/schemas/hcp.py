from typing import List, Optional
from datetime import date
from pydantic import BaseModel

class PrescriptionPoint(BaseModel):
    month_year: str
    trx_count: int
    nrx_count: int
    competitor_trx_count: int

class InteractionItem(BaseModel):
    id: str
    interaction_date: date
    channel: str
    rep_name: str
    topics_discussed: str
    sentiment: str
    notes: Optional[str] = None

class HCPListItem(BaseModel):
    id: str
    npi_synthetic: str
    first_name: str
    last_name: str
    specialty: str
    hospital_affiliation: str
    city: str
    state: str
    territory_id: str
    decile: int
    digital_affinity: str
    adoption_stage: str
    latest_trx: int = 0
    priority_score: Optional[float] = None
    priority_tier: Optional[str] = None
    recommended_action: Optional[str] = None

class HCPDetailResponse(BaseModel):
    hcp: HCPListItem
    prescriptions: List[PrescriptionPoint]
    interactions: List[InteractionItem]
    top_drivers: Optional[dict] = None

class HCPFilterParams(BaseModel):
    specialty: Optional[str] = None
    territory_id: Optional[str] = None
    decile_min: Optional[int] = None
    priority_tier: Optional[str] = None
    search: Optional[str] = None
    limit: int = 50
    offset: int = 0
