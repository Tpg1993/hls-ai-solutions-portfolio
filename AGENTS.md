# AGENTS.md — Mandatory Engineering, Security, and Delivery Standards

> **Scope**: This document governs all projects and coding agents within the HLS AI Solutions Portfolio. All AI coding agents and engineers MUST strictly read and adhere to these directives for every task, plan, and code modification. Treat this as an immutable engineering contract.

---

## 1. Core Principles & Non-Negotiable Rules

1. **Local-First Full Stack**:
   - Frontend: **Next.js + React + TypeScript** (Tailwind CSS + shadcn/ui + Lucide icons + Recharts). *Never use Streamlit.*
   - Backend: **Python 3.11+ / FastAPI** with strict **Pydantic v2** validation.
   - Orchestration: **LangGraph** for multi-agent workflows, state machines, tool calling, and human approval gates.
   - AI Capabilities: **Multi-Agent Systems + Safe NL2SQL + Hybrid RAG + Predictive ML (XGBoost/scikit-learn)**.
   - Database: **PostgreSQL + pgvector** (no proprietary vector databases; hybrid keyword + semantic retrieval; relation tables for NL2SQL).
   - Cache: **Redis** for state, session caches, and rate limiting.
   - Containerization: **Docker Compose** for running the entire local stack without mandatory cloud dependencies.
   - Enterprise Resilience: Structured JSON logging, correlation IDs, health checks (`/health/live`, `/health/ready`), connection pooling, and circuit breakers.
   - Safe NL2SQL Engine: Read-only execution, schema allowlisting, SQL syntax validation, and strict parameterized execution.
2. **Public Git & Zero Secret Leakage**:
   - Every repository is treated as **Public Open Source**.
   - **ZERO SECRETS IN CODE**: Never commit `.env`, API keys, bearer tokens, database passwords, or certificates.
   - Only `.env.example` with non-functional placeholders is tracked in version control.
   - Provider API keys (`SARVAM_API_KEY`, `OPENAI_API_KEY`) reside exclusively in backend server environments. **Never prefix provider keys with `NEXT_PUBLIC_`**.
