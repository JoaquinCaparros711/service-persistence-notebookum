"""Unit tests for DocumentService"""

import pytest
from unittest.mock import MagicMock
from app.services.document_service import DocumentService
from app.models.document import HistorialDocumento
from marshmallow import ValidationError


@pytest.fixture
def mock_repo(mocker):
    # Parcheamos la clase DocumentRepository justo donde se importa dentro del service
    return mocker.patch("app.services.document_service.DocumentRepository")


@pytest.fixture
def document_service(mock_repo):
    # Al inicializar el servicio, tomara el DocumentRepository mockeado
    return DocumentService()


@pytest.mark.unit
class TestDocumentService:
    def test_get_all_no_filter(self, document_service, mock_repo):
        # Arrange: Simular la respuesta del repositorio
        mock_instance = mock_repo.return_value
        mock_instance.list_all.return_value = [
            HistorialDocumento(
                id=1, user_id=1, filename="test1.pdf", file_path="/test1.pdf"
            ),
            HistorialDocumento(
                id=2, user_id=2, filename="test2.pdf", file_path="/test2.pdf"
            ),
        ]

        # Act
        result = document_service.get_all()

        # Assert
        mock_instance.list_all.assert_called_once()
        assert len(result) == 2
        assert result[0]["filename"] == "test1.pdf"

    def test_get_by_id_found(self, document_service, mock_repo):
        # Happy Path: Documento existe
        mock_instance = mock_repo.return_value
        mock_instance.get_by_id.return_value = HistorialDocumento(
            id=1, user_id=1, filename="test.pdf", file_path="/test.pdf"
        )

        result = document_service.get_by_id(1)

        mock_instance.get_by_id.assert_called_once_with(1)
        assert result is not None
        assert result["id"] == 1
        assert result["filename"] == "test.pdf"

    def test_get_by_id_not_found(self, document_service, mock_repo):
        # Sad Path: Documento no existe
        mock_instance = mock_repo.return_value
        mock_instance.get_by_id.return_value = None

        result = document_service.get_by_id(999)

        assert result is None

    def test_create_success(self, document_service, mock_repo, app):
        # Happy Path: Creacion exitosa
        mock_instance = mock_repo.return_value
        mock_instance.session = MagicMock()

        data = {"user_id": 1, "filename": "new.pdf", "file_path": "/new.pdf"}

        # Usamos app_context porque Marshmallow lo requiere para el load/dump
        with app.app_context():
            result = document_service.create(data)

        mock_instance.create.assert_called_once()
        assert result["filename"] == "new.pdf"
        assert result["user_id"] == 1

    def test_create_validation_error(self, document_service, mock_repo, app):
        # Sad Path: Faltan campos requeridos (filename)
        data = {"user_id": 1}

        with app.app_context():
            with pytest.raises(ValidationError):
                document_service.create(data)

    def test_delete_success(self, document_service, mock_repo):
        # Happy Path: Borrado exitoso
        mock_instance = mock_repo.return_value
        mock_instance.get_by_id.return_value = HistorialDocumento(id=1)

        result = document_service.delete(1)

        assert result is True
        mock_instance.delete.assert_called_once()

    def test_delete_not_found(self, document_service, mock_repo):
        # Sad Path: Intentar borrar algo que no existe
        mock_instance = mock_repo.return_value
        mock_instance.get_by_id.return_value = None

        result = document_service.delete(999)

        assert result is False
        mock_instance.delete.assert_not_called()
