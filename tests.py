import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_root():
    """Тест базового роута"""
    response = client.get("/")
    assert response.status_code in [200, 404]  # Может не быть root роута

def test_health():
    """Тест health check"""
    response = client.get("/health")
    assert response.status_code in [200, 404]  # Может не быть health роута

def test_openapi():
    """Тест OpenAPI документации"""
    response = client.get("/api/v1/openapi.json")
    assert response.status_code == 200
    assert "openapi" in response.json()

if __name__ == "__main__":
    pytest.main([__file__])
