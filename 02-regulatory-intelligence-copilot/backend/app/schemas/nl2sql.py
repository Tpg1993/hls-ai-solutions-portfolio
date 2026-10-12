from typing import List, Dict, Any
from pydantic import BaseModel

class NL2SQLRequest(BaseModel):
    query: str

class NL2SQLResponse(BaseModel):
    sql_query: str
    row_count: int
    rows: List[Dict[str, Any]]
    execution_time_ms: float
