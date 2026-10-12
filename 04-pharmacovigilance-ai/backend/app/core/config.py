from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "AI Pharmacovigilance & Safety Signal Intelligence Platform"
    API_V1_STR: str = "/api/v1"
    DATABASE_URL: str = "sqlite+aiosqlite:///pharmacovigilance.db"
    SYNC_DATABASE_URL: str = "sqlite:///pharmacovigilance.db"
    REDIS_URL: str = "redis://localhost:6379/0"

    # LLM Provider Configuration
    SARVAM_API_KEY: Optional[str] = ""
    SARVAM_MODEL: str = "sarvam-105b"
    OPENAI_API_KEY: Optional[str] = ""
    OPENAI_MODEL: str = "gpt-4o-mini"
    OPENAI_FALLBACK_ENABLED: bool = True

    # Security
    JWT_SECRET_KEY: str = "pv_safety_demo_jwt_secret_token_change_in_production"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 480

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
