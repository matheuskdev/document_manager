"""Use Case para criar uma empresa (tenant)."""
from src.core.domain.exceptions import BusinessRuleViolationError
from src.core.domain.entities.tenant import Tenant
from src.core.domain.repositorys.tenant import ITenantRepository
from src.core.domain.events.tenant import TenantCreatedEvent


class CreateTenantUseCase:
    """Caso de uso para criar uma empresa (tenant)."""

    def __init__(self, tenant_repository: ITenantRepository):
        self._tenant_repository = tenant_repository

    def execute(self, tenant: Tenant) -> Tenant:
        """Executa o caso de uso para criar uma empresa (tenant)."""
        if self._tenant_repository.exists_by_name(tenant.name):
            raise BusinessRuleViolationError(
                f"Já existe um tenant com o nome '{tenant.name}'"
            )

        saved_tenant = self._tenant_repository.save(tenant)

        saved_tenant.add_domain_event(
            TenantCreatedEvent(
                tenant_id=saved_tenant.entity_id,
                user_id=saved_tenant.user_id,
            )
        )

        return saved_tenant
