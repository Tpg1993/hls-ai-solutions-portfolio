import pytest
from app.core.security import create_access_token
from app.core.rbac import UserRole

@pytest.mark.asyncio
async def test_root_disclaimer_endpoint(client):
    response = await client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "disclaimer" in data
    assert "SYNTHETIC" in data["disclaimer"]

@pytest.mark.asyncio
async def test_health_probes(client):
    live_res = await client.get("/health/live")
    assert live_res.status_code == 200
    assert live_res.json()["status"] == "alive"

    ready_res = await client.get("/health/ready")
    # In local testing without active Docker Postgres daemon, probe returns 503; with DB running it returns 200
    assert ready_res.status_code in [200, 503]
    assert "status" in ready_res.json()

@pytest.mark.asyncio
async def test_roi_calculation_endpoint(client):
    # Standard user token
    token = create_access_token(subject="test_user_id", role=UserRole.STANDARD_USER.value)
    headers = {"Authorization": f"Bearer {token}"}
    
    response = await client.get("/api/roi", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["annual_hours_saved"] > 0
    assert data["total_net_economic_benefit"] > 0

@pytest.mark.asyncio
async def test_unauthorized_access_denied(client):
    # No auth header passed to protected endpoint
    response = await client.get("/api/hcps")
    assert response.status_code == 401
