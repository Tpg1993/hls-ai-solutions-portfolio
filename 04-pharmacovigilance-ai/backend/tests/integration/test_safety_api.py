import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.core.security import create_access_token

@pytest.fixture
def auth_headers_reviewer():
    token = create_access_token({"sub": "safety_reviewer", "role": "SAFETY_REVIEWER"})
    return {"Authorization": f"Bearer {token}"}

@pytest.fixture
def auth_headers_analyst():
    token = create_access_token({"sub": "analyst", "role": "ANALYST"})
    return {"Authorization": f"Bearer {token}"}

@pytest.fixture
def auth_headers_auditor():
    token = create_access_token({"sub": "auditor", "role": "AUDITOR"})
    return {"Authorization": f"Bearer {token}"}

@pytest.mark.asyncio
async def test_root_and_health():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        resp = await client.get("/")
        assert resp.status_code == 200
        assert "SYNTHETIC" in resp.json()["disclaimer"]

        live = await client.get("/health/live")
        assert live.status_code == 200
        assert live.json()["status"] == "alive"

@pytest.mark.asyncio
async def test_list_cases():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        resp = await client.get("/api/v1/cases?limit=5")
        assert resp.status_code == 200
        data = resp.json()
        assert len(data) > 0
        assert "case_id" in data[0]

@pytest.mark.asyncio
async def test_extract_case_endpoint(auth_headers_analyst):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        payload = {
            "narrative": "55yo male given CardioShield 50mg, admitted with acute hepatitis.",
            "suspect_drug": "CardioShield",
            "adverse_event": "Acute Hepatitis"
        }
        resp = await client.post("/api/v1/cases/extract", json=payload, headers=auth_headers_analyst)
        assert resp.status_code == 200
        data = resp.json()
        assert data["suspect_drug"] == "CardioShield"
        assert data["adverse_event"] == "Acute Hepatitis"

@pytest.mark.asyncio
async def test_list_signals_and_evidence():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        resp = await client.get("/api/v1/signals")
        assert resp.status_code == 200
        signals = resp.json()
        assert len(signals) > 0
        sig_id = signals[0]["id"]

        ev_resp = await client.get(f"/api/v1/signals/{sig_id}/evidence")
        assert ev_resp.status_code == 200

@pytest.mark.asyncio
async def test_safety_review_submission(auth_headers_reviewer):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        review_data = {
            "signal_id": 1,
            "decision": "ESCALATE_LABEL_UPDATE",
            "comments": "Confirmed elevated PRR and PubMed literature evidence; escalating to safety committee."
        }
        resp = await client.post("/api/v1/reviews", json=review_data, headers=auth_headers_reviewer)
        assert resp.status_code == 200
        data = resp.json()
        assert data["decision"] == "ESCALATE_LABEL_UPDATE"

@pytest.mark.asyncio
async def test_audit_trail_endpoint(auth_headers_auditor):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        resp = await client.get("/api/v1/reviews/audit", headers=auth_headers_auditor)
        assert resp.status_code == 200
        events = resp.json()
        assert len(events) > 0
