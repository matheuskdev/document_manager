"""Entidade base para o domínio."""

from abc import ABC
from datetime import datetime
from typing import Any, Optional
from uuid import UUID, uuid4




class DomainEvent:
    """
    Evento de domínio base.

    Cada evento possui um tipo, dados associados,
    momento de ocorrência e um identificador único.
    
    Attributes:
        event_type (str): Tipo do evento.
        data (dict[str, Any]): Dados do evento.
        occurred_at (datetime): Momento em que o evento ocorreu.
        event_id (UUID): Identificador único do evento.
    """

    def __init__(self, event_type: str, data: dict[str, Any]):
        """
        Inicializa um novo evento de domínio.

        Args:
            event_type (str): Tipo do evento.
            data (dict[str, Any]): Dados associados ao evento.
        """
        self.event_type = event_type
        self.data = data
        self.occurred_at = datetime.now()
        self.event_id = uuid4()


class Entity(ABC):
    """
    Entidade base do domínio.

    Cada entidade possui um identificador único, 
    timestamps de criação/atualização e pode acumular eventos de domínio.

    Attributes:
        id (UUID): Identificador único da entidade.
        created_at (datetime): Timestamp de criação.
        updated_at (datetime): Timestamp da última modificação.
    """

    def __init__(self, entity_id: Optional[UUID] = None):
        """
        Inicializa uma nova entidade.

        Args:
            entity_id (UUID, optional): ID da entidade. 
            Um novo UUID será gerado se não fornecido.
        """
        self._id: UUID = entity_id or uuid4()
        self._created_at: datetime = datetime.now()
        self._updated_at: datetime = datetime.now()
        self._domain_events: list[DomainEvent] = []

    @property
    def id(self) -> UUID:
        """Retorna o ID da entidade."""
        return self._id

    @property
    def created_at(self) -> datetime:
        """Retorna a data de criação da entidade."""
        return self._created_at

    @property
    def updated_at(self) -> datetime:
        """Retorna a data de atualização da entidade."""
        return self._updated_at

    def _update_timestamp(self):
        """Atualiza o timestamp da entidade."""
        self._updated_at = datetime.now()

    def add_domain_event(self, event: DomainEvent) -> None:
        """
        Adiciona um evento de domínio à entidade.

        Args:
            event (DomainEvent): Evento a ser adicionado.
        """
        self._domain_events.append(event)

    def clear_domain_events(self) -> None:
        """Remove todos os eventos de domínio da entidade."""
        self._domain_events.clear()

    def get_domain_events(self) -> list[DomainEvent]:
        """
        Retorna os eventos de domínio acumulados.

        Returns:
            list[DomainEvent]: Lista de eventos associados à entidade.
        """
        return self._domain_events.copy()

    def __eq__(self, other: Any) -> bool:
        """Compara entidades por ID."""
        return isinstance(other, Entity) and self._id == other._id

    def __hash__(self) -> int:
        """Retorna o hash da entidade baseado no ID."""
        return hash(self._id)
