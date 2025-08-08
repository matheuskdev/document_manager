"""Testes para o Use Case de criação de tenant(empresa)."""

from unittest.mock import MagicMock
from uuid import uuid4

import pytest

from src.core.application.services.tenant_service import TenantService
from src.core.application.use_cases.tenant.create import CreateTenantUseCase
from src.core.domain.entities.tenant import Tenant
from src.core.domain.exceptions import BusinessRuleViolationError


@pytest.fixture
def tenant_repository_mock():
    """Mock do repositório de tenant."""
    return MagicMock()


@pytest.fixture
def tenant_service_mock():
    """Mock do serviço de tenant."""
    return MagicMock(spec=TenantService)


@pytest.fixture
def create_tenant_use_case(
    tenant_repository_mock,
    tenant_service_mock,
):  # pylint: disable=redefined-outer-name
    """Instância do Use Case de criação de tenant."""
    return CreateTenantUseCase(
        tenant_repository=tenant_repository_mock,
        tenant_service=tenant_service_mock,
    )


@pytest.fixture
def valid_tenant():
    """Retorna uma instância válida de Tenant."""
    return Tenant(
        name="Empresa Teste",
        description="Descrição da Empresa Teste",
        logo="logo.png",
        user_id=uuid4(),
    )


def test_create_tenant_success(
    valid_tenant, tenant_repository_mock
):  # pylint: disable=redefined-outer-name
    """
    Testa a criação bem-sucedida de um novo Tenant,
    garantindo que o método de criação
    seja chamado e que nenhuma exceção seja lançada.
    """
    tenant_repository_mock.exists_by_name.return_value = False
    tenant_service = TenantService()
    create_tenant_use_case = CreateTenantUseCase(
        tenant_repository_mock, tenant_service
    )

    create_tenant_use_case.execute(valid_tenant)

    tenant_repository_mock.save.assert_called_once_with(valid_tenant)


def test_create_tenant_with_existing_name_raises_error(
    valid_tenant, tenant_repository_mock
):  # pylint: disable=redefined-outer-name
    """
    Testa se o CreateTenantUseCase levanta uma exceção
    BusinessRuleViolationError
    ao tentar criar um Tenant com um nome já existente.
    """
    tenant_repository_mock.exists_by_name.return_value = True
    tenant_service = TenantService()
    create_tenant_use_case = CreateTenantUseCase(
        tenant_repository_mock, tenant_service
    )

    with pytest.raises(BusinessRuleViolationError) as exc_info:
        create_tenant_use_case.execute(valid_tenant)

    assert "já existe" in str(exc_info.value).lower()
