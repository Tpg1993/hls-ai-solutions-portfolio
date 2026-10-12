# Feature 01: Regulatory Hybrid Search & Evidence-Backed Copilot

## 1. Feature Name & Purpose
- **Feature Name**: Multi-Authority Hybrid Semantic RAG & Evidence Verification
- **Purpose**: Enables regulatory affairs analysts to query global health authority guidances (FDA, EMA, ICH, PMDA, WHO) and receive answers strictly grounded in official clauses with verifiable chunk-level and page-level citations.

## 2. User Journey
1. Analyst navigates to **Copilot Search**.
2. Types inquiry or selects a pre-configured template (e.g. *What are the mandatory source data verification requirements for registry external control arms in FDA oncology submissions?*).
3. LangGraph multi-agent team retrieves relevant guidance chunks from the database, scores evidence grounding, and synthesizes an executive summary via **Sarvam AI (105B)**.
4. If retrieved evidence is insufficient, the system executes a calibrated refusal instead of hallucinating.
5. Analyst clicks any citation badge `[FDA, Section 3.2, Page 14]` to inspect the exact source text snippet in the Evidence Drawer.

## 3. RBAC Permissions
- Minimum Role: `STANDARD_USER` (Level 10) to search; `REGULATORY_REVIEWER` (Level 40) for full citation drill-down.

## 4. API Endpoints
- `POST /api/search`: Accepts `{ query, authority, therapeutic_area }`, returns structured answer and citations.
