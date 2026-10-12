from fastapi import APIRouter
from app.api.routes import auth, trials, patients, sites, matching, nl2sql

api_router = APIRouter()
api_router.include_router(auth.router)
api_router.include_router(trials.router)
api_router.include_router(patients.router)
api_router.include_router(sites.router)
api_router.include_router(matching.router)
api_router.include_router(nl2sql.router)
