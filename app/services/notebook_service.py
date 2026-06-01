from typing import Optional, List, Dict, Any
from app.repositories.notebook_repository import NotebookRepository
from app.schemas.notebook import notebook_schema, notebooks_schema


class NotebookService:
    def __init__(self) -> None:
        self.repository = NotebookRepository()

    def get_all(self, user_id: Optional[int] = None) -> List[Dict[str, Any]]:
        notebooks = (
            self.repository.get_by_user_id(user_id)
            if user_id is not None
            else self.repository.list_all()
        )
        return notebooks_schema.dump(notebooks)

    def create(self, data: Dict[str, Any]) -> Dict[str, Any]:
        new_notebook = notebook_schema.load(data, session=self.repository.session)
        self.repository.create(new_notebook)
        return notebook_schema.dump(new_notebook)

    def get_by_id(self, notebook_id: int) -> Optional[Dict[str, Any]]:
        notebook = self.repository.get_by_id(notebook_id)
        if not notebook:
            return None
        return notebook_schema.dump(notebook)

    def update(self, notebook_id: int, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        notebook = self.repository.get_by_id(notebook_id)
        if not notebook:
            return None

        notebook = notebook_schema.load(
            data, instance=notebook, partial=True, session=self.repository.session
        )
        self.repository.update(notebook)
        return notebook_schema.dump(notebook)

    def delete(self, notebook_id: int) -> bool:
        notebook = self.repository.get_by_id(notebook_id)
        if not notebook:
            return False
        self.repository.delete(notebook)
        return True
