from fastapi import APIRouter
from app.api.routes import auth, cases, signals, reviews, nl2sql

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(cases.router, prefix="/cases", tags=["Safety Cases"])
api_router.include_router(signals.router, prefix="/signals", tags=["Signal Detection"])
api_router.include_router(reviews.router, prefix="/reviews", tags=["Human Review & Audit"])
api_router.include_router(nl2sql.router, prefix="/nl2sql", tags=["Safe NL2SQL"])
