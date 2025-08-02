"""Eventos relacionados a documentos."""

from typing import Any
from uuid import UUID

from src.core.domain.entities.base import DomainEvent


class TenantUpdatedEvent(DomainEvent):
    """Evento disparado quando um tenant é atualizado.

    Args:
        tenant_id (UUID): ID do tenant atualizado.
        user_id (UUID): ID do usuário que realizou a atualização.
        old_value: Valor antigo do atributo atualizado.
        new_value: Novo valor do atributo atualizado.
    """

    def __init__(
        self,
        tenant_id: UUID,
        user_id: UUID,
        old_value: Any,
        new_value: Any
    ):
        super().__init__(
            event_type="tenant_updated",
            data={
                "tenant_id": str(tenant_id),
                "user_id": str(user_id),
                "old_value": str(old_value),
                "new_value": str(new_value),
            },
        )


class TenantCreatedEvent(DomainEvent):
    """Evento disparado quando um tenant é criado.

    Args:
        tenant_id (UUID): ID do tenant criado.
        user_id (UUID): ID do usuário que criou o tenant.
        document_type (str): Tipo do documento criado.
    """

    def __init__(self, tenant_id: UUID, user_id: UUID):
        super().__init__(
            event_type="tenant_created",
            data={
                "tenant_id": str(tenant_id),
                "user_id": str(user_id),
            },
        )


class TenantDeletedEvent(DomainEvent):
    """Evento disparado quando um tenant é deletado.

    Args:
        tenant_id (UUID): ID do tenant deletado.
        user_id (UUID): ID do usuário que deletou o tenant.
    """

    def __init__(self, tenant_id: UUID, user_id: UUID):
        super().__init__(
            event_type="tenant_deleted",
            data={
                "tenant_id": str(tenant_id),
                "user_id": str(user_id),
            },
        )
