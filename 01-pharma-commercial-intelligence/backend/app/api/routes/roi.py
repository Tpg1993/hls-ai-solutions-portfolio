from fastapi import APIRouter, Depends
from app.core.rbac import require_role, UserRole, TokenPayload
from app.services.roi_service import roi_service
from app.schemas.roi import ROIInputs, ROIOutputs

router = APIRouter(prefix="/roi", tags=["ROI Calculator"])

@router.post("", response_model=ROIOutputs)
async def calculate_roi(
    inputs: ROIInputs,
    current_user: TokenPayload = Depends(require_role(UserRole.BUSINESS_OWNER)),
):
    return roi_service.calculate_commercial_roi(inputs)

@router.get("", response_model=ROIOutputs)
async def get_default_roi(
    current_user: TokenPayload = Depends(require_role(UserRole.STANDARD_USER)),
):
    # Returns baseline default simulation
    return roi_service.calculate_commercial_roi(ROIInputs())
