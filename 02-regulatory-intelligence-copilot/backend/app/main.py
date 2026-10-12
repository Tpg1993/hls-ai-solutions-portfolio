from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.logging import logger
from app.api.api_v1 import api_router
from app.api.routes import health
from app.data.seed import seed_database

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Initializing Pharma Regulatory Intelligence Copilot backend...")
    await seed_database()
    logger.info("Startup complete. System ready for regulatory queries.")
    yield
    logger.info("Shutting down Regulatory Intelligence Copilot backend...")

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.PROJECT_VERSION,
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(health.router)
app.include_router(api_router, prefix=settings.API_V1_STR)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=8001, reload=True)
