"""Use Case para criar uma empresa (tenant)."""

from src.core.application.services.base import IBaseService
from src.core.domain.entities.tenant import Tenant
from src.core.domain.events.tenant import TenantCreatedEvent
from src.core.domain.repositorys.tenant import ITenantRepository


class CreateTenantUseCase:
    """Caso de uso para criar uma empresa (tenant)."""

    def __init__(
        self,
        tenant_repository: ITenantRepository,
        tenant_service: IBaseService,
    ):
        self._tenant_repository = tenant_repository
        self._tenant_service = tenant_service

    def execute(self, tenant: Tenant) -> Tenant:
        """Executa o caso de uso para criar uma empresa (tenant)."""

        self._tenant_service.validate(tenant, self._tenant_repository)

        saved_tenant = self._tenant_repository.save(tenant)

        saved_tenant.add_domain_event(
            TenantCreatedEvent(
                tenant_id=saved_tenant.entity_id,
                user_id=saved_tenant.user_id,
            )
        )

        return saved_tenant
