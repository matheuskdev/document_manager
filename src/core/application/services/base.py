"""Interface para os serviços de domínio."""

from src.core.domain.entities.document import Document


class IDocumentService:
    """Interface para o serviço de documentos."""

    def validate(self, document: Document) -> None:
        """Valida um documento."""
        raise NotImplementedError
