"""Contract tests for internal db summaries API"""

import pytest
from app.models.document import HistorialDocumento
from app.models.summary import Summary


@pytest.mark.contract
class TestDBSummariesAPI:
    def test_create_summary(self, client, session):
        doc = HistorialDocumento(user_id=1, filename="test.pdf", file_path="/test.pdf")
        session.add(doc)
        session.commit()

        data = {
            "documento_id": doc.id,
            "contenido": "Summarized content",
            "modelo_utilizado": "gpt-4",
        }
        response = client.post("/api/v1/db/summaries", json=data)
        assert response.status_code == 201
        assert response.get_json()["contenido"] == "Summarized content"

    def test_get_summary(self, client, session):
        doc = HistorialDocumento(user_id=1, filename="get.pdf", file_path="/get.pdf")
        session.add(doc)
        session.commit()

        summary = Summary(
            documento_id=doc.id, contenido="text", modelo_utilizado="gpt-3"
        )
        session.add(summary)
        session.commit()

        response = client.get(f"/api/v1/db/summaries/{summary.id}")
        assert response.status_code == 200
