# Project 01: Implementation Blueprint & Execution Plan
## Pharma Commercial Intelligence & Next-Best-Action (NBA) Platform

> **Target Organizations**: Commercial Biopharma Enterprises, Specialty Therapeutics & Life Sciences Organizations  
> **Status**: Ready for Implementation  
> **Governance Reference**: Follows all guidelines in [AGENTS.md](./AGENTS.md) and [Root AGENTS.md](../AGENTS.md).

---

## 1. Executive Summary & Business Rationale

Pharma commercial field teams manage tens of thousands of Healthcare Professionals (HCPs) across multiple territories, therapeutic areas, and competing brands. Field sales representatives and medical science liaisons (MSLs) frequently face fragmented data: CRM logs, prescription (Rx/TRx/NRx) claims, digital marketing touches, and conference interactions live in siloed databases.

### Core Problems Solved:
1. **Inefficient Prioritization**: Field reps spend up to 40% of their pre-call planning time manually deciding which HCPs to contact.
2. **Inconsistent Messaging**: Engagement channels (in-person visit, email, webinar, peer advisory) are chosen based on rep habit rather than HCP behavioral affinity.
3. **Black-box Distrust**: Traditional AI scoring is ignored by reps when they cannot inspect the evidence and drivers behind an HCP's recommendation.

### The Solution:
A local-first, full-stack intelligence platform that:
- Ingests and processes **10,000 synthetic HCPs** with longitudinal prescription, interaction, and competitor affinity records.
- Computes deterministic conversion probabilities using a trained **XGBoost propensity model**.
- Applies a transparent **Next-Best-Action (NBA) rule engine** to recommend specific action types, channels, and timing.
- Orchestrates a **LangGraph multi-agent team** that queries underlying facts and synthesizes an executive explanation using **Sarvam AI** (with resilient **OpenAI fallback**).
- Provides an enterprise Next.js dashboard with role-based access control, interactive territory heatmaps, an evidence inspection drawer, and a configurable ROI calculator.

---

## 2. System Architecture & Component Topology

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                                 FRONTEND (Next.js 14+)                                 │
│  • App Router (TypeScript)  • Tailwind CSS + shadcn/ui  • Lucide Icons  • Recharts     │
│  • RBAC Route Guards        • Evidence Inspection Drawer • Interactive ROI Calculator  │
└───────────────────────────────────────────┬────────────────────────────────────────────┘
                                            │ HTTP / JSON (Port 8000)
                                            ▼
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                                  BACKEND (FastAPI)                                     │
│  ┌───────────────────────────────┐                  ┌───────────────────────────────┐  │
│  │     API & Security Layer      │                  │       ML & Analytics Engine   │  │
│  │ • Pydantic v2 Contracts       │                  │ • Feature Engineering Engine  │  │
│  │ • RBAC Dependency Guards      │                  │ • Trained XGBoost Classifier  │  │
│  │ • Presidio PII/PHI Redactor   │                  │ • Rule-Based NBA Matrix       │  │
│  │ • Immutable Audit Logger      │                  │ • Deterministic ROI Logic     │  │
│  └──────────────┬────────────────┘                  └───────────────┬───────────────┘  │
│                 │                                                   │                  │
│                 ▼                                                   ▼                  │
│  ┌──────────────────────────────────────────────────────────────────────────────────┐  │
│  │                         LangGraph Multi-Agent Team                               │  │
│  │  [Supervisor Agent]                                                              │  │
│  │     ├── [HCP Profile Agent]      ───► Queries HCP Core Profile                   │  │
│  │     ├── [Rx Trend Agent]         ───► Analyzes Longitudinal Prescriptions        │  │
│  │     ├── [Engagement Agent]       ───► Reviews Historical Interactions & Channel  │  │
│  │     ├── [Market/Competitor Agent]───► Evaluates Competitor Brand Affinity        │  │
│  │     └── [Explanation Synthesizer]───► Compiles Evidence into Grounded Briefing   │  │
│  └──────────────────────────────────────────┬───────────────────────────────────────┘  │
│                                             │                                          │
│                                             ▼                                          │
│  ┌──────────────────────────────────────────────────────────────────────────────────┐  │
│  │                       Resilient LLM Provider Service                             │  │
│  │  • Primary: Sarvam AI (sarvam-105b)                                              │  │
│  │  • Fallback: OpenAI (gpt-4o-mini) via Circuit Breaker & Exponential Backoff       │  │
│  └──────────────────────────────────────────────────────────────────────────────────┘  │
└───────────────────────────────────────────┬────────────────────────────────────────────┘
                                            │ SQL / Cache
                                            ▼
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                              DATA PERSISTENCE & CACHE                                  │
│  • PostgreSQL (pgvector enabled) : 10k Synthetic HCPs, Rx History, Interactions, Audit │
│  • Redis (Port 6379)             : Session State, Rate Limiting, LangGraph Checkpoints │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Data Architecture & Synthetic Dataset Specifications

