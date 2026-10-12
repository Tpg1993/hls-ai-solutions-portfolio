from typing import List, Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel

class RecommendationItem(BaseModel):
    id: str
    hcp_id: str
    hcp_name: str
    specialty: str
    territory_id: str
    product_name: str
    propensity_score: float
    priority_tier: str
    recommended_action: str
    recommended_channel: str
    top_drivers: Optional[Dict[str, Any]] = None
    model_version: str
    status: str
    generated_at: Optional[datetime] = None

class BatchGenerateResponse(BaseModel):
    total_processed: int
    recommendations_generated: int
    model_version: str
    execution_time_seconds: float

class RecommendationUpdate(BaseModel):
    status: str  # ACCEPTED, DISMISSED
    feedback_notes: Optional[str] = None
