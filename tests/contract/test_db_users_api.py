"""Contract tests for internal db users API"""

import pytest
from app.models.user import User


@pytest.mark.contract
class TestDBUsersAPI:
    def test_create_user_with_name(self, client, session):
        data = {"name": "Alice", "email": "alice@example.com"}
        response = client.post("/api/v1/db/users", json=data)
        assert response.status_code == 201

        resp_data = response.get_json()
        assert resp_data["name"] == "Alice"
        assert resp_data["email"] == "alice@example.com"
        assert "id" in resp_data



    def test_get_user(self, client, session):
        user = User(name="Charlie", email="charlie@example.com")
        session.add(user)
        session.commit()

        response = client.get(f"/api/v1/db/users/{user.id}")
        assert response.status_code == 200
        resp_data = response.get_json()
        assert resp_data["name"] == "Charlie"
        assert resp_data["email"] == "charlie@example.com"

    def test_patch_user(self, client, session):
        user = User(name="David", email="david@example.com")
        session.add(user)
        session.commit()

        response = client.patch(
            f"/api/v1/db/users/{user.id}", json={"name": "David Updated"}
        )
        assert response.status_code == 200
        assert response.get_json()["name"] == "David Updated"

    def test_delete_user(self, client, session):
        user = User(name="Eve", email="eve@example.com")
        session.add(user)
        session.commit()

        response = client.delete(f"/api/v1/db/users/{user.id}")
        assert response.status_code == 204

        # Verify deletion
        assert session.get(User, user.id) is None
