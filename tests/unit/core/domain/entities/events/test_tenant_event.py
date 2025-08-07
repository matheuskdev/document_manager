"""Testes para os eventos de domínio relacionados a tenants."""

from uuid import uuid4

import pytest

from src.core.domain.entities.tenant import Tenant
from src.core.domain.events.tenant import (
    TenantCreatedEvent,
    TenantDeletedEvent,
    TenantUpdatedEvent,
)


@pytest.fixture
def tenant():
    """Retorna uma instância válida de Tenant."""
    return Tenant(
        name="Empresa Teste",
        description="Descrição da Empresa Teste",
        logo="logo.png",
        user_id=uuid4(),
    )


def test_tenant_created_event(tenant):  # pylint: disable=redefined-outer-name
    """Testa o evento de criação do tenant."""
    event = TenantCreatedEvent(tenant.entity_id, tenant.user_id)
    assert event.data.get("tenant_id") == str(tenant.entity_id)
    assert event.data.get("user_id") == str(tenant.user_id)
    assert event.event_type == "tenant_created"
    tenant.add_domain_event(event)
    assert len(tenant.get_domain_events()) == 1
    assert tenant.get_domain_events()[0] == event


def test_tenant_updated_event(tenant):  # pylint: disable=redefined-outer-name
    """Testa o evento de atualização do tenant."""
    event = TenantUpdatedEvent(
        tenant_id=tenant.entity_id,
        user_id=tenant.user_id,
        old_value="Old Name",
        new_value="New Name",
    )
    assert event.data.get("tenant_id") == str(tenant.entity_id)
    assert event.data.get("user_id") == str(tenant.user_id)
    assert event.data.get("old_value") == "Old Name"
    assert event.data.get("new_value") == "New Name"
    assert event.event_type == "tenant_updated"
    tenant.add_domain_event(event)
    assert len(tenant.get_domain_events()) == 1
    assert tenant.get_domain_events()[0] == event


def test_tenant_deleted_event(tenant):  # pylint: disable=redefined-outer-name
    """Testa o evento de deleção do tenant."""
    event = TenantDeletedEvent(
        tenant_id=tenant.entity_id, user_id=tenant.user_id
    )
    assert event.data.get("tenant_id") == str(tenant.entity_id)
    assert event.data.get("user_id") == str(tenant.user_id)
    assert event.event_type == "tenant_deleted"
    tenant.add_domain_event(event)
    assert len(tenant.get_domain_events()) == 1
    assert tenant.get_domain_events()[0] == event
