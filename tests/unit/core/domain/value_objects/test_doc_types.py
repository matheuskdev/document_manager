"""Teste unitário para a classe DocumentType."""

import pytest

from src.core.domain.value_objects.doc_types import DocumentType


@pytest.mark.parametrize(
    "doc_type, expected",
    [
        (DocumentType.REPORT, "Relatório"),
        (DocumentType.CONTRACT, "Contrato"),
        (DocumentType.MANUAL, "Manual"),
        (DocumentType.POP, "POP"),
        (DocumentType.PROTOCOL, "Protocolo"),
        (DocumentType.TUTORIAL, "Tutorial"),
        (DocumentType.OTHER, "Outro"),
    ],
)
def test_document_type(doc_type, expected):
    """Teste para verificar os valores de DocumentType."""
    assert doc_type.value == expected


def test_document_type_str():
    """Teste para verificar a representação em string de DocumentType."""
    doc_type = DocumentType.REPORT
    assert str(doc_type) == "Relatório"
