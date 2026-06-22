from typing import Any, Dict, List, Optional

from werkzeug.utils import secure_filename

from app.repositories.document_repository import DocumentRepository
from app.schemas.document import document_schema, documents_schema


class DocumentService:
    def __init__(self) -> None:
        self.repository = DocumentRepository()

    def get_all(self, user_id: Optional[int] = None) -> List[Dict[str, Any]]:
        docs = (
            self.repository.get_by_user_id(user_id)
            if user_id is not None
            else self.repository.list_all()
        )
        return documents_schema.dump(docs)

    def create(self, data: Dict[str, Any]) -> Dict[str, Any]:
        if "filename" in data and isinstance(data["filename"], str):
            data["filename"] = secure_filename(data["filename"])

        new_doc = document_schema.load(data, session=self.repository.session)
        self.repository.create(new_doc)
        return document_schema.dump(new_doc)

    def get_by_id(self, doc_id: int) -> Optional[Dict[str, Any]]:
        doc = self.repository.get_by_id(doc_id)
        if not doc:
            return None
        return document_schema.dump(doc)

    def update(self, doc_id: int, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        doc = self.repository.get_by_id(doc_id)
        if not doc:
            return None

        if "filename" in data and isinstance(data["filename"], str):
            data["filename"] = secure_filename(data["filename"])

        doc = document_schema.load(
            data, instance=doc, partial=True, session=self.repository.session
        )
        self.repository.update(doc)
        return document_schema.dump(doc)

    def delete(self, doc_id: int) -> bool:
        doc = self.repository.get_by_id(doc_id)
        if not doc:
            return False
        self.repository.delete(doc)
        return True
