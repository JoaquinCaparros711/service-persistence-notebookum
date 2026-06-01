"""Unit tests for UserService"""

import pytest
from unittest.mock import MagicMock
from app.services.user_service import UserService
from app.models.user import User
from marshmallow import ValidationError


@pytest.fixture
def mock_user_repo(mocker):
    return mocker.patch("app.services.user_service.UserRepository")


@pytest.fixture
def user_service(mock_user_repo):
    return UserService()


@pytest.mark.unit
class TestUserService:
    def test_get_all(self, user_service, mock_user_repo):
        repo_mock = mock_user_repo.return_value
        repo_mock.list_all.return_value = [
            User(id=1, name="Alice", email="alice@example.com"),
            User(id=2, name="Bob", email="bob@example.com"),
        ]

        result = user_service.get_all()

        repo_mock.list_all.assert_called_once()
        assert len(result) == 2
        assert result[0]["name"] == "Alice"
        assert result[1]["email"] == "bob@example.com"

    def test_create_success_with_name(self, user_service, mock_user_repo, app):
        repo_mock = mock_user_repo.return_value
        repo_mock.get_by_email.return_value = None
        repo_mock.session = MagicMock()

        data = {"name": "Charlie", "email": "charlie@example.com"}

        with app.app_context():
            result = user_service.create(data)

        repo_mock.create.assert_called_once()
        assert result["name"] == "Charlie"
        assert result["email"] == "charlie@example.com"



    def test_create_email_in_use(self, user_service, mock_user_repo):
        repo_mock = mock_user_repo.return_value
        repo_mock.get_by_email.return_value = User(id=1, name="Alice", email="alice@example.com")

        data = {"name": "Charlie", "email": "alice@example.com"}

        with pytest.raises(ValueError, match="Email already in use"):
            user_service.create(data)

    def test_get_by_id_found(self, user_service, mock_user_repo):
        repo_mock = mock_user_repo.return_value
        repo_mock.get_by_id.return_value = User(id=10, name="Alice", email="alice@example.com")

        result = user_service.get_by_id(10)

        assert result is not None
        assert result["id"] == 10
        assert result["name"] == "Alice"

    def test_get_by_id_not_found(self, user_service, mock_user_repo):
        repo_mock = mock_user_repo.return_value
        repo_mock.get_by_id.return_value = None

        assert user_service.get_by_id(999) is None

    def test_update_success(self, user_service, mock_user_repo, app):
        repo_mock = mock_user_repo.return_value
        user_instance = User(id=1, name="Old Name", email="old@example.com")
        repo_mock.get_by_id.return_value = user_instance
        repo_mock.session = MagicMock()

        data = {"name": "New Name"}

        with app.app_context():
            result = user_service.update(1, data)

        repo_mock.update.assert_called_once()
        assert result["name"] == "New Name"

    def test_update_email_in_use(self, user_service, mock_user_repo, app):
        repo_mock = mock_user_repo.return_value
        user_instance = User(id=1, name="Alice", email="alice@example.com")
        repo_mock.get_by_id.return_value = user_instance
        repo_mock.get_by_email.return_value = User(id=2, name="Bob", email="bob@example.com")

        data = {"email": "bob@example.com"}

        with app.app_context():
            with pytest.raises(ValueError, match="Email already in use"):
                user_service.update(1, data)

    def test_delete_success(self, user_service, mock_user_repo):
        repo_mock = mock_user_repo.return_value
        repo_mock.get_by_id.return_value = User(id=1)

        result = user_service.delete(1)

        repo_mock.delete.assert_called_once()
        assert result is True

    def test_delete_not_found(self, user_service, mock_user_repo):
        repo_mock = mock_user_repo.return_value
        repo_mock.get_by_id.return_value = None

        result = user_service.delete(999)

        repo_mock.delete.assert_not_called()
        assert result is False
