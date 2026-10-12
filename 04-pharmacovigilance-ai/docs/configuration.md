# Configuration & Environment Variables

## 1. Backend Environment Configuration (`backend/.env`)

Validated via Pydantic v2 `BaseSettings` in `app.core.config.Settings`.

| Variable | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `PROJECT_NAME` | string | `AI Pharmacovigilance & Safety Signal Intelligence Platform` | Microservice title |
| `DATABASE_URL` | string | `sqlite+aiosqlite:///pharmacovigilance.db` | Async SQLAlchemy database URL |
| `SYNC_DATABASE_URL`| string | `sqlite:///pharmacovigilance.db` | Sync SQLAlchemy database URL for seeding |
| `REDIS_URL` | string | `redis://localhost:6379/0` | Redis caching & state connection string |
| `SARVAM_API_KEY` | string | `""` | Primary LLM key for Sarvam AI (`sarvam-105b`) |
| `SARVAM_MODEL` | string | `sarvam-105b` | Model endpoint for medical synthesis |
| `OPENAI_API_KEY` | string | `""` | Secondary fallback provider key (`gpt-4o-mini`) |
| `OPENAI_MODEL` | string | `gpt-4o-mini` | Secondary fallback model endpoint |
| `OPENAI_FALLBACK_ENABLED` | bool | `true` | Enables failover router if Sarvam times out or errors |
| `JWT_SECRET_KEY` | string | `pv_demo_secret_token_change_in_production` | Cryptographic secret for signing JWTs |
| `JWT_ALGORITHM` | string | `HS256` | JWT cryptographic algorithm |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | int | `480` | Access token lifespan in minutes (8 hours) |

---

## 2. Frontend Configuration (`frontend/.env.local`)

| Variable | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `NEXT_PUBLIC_API_BASE_URL` | string | `http://localhost:8003` | URL pointing to the FastAPI backend |
