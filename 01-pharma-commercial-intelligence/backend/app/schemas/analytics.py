from typing import List, Dict, Any
from pydantic import BaseModel

class TerritoryMetric(BaseModel):
    territory_id: str
    territory_name: str
    region: str
    assigned_rep: str
    quota: float
    total_hcps: int
    high_priority_hcps: int
    latest_monthly_trx: int
    market_share_percentage: float

class CommercialOverviewKPIs(BaseModel):
    total_hcps: int
    high_priority_count: int
    medium_priority_count: int
    low_priority_count: int
    total_monthly_trx: int
    average_conversion_propensity: float
    top_recommended_channel: str
    active_territories_count: int

class SpecialtyBreakdown(BaseModel):
    specialty: str
    count: int
    average_trx: float
    high_priority_count: int
