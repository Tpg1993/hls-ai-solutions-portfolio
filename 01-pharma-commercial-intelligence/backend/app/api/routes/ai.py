from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.core.rbac import require_role, UserRole, TokenPayload
from app.ai.agents.commercial_team import run_commercial_agent_workflow
from app.ai.nl2sql import safe_nl2sql
from app.services.audit_service import audit_service
from app.schemas.ai import ExplainRequest, ExplanationResponse, NL2SQLRequest, NL2SQLResponse

router = APIRouter(prefix="/ai", tags=["AI & Agents"])

@router.post("/explain", response_model=ExplanationResponse)
async def explain_recommendation(
    request: ExplainRequest,
    db: AsyncSession = Depends(get_db),
    current_user: TokenPayload = Depends(require_role(UserRole.ANALYST)),
):
    try:
        result = await run_commercial_agent_workflow(
            db=db,
            hcp_id=request.hcp_id,
            custom_query=request.custom_prompt,
        )
        await audit_service.log_event(
            db=db,
            user_id=current_user.sub,
            user_role=current_user.role.value,
            action="AI_EXPLANATION_GENERATION",
            resource_type="HCP",
            resource_id=request.hcp_id,
            details={
                "provider": result["provider_used"],
                "fallback": result["fallback_triggered"],
                "latency_ms": result["latency_ms"],
            },
        )
        return ExplanationResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI Agent workflow failure: {str(e)}")

@router.post("/nl2sql", response_model=NL2SQLResponse)
async def query_nl2sql(
    request: NL2SQLRequest,
    db: AsyncSession = Depends(get_db),
    current_user: TokenPayload = Depends(require_role(UserRole.ANALYST)),
):
    try:
        result = await safe_nl2sql.execute_query(db=db, natural_query=request.query)
        await audit_service.log_event(
            db=db,
            user_id=current_user.sub,
            user_role=current_user.role.value,
            action="NL2SQL_QUERY_EXECUTION",
            resource_type="Query",
            details={
                "natural_query": request.query,
                "rows_returned": result["row_count"],
                "execution_time_ms": result["execution_time_ms"],
            },
        )
        return NL2SQLResponse(**result)
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"NL2SQL processing failure: {str(e)}")

@router.post("/enrich-data")
async def enrich_data_with_sarvam(
    count: int = 5,
    db: AsyncSession = Depends(get_db),
    current_user: TokenPayload = Depends(require_role(UserRole.ANALYST)),
):
    """
    Enriches top HCP accounts with live Sarvam AI generated clinical interactions and notes.
    """
    from app.cli.generate_ai_data import run_enrichment
    try:
        await run_enrichment(limit=count)
        return {
            "status": "success",
            "message": f"Successfully generated {count} realistic clinical call notes using Sarvam AI (105B).",
            "count": count
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Sarvam AI data generation failed: {str(e)}")
