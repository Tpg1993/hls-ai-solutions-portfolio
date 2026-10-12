import time
import uuid
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy import text
from app.core.config import settings
from app.core.logging import setup_logging, logger, correlation_id_ctx
from app.core.database import async_engine, Base
from app.api.api_v1 import api_router
from app.data.seed import seed_database

setup_logging(settings.LOG_LEVEL)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Initializing Pharma Commercial Intelligence backend...")
    # Create DB tables
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    # Auto-seed database with initial dataset if empty
    try:
        await seed_database(num_hcps=500)
    except Exception as e:
        logger.warning(f"Auto-seed check: {e}")
        
    yield
    logger.info("Shutting down backend services gracefully...")

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.PROJECT_VERSION,
    description="Enterprise Next-Best-Action (NBA) platform for pharmaceutical sales and commercial operations.",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Correlation ID and Request Timing Middleware
@app.middleware("http")
async def trace_and_timing_middleware(request: Request, call_next):
    correlation_id = request.headers.get("X-Correlation-ID", str(uuid.uuid4()))
    token = correlation_id_ctx.set(correlation_id)
    start_time = time.perf_counter()

    try:
        response: Response = await call_next(request)
        process_time = (time.perf_counter() - start_time) * 1000
        response.headers["X-Correlation-ID"] = correlation_id
        response.headers["X-Process-Time"] = f"{process_time:.2f}ms"
        return response
    finally:
        correlation_id_ctx.reset(token)

# Root endpoint with mandatory Synthetic Data Disclaimer
@app.get("/")
async def root():
    return {
        "app_name": settings.APP_NAME,
        "version": settings.PROJECT_VERSION,
        "status": "operational",
        "docs_url": "/docs",
        "disclaimer": "SYNTHETIC / DEMO DATA ONLY. For commercial prioritization decision support only.",
    }

# Liveness Probe
@app.get("/health/live", tags=["Health"])
async def liveness():
    return {"status": "alive", "timestamp": time.time()}

# Readiness Probe (checks DB connectivity)
@app.get("/health/ready", tags=["Health"])
async def readiness():
    try:
        async with async_engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
        return {"status": "ready", "database": "connected"}
    except Exception as exc:
        return JSONResponse(
            status_code=503,
            content={"status": "not_ready", "database": f"unhealthy: {str(exc)}"},
        )

# Mount API routes
app.include_router(api_router, prefix=settings.API_V1_STR)
