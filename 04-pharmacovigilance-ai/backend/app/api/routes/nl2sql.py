from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.core.security import require_role
from app.schemas.safety import NL2SQLRequest, NL2SQLResponse
from app.ai.nl2sql import safe_pv_nl2sql

router = APIRouter()

@router.post("/query", response_model=NL2SQLResponse)
async def query_nl2sql(
    payload: NL2SQLRequest,
    current_user: dict = Depends(require_role("ANALYST")),
    db: AsyncSession = Depends(get_db)
):
    if not payload.question or len(payload.question.strip()) < 3:
        raise HTTPException(status_code=400, detail="Query too short")
    result = await safe_pv_nl2sql.execute_query(payload.question, db)
    return {
        "sql": result.get("sql", ""),
        "data": result.get("data", []),
        "row_count": result.get("row_count", 0),
        "explanation": result.get("explanation"),
        "error": result.get("error")
    }
