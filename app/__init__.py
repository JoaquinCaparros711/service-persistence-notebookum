from flask import Flask
from .database import db
import os

def create_app(test_config=None):
    app = Flask(__name__)
    
    if test_config:
        app.config.update(test_config)
    else:
        # Configuracion de BD
        db_host = os.environ.get("DB_WRITE_HOST", "mysql")
        db_user = os.environ.get("DB_USER", "notebookum_user")
        db_pass = os.environ.get("DB_PASS", "notebookum_password")
        db_name = os.environ.get("DB_NAME", "notebookum_db")
        
        app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql+mysqlconnector://{db_user}:{db_pass}@{db_host}/{db_name}"
        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    
    db.init_app(app)
    
    from .routes.db_users import db_users_bp
    from .routes.db_documents import db_documents_bp
    from .routes.db_summaries import db_summaries_bp
    
    app.register_blueprint(db_users_bp)
    app.register_blueprint(db_documents_bp)
    app.register_blueprint(db_summaries_bp)
    
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
