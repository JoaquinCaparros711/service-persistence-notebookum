from typing import Optional, List, Dict, Any
from app.repositories.conversation_repository import ConversationRepository
from app.schemas.conversation import conversation_schema, conversations_schema

class ConversationService:
    def __init__(self) -> None:
        self.repository = ConversationRepository()

    def get_all(self, notebook_id: Optional[int] = None) -> List[Dict[str, Any]]:
        convs = self.repository.get_by_notebook_id(notebook_id) if notebook_id else self.repository.list_all()
        return conversations_schema.dump(convs)

    def create(self, data: Dict[str, Any]) -> Dict[str, Any]:
        new_conv = conversation_schema.load(data, session=self.repository.session)
        self.repository.create(new_conv)
        return conversation_schema.dump(new_conv)

    def get_by_id(self, conv_id: int) -> Optional[Dict[str, Any]]:
        conv = self.repository.get_by_id(conv_id)
        return conversation_schema.dump(conv) if conv else None

    def delete(self, conv_id: int) -> bool:
        conv = self.repository.get_by_id(conv_id)
        if not conv: return False
        self.repository.delete(conv)
        return True
