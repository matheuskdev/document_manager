"""Testes unitários para o DocumentService."""

import pytest

from src.core.application.services.document_service import DocumentService
from src.core.domain.entities.document import Document
from src.core.domain.exceptions import DocumentTypeException
from src.core.domain.value_objects.doc_types import DocumentType


@pytest.fixture
def document():
    """Cria um documento de exemplo."""
    return Document(
        title="Documento de Teste",
        user_id="user_456",
        document_type=DocumentType.REPORT,
    )


def test_document_service_validate_success(
    document,
):  # pylint: disable=redefined-outer-name
    """Testa a validação bem-sucedida do documento."""
    service = DocumentService(document)
    service.validate()  # Não deve levantar exceções
    assert True  # Se não levantar exceção, o teste passa


def test_document_service_validate_empty_title(
    document,
):  # pylint: disable=redefined-outer-name
    """Testa a validação do documento com título vazio."""
    document.title = ""
    service = DocumentService(document)
    with pytest.raises(
        ValueError, match="O título do documento não pode ser vazio."
    ):
        service.validate()


def test_document_service_validate_invalid_document_type(
    document,
):  # pylint: disable=redefined-outer-name
    """Testa a validação do documento com tipo de documento inválido."""
    document.document_type = "tipo_invalido"
    service = DocumentService(document)
    with pytest.raises(
        DocumentTypeException, match="O tipo de documento deve ser válido."
    ):
        service.validate()


def test_document_service_validate_empty_user_id(
    document,
):  # pylint: disable=redefined-outer-name
    """Testa a validação do documento com ID de usuário vazio."""
    document.user_id = ""
    service = DocumentService(document)
    with pytest.raises(
        ValueError, match="O ID do usuário não pode ser vazio."
    ):
        service.validate()
