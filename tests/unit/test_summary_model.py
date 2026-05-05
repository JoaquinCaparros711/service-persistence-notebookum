"""Unit tests for Summary model"""

import pytest
from app.models.document import HistorialDocumento
from app.models.user import User
from app.models.summary import Summary

@pytest.mark.unit
class TestSummaryModel:
    def test_summary_creation(self, session):
        user = User(email="sum_test@example.com", nombre="Sum Test User")
        session.add(user)
        session.commit()
        
        doc = HistorialDocumento(
            usuario_id=user.id,
            nombre_archivo="test.pdf",
            tamanio_bytes=1024,
            estado="completed"
        )
        session.add(doc)
        session.commit()
        
        summary = Summary(
            documento_id=doc.id,
            contenido="This is a summary",
            modelo_utilizado="gpt-4o",
            status="completed"
        )
        session.add(summary)
        session.commit()
        
        assert summary.id is not None
        assert summary.documento_id == doc.id
        assert summary.contenido == "This is a summary"
        assert summary.modelo_utilizado == "gpt-4o"
