# Project 01: AGENTS.md — Engineering & Operational Directives

> **Project**: Pharma Commercial Intelligence & Next-Best-Action Platform  
> **Master Standards Reference**: Inherits and strictly enforces all policies in [Root AGENTS.md](../AGENTS.md).

---

## 1. Project Overview & Boundaries

- **Business Domain**: Life Sciences Commercial Operations, Sales Force Effectiveness, Next-Best-Action (NBA) for Healthcare Professionals (HCPs).
- **Core AI Mission**: Predict which HCPs to prioritize, compute explainable drivers via XGBoost + rule-based NBA engine, orchestrate LangGraph multi-agent analysis, and generate evidence-grounded action briefings using Sarvam AI (with OpenAI fallback).
- **Hard Guardrail**: **The LLM must NEVER generate numerical propensity scores, Rx figures, or financial metrics.** Scores come strictly from the ML model and database aggregations; LLM explains and summarizes the factual evidence.

---

## 2. Security, Paths & Git Rules

1. **Zero Secret Policy**:
   - `SARVAM_API_KEY` and `OPENAI_API_KEY` must be loaded exclusively by the backend configuration (`app.core.config.Settings`).
   - Frontend must never have access to external LLM keys or internal database connection strings.
   - Any secret committed is an immediate P0 failure requiring credential rotation.
2. **Relative Paths**:
   - All file operations must use paths relative to the project root (`Path(__file__).resolve().parent...`).
   - No hardcoded developer usernames, local drive letters (`C:\Users\...`), or operating-system-specific paths.
3. **Presidio PII/PHI Scrubbing**:
   - All free-text queries entered into the AI assistant must pass through Presidio analyzer/anonymizer before processing.

---

## 3. RBAC Hierarchy for Project 01

| Role | Access Level | Permitted Operations |
| :--- | :---: | :--- |
| `SUPER_ADMIN` | 100 | Full system access, user administration, data regeneration trigger, system logs. |
| `ADMIN` | 80 | User management, territory assignments, model retrain trigger. |
| `BUSINESS_OWNER` | 60 | Configure ROI assumptions (call duration, rep hourly cost, conversion lift multipliers), view commercial KPI dashboards. |
| `ANALYST` | 40 | HCP search, profile drilldown, trigger NBA recommendation runs, execute AI explanations, export reports. |
| `AUDITOR` | 20 | Read-only access to audit logs, recommendation history, model evaluation metrics. |
| `STANDARD_USER` | 10 | Read-only view of HCP directory and high-level territory summaries. |

---

## 4. LLM Provider Hierarchy & Fallback

- **Primary**: Sarvam AI (`sarvam-105b` or chat endpoint) via `app.ai.providers.sarvam_provider.py`.
- **Fallback**: OpenAI (`gpt-4o-mini`) via `app.ai.providers.openai_provider.py`.
- **Policy**:
  - Fallback triggers only on HTTP 5xx, timeouts (>15s), or HTTP 429 rate limits from Sarvam.
  - Circuit breaker trips after 3 consecutive failures, routing traffic to OpenAI for 5 minutes before probing Sarvam health.
  - LLM outputs must strictly validate against Pydantic models (`app.schemas.ai.ExplanationResponse`).

---

## 5. Mandatory Testing & Quality Standards

Every feature change must include corresponding tests:
1. **Pytest Unit Tests (`backend/tests/unit/`)**:
   - ML feature pipeline and XGBoost scoring accuracy.
   - Rule-based NBA logic (priority tiers, channel recommendations, frequency caps).
   - Sarvam/OpenAI router and circuit breaker mock tests.
   - RBAC dependency permissions on all FastAPI routes.
2. **Pytest Integration Tests (`backend/tests/integration/`)**:
   - End-to-end API test suite covering `/api/hcps`, `/api/recommendations`, `/api/ai/explain`, and `/api/roi`.
3. **Playwright E2E Suite (`frontend/e2e/`)**:
   - Next.js user flows: login, HCP search and filter, NBA recommendation generation, AI explanation drawer inspection, and ROI calculator scenario adjustment.
4. **Selenium Cross-Browser Suite (`tests/selenium/`)**:
   - Automated cross-browser tests (Chrome/Firefox headless) verifying auth route guards, dashboard charts rendering, and responsive table interactions.

---

## 6. Documentation Requirements

Maintain and update documentation in the same commit as code changes:
- `docs/architecture.md`: System components, data flows, and LangGraph multi-agent topology.
- `docs/security.md`: Threat model, RBAC details, JWT lifecycle, Presidio configuration.
- `docs/configuration.md`: All `.env` parameters and defaults.
- `docs/data-dictionary.md`: Schema for 10,000 synthetic HCPs, Rx tables, and interactions.
- `docs/api.md`: FastAPI OpenAPI contracts and payload examples.
- `docs/testing.md`: Setup and execution commands for Pytest, Playwright, and Selenium.
- `docs/evaluation.md`: ML AUC/ROC metrics, latency, and LangGraph evaluation runs.
- `docs/roi-assumptions.md`: Mathematical models and assumptions for ROI calculations.
- `docs/features/`: Dedicated Markdown file for each major capability.