The platform requires a realistic, longitudinally consistent synthetic dataset representing a commercial pharma oncology and cardiology portfolio.

### Synthetic Schema Tables (`database/schema.sql`):
1. **`territories`**:
   - `id`, `name`, `region` (North, South, East, West), `quota`, `assigned_rep_name`.
2. **`products`**:
   - `id`, `name` (e.g., *OncoVex*, *CardioShield*), `therapeutic_area`, `brand_tier`, `launch_date`.
3. **`hcps`** (10,000 records):
   - `id`, `npi_synthetic` (10-digit synthetic identifier), `first_name`, `last_name`, `specialty` (Oncology, Cardiology, Internal Medicine, Endocrinology), `territory_id`, `hospital_affiliation`, `city`, `state`, `zip_code`, `decile` (1-10 prescription volume).
4. **`prescriptions`** (monthly time series per HCP per product over 12 months):
   - `id`, `hcp_id`, `product_id`, `month`, `trx_volume`, `nrx_volume`, `competitor_trx_volume`.
5. **`interactions`** (CRM interaction logs):
   - `id`, `hcp_id`, `interaction_date`, `channel` (F2F Detail, Email, Remote Call, Webinar, Advisory Board), `rep_id`, `topics_discussed`, `hcp_sentiment` (Positive, Neutral, Hesitant), `next_steps`.
6. **`recommendations`** (Persisted Next-Best-Action outputs):
   - `id`, `hcp_id`, `product_id`, `propensity_score`, `priority_tier` (High, Medium, Low), `recommended_action`, `recommended_channel`, `model_version`, `generated_at`.
7. **`audit_logs`**:
   - `id`, `user_id`, `user_role`, `action`, `resource_type`, `resource_id`, `timestamp`, `metadata`.

---

## 4. Machine Learning & Next-Best-Action Pipeline

### 4.1 Feature Engineering (`app/ml/features.py`)
Features extracted per HCP:
- `trx_growth_3m`: 3-month rolling prescription growth rate.
- `nrx_to_trx_ratio`: Share of new-to-brand prescriptions.
- `competitor_share`: Competitor volume / total market volume in territory.
- `days_since_last_interaction`: Recency of field touchpoint.
- `interaction_frequency_6m`: Total engagements across all channels in 6 months.
- `digital_affinity_score`: Ratio of email/webinar responses to total engagements.
- `hcp_decile`: High-volume potential indicator (1-10).
- `historical_response_rate`: Percentage of prior details leading to subsequent Rx uptick.

### 4.2 XGBoost Propensity Model (`app/ml/model.py`)
- **Objective**: Binary classification predicting conversion propensity (HCP willing to initiate/switch patients within next 30 days).
- **Training**: Synthetic historical ground-truth target `converted` (0 or 1).
- **Evaluation**: Calibration plot, ROC-AUC (target > 0.82), PR-AUC, Confusion Matrix.
- **Explainability**: Tree SHAP / Feature importances outputted as standardized JSON drivers for UI rendering.

### 4.3 Deterministic Rule-Based NBA Matrix (`app/ml/nba_rules.py`)
Combines ML propensity score with explicit business logic:
- **High Propensity (> 0.70) + High Competitor Share (> 0.50)**:
  - *Action*: In-person clinical detail focusing on head-to-head clinical efficacy data.
- **High Propensity (> 0.70) + Low Recency (> 45 days)**:
  - *Action*: Urgent follow-up meeting with medical specialist.
- **Medium Propensity (0.40 - 0.70) + High Digital Affinity**:
  - *Action*: Approved personalized email with link to digital patient case study.
