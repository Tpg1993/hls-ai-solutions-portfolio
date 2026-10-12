# Configuration & Environment Variables

## 1. Backend Environment Configuration (`backend/.env`)

All settings are strongly validated via Pydantic v2 `BaseSettings` in `app.core.config.Settings`.

| Variable | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `PROJECT_NAME` | string | `Clinical Trial Intelligence` | Display name of the microservice. |
| `DATABASE_URL` | string | `sqlite+aiosqlite:///clinical_trials.db` | Async SQLAlchemy database connection URL. |
| `SYNC_DATABASE_URL`| string | `sqlite:///clinical_trials.db` | Synchronous SQLAlchemy URL for seeding & migrations. |
| `REDIS_URL` | string | `redis://localhost:6379/0` | Redis caching & rate limiting connection string. |
| `SARVAM_API_KEY` | string | `""` | Primary LLM API key for Sarvam AI (`sarvam-105b`). |
| `SARVAM_MODEL` | string | `sarvam-105b` | Model endpoint for complex reasoning. |
| `OPENAI_API_KEY` | string | `""` | Fallback LLM provider key (`gpt-4o-mini`). |
| `OPENAI_MODEL` | string | `gpt-4o-mini` | Secondary fallback model endpoint. |
| `OPENAI_FALLBACK_ENABLED` | bool | `true` | Enables failover router if Sarvam times out or errors. |
| `JWT_SECRET_KEY` | string | `demo_secret_token_change_in_prod` | Secret salt for signing RS256 / HS256 tokens. |
| `JWT_ALGORITHM` | string | `HS256` | JWT cryptographic algorithm. |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | int | `480` | Token validity duration in minutes (8 hours). |

---

## 2. Frontend Configuration (`frontend/.env.local`)

| Variable | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `NEXT_PUBLIC_API_BASE_URL` | string | `http://localhost:8002` | Endpoint URL pointing to the FastAPI backend. |

> **IMPORTANT**: Never add provider LLM API keys (`SARVAM_API_KEY`, `OPENAI_API_KEY`) to `frontend/.env.local`. All AI calls must remain strictly backend-mediated.
