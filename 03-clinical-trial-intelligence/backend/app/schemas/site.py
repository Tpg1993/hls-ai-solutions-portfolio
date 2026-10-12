from typing import List, Optional
from pydantic import BaseModel

class SiteMetricItem(BaseModel):
    id: str
    target_patients: int
    actual_enrolled: int
    screening_velocity_per_month: float
    screen_failure_rate: float
    activation_delay_days: int
    dropout_rate: float
    predicted_risk: str
    risk_score: float

class SiteListItem(BaseModel):
    id: str
    site_number: str
    site_name: str
    institution: str
    city: str
    state: str
    pi_name: str
    metric: Optional[SiteMetricItem] = None
