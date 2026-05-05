"""Unit tests for Document model"""

import pytest
from app.models.document import HistorialDocumento
from app.models.user import User

@pytest.mark.unit
class TestDocumentModel:
    def test_document_creation(self, session):
        user = User(email="doc_test@example.com", nombre="Doc Test User")
        session.add(user)
        session.commit()
        
        doc = HistorialDocumento(
            usuario_id=user.id,
            nombre_archivo="test.pdf",
            tamanio_bytes=1024,
            estado="pending"
        )
        session.add(doc)
        session.commit()
        
        assert doc.id is not None
        assert doc.usuario_id == user.id
        assert doc.estado == "pending"
        assert doc.nombre_archivo == "test.pdf"
        assert doc.tamanio_bytes == 1024
