"""Repository para a entidade Document."""

from abc import ABC, abstractmethod
from uuid import UUID

from src.core.domain.entities.document import Document
from src.core.domain.value_objects.doc_types import DocumentType


class IDocumentRepository(ABC):
    """Interface para o repositório de documentos."""

    @abstractmethod
    def add(self, document: Document) -> None:
        """Adiciona um documento ao repositório."""
        raise NotImplementedError

    @abstractmethod
    def get(self, document_id: UUID) -> Document:
        """Obtém um documento do repositório."""
        raise NotImplementedError

    @abstractmethod
    def update(self, document: Document) -> None:
        """Atualiza um documento no repositório."""
        raise NotImplementedError

    @abstractmethod
    def delete(self, document_id: UUID) -> None:
        """Remove um documento do repositório."""
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, document_id: UUID) -> Document:
        """Obtém um documento pelo ID."""
        raise NotImplementedError

    @abstractmethod
    def get_by_type(self, document_type: DocumentType) -> list[Document]:
        """Obtém documentos pelo tipo."""
        raise NotImplementedError
