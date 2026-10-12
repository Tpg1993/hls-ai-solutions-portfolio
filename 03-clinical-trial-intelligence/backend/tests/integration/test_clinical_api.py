import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.data.seed import seed_database

@pytest_asyncio.fixture(scope="module", autouse=True)
async def init_db():
    await seed_database()

@pytest.mark.asyncio
async def test_health_endpoints():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        res = await client.get("/health/live")
        assert res.status_code == 200
        assert res.json()["status"] == "ok"

@pytest.mark.asyncio
async def test_trials_list():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        res = await client.get("/api/trials")
        assert res.status_code == 200
        trials = res.json()
        assert len(trials) >= 2
        assert any("NCT04488081" in t["nct_id"] for t in trials)

@pytest.mark.asyncio
async def test_patients_list():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        res = await client.get("/api/patients")
        assert res.status_code == 200
        patients = res.json()
        assert len(patients) >= 3

@pytest.mark.asyncio
async def test_sites_risk_metrics():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        res = await client.get("/api/sites")
        assert res.status_code == 200
        sites = res.json()
        assert len(sites) >= 4
        # Verify ML predictions present
        assert any(s["metric"]["predicted_risk"] in ["High", "Medium", "Low"] for s in sites if s["metric"])

@pytest.mark.asyncio
async def test_matching_list():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        res = await client.get("/api/matching")
        assert res.status_code == 200
        matches = res.json()
        assert len(matches) >= 3
