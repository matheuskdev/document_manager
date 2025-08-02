"""Entidade de Documento."""

from datetime import datetime
from typing import Any
from uuid import UUID

from src.core.domain.entities.base import Entity
from src.core.domain.events.document import DocumentUpdatedEvent
from src.core.domain.exceptions import (
    DocumentTypeException,
    DocumentUpdateAttrException,
    DomainValidationError,
)
from src.core.domain.value_objects.doc_status import DocumentStatus
from src.core.domain.value_objects.doc_types import DocumentType


class Document(Entity):
    """Entidade de Documento.

    Entidade que representa um documento no sistema.
    Contém características e comportamentos comuns
    a todos os tipos de documentos.

    Attributes:
        title (str): Título do documento.
        user_id (UUID): ID do usuário que criou o documento.
        document_type (DocumentType): Tipo do documento.
        version (int): Versão do documento.
        status (DocumentStatus): Status do documento.
        tenant_id (UUID): ID da empresa.
        entity_id (UUID, optional): ID da entidade.
        created_at (datetime, optional): Timestamp de criação.
        updated_at (datetime, optional): Timestamp da última modificação.
    """

    def __init__(
        self,
        title: str,
        user_id: UUID,
        document_type: DocumentType,
        version: int = 1,
        status: DocumentStatus = DocumentStatus.DRAFT,
        tenant_id: UUID = None,
        entity_id: UUID = None,
        created_at: datetime = None,
        updated_at: datetime = None,
    ):
        super().__init__(entity_id, created_at, updated_at)
        self.title = title
        self.user_id = user_id
        self.version = version
        self.document_type = document_type
        self.status = status
        self.tenant_id = tenant_id

    @property
    def title(self) -> str:
        """Retorna o título do documento."""
        return self._title

    @title.setter
    def title(self, value: str):
        """Define o título do documento,
        garantindo que não seja vazio.
        """
        if not value or not value.strip():
            raise ValueError("O título do documento não pode ser vazio.")
        if len(value) < 2:
            raise ValueError(
                "O título do documento deve ter pelo menos 2 caracteres."
            )

        self._title = value

    @property
    def user_id(self) -> UUID:
        """Retorna o ID do usuário que criou o documento."""
        return self._user_id

    @user_id.setter
    def user_id(self, value: UUID):
        """Define o ID do usuário que criou o documento."""
        if not isinstance(value, UUID):
            raise ValueError("O ID do usuário deve ser um UUID válido.")
        self._user_id = value

    @property
    def version(self) -> int:
        """Retorna a versão do documento."""
        return self._version

    @version.setter
    def version(self, value: int):
        """Define a versão do documento,
        garantindo que seja um número positivo.
        """
        if not isinstance(value, int) or value < 1:
            raise ValueError(
                "A versão do documento deve ser um número positivo."
            )
        self._version = value

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
    def status(self) -> DocumentStatus:
        """Retorna o status do documento."""
        return self._status

    @status.setter
    def status(self, value: DocumentStatus):
        """Define o status do documento,
        garantindo que seja uma instância de DocumentStatus.
        """
        if not isinstance(value, DocumentStatus):
            raise DocumentTypeException(
                "O status do documento deve ser uma instância de DocumentStatus."
            )
        self._status = value

    @property
    def tenant_id(self) -> UUID:
        """Retorna o ID da empresa associada ao documento."""
        return self._tenant_id

    @tenant_id.setter
    def tenant_id(self, value: UUID):
        """Define o ID da empresa associada ao documento."""
        if not isinstance(value, UUID):
            raise DocumentTypeException(
                "O ID da empresa deve ser um UUID válido."
            )
        self._tenant_id = value

    def is_draft(self) -> bool:
        """Verifica se o documento está em rascunho."""
        return self._status == DocumentStatus.DRAFT

    def is_published(self) -> bool:
        """Verifica se o documento está publicado."""
        return self._status == DocumentStatus.PUBLISHED

    def is_archived(self) -> bool:
        """Verifica se o documento está arquivado."""
        return self._status == DocumentStatus.ARCHIVED

    def is_deleted(self) -> bool:
        """Verifica se o documento está marcado como deletado."""
        return self._status == DocumentStatus.DELETED

    def publish(self) -> None:
        """Publica o documento."""
        if self._status == DocumentStatus.DELETED:
            raise DomainValidationError(
                "Não é possível publicar um documento deletado"
            )
        self._status = DocumentStatus.PUBLISHED

    def archive(self) -> None:
        """Arquiva o documento."""
        if self._status == DocumentStatus.DELETED:
            raise DomainValidationError(
                "Não é possível arquivar um documento deletado"
            )
        self._status = DocumentStatus.ARCHIVED

    def delete(self) -> None:
        """Marca o documento como deletado (soft delete)."""
        self._status = DocumentStatus.DELETED

    def increment_version(self) -> None:
        """Incrementa a versão do documento."""
        self._version += 1

    def belongs_to_tenant(self, tenant_id: str) -> bool:
        """Verifica se o documento pertence ao tenant especificado."""
        return self._tenant_id == tenant_id

    def __str__(self):
        return (
            f"Document(id={self.entity_id}, "
            f"document_type={self.document_type.value}, "
            f"status={self.status.value}, "
            f"tenant_id={self.tenant_id}) "
            f"version={self.version}"
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

        if not isinstance(new_value, type(old_value)):
            raise DocumentUpdateAttrException(
                f"Não é possível atualizar '{attr}'. \n"
                f"Os tipos não são compatíveis.\n"
                f"Novo valor: {type(new_value)}, \n"
                f"Valor antigo: {type(old_value)} \n"
            )

        try:
            setattr(self, attr, new_value)
        except Exception as e:
            raise DocumentUpdateAttrException(
                f"Falha ao atualizar '{attr}': {e}"
            ) from e

        self._update_timestamp()
        self.add_domain_event(
            DocumentUpdatedEvent(
                document_id=self.entity_id,
                user_id=user_id_modifier,
                old_value=old_value,
                new_value=new_value,
                document_type=self.document_type,
            )
        )
