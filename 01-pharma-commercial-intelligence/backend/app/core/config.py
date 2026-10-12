import os
from pathlib import Path
from typing import List, Optional
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, field_validator

# Anchored strictly to the backend directory, resolving relative paths safely
BASE_DIR = Path(__file__).resolve().parent.parent.parent
PROJECT_ROOT = BASE_DIR.parent

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=[str(BASE_DIR / ".env"), str(PROJECT_ROOT / ".env")],
        env_file_encoding="utf-8",
        extra="ignore"
    )

    # Application
    APP_NAME: str = "Pharma Commercial Intelligence & NBA Platform"
    APP_ENV: str = "development"
    LOG_LEVEL: str = "INFO"
    DEBUG: bool = False
    PROJECT_VERSION: str = "1.0.0"

    # API & CORS
    API_V1_STR: str = "/api"
    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ]

    # Database
    DATABASE_URL: str = Field(
        default="postgresql+asyncpg://postgres:postgres@localhost:5432/pharma_commercial",
        description="Async PostgreSQL connection string"
    )
    SYNC_DATABASE_URL: str = Field(
        default="postgresql://postgres:postgres@localhost:5432/pharma_commercial",
        description="Sync PostgreSQL connection string for migrations/sync scripts"
    )

    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"

    # Security & JWT
    JWT_SECRET_KEY: str = "super_secure_demo_secret_key_pharma_nba_2026_change_in_prod"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 120

    # LLM Providers (Strictly Backend Only)
    SARVAM_API_KEY: Optional[str] = None
    SARVAM_MODEL: str = "sarvam-105b-conversations"
    SARVAM_BASE_URL: str = "https://api.sarvam.ai"

    OPENAI_API_KEY: Optional[str] = None
    OPENAI_MODEL: str = "gpt-4o-mini"
    OPENAI_FALLBACK_ENABLED: bool = True
    LLM_TIMEOUT_SECONDS: float = 15.0
    LLM_CIRCUIT_BREAKER_FAILURES: int = 3
    LLM_CIRCUIT_BREAKER_RESET_SECONDS: int = 300

    # Synthetic Data Parameters
    SYNTHETIC_HCP_COUNT: int = 10000
    RANDOM_SEED: int = 42

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v):
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        return ["http://localhost:3000"]

settings = Settings()
