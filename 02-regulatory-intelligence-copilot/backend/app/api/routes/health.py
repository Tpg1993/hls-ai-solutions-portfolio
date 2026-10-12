from fastapi import APIRouter
from app.core.config import settings

router = APIRouter(tags=["Health"])

@router.get("/health/live")
async def health_live():
    return {"status": "ok", "app": settings.APP_NAME, "version": settings.PROJECT_VERSION}

@router.get("/health/ready")
async def health_ready():
    return {"status": "ready", "database": "connected"}
