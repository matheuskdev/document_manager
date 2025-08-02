"""Entidade para Multi-Empresa."""

from datetime import datetime
from typing import Optional
from uuid import UUID

from src.core.domain.entities.base import Entity
from src.core.domain.exceptions import DomainValidationError


class Tenant(Entity):
    """Entidade de Multi-Empresa.

    Entidade que representa um tenant (empresa/organização) no sistema.
    Suporta arquitetura multi-empresa (multi-tenancy).

    Attributes:
        tenant_id (UUID, optional): ID da empresa.
        Se não fornecido, um novo UUID é gerado.
    """

    def __init__(
        self,
        name: str,
        description: str,
        logo: str,
        user_id:UUID,
        is_active: bool = True,
        entity_id: Optional[UUID] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
    ):
        super().__init__(entity_id, created_at, updated_at)
        self.name = name
        self.description = description
        self.logo = logo
        self.user_id = user_id
        self.is_active: bool = is_active

    @property
    def entity_id(self) -> UUID:
        """Retorna o ID da empresa."""
        return self.entity_id

    @property
    def name(self) -> str:
        """Retorna o nome da empresa."""
        return self._name

    @name.setter
    def name(self, value: str):
        """Define o nome da empresa."""
        if not value or not value.strip():
            raise DomainValidationError(
                "O nome da empresa não pode ser vazio."
            )
        if len(value) < 2:
            raise DomainValidationError(
                "O nome da empresa deve ter pelo menos 2 caracteres."
            )
        if len(value) > 255:
            raise DomainValidationError(
                "O nome da empresa não pode ter mais de 255 caracteres."
            )
        self._name = value

    @property
    def description(self) -> str:
        """Retorna a descrição da empresa."""
        return self.description

    @description.setter
    def description(self, value: str):
        """Define a descrição da empresa."""
        if not value or not value.strip():
            raise DomainValidationError(
                "A descrição da empresa não pode ser vazia."
            )
        if len(value) > 1000:
            raise DomainValidationError(
                "A descrição da empresa não pode ter mais de 1000 caracteres."
            )
        self._description = value

    @property
    def logo(self) -> str:
        """Retorna o logo da empresa."""
        return self._logo

    @logo.setter
    def logo(self, value: str):
        """Define o logo da empresa."""
        if not value or not value.strip():
            raise DomainValidationError(
                "O logo da empresa não pode ser vazio."
            )
        self._logo = value

    @property
    def user_id(self) -> UUID:
        """ID do usuário associado ao tenant."""
        return self._user_id

    @user_id.setter
    def user_id(self, value: UUID) -> None:
        """Define o ID do usuário associado ao tenant."""
        if not isinstance(value, UUID):
            raise DomainValidationError(
                "O ID do usuário deve ser um UUID válido."
            )
        self._user_id = value


    @property
    def is_active(self) -> bool:
        """Status de ativação do tenant."""
        return self._is_active

    @is_active.setter
    def is_active(self, value: bool) -> None:
        """Define o status de ativação do tenant."""
        self._is_active = bool(value)

    def activate(self) -> None:
        """Ativa o tenant."""
        self._is_active = True

    def deactivate(self) -> None:
        """Desativa o tenant."""
        self._is_active = False

    def __str__(self):
        return f"Tenant(id={self.entity_id})"
