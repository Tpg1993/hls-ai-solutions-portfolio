from typing import List, Dict, Any, Optional
from pydantic import BaseModel

class RegulatoryCitation(BaseModel):
    authority: str
    document_title: str
    section_number: str
    page_number: int
    exact_snippet: str
    relevance_score: float

class RegulatoryAgentState(BaseModel):
    query: str
    authority_filter: Optional[str] = None
    therapeutic_filter: Optional[str] = None
    sub_questions: List[str] = []
    retrieved_sections: List[Dict[str, Any]] = []
    citations: List[RegulatoryCitation] = []
    synthesized_answer: str = ""
    evidence_sufficient: bool = True
    provider_used: str = ""
    latency_ms: float = 0.0
