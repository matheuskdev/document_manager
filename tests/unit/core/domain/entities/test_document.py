"Testes unitários para a entidade Document."

import time
from datetime import datetime
from uuid import UUID, uuid4

import pytest

from src.core.domain.entities.document import Document
from src.core.domain.events.document import DocumentUpdatedEvent
from src.core.domain.value_objects.doc_types import DocumentType


@pytest.fixture
def docs():
    """Fixture para criar um documento de teste."""
    return Document("Test Document", DocumentType.REPORT, uuid4())


def test_document_creation_with_specific_id():
    """Testa a criação de um documento com um ID específico."""
    uuid = uuid4()
    document = Document("Test Document", DocumentType.CONTRACT, uuid4(), uuid)
    assert document.id == uuid


def test_document_creation_without_id():
    """Testa a criação de um documento sem um ID específico."""
    document = Document("Test Document", DocumentType.REPORT, uuid4())
    assert document.id is not None
    assert isinstance(document.id, UUID)


def test_document_created_at(docs):  # pylint: disable=redefined-outer-name
    """Testa a data de criação do documento."""
    now = datetime.now()
    delta = abs((now - docs.created_at).total_seconds())
    assert delta < 1


def test_document_updated_at_initial(
    docs,
):  # pylint: disable=redefined-outer-name
    """Testa a data de atualização inicial do documento."""
    now = datetime.now()
    delta = abs((now - docs.updated_at).total_seconds())
    assert delta < 1


def test_document_update_timestamp(
    docs,
):  # pylint: disable=redefined-outer-name
    """Testa a atualização do timestamp de modificação do documento."""
    initial = docs.updated_at
    time.sleep(0.1)
    docs._update_timestamp()  # pylint: disable=protected-access
    assert docs.updated_at > initial


def test_document_update_attribute(
    docs,
):  # pylint: disable=redefined-outer-name
    """Testa a atualização de um atributo do documento."""
    time.sleep(0.1)
    docs.update("title", "Updated Title", DocumentUpdatedEvent)
    assert docs.title == "Updated Title"
    assert docs.updated_at > docs.created_at


def test_document_update_invalid_attribute(
    docs,
):  # pylint: disable=redefined-outer-name
    """Testa a atualização de um atributo inválido do documento."""
    with pytest.raises(AttributeError):
        docs.update("invalid_attr", "New Value", DocumentUpdatedEvent)


def test_document_update_invalid_type(
    docs,
):  # pylint: disable=redefined-outer-name
    """Testa a atualização de um atributo com tipo inválido."""
    with pytest.raises(TypeError):
        docs.update("title", 123, DocumentUpdatedEvent)


def test_document_add_domain_event(
    docs,
):  # pylint: disable=redefined-outer-name
    """Testa a adição de um evento de domínio ao documento."""
    event = DocumentUpdatedEvent(
        docs.id,
        docs.user_id,
        "Old Title",
        "New Title",
        docs.document_type.value,
    )
    docs.add_domain_event(event)
    assert len(docs.get_domain_events()) == 1
    assert docs.get_domain_events()[0] == event


def test_document_clear_domain_events(
    docs,
):  # pylint: disable=redefined-outer-name
    """Testa a limpeza dos eventos de domínio do documento."""
    event = DocumentUpdatedEvent(
        docs.id,
        docs.user_id,
        "Old Title",
        "New Title",
        docs.document_type.value,
    )
    docs.add_domain_event(event)
    assert len(docs.get_domain_events()) == 1
    docs.clear_domain_events()
    assert not docs.get_domain_events()


def test_document_str_representation(
    docs,
):  # pylint: disable=redefined-outer-name
    """Testa a representação em string do documento."""
    expected = f"Document(id={docs.id}, document_type={docs.document_type})"
    assert str(docs) == expected
