# AGENTS.md — Project 02: Pharma Regulatory Intelligence Copilot

> **Scope**: Governs all engineering, security, and agentic workflows for the Regulatory Intelligence Copilot. Adheres strictly to the Root [AGENTS.md](../AGENTS.md).

---

## 1. Core Principles
1. **Local-First Architecture**:
   - Backend: Python 3.11+ / FastAPI on port 8001.
   - Frontend: Next.js 14 App Router, Tailwind CSS, Lucide icons, Dark mode on port 3001.
   - Database: SQLite / PostgreSQL fallback (`regulatory_intelligence.db`).
   - LLM: Sarvam AI (`sarvam-105b-conversations`) primary with OpenAI (`gpt-4o-mini`) fallback.
2. **Zero Hallucination & Citation Grounding**:
   - Every answer to a regulatory question must cite specific authority, document title, section, and page number: `[FDA-2024-RWE, Section 3.2, Page 14]`.
   - If retrieved evidence is below relevance threshold, the system must issue a calibrated refusal (*"Insufficient evidence in authoritative guidance catalog"*).
3. **Safe NL2SQL Metadata Engine**:
   - Read-only parameterized queries against guidance registry, publication dates, authorities, and submission impact tables.
4. **Automated Cross-Version Diff Engine**:
   - Analyzes draft vs. final and historical iterations of regulatory guidances with semantic classifications (`Mandatory Requirement Added`, `Guidance Clarification`, `Scope Expansion`).
5. **Role-Based Access Control (RBAC)**:
   - Hierarchy: `SUPER_ADMIN` (100) > `ADMIN` (80) > `REGULATORY_REVIEWER` (40) > `AUDITOR` (20) > `STANDARD_USER` (10).
