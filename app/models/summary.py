"""Summary model for document summaries."""

from datetime import UTC, datetime
from sqlalchemy import ForeignKey
from app.database import db
import app.models.document  # Evita errores de mapper en SQLAlchemy


class Resumen(db.Model):
    """Represents a generated summary linked to a processed document."""

    __tablename__ = "resumenes"

    id = db.Column(db.Integer, primary_key=True)
    documento_id = db.Column(
        db.Integer,
        ForeignKey("historial_documentos.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    contenido = db.Column(db.Text, nullable=False)
    modelo_utilizado = db.Column(db.String(100), nullable=False, default="gpt-4o")
    created_at = db.Column(
        db.DateTime, nullable=False, default=lambda: datetime.now(UTC)
    )


Summary = Resumen
