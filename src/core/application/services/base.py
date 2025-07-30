"""Interface para os serviços de domínio."""

from abc import ABC, abstractmethod

from src.core.domain.entities.document import Document


class IDocumentService():
    """Interface para o serviço de documentos."""

    @abstractmethod
    def validate(self, document: Document) -> None:
        """Valida um documento."""
        raise NotImplementedError
