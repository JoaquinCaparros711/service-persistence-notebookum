"""Message model for chat history."""

from datetime import UTC, datetime
from app.database import db

class Message(db.Model):
    """Represents a single message in a conversation."""

    __tablename__ = "messages"

    id = db.Column(db.Integer, primary_key=True)
    conversation_id = db.Column(db.Integer, db.ForeignKey("conversations.id", ondelete="CASCADE"), nullable=False, index=True)
    role = db.Column(db.String(50), nullable=False) # 'user' or 'assistant'
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(
        db.DateTime, nullable=False, default=lambda: datetime.now(UTC)
    )

    conversation = db.relationship("Conversation", backref=db.backref("messages", lazy=True, cascade="all, delete-orphan"))
