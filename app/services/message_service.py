from typing import Any, Dict, List, Optional

from app.repositories.message_repository import MessageRepository
from app.schemas.message import message_schema, messages_schema

class MessageService:
    def __init__(self) -> None:
        self.repository = MessageRepository()

    def get_all(self, conversation_id: Optional[int] = None) -> List[Dict[str, Any]]:
        msgs = self.repository.get_by_conversation_id(conversation_id) if conversation_id else self.repository.list_all()
        return messages_schema.dump(msgs)

    def create(self, data: Dict[str, Any]) -> Dict[str, Any]:
        new_msg = message_schema.load(data, session=self.repository.session)
        self.repository.create(new_msg)
        return message_schema.dump(new_msg)

    def get_by_id(self, msg_id: int) -> Optional[Dict[str, Any]]:
        msg = self.repository.get_by_id(msg_id)
        return message_schema.dump(msg) if msg else None
