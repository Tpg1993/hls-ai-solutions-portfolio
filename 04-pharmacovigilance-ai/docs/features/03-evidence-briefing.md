# Feature 03: Evidence Assembly & AI Investigator Briefing

## 1. Feature Name & Purpose
- **Feature**: Hybrid Evidence Retrieval & Clinical Synthesis.
- **Purpose**: Links statistical safety signals to FDA product package insert warnings and published PubMed biomedical literature, generating an objective investigator briefing.

## 2. User Journey
1. Safety reviewer selects a target signal (e.g., CardioShield ↔ Acute Hepatitis).
2. System retrieves relevant label warnings and literature citations.
3. Reviewer clicks "Generate AI Briefing".
4. Sarvam AI (`sarvam-105b`) synthesizes an objective, evidence-grounded briefing over deterministic statistics and retrieved excerpts.

## 3. RBAC Permissions
- **Generate AI Briefing**: `ANALYST`, `SAFETY_REVIEWER`, `ADMIN`, `SUPER_ADMIN`.

## 4. API Endpoints
- `GET /api/v1/signals/{signal_id}/evidence`
- `POST /api/v1/signals/{signal_id}/summary`
