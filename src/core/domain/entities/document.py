"""Entidade de Documento"""

from typing import Any
from uuid import UUID

from src.core.domain.entities.base import Entity
from src.core.domain.events.document import DocumentUpdatedEvent
from src.core.domain.value_objects.doc_types import DocumentType


class Document(Entity):
    """Entidade de Documento.

    Args:
        title (str): Título do documento.
        document_type (DocumentType): Tipo do documento.
        user_id (UUID): ID do usuário que criou o documento.
        entity_id (UUID, optional): ID da entidade.
        Se não fornecido, um novo UUID é gerado.
    """

    def __init__(
        self,
        title: str,
        document_type: DocumentType,
        user_id: UUID,
        entity_id: UUID = None,
    ):
        super().__init__(entity_id)
        self.title = title
        self.document_type = document_type
        self.user_id = user_id

    def __str__(self):
        return f"Document(id={self.id}, document_type={self.document_type})"

    def update(
        self, attr: str, new_value: Any, event_update: DocumentUpdatedEvent
    ):
        """
        Atualiza um atributo do documento e marca a entidade como modificada.

        Args:
            attr (str): Nome do atributo a ser atualizado.
            new_value (Any): Novo valor para o atributo.
            event_update (DomainEvent): Evento de atualização a ser registrado.

        Returns:
            None
        """
        obj_property = attr

        if not hasattr(self, obj_property):
            raise AttributeError(
                f"<{self.__class__.__name__}> não tem o atributo <{attr}>"
            )

        old_value = getattr(self, obj_property)

        if not isinstance(new_value, type(old_value)):
            raise TypeError(
                f"Tipo de dado inválido para o atributo: <{attr}>. "
                f"Esperado: <{type(old_value).__name__}>, "
                f"Recebido: <{type(new_value).__name__}>"
            )
        setattr(self, obj_property, new_value)
        self._update_timestamp()
        self.add_domain_event(
            event_update(
                self.id,
                self.user_id,
                old_value,
                new_value,
                self.document_type.value,
            )
        )
