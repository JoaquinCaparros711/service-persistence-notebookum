"""Unit tests for Document model"""

import pytest
from app.models.document import HistorialDocumento


@pytest.mark.unit
class TestDocumentModel:
    def test_document_creation(self, session):
        doc = HistorialDocumento(
            user_id=1, filename="test.pdf", file_path="/tmp/test.pdf"
        )
        session.add(doc)
        session.commit()

        assert doc.id is not None
        assert doc.user_id == 1
        assert doc.filename == "test.pdf"
        assert doc.file_path == "/tmp/test.pdf"
