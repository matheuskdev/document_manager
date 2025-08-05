"Configuração de fixtures para testes unitários do core"

from datetime import datetime
from uuid import uuid4

import pytest

from src.core.domain.entities.document import Document
from src.core.domain.entities.tenant import Tenant
from src.core.domain.value_objects.doc_types import DocumentType


@pytest.fixture
def user_id():
    """Fixture para criar um usuário de teste."""
    return uuid4()


@pytest.fixture
def tenant(user_id):  # pylint: disable=redefined-outer-name
    """Fixture para criar um inquilino de teste."""
    return Tenant(
        name="Empresa de Teste",
        description="Empresa de Teste para Documentos",
        logo="https://example.com/logo.png",
        user_id=user_id,
        is_active=True,
        entity_id=uuid4(),
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )


@pytest.fixture
def docs(tenant, user_id):  # pylint: disable=redefined-outer-name
    """Fixture para criar um documento de teste."""
    return Document(
        title="Test Document",
        document_type=DocumentType.REPORT,
        user_id=user_id,
        tenant_id=tenant.entity_id,
    )
