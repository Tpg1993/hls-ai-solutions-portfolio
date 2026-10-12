# Feature: HCP Search and 360° Commercial Profiling

## 1. Purpose & Business Context
Provides sales representatives and commercial analysts with immediate access to 10,000 synthetic Healthcare Professionals, longitudinal 12-month prescription time series, past CRM interaction logs, and volume deciles.

## 2. User Journey
1. User searches HCP by name, NPI, or hospital affiliation.
2. Applies filters by Specialty (Oncology, Cardiology), Territory, or Decile.
3. Clicks on an HCP to open the 360° Commercial Dossier with monthly Rx graphs and CRM sentiment logs.

## 3. RBAC Permissions
- Required Role: `STANDARD_USER` or higher.

## 4. API Contracts
- `GET /api/hcps` (query params: `specialty`, `territory_id`, `decile_min`, `search`, `limit`, `offset`)
- `GET /api/hcps/{hcp_id}` (returns complete profile, prescriptions, and interactions)

## 5. Security & Privacy
- All HCP data is 100% synthetic.
- Search inputs are parameterized to prevent SQL injection.
