"""Unit tests for Summary model"""

import pytest
from app.models.document import HistorialDocumento
from app.models.summary import Summary


@pytest.mark.unit
class TestSummaryModel:
    def test_summary_creation(self, session):
        doc = HistorialDocumento(
            user_id=1, filename="test.pdf", file_path="/tmp/test.pdf"
        )
        session.add(doc)
        session.commit()

        summary = Summary(
            documento_id=doc.id,
            contenido="This is a summary",
            modelo_utilizado="gpt-4o",
        )
        session.add(summary)
        session.commit()

        assert summary.id is not None
        assert summary.documento_id == doc.id
        assert summary.contenido == "This is a summary"
        assert summary.modelo_utilizado == "gpt-4o"
