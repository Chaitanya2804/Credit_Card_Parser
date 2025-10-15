"""
API endpoint tests
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health_check():
    """Test root health check endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
    assert "service" in response.json()


def test_upload_without_file():
    """Test upload endpoint without file"""
    response = client.post("/upload")
    assert response.status_code == 422  # Validation error


def test_upload_invalid_file_type():
    """Test upload with non-PDF file"""
    files = {"file": ("test.txt", b"test content", "text/plain")}
    response = client.post("/upload", files=files)
    assert response.status_code == 400
    assert "PDF" in response.json()["detail"]


def test_get_nonexistent_result():
    """Test getting result that doesn't exist"""
    response = client.get("/results/nonexistent-id")
    assert response.status_code == 404


def test_get_history():
    """Test history endpoint"""
    response = client.get("/history")
    assert response.status_code == 200
    assert isinstance(response.json(), list)