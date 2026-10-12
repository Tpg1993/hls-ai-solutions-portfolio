# Testing Strategy & Execution Guide

## 1. Backend Testing with Pytest
All tests run inside the Python virtual environment (`.venv`):

```bash
# Activate virtual environment
.\.venv\Scripts\Activate.ps1   # Windows PowerShell
source .venv/bin/activate      # Linux / macOS

# Run all unit and integration tests
pytest -v

# Run with test coverage report
pytest -v --cov=backend/app --cov-report=term-missing
```

### Test Coverage Highlights:
- `test_ml_pipeline.py`: Verifies feature extraction, growth calculations, and calibrated probability bounds [0.0 - 1.0].
- `test_nba_rules.py`: Verifies priority tier and channel assignment rules.
- `test_nl2sql_guardrails.py`: Asserts AST validation blocking unauthorized SQL injections and write operations.
- `test_rbac.py`: Tests hierarchy permissions and unauthorized access rejections.
- `test_llm_router.py`: Mocks Sarvam failure, tests circuit breaker trip and OpenAI fallback.
- `test_api_endpoints.py`: Integration tests for FastAPI endpoints with auth tokens and response schemas.

## 2. Cross-Browser Automated Tests (Selenium)
```bash
pytest tests/selenium/ -v
```
Runs headless browser checks for route guards and API documentation availability.
