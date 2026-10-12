from typing import List, Optional
from pydantic import BaseModel

class CitationItem(BaseModel):
    authority: str
    document_title: str
    section_number: str
    section_title: str
    page_number: int
    exact_snippet: str
    relevance_score: float

class SearchRequest(BaseModel):
    query: str
    authority: Optional[str] = None
    therapeutic_area: Optional[str] = None

class SearchResponse(BaseModel):
    query: str
    answer: str
    citations: List[CitationItem]
    evidence_sufficient: bool
    provider_used: str
    latency_ms: float
    fallback_triggered: bool
