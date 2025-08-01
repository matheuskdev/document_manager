"""Entidade de Documento."""

from typing import Any
from uuid import UUID

from src.core.domain.entities.base import Entity
from src.core.domain.events.document import DocumentUpdatedEvent
from src.core.domain.exceptions import (
    DocumentTypeException,
    DocumentUpdateAttrException,
)
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

    @property
    def title(self) -> str:
        """Retorna o título do documento."""
        return self._title

    @title.setter
    def title(self, value: str):
        """Define o título do documento,
        garantindo que não seja vazio.
        """
        if not value:
            raise ValueError("O título do documento não pode ser vazio.")
        self._title = value

    @property
    def document_type(self) -> DocumentType:
        """Retorna o tipo do documento."""
        return self._document_type

    @document_type.setter
    def document_type(self, value: DocumentType):
        """Define o tipo do documento,
        garantindo que seja uma instância de DocumentType.
        """
        if not isinstance(value, DocumentType):
            raise DocumentTypeException(
                "O tipo de documento deve ser uma instância de DocumentType."
            )
        self._document_type = value

    @property
    def user_id(self) -> UUID:
        """Retorna o ID do usuário que criou o documento."""
        return self._user_id

    def __str__(self):
        return (
            f"Document(id={self.id}, document_type={self.document_type.value})"
        )

    def update_attribute(
        self, attr: str, new_value: Any, user_id_modifier: UUID
    ):
        """
        Atualiza um atributo do documento e registra o evento de domínio.
        """
        if not hasattr(self, attr):
            raise DocumentUpdateAttrException(
                f"A entidade '{self.__class__.__name__}'"
                f"não tem o atributo '{attr}'."
            )

        old_value = getattr(self, attr)

        if old_value == new_value:
            return

        try:
            setattr(self, attr, new_value)
        except Exception as e:
            raise DocumentUpdateAttrException(
                f"Falha ao atualizar '{attr}': {e}"
            ) from e

        self._update_timestamp()
        self.add_domain_event(
            DocumentUpdatedEvent(
                document_id=self.id,
                user_id=user_id_modifier,
                old_value=old_value,
                new_value=new_value,
                document_type=self.document_type,
            )
        )
