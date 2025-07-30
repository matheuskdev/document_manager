"""Teste unitário para a interface de serviços de documentos."""

import pytest

from src.core.application.services.base import IDocumentService


def test_exception_service_base():
    """Testa se o serviço"""
    service = IDocumentService()
    with pytest.raises(NotImplementedError):
        service.validate(document=None)
