"""Eventos relacionados a documentos."""

from typing import Any
from uuid import UUID

from src.core.domain.entities.base import DomainEvent


class DocumentUpdatedEvent(DomainEvent):
    """Evento disparado quando um documento é atualizado.

    Args:
        document_id (UUID): ID do documento atualizado.
        user_id (UUID): ID do usuário que realizou a atualização.
        old_value: Valor antigo do atributo atualizado.
        new_value: Novo valor do atributo atualizado.
    """

    def __init__(
        self,
        document_id: UUID,
        user_id: UUID,
        old_value: Any,
        new_value: Any,
        document_type: str,
    ):
        super().__init__(
            event_type="document_updated",
            data={
                "document_id": str(document_id),
                "document_type": str(document_type),
                "user_id": str(user_id),
                "old_value": str(old_value),
                "new_value": str(new_value),
            },
        )
