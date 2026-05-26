"""Contract tests for internal db documents API"""

import pytest
from app.models.document import HistorialDocumento


@pytest.mark.contract
class TestDBDocumentsAPI:
    def test_create_document(self, client, session):
        data = {"user_id": 1, "filename": "test.pdf", "file_path": "/tmp/test.pdf"}
        response = client.post("/api/v1/db/documents", json=data)
        assert response.status_code == 201

        resp_data = response.get_json()
        assert resp_data["filename"] == "test.pdf"
        assert resp_data["user_id"] == 1

    def test_get_document(self, client, session):
        doc = HistorialDocumento(user_id=1, filename="get.pdf", file_path="/get.pdf")
        session.add(doc)
        session.commit()

        response = client.get(f"/api/v1/db/documents/{doc.id}")
        assert response.status_code == 200

    def test_patch_document(self, client, session):
        doc = HistorialDocumento(
            user_id=1, filename="patch.pdf", file_path="/patch.pdf"
        )
        session.add(doc)
        session.commit()

        response = client.patch(
            f"/api/v1/db/documents/{doc.id}", json={"filename": "new.pdf"}
        )
        assert response.status_code == 200
        assert response.get_json()["filename"] == "new.pdf"

    def test_delete_document(self, client, session):
        doc = HistorialDocumento(user_id=1, filename="del.pdf", file_path="/del.pdf")
        session.add(doc)
        session.commit()

        response = client.delete(f"/api/v1/db/documents/{doc.id}")
        assert response.status_code == 204

        # Verify deletion
        assert session.get(HistorialDocumento, doc.id) is None
