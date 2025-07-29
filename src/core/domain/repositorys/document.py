"""Repository para a entidade Document."""

from uuid import UUID

from src.core.domain.entities.document import Document
from src.core.domain.value_objects.doc_types import DocumentType


class IDocumentRepository:
    """Interface para o repositório de documentos."""

    def add(self, document: Document) -> None:
        """Adiciona um documento ao repositório."""
        raise NotImplementedError

    def get(self, document_id: UUID) -> Document:
        """Obtém um documento do repositório."""
        raise NotImplementedError

    def update(self, document: Document) -> None:
        """Atualiza um documento no repositório."""
        raise NotImplementedError

    def delete(self, document_id: UUID) -> None:
        """Remove um documento do repositório."""
        raise NotImplementedError

    def get_by_id(self, document_id: UUID) -> Document:
        """Obtém um documento pelo ID."""
        raise NotImplementedError

    def get_by_type(self, document_type: DocumentType) -> list[Document]:
        """Obtém documentos pelo tipo."""
        raise NotImplementedError
