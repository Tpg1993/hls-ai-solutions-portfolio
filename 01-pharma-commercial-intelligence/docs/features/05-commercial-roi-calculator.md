# Feature: Commercial ROI & Economic Value Calculator

## 1. Purpose & Business Context
Allows Commercial VPs and Business Owners to configure field force parameters (number of reps, calls per month, hourly cost, conversion lift) and model deterministic returns in both hours saved and gross brand revenue.

## 2. Technical Design
- Implemented as deterministic Python calculation service in `app/services/roi_service.py`.
- No LLM hallucination of financial figures.
- Displays explicit synthetic demo disclaimer.

## 3. RBAC Permissions
- `GET /api/roi`: `STANDARD_USER`+
- `POST /api/roi`: `BUSINESS_OWNER`+
