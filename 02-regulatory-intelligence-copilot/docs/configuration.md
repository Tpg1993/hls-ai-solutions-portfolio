# Configuration & Environment Variables

## 1. Backend Environment Configuration (`backend/.env`)

Validated via Pydantic v2 `BaseSettings` in `app.core.config.Settings`.

| Variable | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `PROJECT_NAME` | string | `Regulatory Intelligence Copilot` | Microservice title |
| `DATABASE_URL` | string | `sqlite+aiosqlite:///regulatory_intelligence.db` | Async SQLAlchemy database URL |
| `SYNC_DATABASE_URL`| string | `sqlite:///regulatory_intelligence.db` | Sync SQLAlchemy database URL for seeding |
| `REDIS_URL` | string | `redis://localhost:6379/0` | Redis caching & state connection string |
| `SARVAM_API_KEY` | string | `""` | Primary LLM key for Sarvam AI (`sarvam-105b`) |
| `SARVAM_MODEL` | string | `sarvam-105b` | Model endpoint for regulatory reasoning |
| `OPENAI_API_KEY` | string | `""` | Secondary fallback provider key (`gpt-4o-mini`) |
| `OPENAI_MODEL` | string | `gpt-4o-mini` | Secondary fallback model endpoint |
| `OPENAI_FALLBACK_ENABLED` | bool | `true` | Enables failover router if Sarvam times out or errors |
| `JWT_SECRET_KEY` | string | `regulatory_demo_secret_token_change_in_production` | Cryptographic secret for signing JWTs |
| `JWT_ALGORITHM` | string | `HS256` | Cryptographic algorithm for JWTs |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | int | `480` | Access token lifespan in minutes (8 hours) |

---

## 2. Frontend Configuration (`frontend/.env.local`)

| Variable | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `NEXT_PUBLIC_API_BASE_URL` | string | `http://localhost:8001` | URL pointing to the FastAPI backend |
