from app.models.summary import Summary
from app.repositories.base_repository import BaseRepository


class SummaryRepository(BaseRepository[Summary]):
    """Repository specific for Summary."""

    def __init__(self):
        super().__init__(Summary)

    def get_by_documento_id(self, documento_id: int):
        """Fetch all summaries for a specific document."""
        return self.list_all(documento_id=documento_id)
