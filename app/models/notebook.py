"""Notebook model for grouping documents."""

from datetime import UTC, datetime
from app.database import db

class Notebook(db.Model):
    """Represents a notebook that groups documents."""

    __tablename__ = "notebooks"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(
        db.DateTime, nullable=False, default=lambda: datetime.now(UTC)
    )

    user = db.relationship("User", backref=db.backref("notebooks", lazy=True))
