from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.core.rbac import require_role, UserRole, TokenPayload
from app.ai.diff_engine import analyze_cross_version_diff
from app.schemas.diff import DiffResponse

router = APIRouter(prefix="/diff", tags=["Cross-Version Diff"])

@router.get("/compare", response_model=DiffResponse)
async def compare_guidance_versions(
    baseline_id: str = Query("DOC-FDA-RWE-2021", description="Baseline guidance doc ID"),
    comparison_id: str = Query("DOC-FDA-RWE-2024", description="Comparison guidance doc ID"),
    db: AsyncSession = Depends(get_db),
    current_user: TokenPayload = Depends(require_role(UserRole.STANDARD_USER)),
):
    try:
        diff_result = await analyze_cross_version_diff(
            db=db,
            baseline_doc_id=baseline_id,
            comparison_doc_id=comparison_id,
        )
        return DiffResponse(**diff_result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Version comparison failed: {str(e)}")
