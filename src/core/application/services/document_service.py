"""Serviço para gerenciar documentos."""

from src.core.domain.entities.document import Document
from src.core.domain.exceptions import DocumentTypeException
from src.core.domain.value_objects.doc_types import DocumentType


class DocumentService:
    """Serviço para gerenciar documentos."""

    def __init__(self, document: Document):
        self.document = document

    def validate(self):
        """Valida o documento."""
        if not self.document.title:
            raise ValueError("O título do documento não pode ser vazio.")
        if not isinstance(self.document.document_type, DocumentType):
            raise DocumentTypeException("O tipo de documento deve ser válido.")
        if not self.document.user_id:
            raise ValueError("O ID do usuário não pode ser vazio.")
