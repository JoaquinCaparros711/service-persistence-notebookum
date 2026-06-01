from flask import Flask, jsonify
from flask_cors import CORS
from flask_talisman import Talisman
from .database import db
import os
from werkzeug.exceptions import HTTPException
from sqlalchemy.exc import SQLAlchemyError
from marshmallow import ValidationError
from app.config import get_config


def create_app(test_config=None):
    app = Flask(__name__)

    # Load Configuration
    app_config = get_config()
    app.config.from_object(app_config)

    if test_config:
        app.config.update(test_config)

    # 1. CORS Configuration
    CORS(app, origins=app.config.get("ALLOWED_ORIGINS", ["*"]))

    # 2. Security Headers (Talisman)
    force_https = os.environ.get("FLASK_ENV") == "production"
    Talisman(
        app,
        force_https=force_https,
        strict_transport_security=True,
        strict_transport_security_max_age=31536000,  # 1 year
        content_security_policy=None,  # Allow APIs
        session_cookie_secure=force_https,
        session_cookie_http_only=True,
    )

    db.init_app(app)

    # Preload models to populate SQLAlchemy registry before Marshmallow schemas introspect them
    from app.models.user import User
    from app.models.notebook import Notebook
    from app.models.document import HistorialDocumento
    from app.models.summary import Summary

    from app.schemas import ma

    ma.init_app(app)

    from .routes.db_documents import db_documents_bp
    from .routes.db_notebooks import db_notebooks_bp
    from .routes.db_summaries import db_summaries_bp
    from .routes.db_users import db_users_bp

    app.register_blueprint(db_documents_bp)
    app.register_blueprint(db_notebooks_bp)
    app.register_blueprint(db_summaries_bp)
    app.register_blueprint(db_users_bp)

    # Manejadores de Errores Estandarizados (RFC 9457)
    @app.errorhandler(ValidationError)
    def handle_validation_error(err):
        return (
            jsonify(
                {
                    "type": "validation_error",
                    "title": "Invalid data",
                    "status": 400,
                    "detail": err.messages,
                }
            ),
            400,
        )

    @app.errorhandler(HTTPException)
    def handle_http_exception(err):
        return (
            jsonify(
                {
                    "type": "http_error",
                    "title": err.name,
                    "status": err.code,
                    "detail": err.description,
                }
            ),
            err.code,
        )

    @app.errorhandler(SQLAlchemyError)
    def handle_sqlalchemy_error(err):
        return (
            jsonify(
                {
                    "type": "database_error",
                    "title": "Database operation failed",
                    "status": 500,
                    "detail": str(err),
                }
            ),
            500,
        )

    @app.errorhandler(Exception)
    def handle_generic_exception(err):
        return (
            jsonify(
                {
                    "type": "internal_error",
                    "title": "Internal Server Error",
                    "status": 500,
                    "detail": str(err),
                }
            ),
            500,
        )

    @app.route("/health")
    def health_check():
        try:
            from sqlalchemy import text

            db.session.execute(text("SELECT 1"))
            db_status = "connected"
        except Exception as e:
            db_status = f"error: {str(e)}"

        return {"status": "ok", "service": "persistence", "db": db_status}, 200

    return app
