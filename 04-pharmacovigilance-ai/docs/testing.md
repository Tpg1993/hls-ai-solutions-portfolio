# Testing Guide: Pharmacovigilance AI

## 1. Pytest Backend Suite

Run unit and integration tests:
```powershell
cd backend
python -m pytest -v
```

With coverage analysis:
```powershell
python -m pytest --cov=app --cov-report=term-missing
```

### Coverage Breakdown:
- `tests/unit/test_disproportionality.py`: PRR/ROR math, Evans criteria, Yates continuity correction, zero division resilience.
- `tests/unit/test_case_extraction.py`: PII/PHI redaction patterns and MedDRA entity mapping.
- `tests/unit/test_security_rbac.py`: Role hierarchies, JWT token verification, and permission barriers.
- `tests/unit/test_nl2sql.py`: AST parsing, keyword blacklisting, and SQL injection defense.
- `tests/integration/test_safety_api.py`: FastAPI route integration tests.

---

## 2. Frontend Playwright E2E Tests

Run end-to-end browser specifications:
```powershell
cd frontend
npm run test:e2e # or npx playwright test
```

Verifies disclaimer banners, signal table navigation, spontaneous case intake, and reviewer sign-off gate.

---

## 3. Selenium Headless Automation

```powershell
python -m pytest tests/selenium/test_cross_browser_flow.py -v
```
Verifies FastAPI OpenAPI Swagger endpoints and Next.js portal DOM rendering under headless Chrome.
