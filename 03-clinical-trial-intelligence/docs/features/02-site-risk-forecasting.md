# Feature 02: Predictive Trial Site Risk Forecasting

## 1. Feature Name & Purpose
- **Feature**: Machine Learning Trial Site Operational Risk & Failure Forecaster
- **Purpose**: Assesses investigator site health across enrollment velocity, protocol deviation rates, IRB delay timelines, and query response latency using a Gradient Boosting / XGBoost model.
- **Target Personas**: Clinical Operations Directors, Clinical Study Managers, CRO Leads.

## 2. User Journey
1. Study Manager opens the "Site Intelligence & Risk" tab.
2. The dashboard displays real participating institutions (e.g., Dana-Farber, Memorial Sloan Kettering, MD Anderson, UCLA Health).
3. The ML model computes an empirical Risk Score [0-100] and risk tier (LOW, MEDIUM, HIGH, CRITICAL).
4. Feature importance indicators reveal primary operational bottlenecks (e.g. protocol deviations > 12/month, staff turnover).
5. Manager reviews recommended mitigations (e.g., CRC re-training, site visit escalation).

## 3. RBAC Permissions
- `ANALYST` / `CLINICAL_REVIEWER` (Level 40) or higher: View site predictions and operational metrics.
- `ADMIN` (Level 80): Adjust operational thresholds and configure monitoring alerts.

## 4. API Endpoints
- `GET /api/v1/sites`: List trial sites with enrollment metrics.
- `POST /api/v1/sites/{id}/predict-risk`: Run ML site risk assessment.

## 5. Data & ML Models
- **Algorithm**: scikit-learn `GradientBoostingClassifier` / `XGBClassifier`.
- **Features**: Historical accrual rate, screen failure ratio, protocol deviation count, data query turnaround time, staff vacancy rate.
- **Grounded Numerics**: All probabilities generated deterministically by the model; Sarvam AI explains operational drivers.

## 6. Error & Edge States
- Sites with insufficient telemetry (<30 days operational): Displayed as "Calibrating" with baseline heuristic score.
- Model serialization failure: Fallback to rule-based composite risk score.

## 7. Testing Strategy
- Pytest suite validates ML model output ranges [0, 1] and risk tier boundaries.
- Cross-validation on synthetic site dataset ensures consistency.
