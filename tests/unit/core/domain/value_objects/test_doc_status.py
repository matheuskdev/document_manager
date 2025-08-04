"""Testes unitários para a classe DocumentStatus."""

import pytest

from src.core.domain.value_objects.doc_status import DocumentStatus


@pytest.mark.parametrize(
    "doc_status, expected",
    [
        (DocumentStatus.DRAFT, "Rascunho"),
        (DocumentStatus.ARCHIVED, "Arquivado"),
        (DocumentStatus.DELETED, "Excluído"),
        (DocumentStatus.PUBLISHED, "Publicado"),
    ],
)
def test_document_status(doc_status, expected):
    """Teste para verificar os valores de DocumentStatus."""
    assert doc_status.value == expected


def test_document_status_str():
    """Teste para verificar a representação em string de DocumentStatus."""
    doc_status = DocumentStatus.PUBLISHED
    assert str(doc_status) == "Publicado"
