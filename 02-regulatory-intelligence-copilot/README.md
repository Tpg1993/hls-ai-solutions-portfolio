# Project 02: Pharma Regulatory Intelligence Copilot

[![Python](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110-teal.svg)](https://fastapi.tiangolo.com/)
[![Next.js](https://img.shields.io/badge/Next.js-14-black.svg)](https://nextjs.org/)
[![Hybrid RAG](https://img.shields.io/badge/Hybrid--RAG-pgvector%2BBM25-blueviolet.svg)](https://github.com/pgvector/pgvector)
[![Sarvam AI](https://img.shields.io/badge/Sarvam--105b-Primary-purple.svg)](https://sarvam.ai/)
[![Docker](https://img.shields.io/badge/Docker-Compose-2496ED.svg)](https://www.docker.com/)

> **Executive Summary**: A local-first regulatory intelligence copilot built to navigate health authority guidance (FDA, EMA, ICH), answer evidence-backed regulatory questions with inspectable citations, automatically detect cross-version clause modifications, and map submission impacts across drug development portfolios.

---

## 1. Key Business Features

1. **Hybrid Regulatory RAG with Reranking**:
   - Blends dense vector retrieval (pgvector) with keyword search to surface relevant guidance sections.
   - Cross-encoder reranker ensures high retrieval precision with line-level citations.
2. **Cross-Version Guidance Diff Engine**:
   - Detects added, modified, and deleted clauses between guidance revisions with impact severity ratings (`CRITICAL`, `MAJOR`, `MINOR`).
3. **Submission Impact Matrix**:
   - Maps regulatory shifts to specific drug development dossiers (NDA, BLA, IND, MAA) and affected CTD modules.
4. **Mandatory Reviewer Sign-Off**:
   - Role-gated to `REGULATORY_REVIEWER` for sign-off on submission impact mitigation plans.
5. **Safe Read-Only NL2SQL**:
   - Parameterized read-only SQL queries over guidance and submission catalogs with AST validation.

---

## 2. Architecture & Tech Stack

```mermaid
graph TD
    User["Regulatory Affairs Strategist"] --> Frontend["Next.js 14 App Router (Port 3001)"]
    Frontend --> Backend["FastAPI REST Backend (Port 8001)"]
    Backend --> DB[("SQLite / PostgreSQL + pgvector")]
    Backend --> Search["Hybrid Retrieval (BM25 + Semantic Vector)"]
    Backend --> Diff["AST Clause Diff Engine"]
    Backend --> AI["Sarvam AI (sarvam-105b) + OpenAI Fallback"]
    Backend --> Audit["Immutable Regulatory Review Trail"]
```

---

## 3. Quickstart & Local Setup

### Option A: Running with Docker Compose (Recommended)
```bash
# From 02-regulatory-intelligence-copilot root
docker compose up --build
```
- Frontend UI: `http://localhost:3001`
- FastAPI OpenAPI Docs: `http://localhost:8001/docs`

### Option B: Local Development

#### 1. Backend Setup:
```bash
cd backend
python -m venv .venv
# On Windows:
.venv\Scripts\activate
# On Linux/macOS:
source .venv/bin/activate

pip install -r requirements.txt
python -m uvicorn app.main:app --port 8001 --reload
```

#### 2. Frontend Setup:
```bash
cd frontend
npm install
npm run dev -- -p 3001
```

---

## 4. Running Test Suites

### Backend Pytest Suite
```bash
cd backend
python -m pytest -v
```
*Current test suite: 11 unit & integration tests passing with 100% success rate.*

### E2E Cross-Browser Automation (Selenium & Playwright)
```bash
# Selenium
python -m pytest tests/selenium/test_cross_browser_flow.py -v

# Playwright
cd frontend
npm run test:e2e
```

---

## 5. Documentation Map

Detailed documentation in `docs/`:
- [Business Use Case](docs/business-use-case.md)
- [System Architecture](docs/architecture.md)
- [Security & RBAC](docs/security.md)
- [Configuration & Environment](docs/configuration.md)
- [Data Dictionary & Schema](docs/data-dictionary.md)
- [REST API Specifications](docs/api.md)
- [Testing Standards](docs/testing.md)
- [AI Evaluation Framework](docs/evaluation.md)
- [Financial ROI Model](docs/roi-assumptions.md)
- [Known Limitations & Disclaimers](docs/known-limitations.md)
- **Features**:
  - [01: Regulatory Hybrid Search](docs/features/01-regulatory-hybrid-search.md)
  - [02: Cross-Version Diff](docs/features/02-cross-version-diff.md)
  - [03: Submission Impact Matrix](docs/features/03-submission-impact-matrix.md)
  - [04: Safe NL2SQL Catalog](docs/features/04-safe-nl2sql-catalog.md)

---

## 6. Synthetic Data Disclaimer
All regulatory guidance comparisons, submission impact mappings, and protocol references are 100% synthetic and generated for demonstration and research purposes only. Official regulatory filings must consult official agency publications.
