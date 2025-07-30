"""Enum para status de um contrato."""

from enum import Enum


class ContractStatus(Enum):
    """Status de um contrato."""

    DRAFT = "Rascunho"
    APPROVED = "Aprovado"
    REJECTED = "Rejeitado"
    CANCELLED = "Cancelado"
    PENDING = "Pendente"
    ACTIVE = "Ativo"
    INACTIVE = "Inativo"

    def __str__(self):
        return self.value


class ContractType(Enum):
    """Tipo de contrato."""

    SERVICE = "Serviços"
    SALES = "Vendas"
    RENTAL = "Aluguel"
    PARTNERSHIP = "Parceria"
    OTHER = "Outro"

    def __str__(self):
        return self.value
