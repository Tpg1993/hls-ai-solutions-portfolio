# Testing Guide: Regulatory Intelligence Copilot

## 1. Backend Pytest Suite

Run unit and integration tests:
```powershell
cd backend
python -m pytest -v
```

With coverage reporting:
```powershell
python -m pytest --cov=app --cov-report=term-missing
```

### Coverage Scope:
- `tests/unit/test_nl2sql.py`: Safe SQL AST parsing, read-only constraints, and injection blocking.
- `tests/unit/test_security_rbac.py`: Role hierarchies, JWT token verification, and permission enforcement.
- `tests/integration/test_api_endpoints.py`: FastAPI route integration tests.

---

## 2. Frontend Playwright E2E Tests

Run end-to-end browser specifications:
```powershell
cd frontend
npm run test:e2e # or npx playwright test
```

Verifies disclaimer banners, guidance search, cross-version diff inspection, and impact matrix workflows.

---

## 3. Selenium Headless Automation

```powershell
python -m pytest tests/selenium/test_cross_browser_flow.py -v
```
Verifies OpenAPI Swagger documentation and Next.js portal DOM rendering under headless Chrome.
