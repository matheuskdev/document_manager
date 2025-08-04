"""Use Cases Base"""

from abc import ABC, abstractmethod

from src.core.application.services.base import IDocumentService
from src.core.domain.entities.document import Document
from src.core.domain.repositorys.document import IDocumentRepository


class UseCase(ABC):
    """Classe base para todos os casos de uso."""

    @abstractmethod
    def execute(
        self,
        repository: IDocumentRepository,
        service: IDocumentService,
        document: Document,
    ) -> Document:
        """Método que executa o caso de uso."""
