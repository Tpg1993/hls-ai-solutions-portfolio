# Architecture Specification: Pharma Commercial Intelligence & NBA Platform

## 1. High-Level Architecture Overview

The platform uses a **local-first, full-stack microservices architecture** orchestrated via Docker Compose:

```
┌────────────────────────────────────────────────────────────────────────┐
│                          User Browser (Port 3000)                      │
│                  Next.js 14 App Router + Tailwind + Recharts           │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │ HTTP / JSON
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│                        FastAPI Backend (Port 8000)                     │
│  ├── Security & RBAC Guards (SUPER_ADMIN > ADMIN > BUSINESS_OWNER...)  │
│  ├── Safe NL2SQL Query Parser (SELECT only, Table Allowlisting)        │
│  ├── Presidio PII/PHI Sanitizer                                        │
│  ├── Machine Learning Propensity Engine (XGBoost + Calibrated Sigmoid) │
│  ├── Deterministic NBA Rule Engine                                     │
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

## 2. LangGraph Agentic Multi-Agent Topology
1. **Commercial Supervisor Node**: Analyzes analyst intent, decomposes complex commercial inquiries, and coordinates child agent state.
2. **HCP Dossier Agent**: Retrieves demographic and institutional facts.
3. **Rx Analytics Agent**: Computes rolling 3-month growth and competitor share trends.
4. **CRM Engagement Agent**: Evaluates recency and sentiment across channels.
5. **Safe NL2SQL Tool Node**: Executes read-only queries with strict AST checks.
6. **Recommendation Explanation Synthesizer**: Uses Sarvam AI (with OpenAI fallback) to draft executive briefings grounded exclusively in retrieved facts.

## 3. Resilient LLM Router Design
- **Primary**: Sarvam AI (`sarvam-105b`).
- **Fallback**: OpenAI (`gpt-4o-mini`) via Circuit Breaker (opens after 3 failures).
- **Deterministic Offline Fallback**: Generates structured grounded briefings even when external keys are unconfigured in offline CI.
