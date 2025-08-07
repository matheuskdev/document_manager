"""Testes para o Use Case de criação de tenant(empresa)."""

from unittest.mock import MagicMock
from uuid import uuid4

import pytest

from src.core.application.use_cases.tenant.create import CreateTenantUseCase
from src.core.domain.entities.tenant import Tenant


@pytest.fixture
def tenant_repository_mock():
    """Mock do repositório de tenant."""
    return MagicMock()


@pytest.fixture
def create_tenant_use_case(
    tenant_repository_mock
):  # pylint: disable=redefined-outer-name
    """Instância do Use Case de criação de tenant."""
    return CreateTenantUseCase(tenant_repository=tenant_repository_mock)


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
    create_tenant_use_case, tenant_repository_mock, valid_tenant
):  # pylint: disable=redefined-outer-name
    """Teste para criação bem-sucedida de um tenant."""
    tenant_repository_mock.exists_by_name.return_value = False
    tenant_repository_mock.save.return_value = valid_tenant

    result = create_tenant_use_case.execute(valid_tenant)

    tenant_repository_mock.exists_by_name.assert_called_once_with(
        valid_tenant.name
    )
    tenant_repository_mock.save.assert_called_once_with(valid_tenant)
    assert result == valid_tenant
    assert len(result.get_domain_events()) == 1
    assert result.get_domain_events()[0].event_type == "tenant_created"


def test_create_tenant_name_already_exists(
    create_tenant_use_case, tenant_repository_mock, valid_tenant
):  # pylint: disable=redefined-outer-name
    """
    Teste para tentativa de criação de um tenant com nome já existente.
    """
    tenant_repository_mock.exists_by_name.return_value = True

    with pytest.raises(Exception) as exc_info:
        create_tenant_use_case.execute(valid_tenant)

    tenant_repository_mock.exists_by_name.assert_called_once_with(
        valid_tenant.name
    )
    tenant_repository_mock.save.assert_not_called()
    assert (
        str(exc_info.value)
        == f"Já existe um tenant com o nome '{valid_tenant.name}'"
    )
