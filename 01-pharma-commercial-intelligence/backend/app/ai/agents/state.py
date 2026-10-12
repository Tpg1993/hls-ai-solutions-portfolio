from typing import Dict, Any, List, Optional, TypedDict

class CommercialAgentState(TypedDict):
    hcp_id: str
    custom_query: Optional[str]
    hcp_profile: Dict[str, Any]
    prescriptions: List[Dict[str, Any]]
    interactions: List[Dict[str, Any]]
    ml_features: Dict[str, float]
    propensity_score: float
    priority_tier: str
    recommended_action: str
    recommended_channel: str
    drivers: Dict[str, Any]
    final_briefing: str
    citations: List[Dict[str, str]]
    provider_name: str
    latency_ms: float
    fallback_triggered: bool
    error: Optional[str]
