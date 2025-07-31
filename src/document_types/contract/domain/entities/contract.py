from datetime import date, datetime, timedelta
from decimal import Decimal
from uuid import UUID

from src.core.domain.entities.document import Document
from src.core.domain.events.document import DocumentCreatedEvent
from src.core.domain.value_objects.doc_types import DocumentType
from src.document_types.contract.domain.entities.exceptions import (
    ContractRenewalException,
)
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
        super().__init__(title, DocumentType.CONTRACT, user_id)
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

        if self.automatic_renewal and self.end_date is None:
            self._set_automatic_renewal()

    def __str__(self):
        return f"Contract(id={self.id}, document_type={self.document_type})"

    def _set_automatic_renewal(self):
        self.end_date = datetime.now() + timedelta(days=365)

    def renew_contract(self, user_id_modifier: UUID):
        """Renova o contrato se a renovação automática estiver habilitada."""
        if not self.automatic_renewal:
            raise ContractRenewalException(
                "Renovação automática não habilitada para este contrato."
            )

        if self.end_date:
            self.end_date = self.end_date + timedelta(days=365)

        self.add_domain_event(
            DocumentCreatedEvent(self.id, user_id_modifier, self.document_type)
        )

    def activate(self, user_id_modifier: UUID):
        """Ativa o contrato, alterando seu status para ATIVO."""
        if self.status != ContractStatus.ACTIVE:
            self.status = ContractStatus.ACTIVE
            self._update_timestamp()
            self.add_domain_event(
                DocumentCreatedEvent(
                    self.id, user_id_modifier, self.document_type
                )
            )

    def _remove_automatic_renewal(self, user_id_modifier: UUID):
        """Remove a opção de renovação automática do contrato."""
        self.automatic_renewal = False
        self.add_domain_event(
            DocumentCreatedEvent(self.id, user_id_modifier, self.document_type)
        )
