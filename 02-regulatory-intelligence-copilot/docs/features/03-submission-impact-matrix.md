# Feature 03: Active Pipeline Submission Impact Matrix

## 1. Feature Name & Purpose
- **Feature Name**: Pipeline Submission Impact Matrix
- **Purpose**: Maps regulatory guidance shifts directly to internal pipeline products (`OncoVax-7`, `CardioStat-Alpha`, `NeuroRegen-09`), ongoing IND/NDA filings, and clinical phases, highlighting required protocol amendments and compliance deadlines.

## 2. User Journey
1. Regulatory Director opens **Pipeline Impacts**.
2. Reviews prioritized list of affected pipeline programs.
3. Observes that `OncoVax-7` (Phase 2b mRNA Neoantigen Vaccine) has a **Critical** impact requiring 15% source data verification on 310 registry patient records prior to the Type B FDA meeting.
4. Compliance deadlines and required remediation actions are clearly tracked.

## 3. RBAC Permissions
- Minimum Role: `STANDARD_USER` (Level 10).

## 4. API Endpoints
- `GET /api/impacts`: Returns impacted drug programs, action items, and deadlines.
