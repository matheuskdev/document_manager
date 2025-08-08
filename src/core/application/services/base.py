"""Interface para os serviços de domínio."""

from abc import ABC, abstractmethod

from src.core.domain.entities.base import Entity
from src.core.domain.entities.document import Document
from src.core.domain.repositorys.base import IRepository


class IDocumentService(ABC):
    """Interface para o serviço de documentos."""

    @abstractmethod
    def validate(self, document: Document) -> None:
        """Valida um documento."""


class IBaseService(ABC):
    """Interface para os serviços base."""

    @abstractmethod
    def validate(self, entity: Entity, repository: IRepository) -> None:
        """Valida uma nova entidade."""
