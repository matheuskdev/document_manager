"""Use case para criar um documento."""

from src.core.application.services.base import IDocumentService
from src.core.application.use_cases.base import UseCase
from src.core.domain.entities.document import Document
from src.core.domain.events.document import DocumentCreatedEvent
from src.core.domain.repositorys.document import IDocumentRepository


class CreateDocumentUseCase(UseCase):
    """Caso de uso para criar um documento."""

    def execute(
        self,
        repository: IDocumentRepository,
        service: IDocumentService,
        document: Document,
    ) -> Document:
        """Executa o caso de uso para criar um documento."""

        service.validate(document)
        saved_document = repository.save(document)

        event = DocumentCreatedEvent(
            document.id, document.user_id, document.document_type.value
        )
        document.add_domain_event(event)

        return saved_document
