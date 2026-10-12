from fastapi import APIRouter
from app.api.routes import auth, search, guidances, diff, nl2sql, impacts

api_router = APIRouter()
api_router.include_router(auth.router)
api_router.include_router(search.router)
api_router.include_router(guidances.router)
api_router.include_router(diff.router)
api_router.include_router(nl2sql.router)
api_router.include_router(impacts.router)
