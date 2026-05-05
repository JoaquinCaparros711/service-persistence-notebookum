"""Contract tests for internal db documents API"""

import pytest
from app.models.document import HistorialDocumento
from app.models.user import User

@pytest.mark.contract
class TestDBDocumentsAPI:
    def test_create_document(self, client, session):
        user = User(email="api_doc_test@example.com", nombre="Test User")
        session.add(user)
        session.commit()
        
        data = {
            "usuario_id": user.id,
            "nombre_archivo": "test.pdf",
            "tamanio_bytes": 1024
        }
        response = client.post("/api/v1/db/documents", json=data)
        assert response.status_code == 201
        
        resp_data = response.get_json()
        assert resp_data["nombre_archivo"] == "test.pdf"
        assert resp_data["estado"] == "pending"
        
    def test_get_document(self, client, session):
        user = User(email="get_doc_test@example.com", nombre="Get User")
        session.add(user)
        session.commit()
        
        doc = HistorialDocumento(usuario_id=user.id, nombre_archivo="get.pdf", tamanio_bytes=500)
        session.add(doc)
        session.commit()
        
        response = client.get(f"/api/v1/db/documents/{doc.id}")
        assert response.status_code == 200
        
    def test_patch_document(self, client, session):
        user = User(email="patch_doc_test@example.com", nombre="Patch User")
        session.add(user)
        session.commit()
        
        doc = HistorialDocumento(usuario_id=user.id, nombre_archivo="patch.pdf", tamanio_bytes=500, estado="pending")
        session.add(doc)
        session.commit()
        
        response = client.patch(f"/api/v1/db/documents/{doc.id}", json={"estado": "completed", "extracto_texto": "text"})
        assert response.status_code == 200
        assert response.get_json()["estado"] == "completed"
        
    def test_delete_document(self, client, session):
        user = User(email="del_doc_test@example.com", nombre="Del User")
        session.add(user)
        session.commit()
        
        doc = HistorialDocumento(usuario_id=user.id, nombre_archivo="del.pdf", tamanio_bytes=500)
        session.add(doc)
        session.commit()
        
        response = client.delete(f"/api/v1/db/documents/{doc.id}")
        assert response.status_code == 204
        
        # Verify deletion
        assert session.get(HistorialDocumento, doc.id) is None