- **Low Propensity (< 0.40) + Low Decile (< 4)**:
  - *Action*: Maintain low-cost automated digital newsletter cadence.
- **Frequency Capping**: Maximum 2 touches per month to prevent HCP fatigue.

---

## 5. LangGraph Multi-Agent Orchestration, Safe NL2SQL & LLM Architecture

```
                                  ┌───────────────────────────────┐
                                  │    Commercial Supervisor      │
                                  └───────────────┬───────────────┘
                                                  │
                 ┌────────────────────────────────┼────────────────────────────────┐
                 ▼                                ▼                                ▼
       ┌──────────────────┐             ┌──────────────────┐             ┌──────────────────┐
       │ HCP Dossier      │             │ Rx Analytics     │             │ CRM Engagement   │
       │ Agent            │             │ Agent            │             │ Agent            │
       └────────┬─────────┘             └────────┬─────────┘             └────────┬─────────┘
                │                                │                                │
                └────────────────────────────────┼────────────────────────────────┘
                                                 │
                                                 ▼
                                  ┌───────────────────────────────┐
                                  │      Safe NL2SQL Tool         │
                                  │  • AST / Syntax Validation    │
                                  │  • SELECT-only Guardrails     │
                                  │  • Schema-Bounded Queries     │
                                  └───────────────┬───────────────┘
                                                  │
                                                  ▼
                                  ┌───────────────────────────────┐
                                  │ Recommendation Explanation    │
                                  │ Agent (Sarvam / OpenAI)       │
                                  └───────────────────────────────┘
```

### 5.1 Agent Nodes & Specialized Capabilities:
1. **Commercial Supervisor Node**: Analyzes analyst intent, decomposes complex commercial questions, and delegates to specialized sub-agents with state checkpointing via Redis/MemorySaver.
2. **HCP Dossier Agent**: Retrieves HCP profile facts, specialty, affiliated hospitals, and commercial tier.
3. **Rx Analytics Agent**: Analyzes 12-month longitudinal prescription trends, TRx growth velocity, and new patient share.
4. **CRM Engagement Agent**: Evaluates historical rep details, sample deliveries, digital interactions, and sentiment.
5. **Safe NL2SQL Tool Node**:
   - Generates and executes read-only SQL queries to answer arbitrary natural language commercial questions (e.g., *"How many oncologists in District 3 have >50 competitor TRx and zero visits in the last 45 days?"*).
   - **Enterprise Security Guardrails**:
     - Strict `SELECT` statement verification using SQL parsing (prohibits `DROP`, `UPDATE`, `DELETE`, `ALTER`, `EXEC`).
     - Allowlisted tables only (`hcps`, `prescriptions`, `products`, `territories`, `interactions`, `recommendations`).
     - Query timeout enforcement (max 3 seconds) and bounded result limit (max 100 rows).
6. **Recommendation Explanation Synthesizer**: Grounded LLM agent synthesizing the factual evidence into an executive briefing citing specific dates, verified numbers, and reasons. **Never hallucinates scores.**

### 5.2 Enterprise Production-Grade Architecture:
- **Resilient LLM Provider Service (`app/ai/`)**:
  - `BaseLLMProvider` abstract interface with strict Pydantic v2 validation.
  - `SarvamProvider`: Primary adapter defaulting to `sarvam-105b`.
  - `OpenAIProvider`: Automatic fallback adapter using `gpt-4o-mini`.
  - `LLMRouter`: Implements bounded timeout (15s), exponential backoff with jitter (max 3 retries), and a stateful circuit breaker that trips after 3 consecutive failures.
- **Enterprise Observability & Reliability**:
  - **Structured JSON Logging**: Every request, database query, and LLM call tagged with a unique `X-Correlation-ID`.
  - **Health Probes**: `/health/live` (process health) and `/health/ready` (database, Redis, and LLM circuit status).
  - **Presidio Scrubbing**: Free-text prompts and queries sanitized before forwarding to external LLM providers.

---

## 6. Security, RBAC & Privacy Implementation

1. **Authentication**:
   - JWT tokens generated with `PyJWT` containing user ID, username, and assigned role.
   - Passwords securely hashed with `bcrypt`.
