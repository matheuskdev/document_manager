"""Serviço para gerenciar empresas."""

from src.core.application.services.base import IBaseService
from src.core.domain.entities.tenant import Tenant
from src.core.domain.exceptions import BusinessRuleViolationError
from src.core.domain.repositorys.tenant import ITenantRepository


class TenantService(IBaseService):
    """Serviço para gerenciar empresas."""

    def validate(self, entity: Tenant, repository: ITenantRepository) -> None:
        """Valida uma nova empresa."""
        if repository.exists_by_name(entity.name):
            raise BusinessRuleViolationError(
                f"Já existe um tenant com o nome '{entity.name}'"
            )
