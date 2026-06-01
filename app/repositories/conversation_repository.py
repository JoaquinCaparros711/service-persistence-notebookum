from app.models.conversation import Conversation
from app.repositories.base_repository import BaseRepository

class ConversationRepository(BaseRepository[Conversation]):
    def __init__(self):
        super().__init__(Conversation)

    def get_by_notebook_id(self, notebook_id: int):
        return self.list_all(notebook_id=notebook_id)
