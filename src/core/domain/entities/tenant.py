"""Entidade para Multi-Empresa."""

from datetime import datetime
from uuid import UUID


class Tenant:
    """Entidade de Multi-Empresa.

    Toda empresa possui um ID, nome, descrição,
    timestamps de criação e atualização, e um logo.

    Args:
        tenant_id (UUID, optional): ID da empresa.
        Se não fornecido, um novo UUID é gerado.
    """

    def __init__(
        self,
        tenant_id: UUID,
        name: str,
        description: str,
        created_at: datetime,
        updated_at: datetime,
        logo: str,
    ):
        self._tenant_id = tenant_id
        self.name = name
        self.description = description
        self.created_at = created_at
        self.updated_at = updated_at
        self.logo = logo

    @property
    def tenant_id(self) -> UUID:
        """Retorna o ID da empresa."""
        return self._tenant_id

    @property
    def name(self) -> str:
        """Retorna o nome da empresa."""
        return self.name

    @name.setter
    def name(self, value: str):
        """Define o nome da empresa."""
        self._name = value

    def __str__(self):
        return f"Tenant(id={self.tenant_id})"
