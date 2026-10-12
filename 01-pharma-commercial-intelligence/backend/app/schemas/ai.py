from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

class ExplainRequest(BaseModel):
    hcp_id: str
    custom_prompt: Optional[str] = None

class ExplanationCitation(BaseModel):
    metric: str
    observed_value: str
    context: str

class ExplanationResponse(BaseModel):
    hcp_id: str
    hcp_name: str
    priority_tier: str
    propensity_score: float
    recommended_action: str
    recommended_channel: str
    summary_briefing: str
    key_drivers: List[str]
    citations: List[ExplanationCitation]
    provider_used: str  # Sarvam AI or OpenAI (Fallback)
    latency_ms: float
    fallback_triggered: bool = False

class NL2SQLRequest(BaseModel):
    query: str

class NL2SQLResponse(BaseModel):
    natural_query: str
    generated_sql: str
    row_count: int
    columns: List[str]
    results: List[Dict[str, Any]]
    execution_time_ms: float
    explanation: Optional[str] = None
