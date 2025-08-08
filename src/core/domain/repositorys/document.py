"""Repository para a entidade Document."""

from abc import ABC, abstractmethod
from uuid import UUID

from src.core.domain.entities.document import Document
from src.core.domain.repositorys.base import IRepository
from src.core.domain.value_objects.doc_types import DocumentType


class IDocumentRepository(IRepository):
    """Interface para o repositório de documentos."""

    @abstractmethod
    def save(self, document: Document) -> Document:
        """Adiciona um documento ao repositório."""

    @abstractmethod
    def get(self, document_id: UUID) -> Document:
        """Obtém um documento do repositório."""

    @abstractmethod
    def update(self, document: Document) -> Document:
        """Atualiza um documento no repositório."""

    @abstractmethod
    def delete(self, document_id: UUID) -> None:
        """Remove um documento do repositório."""

    @abstractmethod
    def all(self) -> list[Document]:
        """Obtém todos os documentos do repositório."""

    @abstractmethod
    def count(self) -> int:
        """Conta o número de documentos no repositório."""

    @abstractmethod
    def exists(self, document_id: UUID) -> bool:
        """Verifica se um documento existe no repositório."""

    @abstractmethod
    def get_by_id(self, document_id: UUID) -> Document:
        """Obtém um documento pelo ID."""

    @abstractmethod
    def get_by_document_type(
        self, document_type: DocumentType
    ) -> list[Document]:
        """Obtém documentos pelo tipo."""

    @abstractmethod
    def get_by_user_id(self, user_id: UUID) -> list[Document]:
        """Obtém documentos associados a um usuário específico."""

    @abstractmethod
    def get_by_status(self, status: str) -> list[Document]:
        """Obtém documentos pelo status."""

    @abstractmethod
    def get_by_tenant_id(self, tenant_id: UUID) -> list[Document]:
        """Obtém documentos associados a um tenant específico."""
