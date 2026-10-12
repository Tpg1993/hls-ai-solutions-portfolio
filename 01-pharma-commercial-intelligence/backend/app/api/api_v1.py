from fastapi import APIRouter
from app.api.routes import auth, hcps, recommendations, territories, analytics, ai, roi, audit

api_router = APIRouter()

api_router.include_router(auth.router)
api_router.include_router(hcps.router)
api_router.include_router(recommendations.router)
api_router.include_router(territories.router)
api_router.include_router(analytics.router)
api_router.include_router(ai.router)
api_router.include_router(roi.router)
api_router.include_router(audit.router)
