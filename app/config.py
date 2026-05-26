import os


class Config:
    """Base configuration."""

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ALLOWED_ORIGINS = os.environ.get("ALLOWED_ORIGINS", "http://localhost:3000").split(
        ","
    )


class DevelopmentConfig(Config):
    """Development configuration."""

    DEBUG = True

    def __init__(self):
        db_user = os.environ.get("DB_USER", "notebookum_user")
        db_pass = os.environ.get("DB_PASSWORD", "notebookum_password")
        db_name = os.environ.get("DB_NAME", "notebookum_db")
        db_host = os.environ.get("DB_WRITE_HOST", "mysql-primary")
        self.SQLALCHEMY_DATABASE_URI = (
            f"mysql+mysqlconnector://{db_user}:{db_pass}@{db_host}/{db_name}"
        )

        read_host = os.environ.get("DB_READ_HOST", "mysql-replica")
        self.SQLALCHEMY_BINDS = {
            "read_replica": f"mysql+mysqlconnector://{db_user}:{db_pass}@{read_host}/{db_name}"
        }


class ProductionConfig(Config):
    """Production configuration."""

    DEBUG = False

    def __init__(self):
        db_user = os.environ.get("DB_USER")
        db_pass = os.environ.get("DB_PASSWORD")
        db_name = os.environ.get("DB_NAME")

        # Validacion estricta de variables de entorno (Fail-Fast)
        if not all([db_user, db_pass, db_name]):
            raise ValueError(
                "CRITICAL: Missing DB_USER, DB_PASSWORD, or DB_NAME in environment variables!"
            )

        db_host = os.environ.get("DB_WRITE_HOST", "mysql-primary")
        self.SQLALCHEMY_DATABASE_URI = (
            f"mysql+mysqlconnector://{db_user}:{db_pass}@{db_host}/{db_name}"
        )

        read_host = os.environ.get("DB_READ_HOST", "mysql-replica")
        self.SQLALCHEMY_BINDS = {
            "read_replica": f"mysql+mysqlconnector://{db_user}:{db_pass}@{read_host}/{db_name}"
        }


class TestingConfig(Config):
    """Testing configuration."""

    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    SQLALCHEMY_BINDS = {}


def get_config():
    env_name = os.environ.get("FLASK_ENV", "development")
    if env_name == "production":
        return ProductionConfig()
    elif env_name == "testing":
        return TestingConfig()
    return DevelopmentConfig()
