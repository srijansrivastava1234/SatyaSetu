import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import init_db

@pytest.fixture(scope="session", autouse=True)
def setup_database():
    init_db()

@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client

def test_health_check(client):
    """Ensure the health endpoint returns 200 and operational status."""
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data.get("status") == "healthy"
    assert "version" in data

def test_scenarios_endpoint(client):
    """Ensure scenario catalog returns valid pre-configured test scenarios."""
    response = client.get("/api/scenarios")
    assert response.status_code == 200
    data = response.json()
    assert "scenarios" in data
    assert isinstance(data["scenarios"], list)
    assert len(data["scenarios"]) > 0
    first = data["scenarios"][0]
    assert "id" in first
    assert "category" in first
    assert "expected_verdict" in first

def test_system_stats_endpoint(client):
    """Verify system telemetry returns metrics from the SQLite database."""
    response = client.get("/api/stats")
    assert response.status_code == 200
    stats = response.json()
    assert "total_verifications_logged" in stats
    assert "cached_unique_claims" in stats
    assert "cache_savings_hits" in stats
    assert "database_backend" in stats
    assert "SQLite" in stats["database_backend"]

def test_recent_history_endpoint(client):
    """Verify query history endpoint returns list of logged verifications."""
    response = client.get("/api/history?limit=5")
    assert response.status_code == 200
    data = response.json()
    assert "history" in data
    assert isinstance(data["history"], list)

def test_verify_claim_and_caching(client):
    """Verify that a claim is processed, logged to SQLite, and hits cache on repeat."""
    test_claim = "UNESCO has declared the Indian National Anthem as the best anthem in the world."
    payload = {
        "text": test_claim,
        "language": "en"
    }

    # First call: executes pipeline and writes to SQLite cache
    res1 = client.post("/api/verify", json=payload)
    assert res1.status_code == 200
    data1 = res1.json()
    assert "overall_verdict" in data1
    assert "credibility_score" in data1
    assert "manipulation_breakdown" in data1
    assert "certified_evidence" in data1
    assert data1["overall_verdict"] in ["TRUE", "FALSE", "MISLEADING", "FABRICATED", "ALTERED", "VERIFIED", "UNVERIFIED"]

    # Second call: must hit SQLite cache
    res2 = client.post("/api/verify", json=payload)
    assert res2.status_code == 200
    data2 = res2.json()
    assert data2.get("is_cached") is True
    assert data2["overall_verdict"] == data1["overall_verdict"]

def test_verify_empty_payload_validation(client):
    """Verify that missing/empty inputs fail with 400 Bad Request."""
    response = client.post("/api/verify", json={"text": ""})
    assert response.status_code == 400
