"""Entidade base para o domínio."""

from abc import ABC
from datetime import datetime
from typing import Any, Optional
from uuid import UUID, uuid4


class DomainEvent:
    """
    Evento de domínio base.

    Args:
        event_type (str): Tipo do evento.
        data (dict[str, Any]): Dados do evento.
    """

    def __init__(self, event_type: str, data: dict[str, Any]):
        self.event_type = event_type
        self.data = data
        self.occurred_at = datetime.now()
        self.event_id = uuid4()


class Entity(ABC):
    """
    Entidade base do domínio.

    Args:
        entity_id (UUID, optional): ID da entidade.
        Se não fornecido, um novo UUID é gerado.
    """

    def __init__(self, entity_id: Optional[UUID] = None):
        self._id = entity_id or uuid4()
        self._domain_events: list[DomainEvent] = []
        self._created_at = datetime.now()
        self._updated_at = datetime.now()

    @property
    def id(self) -> UUID:
        "Retorna o ID da entidade."
        return self._id

    @property
    def created_at(self) -> datetime:
        "Retorna a data de criação da entidade."
        return self._created_at

    @property
    def updated_at(self) -> datetime:
        "Retorna a data de atualização da entidade."
        return self._updated_at

    def _update_timestamp(self):
        """Atualiza o timestamp de modificação."""
        self._updated_at = datetime.now()

    def add_domain_event(self, event: DomainEvent):
        """Adiciona um evento de domínio."""
        self._domain_events.append(event)

    def clear_domain_events(self):
        """Limpa os eventos de domínio."""
        self._domain_events.clear()

    def get_domain_events(self) -> list[DomainEvent]:
        """Retorna os eventos de domínio."""
        return self._domain_events.copy()

    def __eq__(self, other):
        if not isinstance(other, Entity):
            return False
        return self._id == other._id

    def __hash__(self):
        return hash(self._id)