2. **Role Hierarchy Enforced in FastAPI**:
   ```python
   def require_role(min_role: UserRole):
       def dependency(current_user: User = Depends(get_current_active_user)):
           if ROLE_HIERARCHY[current_user.role] < ROLE_HIERARCHY[min_role]:
               raise HTTPException(status_code=403, detail="Insufficient permissions")
           return current_user
       return dependency
   ```
3. **Presidio Guardrail**:
   - Free-text queries scrubbed of person names, phone numbers, email addresses, and location identifiers before sending to external LLM providers.
4. **Audit Logging**:
   - Every recommendation generation, manual override, and AI explanation query logged with user identity, timestamp, and model version.

---

## 7. Backend API Specification (FastAPI)

| Endpoint | Method | Role Required | Description |
| :--- | :---: | :---: | :--- |
| `/api/auth/login` | POST | Public | Authenticates user and returns JWT token. |
| `/api/auth/me` | GET | STANDARD_USER+ | Returns authenticated user profile and role. |
| `/api/hcps` | GET | STANDARD_USER+ | Paginated HCP list with filtering by specialty, territory, decile. |
| `/api/hcps/{hcp_id}` | GET | STANDARD_USER+ | Detailed HCP dossier: profile, Rx time series, CRM logs. |
| `/api/recommendations` | GET | ANALYST+ | Ranked list of HCPs with priority score and recommended NBA. |
| `/api/recommendations/generate` | POST | ADMIN+ | Triggers batch scoring across all HCPs. |
| `/api/territories` | GET | STANDARD_USER+ | Territory summaries, quota progress, and rep assignments. |
| `/api/analytics/commercial` | GET | BUSINESS_OWNER+ | Overall portfolio KPIs, conversion rates, channel distribution. |
| `/api/ai/explain` | POST | ANALYST+ | Executes LangGraph explanation workflow for a given HCP. |
| `/api/roi` | GET | BUSINESS_OWNER+ | Computes financial uplift and productivity ROI based on query parameters. |
| `/api/evaluation/metrics` | GET | AUDITOR+ | Returns model performance (AUC, F1, calibration) and LLM latency. |
| `/api/audit/logs` | GET | AUDITOR+ | Returns immutable system audit trail. |

---

## 8. Frontend Specification (Next.js 14+)

### Pages & User Journeys:
1. **Login Page (`/login`)**:
   - Clean, professional login with demo role quick-select dropdown (`ADMIN`, `BUSINESS_OWNER`, `ANALYST`, `AUDITOR`) for seamless evaluation.
2. **Executive Commercial Dashboard (`/dashboard`)**:
   - KPI cards: Total HCPs (10,000), High Priority Targets, Projected Rx Lift, Time Saved per Rep.
   - Recharts visualizers: Monthly Rx trends, channel effectiveness breakdown, territory opportunity distribution.
3. **HCP Directory & Search (`/hcps`)**:
   - Fast, searchable table with filters by Specialty, Territory, Decile, and Priority Score.
   - Click to open HCP 360° Profile Drawer.
4. **Next-Best-Action Recommendations (`/recommendations`)**:
   - Ranked prioritization list with action badges (*Clinical Detail*, *Personalized Email*, *Webinar Invite*).
   - "Explain Action" button triggering the LangGraph AI drawer.
5. **AI Evidence Drawer**:
   - Displays model drivers (SHAP waterfall/bar chart), prescription trajectory, past interactions, and the grounded AI summary from Sarvam.
6. **Territory Analytics (`/territories`)**:
   - Territory performance table, quota gap analysis, and sales rep workload indicators.
7. **Interactive ROI Calculator (`/roi`)**:
   - Sliders: Number of Reps (default 50), Calls per Month (default 120), Rep Hourly Cost ($75), Conversion Uplift (2.5%).
   - Live updated financial metrics: Annual Hours Saved, Incremental Revenue, Total Net Benefit, ROI Multiple.
8. **Audit & Evaluation Dashboard (`/evaluation`)**:
   - Model accuracy graphs, ROC curve, LLM provider fallback latency stats, and audit log table.

---

## 9. Comprehensive Testing Architecture

