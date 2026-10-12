# AGENTS.md — Project 03: Clinical Trial Intelligence & Site Selection Platform

> **Scope**: Governs all engineering, security, data integrity, and agentic workflows for the Clinical Trial Intelligence Platform. Adheres strictly to the Root [AGENTS.md](../AGENTS.md).

---

## 1. Core Principles
1. **Local-First Architecture**:
   - Backend: Python 3.11+ / FastAPI on port 8002.
   - Frontend: Next.js 14 App Router, Tailwind CSS, Lucide icons, Dark mode on port 3002.
   - Database: SQLite / PostgreSQL fallback (`clinical_trials.db`).
   - LLM: Sarvam AI (`sarvam-105b-conversations`) primary with OpenAI (`gpt-4o-mini`) fallback.
2. **Deterministic Eligibility & Predictive ML**:
   - Patient-trial matching evaluates inclusion/exclusion criteria with deterministic logic (`PASS`, `FAIL`, `UNKNOWN`).
   - Site enrollment risks are forecasted via an **XGBoost machine learning model** based on screening velocity, historical activation delays, screen failure rate, and dropout count.
   - LLMs act exclusively as reasoning and explanation layers.
3. **Synthetic Healthcare Data**:
   - 100% synthetic trials, patient EHR records, and site telemetry.
   - Prominently display a visible "Synthetic / Demo Data Only" disclaimer.
4. **Human-in-the-Loop Governance**:
   - Mandatory Clinical Reviewer sign-off (`CLINICAL_REVIEWER`) on all patient matching recommendations with full auditability.
5. **Role-Based Access Control (RBAC)**:
   - Hierarchy: `SUPER_ADMIN` (100) > `ADMIN` (80) > `CLINICAL_REVIEWER` (40) > `AUDITOR` (20) > `STANDARD_USER` (10).
