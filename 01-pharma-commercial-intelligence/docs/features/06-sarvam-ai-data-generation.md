# Feature 06: Live Sarvam AI Data Generation & Enrichment

## 1. Feature Name & Purpose
- **Feature Name**: Live Sarvam AI Clinical Data Generator & Account Enrichment Engine
- **Purpose**: Generates realistic, contextual pharmaceutical field notes, medical liaison call transcripts, and account briefings using Sarvam AI 105B (`sarvam-105b-conversations`), directly committed into the commercial intelligence database.

## 2. User Journey
1. **CLI Execution**: Run `$env:PYTHONPATH="backend"; .\.venv\Scripts\python -m app.cli.generate_ai_data` to enrich the top HCP accounts with live Sarvam AI interaction logs.
2. **Dashboard 1-Click Trigger**: Click the **`✨ Generate Actual Data (Sarvam AI)`** button in the header of the web application (`http://localhost:3000`).
3. **Inspect Generated Notes**:
   - Navigate to the **Next-Best-Action** or **HCP Directory** table.
   - Click **AI Briefing** on any HCP.
   - Inspect the **Pre-Call Action Briefing** drawer to review the multi-agent narrative and recent field notes tagged with the `Sarvam AI 105B` badge.

## 3. RBAC Permissions
- **CLI**: System / Local Developer environment.
- **API (`POST /api/ai/enrich-data`)**: Requires role `ANALYST` (Level 40) or higher.

## 4. API Endpoints
- `POST /api/ai/enrich-data?count={n}`: Enriches top accounts with `n` realistic clinical interactions using Sarvam AI.
- `GET /api/hcps/{hcp_id}`: Returns the HCP profile along with longitudinal prescriptions and enriched interaction logs.
- `POST /api/ai/explain`: Synthesizes a real-time pre-call strategic briefing for the target HCP using Sarvam AI 105B.

## 5. Security & Grounding
- **Zero Secret Exposure**: Provider API keys remain strictly server-side in `.env`.
- **Synthetic Grounding**: All physician names and patient counts are 100% synthetic; clinical scenarios ground the LLM in specific medical topics (PFS endpoints, biomarker testing, formulary appeals, adverse event mitigation).
