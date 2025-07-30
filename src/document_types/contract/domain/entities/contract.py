from datetime import date
from decimal import Decimal
from uuid import UUID

from src.core.domain.entities.document import Document
from src.core.domain.exceptions import DocumentTypeException
from src.core.domain.value_objects.doc_types import DocumentType
from src.document_types.contract.domain.value_object import (
    ContractStatus,
    ContractType,
)


class Contract(Document):
    """Classe que representa um contrato, herda de Document."""

    def __init__(
        self,
        title: str,
        document_type: DocumentType,
        user_id: UUID,
        subject: str,
        description: str,
        amount: Decimal,
        number: int,
        department_id: UUID,
        folder_id: UUID,
        parts_id: list[UUID],
        start_date: date,
        end_date: date | None,
        notes: str | None = None,
        slug: str | None = None,
        created_at: date | None = None,
        updated_at: date | None = None,
        is_additional: bool = False,
        email_send: bool = False,
        lgpd: bool = False,
        automatic_renewal: bool = False,
        status: ContractStatus = ContractStatus.DRAFT,
        contract_type: ContractType = ContractType.OTHER,
    ):
        super().__init__(title, document_type, user_id)
        self.subject = subject
        self.description = description
        self.amount = amount
        self.number = number
        self.department_id = department_id
        self.folder_id = folder_id
        self.parts_id = parts_id
        self.start_date = start_date
        self.end_date = end_date
        self.notes = notes
        self.slug = slug
        self.created_at = created_at or date.today()
        self.updated_at = updated_at or date.today()
        self.is_additional = is_additional
        self.email_send = email_send
        self.lgpd = lgpd
        self.automatic_renewal = automatic_renewal
        self.status = status
        self.contract_type = contract_type

        if document_type != DocumentType.CONTRACT:
            raise DocumentTypeException(
                f"Tipo de documento inválido: {document_type}."
                f" Esperado: {DocumentType.CONTRACT}."
            )

    def __str__(self):
        return f"Contract(id={self.id}, document_type={self.document_type})"
