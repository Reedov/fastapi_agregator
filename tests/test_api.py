from fastapi.testclient import TestClient
from app import app

client = TestClient(app)


def test_get_sources():
    response = client.get('/sources/')
    assert response.status_code == 200


