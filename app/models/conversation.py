"""Conversation model for chat sessions."""

from datetime import UTC, datetime
from app.database import db

class Conversation(db.Model):
    """Represents a chat session within a notebook."""

    __tablename__ = "conversations"

    id = db.Column(db.Integer, primary_key=True)
    notebook_id = db.Column(db.Integer, db.ForeignKey("notebooks.id", ondelete="CASCADE"), nullable=False, index=True)
    title = db.Column(db.String(255), nullable=True)
    created_at = db.Column(
        db.DateTime, nullable=False, default=lambda: datetime.now(UTC)
    )

    notebook = db.relationship("Notebook", backref=db.backref("conversations", lazy=True, cascade="all, delete-orphan"))
