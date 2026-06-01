"""Document model for uploaded PDF metadata and processing state."""

from datetime import UTC, datetime
from app.database import db
import app.models.user  # Evita errores de mapper en SQLAlchemy


class HistorialDocumento(db.Model):
    """Represents an uploaded document."""

    __tablename__ = "historial_documentos"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    filename = db.Column(db.String(255), nullable=False)
    file_path = db.Column(db.String(512), nullable=False)
    job_id = db.Column(db.String(36), nullable=True, index=True)
    status = db.Column(db.String(20), nullable=False, default="PENDING", index=True)
    extracted_text = db.Column(db.Text, nullable=True)
    created_at = db.Column(
        db.DateTime, nullable=False, default=lambda: datetime.now(UTC)
    )

    user = db.relationship("User", backref=db.backref("documentos", lazy=True))

    resumenes = db.relationship(
        "Resumen",
        backref=db.backref("documento", lazy=True),
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
