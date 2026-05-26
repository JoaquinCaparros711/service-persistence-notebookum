from app.models.document import HistorialDocumento
from app.repositories.base_repository import BaseRepository


class DocumentRepository(BaseRepository[HistorialDocumento]):
    """Repository specific for HistorialDocumento."""

    def __init__(self):
        super().__init__(HistorialDocumento)

    def get_by_user_id(self, user_id: int):
        """Fetch all documents belonging to a specific user."""
        return self.list_all(user_id=user_id)
