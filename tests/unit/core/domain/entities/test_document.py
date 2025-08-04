"Testes unitários para a entidade Document."

import time
from datetime import datetime
from uuid import UUID, uuid4

import pytest

from src.core.domain.entities.document import Document
from src.core.domain.entities.tenant import Tenant
from src.core.domain.events.document import DocumentUpdatedEvent
from src.core.domain.exceptions import (
    DocumentUpdateAttrException,
    DomainValidationError,
)
from src.core.domain.value_objects.doc_status import DocumentStatus
from src.core.domain.value_objects.doc_types import DocumentType


@pytest.fixture
def user_id():
    """Fixture para criar um usuário de teste."""
    return uuid4()


@pytest.fixture
def tenant(user_id):  # pylint: disable=redefined-outer-name
    """Fixture para criar um inquilino de teste."""
    return Tenant(
        name="Empresa de Teste",
        description="Empresa de Teste para Documentos",
        logo="https://example.com/logo.png",
        user_id=user_id,
        is_active=True,
        entity_id=uuid4(),
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )


@pytest.fixture
def docs(tenant, user_id):  # pylint: disable=redefined-outer-name
    """Fixture para criar um documento de teste."""
    return Document(
        title="Test Document",
        document_type=DocumentType.REPORT,
        user_id=user_id,
        tenant_id=tenant.entity_id,
    )


def test_document_creation_with_specific_id(
    user_id, tenant
):  # pylint: disable=redefined-outer-name
    """Testa a criação de um documento com um ID específico."""
    uuid = uuid4()
    document = Document(
        title="Documento com ID Específico",
        user_id=user_id,
        document_type=DocumentType.REPORT,
        tenant_id=tenant.entity_id,
        entity_id=uuid,
    )
    assert document.entity_id == uuid


def test_document_creation_without_id():
    """Testa a criação de um documento sem um ID específico."""
    document = Document(
        title="Documento sem ID Específico",
        user_id=uuid4(),
        document_type=DocumentType.REPORT,
        tenant_id=uuid4(),
    )
    assert document.entity_id is not None
    assert isinstance(document.entity_id, UUID)


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
    docs.update_attribute("title", "Updated Title", uuid4())
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
    with pytest.raises(DocumentUpdateAttrException):
        docs.update_attribute("title", 123, DocumentUpdatedEvent)


