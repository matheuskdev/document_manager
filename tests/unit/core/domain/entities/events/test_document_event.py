"""Testes unitários para eventos de domínio do documento."""

from uuid import uuid4

import pytest

from src.core.domain.entities.document import Document
from src.core.domain.events.document import (
    DocumentCreatedEvent,
    DocumentDeletedEvent,
    DocumentUpdatedEvent,
)
from src.core.domain.value_objects.doc_types import DocumentType


@pytest.fixture
def docs():
    """Fixture para criar um documento de teste."""
    return Document(
        title="Test Document",
        user_id=uuid4(),
        document_type=DocumentType.REPORT,
        tenant_id=uuid4(),
    )


def test_document_created_event(docs):  # pylint: disable=redefined-outer-name
    """Testa o evento de criação do documento."""
    event = DocumentCreatedEvent(
        docs.entity_id,
        docs.user_id,
        docs.document_type.value,
    )
    docs.add_domain_event(event)
    assert len(docs.get_domain_events()) == 1
    assert docs.get_domain_events()[0] == event


def test_document_updated_event(docs):  # pylint: disable=redefined-outer-name
    """Testa o evento de atualização do documento."""
    old_value = "Old Title"
    new_value = "New Title"
    event = DocumentUpdatedEvent(
        docs.entity_id,
        docs.user_id,
        old_value,
        new_value,
        docs.document_type.value,
    )
    docs.add_domain_event(event)
    assert len(docs.get_domain_events()) == 1
    assert docs.get_domain_events()[0] == event


def test_document_deleted_event(docs):  # pylint: disable=redefined-outer-name
    """Testa o evento de deleção do documento."""
    event = DocumentDeletedEvent(docs.entity_id, docs.user_id)
    docs.add_domain_event(event)
    assert len(docs.get_domain_events()) == 1
    assert docs.get_domain_events()[0] == event