### 9.1 Pytest Suite (`backend/tests/`)
- `tests/unit/test_ml_pipeline.py`: Verifies feature extraction, model inference, and output score boundaries [0.0, 1.0].
- `tests/unit/test_nba_rules.py`: Verifies deterministic priority assignments and channel frequency capping.
- `tests/unit/test_llm_router.py`: Mocks Sarvam failure to verify circuit breaker trip and seamless OpenAI fallback.
- `tests/unit/test_rbac.py`: Asserts that `ANALYST` cannot trigger batch generation or access system user administration.
- `tests/integration/test_api_endpoints.py`: Tests full HTTP response cycles for all routes using FastAPI `TestClient`.

### 9.2 Playwright E2E Suite (`frontend/e2e/`)
- `e2e/auth.spec.ts`: Tests role logins, session persistence, and unauthorized route redirects.
- `e2e/hcp_search.spec.ts`: Tests search filtering, pagination, and dossier opening.
- `e2e/recommendations.spec.ts`: Tests recommendation ranking, action filtering, and triggering AI explanation.
- `e2e/roi_calculator.spec.ts`: Tests slider adjustments and mathematical verification of recalculated outputs.

### 9.3 Selenium Cross-Browser Suite (`tests/selenium/`)
- `test_cross_browser_auth.py`: Runs on headless Chrome and Firefox to verify responsive navigation and table interactions.
- `test_evidence_drawer.py`: Verifies modal rendering and DOM elements for accessibility.

---

## 10. Step-by-Step Implementation Roadmap

| Phase | Milestone | Key Deliverables | Estimated Steps |
| :---: | :--- | :--- | :--- |
| **Phase 1** | **Foundations & Environment** | Repository structure, Docker Compose, `.env.example`, Pydantic Settings, DB migration scripts. | 1.1 - 1.5 |
| **Phase 2** | **Synthetic Data Generator** | Generator script generating 10,000 realistic synthetic HCPs, Rx histories, CRM interactions, and territories. | 2.1 - 2.4 |
| **Phase 3** | **Machine Learning & NBA Engine** | Feature extractor, XGBoost training script, model persistence, and rule-based NBA matrix. | 3.1 - 3.4 |
| **Phase 4** | **FastAPI Backend & RBAC** | Core database models, authentication, role middleware, REST endpoints, and Presidio PII integration. | 4.1 - 4.6 |
| **Phase 5** | **LLM Provider & LangGraph** | `LLMProviderInterface`, Sarvam adapter, OpenAI fallback, circuit breaker, and 5-node LangGraph workflow. | 5.1 - 5.5 |
| **Phase 6** | **Next.js UI & Design System** | Tailwind + shadcn setup, Dashboard, HCP Search, Recommendations, AI Drawer, and ROI Calculator. | 6.1 - 6.7 |
| **Phase 7** | **Evaluation & Audit System** | ML metrics collector, LLM latency tracer, and immutable audit logging service. | 7.1 - 7.3 |
| **Phase 8** | **Comprehensive Testing Suite** | Pytest unit/integration tests, Playwright E2E tests, and Selenium cross-browser automation suite. | 8.1 - 8.4 |
| **Phase 9** | **Documentation & Packaging** | Complete `docs/`, feature documents in `docs/features/`, API specs, and updated `README.md`. | 9.1 - 9.4 |
| **Phase 10**| **Docker Compose Verification** | End-to-end containerized run (`docker compose up --build`), validation of all features on clean boot. | 10.1 - 10.3 |

---

## 11. Acceptance & Definition of Done Criteria

- [ ] 10,000 synthetic HCPs seeded and searchable with zero latency issues.
- [ ] Trained XGBoost model produces calibrated propensity scores; NBA rules produce deterministic actions.
- [ ] LangGraph agent pipeline generates evidence-backed explanations using Sarvam AI (verified with mock tests).
- [ ] Fallback to OpenAI operates cleanly on simulated Sarvam outage without dropping requests.
- [ ] Server-side RBAC protects privileged endpoints across all 6 roles.
- [ ] Next.js UI is responsive, dark-mode polished, and contains zero hardcoded placeholder data.
- [ ] Pytest, Playwright, and Selenium test suites pass 100%.
- [ ] Docker Compose starts frontend, backend, PostgreSQL, and Redis in one command.
- [ ] Absolute file paths and secrets are completely absent from the codebase.
