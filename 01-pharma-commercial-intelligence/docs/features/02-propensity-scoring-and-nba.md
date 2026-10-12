# Feature: Propensity Scoring and Next-Best-Action (NBA) Engine

## 1. Purpose & Business Context
Automates the prioritization of 10,000 HCPs by generating calibrated adoption probabilities and assigning recommended actions (e.g. Clinical Detail on Efficacy, Digital Case Study, Medical Webinar) based on empirical features.

## 2. Technical Design
1. **Feature Extractor**: Computes 3-month TRx growth, competitor market share, interaction frequency, and digital affinity.
2. **Propensity Engine**: XGBoost calibrated classification model producing scores [0.0 - 1.0].
3. **NBA Rule Matrix**: Combines ML score with business rules and channel frequency capping (max 2 touches/month).

## 3. RBAC Permissions
- `GET /api/recommendations`: `STANDARD_USER`+
- `POST /api/recommendations/generate`: `ADMIN`+
