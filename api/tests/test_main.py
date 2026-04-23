import pytest
from fastapi.testclient import TestClient
from main import app, r

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_create_job(mocker):
    # Mock Redis lpush and hset
    mock_lpush = mocker.patch.object(r, 'lpush', return_value=1)
    mock_hset = mocker.patch.object(r, 'hset', return_value=1)

    response = client.post("/jobs", json={"title": "Test Job"})
    
    assert response.status_code == 200
    data = response.json()
    assert "job_id" in data
    assert mock_lpush.called
    assert mock_hset.called

def test_get_job(mocker):
    # Mock Redis hgetall
    job_id = "test-uuid"
    mock_data = {
        "status": "completed",
        "title": "Test Job"
    }
    mocker.patch.object(r, 'hgetall', return_value=mock_data)

    response = client.get(f"/jobs/{job_id}")
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "completed"
    assert data["title"] == "Test Job"

def test_get_nonexistent_job(mocker):
    mocker.patch.object(r, 'hgetall', return_value={})
    response = client.get("/jobs/nonexistent")
    assert response.status_code == 404
