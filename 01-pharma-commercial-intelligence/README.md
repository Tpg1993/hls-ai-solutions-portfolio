# Project 01: Pharma Commercial Intelligence & Next-Best-Action (NBA) Platform

> **Target Organizations**: Commercial Biopharma Enterprises, Specialty Therapeutics & Life Sciences Organizations  
> **Status**: Verified Full-Stack Local-First Implementation  
> **Tech Stack**: Next.js 14 • FastAPI • LangGraph • Safe NL2SQL • XGBoost • PostgreSQL/pgvector • Redis • Sarvam AI • Docker Compose

---

## 1. Executive Summary

In life sciences commercial operations, pharmaceutical field sales representatives and Medical Science Liaisons (MSLs) manage thousands of Healthcare Professionals (HCPs) across multiple territories. Manual call planning is inconsistent, pre-call research consumes hours of rep time, and field teams often lack explainable data on *why* an HCP should be contacted.

This platform provides an **enterprise-grade commercial co-pilot**:
1. **Predictive Machine Learning**: Calibrated XGBoost propensity model predicting 30-day treatment adoption based on 12-month longitudinal prescription trends and interaction recency.
2. **Deterministic Next-Best-Action (NBA) Engine**: Transparent commercial rule matrix that assigns tailored action channels (*In-Person Detail*, *Approved Email*, *Medical Webinar*) with frequency capping (max 2 touches/month).
3. **Safe NL2SQL Analytical Tool**: Enables analysts to query 10,000 synthetic HCPs and prescription claims in natural language using AST-validated, read-only SQL queries.
4. **LangGraph Multi-Agent Collaboration**: Multi-agent team (Supervisor, HCP Dossier, Rx Analytics, CRM Engagement) delivering grounded briefings powered by **Sarvam AI** (`sarvam-105b`) with resilient **OpenAI fallback** (`gpt-4o-mini`).
5. **Deterministic Commercial ROI Engine**: Mathematical models calculating annual rep time saved and gross revenue uplift from NBA adoption.

---

## 2. Business Problem & Measurable Impact

| Dimension | Legacy Pharma Commercial Workflow | This Platform |
| :--- | :--- | :--- |
| **HCP Prioritization** | Static quarterly call lists based only on historical volume. | Dynamic weekly propensity scoring combining Rx trajectory and sentiment. |
| **Pre-Call Planning** | Reps spend 30–45 mins per call digging through CRM notes. | Automated AI briefings summarizing key drivers in <3 seconds. |
| **Trust & Transparency** | Reps distrust "black-box" scores without explanations. | 100% explainable drivers, SHAP waterfall charts, and verifiable citations. |
| **Economic Return** | Unmeasured commercial spend. | Deterministic ROI engine projecting **$1.65M+ annual net benefit** for 50 reps. |

---

## 3. System Architecture & Multi-Agent Flow

```
┌────────────────────────────────────────────────────────────────────────┐
│                          User Browser (Port 3000)                      │
│                  Next.js 14 App Router + Tailwind + Recharts           │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │ HTTP / JSON
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│                        FastAPI Backend (Port 8000)                     │
│  ├── Server-Side RBAC (SUPER_ADMIN > ADMIN > BUSINESS_OWNER...)        │
│  ├── Safe NL2SQL Tool (AST / SELECT-only validation)                  │
│  ├── Presidio PII/PHI Sanitizer                                        │
│  ├── XGBoost Propensity Model & Explainable SHAP Drivers               │
│  ├── Next-Best-Action (NBA) Rule Engine                                │
│  ├── LangGraph Multi-Agent Team (Supervisor, Dossier, Rx, CRM Agents)   │
│  └── Resilient LLM Router (Primary: Sarvam AI | Fallback: OpenAI)      │
└───────────────────────┬────────────────────────────┬───────────────────┘
                        │                            │
                        ▼                            ▼
┌───────────────────────────────────┐    ┌───────────────────────────────┐
│       PostgreSQL + pgvector       │    │         Redis Cache           │
│   10,000 Synthetic HCP Records    │    │   Session State, Checkpoints, │
│   Longitudinal Rx & CRM Logs      │    │   Rate Limiting (Port 6379)   │
└───────────────────────────────────┘    └───────────────────────────────┘
```

---

## 4. LLM Provider Hierarchy & Fallback Policy

```
[Request] ──► [LLM Router]
                    │
                    ├──► [Primary: Sarvam AI (sarvam-105b)]
                    │         │ (Fails on timeout / 5xx / 429)
                    │         ▼ (Circuit Breaker trips after 3 failures)
                    └──► [Fallback: OpenAI (gpt-4o-mini)]
                              │ (If unconfigured in offline CI)
                              ▼
                         [Local Deterministic Briefing Engine]
```

- **Zero Secret Exposure**: All provider keys reside strictly server-side in `.env`.
- **Grounded Numerics**: LLM is strictly prohibited from inventing scores, patient numbers, or currency figures. Scores originate exclusively from deterministic Python/SQL/ML services.

---

## 5. Quickstart & Local Setup Instructions

### Prerequisites
- Python 3.11+
- Node.js 18+ (or Docker Compose)

### 1. Set Up Python Virtual Environment (`.venv`)
```bash
# Navigate to project directory
cd "01-pharma-commercial-intelligence"

# Create virtual environment
python -m venv .venv

# Activate virtual environment
.\.venv\Scripts\Activate.ps1    # On Windows PowerShell
source .venv/bin/activate       # On Linux / macOS

# Install backend dependencies
pip install -r backend/requirements.txt
```

### 2. Configure Environment
```bash
cp .env.example .env
# Edit .env and supply SARVAM_API_KEY (and optional OPENAI_API_KEY)
```

### 3. Run Automated Pytest Test Suite
```bash
pytest -v
```
*All 17 unit and integration tests execute and pass out-of-the-box using the deterministic offline mock engine.*

### 4. Run Locally with Docker Compose
```bash
docker compose up --build
```
- **Frontend Dashboard**: `http://localhost:3000`
- **FastAPI OpenAPI Swagger**: `http://localhost:8000/docs`
- **Health Probes**: `http://localhost:8000/health/live` and `/health/ready`

---

## 6. Demo Accounts (Seeded RBAC Credentials)

| Role | Username | Password | Permitted Actions |
| :--- | :--- | :--- | :--- |
| **SUPER_ADMIN** | `superadmin` | `SuperAdmin@123` | Full system access, data regeneration |
| **ADMIN** | `admin` | `Admin@123` | User administration, batch recommendation generation |
| **BUSINESS_OWNER** | `business_owner` | `Business@123` | Configure ROI parameters, view commercial KPIs |
| **ANALYST** | `analyst` | `Analyst@123` | HCP drilldown, AI explanation briefings, Safe NL2SQL |
| **AUDITOR** | `auditor` | `Auditor@123` | Read-only access to immutable audit log |
| **STANDARD_USER** | `standard_user` | `User@123` | View HCP directory and territory charts |

---

## 7. Mandatory Disclaimer

> **SYNTHETIC / DEMO DATA ONLY**: All Healthcare Professionals, National Provider Identifiers (NPIs), hospital affiliations, prescription metrics, and patient counts are 100% synthetically generated. For commercial prioritization and educational demonstration only. Not for clinical decision-making.
