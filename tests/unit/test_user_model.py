"""Unit tests for database models."""

import pytest
from datetime import datetime
from app.models.user import User

@pytest.mark.unit
class TestUserModel:
    """Unit tests for User model"""

    def test_user_creation(self, session):
        """Test successful user model creation"""
        email = "model_test@example.com"
        nombre = "Model Test User"
        user = User(email=email, nombre=nombre)
        session.add(user)
        session.commit()

        assert user.id is not None
        assert user.email == email
        assert user.nombre == nombre
        assert user.created_at is not None
        assert user.updated_at is not None

    def test_user_email_uniqueness(self, session):
        """Test that email uniqueness constraint is enforced"""
        email = "unique@example.com"
        user1 = User(email=email, nombre="First User")
        session.add(user1)
        session.commit()

        user2 = User(email=email, nombre="Second User")
        session.add(user2)

        with pytest.raises(Exception):
            session.commit()

    def test_user_to_dict(self, session):
        """Test that to_dict method returns correct dictionary representation"""
        user = User(email="dict_test@example.com", nombre="Dict Test User")
        session.add(user)
        session.commit()

        user_dict = user.to_dict()
        assert "id" in user_dict
        assert user_dict["email"] == "dict_test@example.com"
        assert user_dict["nombre"] == "Dict Test User"
        assert "created_at" in user_dict
