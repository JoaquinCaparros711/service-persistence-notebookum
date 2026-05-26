from typing import Optional, List, Dict, Any
from app.repositories.summary_repository import SummaryRepository
from app.repositories.document_repository import DocumentRepository
from app.schemas.summary import summary_schema, summaries_schema


class SummaryService:
    def __init__(self) -> None:
        self.repository = SummaryRepository()
        self.document_repository = DocumentRepository()

    def get_all(self, documento_id: Optional[int] = None) -> List[Dict[str, Any]]:
        summaries = (
            self.repository.get_by_documento_id(documento_id)
            if documento_id is not None
            else self.repository.list_all()
        )
        return summaries_schema.dump(summaries)

    def create(self, data: Dict[str, Any]) -> Dict[str, Any]:
        documento_id = data.get("documento_id")
        if not documento_id:
            raise ValueError("documento_id is required")

        doc = self.document_repository.get_by_id(int(documento_id))
        if not doc:
            raise ValueError("Document not found")

        new_summary = summary_schema.load(data, session=self.repository.session)
        self.repository.create(new_summary)
        return summary_schema.dump(new_summary)

    def get_by_id(self, summary_id: int) -> Optional[Dict[str, Any]]:
        summary = self.repository.get_by_id(summary_id)
        if not summary:
            return None
        return summary_schema.dump(summary)

    def update(self, summary_id: int, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        summary = self.repository.get_by_id(summary_id)
        if not summary:
            return None
        summary = summary_schema.load(
            data, instance=summary, partial=True, session=self.repository.session
        )
        self.repository.update(summary)
        return summary_schema.dump(summary)

    def delete(self, summary_id: int) -> bool:
        summary = self.repository.get_by_id(summary_id)
        if not summary:
            return False
        self.repository.delete(summary)
        return True
