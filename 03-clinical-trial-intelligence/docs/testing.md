# Testing Guide: Clinical Trial Intelligence Platform

This project enforces strict automated testing across backend unit logic, API integration routes, and frontend browser automation.

---

## 1. Backend Pytest Suite

Run all unit and integration tests:
```powershell
# From project backend directory
cd backend
python -m pytest -v
```

Run test suite with coverage report:
```powershell
python -m pytest --cov=app --cov-report=term-missing
```

### Test Scope:
- `tests/unit/test_eligibility_engine.py`: Numerical boundaries, ECOG limits, biomarker match scoring.
- `tests/unit/test_site_risk_model.py`: Gradient Boosting / XGBoost model probability predictions and threshold classifications.
- `tests/unit/test_nl2sql.py`: SQL AST validation, injection attempts, schema allowlisting.
- `tests/unit/test_security_rbac.py`: Role hierarchies, JWT issuance, denial of unauthorized endpoints.
- `tests/integration/test_clinical_api.py`: FastAPI route testing using AsyncClient / TestClient.

---

## 2. Frontend Playwright E2E Tests

Run end-to-end browser tests:
```powershell
# From project frontend directory
cd frontend
npm run test:e2e # or npx playwright test
```

### Coverage:
- Visual presence of `"Synthetic / Demo Data Only"` banner.
- Patient selector and criterion verification matrix render test.
- Clinical review sign-off workflow.

---

## 3. Selenium Headless Cross-Browser Automation

Run cross-browser Selenium tests:
```powershell
python -m pytest tests/selenium/test_cross_browser_flow.py -v
```
Verifies OpenAPI Swagger documentation and authentication route guards under headless Chrome.
