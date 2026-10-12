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
async def test_guidances_listing():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        res = await client.get("/api/guidances")
        assert res.status_code == 200
        docs = res.json()
        assert len(docs) >= 3
        assert any(d["authority"] == "FDA" for d in docs)

@pytest.mark.asyncio
async def test_cross_version_diff():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        res = await client.get("/api/diff/compare?baseline_id=DOC-FDA-RWE-2021&comparison_id=DOC-FDA-RWE-2024")
        assert res.status_code == 200
        data = res.json()
        assert "changes" in data
        assert data["total_changes"] >= 1

@pytest.mark.asyncio
async def test_submission_impacts():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        res = await client.get("/api/impacts")
        assert res.status_code == 200
        impacts = res.json()
        assert len(impacts) >= 1
        assert any("OncoVax-7" in i["product_name"] for i in impacts)
