"""Testes unitários para a entidade Tenant."""

from datetime import datetime
from uuid import uuid4

import pytest

from src.core.domain.entities.tenant import Tenant
from src.core.domain.exceptions import DomainValidationError


def test_tenant_initialization_without_created_at_and_updated_at(user_id):
    """Testa a inicialização da entidade Tenant."""
    tenant_id = uuid4()

    tenant = Tenant(
        name="Empresa Teste",
        description="Descrição da empresa de teste",
        logo="http://example.com/logo.png",
        user_id=user_id,
        entity_id=tenant_id,
    )

    assert tenant.entity_id == tenant_id
    assert tenant.user_id == user_id
    assert tenant.name == "Empresa Teste"
    assert tenant.created_at is not None
    assert tenant.updated_at is not None
    assert tenant.is_active is True


def test_tenant_initialization_with_created_at_and_updated_at(user_id):
    """Testa a inicialização da entidade Tenant com created_at e updated_at."""
    tenant_id = uuid4()
    now = datetime.now()

    tenant = Tenant(
        name="Empresa Teste",
        description="Descrição da empresa de teste",
        logo="http://example.com/logo.png",
        user_id=user_id,
        entity_id=tenant_id,
        created_at=now,
        updated_at=now,
    )

    assert tenant.entity_id == tenant_id
    assert tenant.user_id == user_id
    assert tenant.name == "Empresa Teste"
    assert tenant.created_at == now
    assert tenant.updated_at == now
    assert tenant.is_active is True
    assert tenant.description == "Descrição da empresa de teste"
    assert tenant.logo == "http://example.com/logo.png"
    assert tenant.created_at is not None
    assert tenant.created_at == now
    assert tenant.updated_at is not None
    assert tenant.updated_at == now


def test_getter_name(tenant):
    """Testa o getter para o nome da empresa."""
    assert tenant.name == "Empresa de Teste"


def test_setter_name(tenant):
    """Testa o setter para o nome da empresa."""
    new_name = "Novo Nome da Empresa"
    tenant.name = new_name
    assert tenant.name == new_name


def test_setter_name_validation(tenant):
    """Testa a validação do setter para o nome da empresa."""
    with pytest.raises(
        DomainValidationError, match="O nome da empresa não pode ser vazio."
    ):
        tenant.name = ""
    with pytest.raises(
        DomainValidationError, match="O nome da empresa não pode ser vazio."
    ):
        tenant.name = "   "
    with pytest.raises(
        DomainValidationError,
        match="O nome da empresa deve ter pelo menos 2 caracteres.",
    ):
        tenant.name = "A"
    with pytest.raises(
        DomainValidationError,
        match="O nome da empresa não pode ter mais de 255 caracteres.",
    ):
        tenant.name = "A" * 256


def test_getter_description(tenant):
    """Testa o getter para a descrição da empresa."""
    assert tenant.description == "Empresa de Teste para Documentos"


def test_setter_description(tenant):
    """Testa o setter para a descrição da empresa."""
    new_description = "Nova Descrição da Empresa"
    tenant.description = new_description
    assert tenant.description == new_description


def test_setter_description_validation(tenant):
    """Testa a validação do setter para a descrição da empresa."""
    with pytest.raises(DomainValidationError):
        tenant.description = ""
    with pytest.raises(DomainValidationError):
        tenant.description = "   "
    with pytest.raises(DomainValidationError):
        tenant.description = "A" * 1001


def test_getter_logo(tenant):
    """Testa o getter para o logo da empresa."""
    assert tenant.logo == "https://example.com/logo.png"


def test_setter_logo(tenant):
    """Testa o setter para o logo da empresa."""
    new_logo = "http://example.com/novo_logo.png"
    tenant.logo = new_logo
    assert tenant.logo == new_logo


def test_setter_logo_validation(tenant):
    """Testa a validação do setter para o logo da empresa."""
    with pytest.raises(DomainValidationError):
        tenant.logo = ""
    with pytest.raises(DomainValidationError):
        tenant.logo = "   "


def test_getter_user_id(tenant, user_id):
    """Testa o getter para o user_id da empresa."""
    assert tenant.user_id == user_id


def test_setter_user_id(tenant):
    """Testa o setter para o user_id da empresa."""
    new_user_id = uuid4()
    tenant.user_id = new_user_id
    assert tenant.user_id == new_user_id


def test_setter_user_id_validation(tenant):
    """Testa a validação do setter para o user_id da empresa."""
    with pytest.raises(DomainValidationError):
        tenant.user_id = "1234"


def test_getter_is_active(tenant):
    """Testa o getter para o status ativo da empresa."""
    assert tenant.is_active is True


def test_setter_is_active(tenant):
    """Testa o setter para o status ativo da empresa."""
    with pytest.raises(DomainValidationError):
        tenant.is_active = "ativo"


def test_activate_tenant(tenant):
    """Testa a ativação da empresa."""
    tenant.activate()
    assert tenant.is_active is True


def test_deactivate_tenant(tenant):
    """Testa a desativação da empresa."""
    tenant.deactivate()
    assert tenant.is_active is False


def test_str(tenant):
    """Testa a representação em string da empresa."""
    expected_str = (
        f"Tenant(id={tenant.entity_id}),\n"
        f"name={tenant.name}, active={tenant.is_active})"
    )
    assert str(tenant) == expected_str
