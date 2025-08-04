"""Repository para a entidade Tenant."""

from abc import ABC, abstractmethod
from uuid import UUID

from src.core.domain.entities.tenant import Tenant


class ITenantRepository(ABC):
    """Interface para o repositório de empresas."""

    @abstractmethod
    def save(self, tenant: Tenant) -> Tenant:
        """Adiciona uma empresa ao repositório."""

    @abstractmethod
    def get(self, tenant_id: UUID) -> Tenant:
        """Obtém uma empresa do repositório."""

    @abstractmethod
    def update(self, tenant: Tenant) -> Tenant:
        """Atualiza uma empresa no repositório."""

    @abstractmethod
    def delete(self, tenant_id: UUID) -> None:
        """Remove uma empresa do repositório."""

    @abstractmethod
    def all(self) -> list[Tenant]:
        """Obtém todas as empresas do repositório."""

    @abstractmethod
    def count(self) -> int:
        """Conta o número de empresas no repositório."""

    @abstractmethod
    def exists(self, tenant_id: UUID) -> bool:
        """Verifica se uma empresa existe no repositório."""

    @abstractmethod
    def get_by_id(self, tenant_id: UUID) -> Tenant:
        """Obtém uma empresa pelo ID."""

    @abstractmethod
    def get_by_user_id(self, user_id: UUID) -> list[Tenant]:
        """Obtém empresas associadas a um usuário específico."""

    @abstractmethod
    def get_actives(self) -> list[Tenant]:
        """Obtém empresas ativas."""

    @abstractmethod
    def get_inactives(self) -> list[Tenant]:
        """Obtém empresas inativas."""
