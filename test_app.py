from fastapi.testclient import TestClient
from main import app
from database import engine, Base

Base.metadata.create_all(bind=engine)
client = TestClient(app)

def test_auth_flow():
    response = client.post("/register", json={"username": "testuser", "password": "testpass123"})
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "testuser"
    assert "id" in data

    response = client.post("/login", json={"username": "testuser", "password": "testpass123"})
    assert response.status_code == 200
    token = response.json()["access_token"]
    assert token is not None

    response = client.get("/users/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["username"] == "testuser"

    response = client.get("/users/me")
    assert response.status_code == 401