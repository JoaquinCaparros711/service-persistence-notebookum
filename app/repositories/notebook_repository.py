from app.models.notebook import Notebook
from app.repositories.base_repository import BaseRepository


class NotebookRepository(BaseRepository[Notebook]):
    """Repository specific for Notebook."""

    def __init__(self):
        super().__init__(Notebook)

    def get_by_user_id(self, user_id: int):
        """Fetch all notebooks belonging to a specific user."""
        return self.list_all(user_id=user_id)