def test_document_clear_domain_events(
    docs,
):  # pylint: disable=redefined-outer-name
    """Testa a limpeza dos eventos de domínio do documento."""
    event = DocumentUpdatedEvent(
        docs.entity_id,
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
    expected = (
        f"\n"
        f"Informações do Documento:\n"
        f"Document(id={docs.entity_id},\n"
        f"document_type={docs.document_type.value},\n"
        f"status={docs.status.value},\n"
        f"tenant_id={docs.tenant_id}) \n"
        f"version={docs.version}\n"
    )
    assert str(docs) == expected


def test_title_setter_validation(docs):  # pylint: disable=redefined-outer-name
    """Testa a validação do setter do título do documento."""
    with pytest.raises(DomainValidationError):
        docs.title = ""
    with pytest.raises(DomainValidationError):
        docs.title = "    "
    with pytest.raises(DomainValidationError):
        docs.title = "A"


def test_user_id_setter_validation(
    docs,
):  # pylint: disable=redefined-outer-name
    """Testa a validação do setter do user_id do documento."""
    with pytest.raises(DomainValidationError):
        docs.user_id = "invalid_uuid"
    with pytest.raises(DomainValidationError):
        docs.user_id = None


def test_version_setter_validation(
    docs,
):  # pylint: disable=redefined-outer-name
    """Testa a validação do setter da versão do documento."""
    with pytest.raises(DomainValidationError):
        docs.version = -1
    with pytest.raises(DomainValidationError):
        docs.version = "invalid_version"
    with pytest.raises(DomainValidationError):
        docs.version = None


def test_document_type_setter_validation(
    docs,
):  # pylint: disable=redefined-outer-name
    """Testa a validação do setter do tipo do documento."""
    with pytest.raises(DomainValidationError):
        docs.document_type = "invalid_type"
    with pytest.raises(DomainValidationError):
        docs.document_type = None


def test_status_setter_validation(
    docs,
):  # pylint: disable=redefined-outer-name
    """Testa a validação do setter do status do documento."""
    with pytest.raises(DomainValidationError):
        docs.status = "invalid_status"
    with pytest.raises(DomainValidationError):
        docs.status = None


def test_tenant_id_setter_validation(
    docs,
):  # pylint: disable=redefined-outer-name
    """Testa a validação do setter do tenant_id do documento."""
    with pytest.raises(DomainValidationError):
        docs.tenant_id = "invalid_uuid"
    with pytest.raises(DomainValidationError):
        docs.tenant_id = None


def test_is_draft_validation(
    docs,
):  # pylint: disable=redefined-outer-name
    """Testa a validação do método is_draft."""
    docs.status = DocumentStatus.DRAFT
    assert docs.is_draft() is True

    docs.status = DocumentStatus.PUBLISHED
    assert docs.is_draft() is False


def test_is_published_validation(
    docs,
):  # pylint: disable=redefined-outer-name
    """Testa a validação do método is_published."""
    docs.status = DocumentStatus.PUBLISHED
    assert docs.is_published() is True

    docs.status = DocumentStatus.DRAFT
    assert docs.is_published() is False


def test_is_archived_validation(
    docs,
):  # pylint: disable=redefined-outer-name
    """Testa a validação do método is_archived."""
    docs.status = DocumentStatus.ARCHIVED
    assert docs.is_archived() is True

    docs.status = DocumentStatus.DRAFT
    assert docs.is_archived() is False


def test_is_deleted_validation(
    docs,
):  # pylint: disable=redefined-outer-name
    """Testa a validação do método is_deleted."""
    docs.status = DocumentStatus.DELETED
    assert docs.is_deleted() is True

    docs.status = DocumentStatus.DRAFT
    assert docs.is_deleted() is False


def test_publish_document(
    docs,
):  # pylint: disable=redefined-outer-name
    """Testa a publicação do documento."""
    docs.publish()
    assert docs.status == DocumentStatus.PUBLISHED


def test_publish_document_with_status_deleted(
    docs,
):  # pylint: disable=redefined-outer-name
    """Testa a publicação do documento com status DELETED."""
    docs.status = DocumentStatus.DELETED
    with pytest.raises(DomainValidationError):
        docs.publish()


def test_archive_document(
    docs,
):  # pylint: disable=redefined-outer-name
    """Testa o arquivamento do documento."""
    docs.archive()
    assert docs.status == DocumentStatus.ARCHIVED


def test_archive_document_with_status_deleted(
    docs,
):  # pylint: disable=redefined-outer-name
    """Testa o arquivamento do documento com status DELETED."""
    docs.status = DocumentStatus.DELETED
    with pytest.raises(DomainValidationError):
        docs.archive()


def test_delete_document(
    docs,
):  # pylint: disable=redefined-outer-name
    """Testa a exclusão do documento."""
    docs.delete()
    assert docs.status == DocumentStatus.DELETED


def test_increment_version(
    docs,
):  # pylint: disable=redefined-outer-name
    """Testa o incremento da versão do documento."""
    initial_version = docs.version
    docs.increment_version()
    assert docs.version == initial_version + 1


def test_belongs_to_tenant(
    docs, tenant
):  # pylint: disable=redefined-outer-name
    """Testa se o documento pertence a empresa."""
    assert docs.belongs_to_tenant(tenant.entity_id) is True


def test_update_attribute_with_invalid_user_id(
    docs,
):  # pylint: disable=redefined-outer-name
    """Testa a atualização de um atributo com um user_id inválido."""
    with pytest.raises(DocumentUpdateAttrException):
        docs.update_attribute("title", "New Title", "invalid_user_id")


def test_update_attribute_with_invalid_attr(
    docs,
):  # pylint: disable=redefined-outer-name
    """Testa a atualização de um atributo inválido."""
    with pytest.raises(DocumentUpdateAttrException):
        docs.update_attribute("invalid_attr", "New Value", uuid4())


def test_update_attribute_with_invalid_type(
    docs,
):  # pylint: disable=redefined-outer-name
    """Testa a atualização de um atributo com um tipo inválido."""
    with pytest.raises(DocumentUpdateAttrException):
        docs.update_attribute("title", 123, uuid4())


def test_update_attribute_with_valid_attr(
    docs,
):  # pylint: disable=redefined-outer-name
    """Testa a atualização de um atributo válido."""
    old_title = docs.title
    new_title = "Updated Title"
    time.sleep(0.1)
    docs.update_attribute("title", new_title, uuid4())
    assert docs.title == new_title
    assert docs.updated_at > docs.created_at
    assert len(docs.get_domain_events()) == 1

    event = docs.get_domain_events()[0]
    assert isinstance(event, DocumentUpdatedEvent)
    assert event.data.get("old_value") == old_title
    assert event.data.get("new_value") == new_title


def test_update_attribute_with_same_value(
    docs,
):  # pylint: disable=redefined-outer-name
    """Testa a atualização de um atributo com o mesmo valor."""
    old_title = docs.title
    docs.update_attribute("title", old_title, uuid4())
    assert docs.title == old_title
    assert docs.updated_at == docs.created_at
    assert len(docs.get_domain_events()) == 0


def test_update_attribute_with_setter_validation(
    docs,
):  # pylint: disable=redefined-outer-name
    """Testa a atualização de um atributo com validação do setter."""
    with pytest.raises(DocumentUpdateAttrException):
        docs.update_attribute("title", "", uuid4())
    with pytest.raises(DocumentUpdateAttrException):
        docs.update_attribute("title", "   ", uuid4())
    with pytest.raises(DocumentUpdateAttrException):
        docs.update_attribute("title", "A", uuid4())
