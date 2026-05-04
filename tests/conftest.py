"""Pytest configuration and common fixtures."""

import pytest
from app import create_app
from app.database import db

@pytest.fixture
def app():
    """Create and configure a test application instance"""
    import os
    os.environ["DB_WRITE_HOST"] = "localhost" # mock
    app = create_app({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
    })

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    """Create a test client for the app"""
    return app.test_client()

@pytest.fixture
def session(app):
    """Create a database session for tests"""
    with app.app_context():
        yield db.session
