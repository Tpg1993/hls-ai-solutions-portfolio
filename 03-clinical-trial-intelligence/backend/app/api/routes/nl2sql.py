from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.core.rbac import require_role, UserRole, TokenPayload
from app.ai.nl2sql import safe_nl2sql
from app.schemas.nl2sql import NL2SQLRequest, NL2SQLResponse

router = APIRouter(prefix="/nl2sql", tags=["Safe NL2SQL"])

@router.post("", response_model=NL2SQLResponse)
async def query_trials_database(
    request: NL2SQLRequest,
    db: AsyncSession = Depends(get_db),
    current_user: TokenPayload = Depends(require_role(UserRole.CLINICAL_REVIEWER)),
):
    try:
        result = await safe_nl2sql.execute_query(db=db, natural_query=request.query)
        return NL2SQLResponse(**result)
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"NL2SQL processing failure: {str(e)}")
