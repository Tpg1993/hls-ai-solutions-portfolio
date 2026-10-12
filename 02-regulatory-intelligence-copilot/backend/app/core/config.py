import os
from pathlib import Path
from typing import List, Optional
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, field_validator

BASE_DIR = Path(__file__).resolve().parent.parent.parent
PROJECT_ROOT = BASE_DIR.parent

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=[str(BASE_DIR / ".env"), str(PROJECT_ROOT / ".env")],
        env_file_encoding="utf-8",
        extra="ignore"
    )

    APP_NAME: str = "Pharma Regulatory Intelligence Copilot"
    APP_ENV: str = "development"
    LOG_LEVEL: str = "INFO"
    DEBUG: bool = False
    PROJECT_VERSION: str = "1.0.0"

    API_V1_STR: str = "/api"
    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:3001",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:3001",
    ]

    DATABASE_URL: str = Field(
        default="sqlite+aiosqlite:///./regulatory_intelligence.db",
        description="Async connection string"
    )
    SYNC_DATABASE_URL: str = Field(
        default="sqlite:///./regulatory_intelligence.db",
        description="Sync connection string"
    )
    REDIS_URL: str = "redis://localhost:6379/0"

    JWT_SECRET_KEY: str = "super_secure_demo_secret_key_regulatory_2026_change_in_prod"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 120

    SARVAM_API_KEY: Optional[str] = None
    SARVAM_MODEL: str = "sarvam-105b-conversations"
    SARVAM_BASE_URL: str = "https://api.sarvam.ai"

    OPENAI_API_KEY: Optional[str] = None
    OPENAI_MODEL: str = "gpt-4o-mini"
    OPENAI_FALLBACK_ENABLED: bool = True
    LLM_TIMEOUT_SECONDS: float = 15.0

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v):
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        return ["http://localhost:3001"]

settings = Settings()
