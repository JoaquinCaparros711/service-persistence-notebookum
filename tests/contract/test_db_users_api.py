"""Contract tests for internal db users API"""

import pytest
from app.models.user import User

@pytest.mark.contract
class TestDBUsersAPI:
    def test_create_user(self, client):
        data = {"email": "test@example.com", "nombre": "Test User"}
        response = client.post("/api/v1/db/users", json=data)
        assert response.status_code == 201
        
        resp_data = response.get_json()
        assert resp_data["email"] == "test@example.com"
        assert resp_data["nombre"] == "Test User"
        
    def test_create_user_duplicate(self, client, session):
        # Create existing user
        user = User(email="duplicate@example.com", nombre="Existing")
        session.add(user)
        session.commit()
        
        data = {"email": "duplicate@example.com", "nombre": "Test User"}
        response = client.post("/api/v1/db/users", json=data)
        assert response.status_code == 409
        
    def test_get_user(self, client, session):
        user = User(email="get@example.com", nombre="Get User")
        session.add(user)
        session.commit()
        
        response = client.get(f"/api/v1/db/users/{user.id}")
        assert response.status_code == 200
        
        resp_data = response.get_json()
        assert resp_data["email"] == "get@example.com"
        assert resp_data["nombre"] == "Get User"
        
    def test_get_user_not_found(self, client):
        response = client.get("/api/v1/db/users/999")
        assert response.status_code == 404
