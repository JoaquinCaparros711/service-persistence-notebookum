"""Pytest configuration and common fixtures."""

import os
import pytest
from app import create_app
from app.database import db


@pytest.fixture
def app():
    """Create and configure a test application instance"""
    # Forzamos TestingConfig a traves de FLASK_ENV
    os.environ["FLASK_ENV"] = "testing"
    app = create_app()

    with app.app_context():
        # Limpiamos e inicializamos tablas antes de cada test para aislar la data
        db.drop_all()
        db.create_all()

        yield app

        # Cleanup posterior al test
        db.session.remove()
        db.drop_all()
        db.engine.dispose()  # Fix: Cierra la conexion para evitar el ResourceWarning en SQLite


@pytest.fixture
def client(app):
    """Create a test client for the app"""
    return app.test_client()


@pytest.fixture
def session(app):
    """Create a database session for tests"""
    with app.app_context():
        yield db.session
