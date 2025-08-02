"""Testes para o caso de uso de criação de documentos."""

from unittest.mock import MagicMock
from uuid import uuid4

import pytest

from src.core.application.use_cases.create_document import (
    CreateDocumentUseCase,
)
from src.core.domain.entities.document import Document
from src.core.domain.value_objects.doc_types import DocumentType


def create_mock_document() -> Document:
    """Cria um documento de teste."""
    return Document(
        title="Doc Teste",
        document_type=DocumentType.REPORT,
        entity_id=uuid4(),
        tenant_id=uuid4(),
        user_id=uuid4(),
    )


def test_execute_calls_validate_and_save():
    """
    Testa se o caso de uso
    chama os métodos de validação e salvamento corretamente.
    """
    # Arrange
    document = create_mock_document()

    repository = MagicMock()
    service = MagicMock()
    saved_document = MagicMock()
    repository.save.return_value = saved_document

    use_case = CreateDocumentUseCase()

    # Act
    result = use_case.execute(
        repository=repository, service=service, document=document
    )

    # Assert
    service.validate.assert_called_once_with(document)
    repository.save.assert_called_once_with(document)
    assert result == saved_document
    assert len(document.get_domain_events()) == 1
    assert isinstance(
        document.get_domain_events()[0], type(document.get_domain_events()[0])
    )


def test_execute_raises_if_validation_fails():
    """Testa se o caso de uso levanta uma exceção se a validação falhar."""
    # Arrange
    document = create_mock_document()

    repository = MagicMock()
    service = MagicMock()
    service.validate.side_effect = ValueError("Documento inválido")

    use_case = CreateDocumentUseCase()

    # Act & Assert
    with pytest.raises(ValueError, match="Documento inválido"):
        use_case.execute(
            repository=repository, service=service, document=document
        )

    service.validate.assert_called_once_with(document)
    repository.save.assert_not_called()
