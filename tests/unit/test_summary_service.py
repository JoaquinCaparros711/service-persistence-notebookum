"""Unit tests for SummaryService"""

import pytest
from unittest.mock import MagicMock
from app.services.summary_service import SummaryService
from app.models.summary import Summary
from app.models.document import HistorialDocumento
from marshmallow import ValidationError


@pytest.fixture
def mock_summary_repo(mocker):
    return mocker.patch("app.services.summary_service.SummaryRepository")


@pytest.fixture
def mock_document_repo(mocker):
    return mocker.patch("app.services.summary_service.DocumentRepository")


@pytest.fixture
def summary_service(mock_summary_repo, mock_document_repo):
    return SummaryService()


@pytest.mark.unit
class TestSummaryService:
    def test_create_success(
        self, summary_service, mock_summary_repo, mock_document_repo, app
    ):
        doc_mock = mock_document_repo.return_value
        sum_mock = mock_summary_repo.return_value
        sum_mock.session = MagicMock()

        # Simular que el documento SI existe
        doc_mock.get_by_id.return_value = HistorialDocumento(id=1)

        data = {
            "documento_id": 1,
            "contenido": "test content",
            "modelo_utilizado": "gpt-4",
        }

        with app.app_context():
            result = summary_service.create(data)

        sum_mock.create.assert_called_once()
        assert result["contenido"] == "test content"

    def test_create_document_not_found(self, summary_service, mock_document_repo):
        # Sad path: El documento padre no existe
        doc_mock = mock_document_repo.return_value
        doc_mock.get_by_id.return_value = None

        data = {"documento_id": 999, "contenido": "test"}

        with pytest.raises(ValueError, match="Document not found"):
            summary_service.create(data)

    def test_get_by_id_found(self, summary_service, mock_summary_repo):
        sum_mock = mock_summary_repo.return_value
        sum_mock.get_by_id.return_value = Summary(
            id=1, documento_id=1, contenido="test"
        )

        result = summary_service.get_by_id(1)

        assert result is not None
        assert result["id"] == 1
        assert result["contenido"] == "test"

    def test_get_by_id_not_found(self, summary_service, mock_summary_repo):
        sum_mock = mock_summary_repo.return_value
        sum_mock.get_by_id.return_value = None

        assert summary_service.get_by_id(99) is None