3. **No Machine-Specific Static Paths**:
   - **Strictly use relative paths** anchored from project/module roots or loaded via environment configuration.
   - **Never hardcode Windows drive letters (`C:\`), user home directories (`/home/...`, `Users/...`), or fixed absolute paths.**
   - Prevent path traversal (`../`) and arbitrary file write vulnerabilities in all file/upload handlers.
4. **Deterministic Numerics & Grounded AI**:
   - **Never permit an LLM to invent scores, statistics, patient counts, or dollar values.**
   - All numerical scores, probability metrics, and financial ROI must originate from deterministic Python services, SQL aggregations, or scikit-learn / XGBoost ML models.
   - LLMs act exclusively as reasoning and explanation layers over pre-calculated facts and citations.
5. **Synthetic Data Only**:
   - All healthcare, clinical, HCP, and safety records must be **100% synthetic**.
   - Prominently display a visible "Synthetic / Demo Data Only" disclaimer across all UI views and API payloads.
   - Clinical and pharmacovigilance workflows are decision support only; human review is mandatory before any action.

---

## 2. LLM Provider Hierarchy & Fallback Policy

```
[Incoming Request]
        │
        ▼
[Provider Router]
        │
   ┌────┴────────────────────────┐
   ▼                             ▼
[Primary: Sarvam AI]     [Fallback: OpenAI]
(sarvam-105b)            (gpt-4o-mini / gpt-4o)
   │                             ▲
   │ (Timeout / 5xx / RateLimit) │ (Only if enabled & key present)
   └─────────────────────────────┘
```

1. **Sarvam AI as Primary**:
   - Sarvam API is the primary model across all applications (defaulting to `sarvam-105b` or task-optimized endpoints).
   - All calls must use an internal abstraction layer (`LLMProviderInterface`).
2. **OpenAI as Fallback**:
   - OpenAI is an **optional fallback** activated only when:
     1. `OPENAI_API_KEY` is configured in the backend `.env`.
     2. A provider-level failure occurs (network timeout, 5xx server error, or 429 rate limit).
   - **Do NOT fall back** on:
     - Invalid user input or schema validation errors (400 Bad Request).
     - Authentication / authorization failures (401 / 403).
     - Prompt policy / safety violations.
3. **Resilience & Safety**:
   - Implement exponential backoff with jitter and strict bounded timeouts (e.g., max 15s).
   - Implement a circuit breaker to avoid cascading provider failures.
   - If fallback triggers, log safe telemetry (latency, provider token count, provider name) without exposing prompt text or secrets, and inform the UI via neutral response metadata.
4. **Structured Outputs**:
   - Enforce Pydantic schema validation on all LLM responses.
   - Apply prompt injection defenses and Microsoft Presidio PII/PHI redaction where user-generated text is processed.

---

## 3. Role-Based Access Control (RBAC) & Hierarchy

Authorization must be strictly enforced on the **FastAPI backend** (dependency injection on routes), never relying solely on frontend UI button hiding. Default policy: **Deny by default**.

### Role Hierarchy Matrix

| Role | Hierarchy Level | Primary Permissions | Audit Scope |
| :--- | :---: | :--- | :--- |
| **SUPER_ADMIN** | 100 | System & tenant configuration, role assignment, all project datasets. Cannot view unredacted provider secrets. | Full Audit Logs & System Telemetry |
| **ADMIN** | 80 | User management, project settings, batch jobs, cache flushing. | Audit Logs & User Activity |
| **BUSINESS_OWNER** | 60 | Configure business assumptions, KPI definitions, and ROI parameters. View commercial analytics. | Business & Strategy Reports |
| **ANALYST** | 40 | Execute search, trigger ML predictions, run recommendations, query AI assistant, export reports. | Analyst Workspace Activity |
| **REGULATORY_REVIEWER** | 40 | Upload regulatory docs, compare guidance versions, inspect citation evidence, sign off reviews. | Regulatory Decision Trail |
| **CLINICAL_REVIEWER** | 40 | Review trial-patient match criteria, approve/reject/modify match status, review site risk. | Clinical Decision Logs |
| **SAFETY_REVIEWER** | 40 | Review adverse event cases, inspect safety signals, add investigator notes, escalate signals. | Pharmacovigilance Decision Log |
| **AUDITOR** | 20 | Read-only access to immutable audit events, evaluation metrics, and model run history. | Read-Only Audit Inspection |
| **STANDARD_USER** | 10 | Basic view of permitted public dashboards and search. Read-only. | Basic Session Logs |

### Security Requirements:
- Hash passwords using `bcrypt` or `argon2`. Never store plaintext passwords or hardcoded test user credentials in source code.
- Implement JWT or secure session cookies with explicit expiry and revocation.
- Provide a CLI seed script (`python -m app.cli.seed_users`) for bootstrapping local demo accounts.

---

## 4. Comprehensive Testing Standards (Mandatory)

A feature is **NOT DONE** unless its test suite passes. Never report tests as passing without executing them.

1. **Backend Unit & Integration Tests (`pytest`)**:
   - Location: `backend/tests/unit/` and `backend/tests/integration/`
   - Target: ≥ 80% coverage on core business logic, RBAC dependencies, ML pipelines, and LLM routers.
   - Test suites must cover:
     - Fast deterministic mock tests for Sarvam and OpenAI.
     - Role authorization checks (verify both `200 OK` for authorized roles and `403 Forbidden` for unauthorized roles).
     - Edge cases: missing keys, rate limits, malformed inputs, SQL injection attempts, and path traversal strings.
2. **Frontend Component & Unit Tests**:
   - Location: `frontend/__tests__/` (Vitest / React Testing Library).
   - Test components for loading states, error boundaries, empty states, and permission-gated elements.
3. **End-to-End (E2E) Browser Tests**:
   - **Playwright Test Suite**: Primary automated UI suite in `frontend/e2e/` testing login, navigation, filter selection, AI generation triggers, and evidence drawer inspection.
   - **Selenium Test Suite**: Comprehensive cross-browser verification suite in `tests/selenium/` verifying critical user flows, RBAC page guards, and accessibility under headless Chrome/Firefox.
4. **CI Readiness**:
   - All tests must pass in headless local environments and GitHub Actions with zero paid external API dependencies (use mock adapters).

---

## 5. Documentation Maintenance (Must Stay Current)

Documentation must be updated in the **same git commit** as code changes. Stale documentation is considered a defect.

Required Documentation Structure in Every Project:
```
project/
├── docs/
│   ├── architecture.md       # C4 / component diagrams, data flows, tech stack choices
│   ├── security.md           # RBAC rules, authentication, threat model, Presidio PII rules
│   ├── configuration.md      # All environment variables, defaults, validation rules
│   ├── data-dictionary.md    # Database schema, synthetic dataset schemas, data generation logic
│   ├── api.md                # REST endpoints, request/response schemas, error codes
│   ├── testing.md            # Commands to run pytest, Vitest, Playwright, and Selenium
│   ├── evaluation.md         # RAG/ML quality metrics, latency, accuracy, benchmark datasets
│   ├── roi-assumptions.md    # Financial & operational assumptions behind ROI calculators
│   ├── known-limitations.md  # Explicit local demo boundaries, synthetic caveats
│   └── features/             # ONE MARKDOWN FILE PER MAJOR FEATURE
│       ├── 01-hcp-search.md
│       ├── 02-next-best-action.md
│       ├── 03-ai-explanation.md
│       └── ...
├── README.md                 # Complete overview, quickstart, demo walkthrough, screenshots
└── AGENTS.md                 # Project-specific guidelines adhering to this root AGENTS.md
```

### Feature Document Template (`docs/features/*.md`):
1. **Feature Name & Purpose**: Business rationale and target personas.
2. **User Journey**: Step-by-step UI workflow.
3. **RBAC Permissions**: Required roles to view or execute.
4. **API Endpoints**: Contracts and parameters.
5. **Data & ML Models**: Features used, deterministic rules, LLM prompts.
6. **Error & Edge States**: Empty states, failure handling, fallback behavior.
7. **Testing Strategy**: Unit, integration, and E2E coverage.

---

## 6. Project Directory Layout & Clean Architecture

Each project must follow a clean, modular structure:

```
0X-<project-name>/
├── frontend/                 # Next.js 14+ App Router, Tailwind, TypeScript
│   ├── src/app/              # Pages & route groups
│   ├── src/components/       # UI components (shadcn/ui + custom widgets)
│   ├── src/services/         # Type-safe API clients (Fetch / Axios)
│   ├── src/hooks/            # Custom React hooks
│   ├── src/types/            # TypeScript interfaces
│   └── e2e/                  # Playwright E2E specs
├── backend/                  # FastAPI Python backend
│   ├── app/
│   │   ├── api/              # Route controllers (thin, typed)
│   │   ├── core/             # Config, security, DB session, RBAC dependencies
│   │   ├── models/           # SQLAlchemy ORM models
│   │   ├── schemas/          # Pydantic v2 schemas
│   │   ├── services/         # Business logic & services
│   │   ├── ml/               # scikit-learn / XGBoost training & inference
│   │   ├── ai/               # Sarvam + OpenAI provider abstraction & LangGraph agents
│   │   ├── rag/              # Hybrid retrieval, pgvector indexing, rerankers
│   │   └── data/             # Synthetic data generators & seed scripts
│   └── tests/
│       ├── unit/             # Pytest unit tests
│       └── integration/      # Pytest API integration tests
├── tests/
│   └── selenium/             # Selenium cross-browser automation suite
├── docs/                     # System & feature documentation
├── docker-compose.yml        # Multi-service composition (frontend, backend, postgres, redis)
├── Dockerfile.frontend       # Non-root Next.js container
├── Dockerfile.backend        # Non-root FastAPI container
├── .env.example              # Documented environment template with placeholders
├── .gitignore                # Project-level gitignore
├── README.md                 # Executive summary & quickstart guide
└── AGENTS.md                 # Project-level agent instructions
```

---

## 7. Definition of Done (DoD) Checklist

Before marking any task or project phase complete:
- [ ] Code is implemented end-to-end (no mock stubs or fake numbers in production paths).
- [ ] Zero secrets committed; verified against `.env.example` and `.gitignore`.
- [ ] No hardcoded machine paths or usernames (purely relative and configurable).
- [ ] Server-side RBAC enforced with role hierarchy.
- [ ] Primary Sarvam AI with resilient OpenAI fallback implemented and verified.
- [ ] Presidio PII scrubbing active on sensitive ingestion text.
- [ ] All unit and integration tests written and passing.
- [ ] Playwright and Selenium test suites written and runnable.
- [ ] Feature documentation in `docs/features/` created or updated.
- [ ] Docker Compose builds and boots cleanly with `docker compose up --build`.
- [ ] Clear synthetic data disclaimers rendered in UI.
