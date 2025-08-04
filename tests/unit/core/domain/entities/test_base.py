"Testes unitários para as entidades base do domínio."

import time
from datetime import datetime
from uuid import UUID, uuid4

from src.core.domain.entities.base import DomainEvent, Entity


class DummyEntity(Entity):
    """Classe concreta usada para testar Entity (por ser abstrata)."""


def test_entity_creation_with_specific_id():
    """Testa a criação de uma entidade com um ID específico."""
    uuid = uuid4()
    entity = DummyEntity(uuid, created_at=None, updated_at=None)
    assert entity.entity_id == uuid


def test_entity_creation_without_id():
    """Testa a criação de uma entidade sem um ID específico."""
    entity = DummyEntity(entity_id=None, created_at=None, updated_at=None)
    assert entity.entity_id is not None
    assert isinstance(entity.entity_id, UUID)


def test_entity_created_at():
    """Testa a data de criação da entidade."""
    entity = DummyEntity(entity_id=None, created_at=None, updated_at=None)
    now = datetime.now()
    delta = abs((now - entity.created_at).total_seconds())
    assert delta < 1  # tolerância de tempo


def test_entity_updated_at_initial():
    """Testa a data de atualização inicial da entidade."""
    entity = DummyEntity(
        entity_id=None, created_at=datetime.now(), updated_at=None
    )
    now = datetime.now()
    delta = abs((now - entity.updated_at).total_seconds())
    assert delta < 1  # tolerância


def test_entity_update_timestamp():
    """Testa a atualização do timestamp de modificação da entidade."""
    entity = DummyEntity(entity_id=None, created_at=None, updated_at=None)
    initial = entity.updated_at
    time.sleep(0.05)  # leve delay
    entity._update_timestamp()  # pylint: disable=protected-access
    assert entity.updated_at > initial


def test_entity_add_and_clear_domain_events():
    """Testa a adição e limpeza de eventos de domínio na entidade."""
    entity = DummyEntity(entity_id=None, created_at=None, updated_at=None)
    event = DomainEvent("example_event", {"key": "value"})

    entity.add_domain_event(event)
    assert len(entity.get_domain_events()) == 1
    assert entity.get_domain_events()[0] == event

    entity.clear_domain_events()
    assert not entity.get_domain_events()


def test_entity_equality_and_hashing():
    """Testa a igualdade e o hashing de entidades."""
    id_ = uuid4()
    entity1 = DummyEntity(entity_id=id_, created_at=None, updated_at=None)
    entity2 = DummyEntity(entity_id=id_, created_at=None, updated_at=None)
    entity3 = DummyEntity(entity_id=None, created_at=None, updated_at=None)

    assert entity1 == entity2
    assert entity1 != entity3
    assert hash(entity1) == hash(entity2)
    assert hash(entity1) != hash(entity3)


def test_entity_equality():
    """Testa a igualdade de entidades com o mesmo ID."""
    id_ = uuid4()
    entity1 = DummyEntity(entity_id=id_, created_at=None, updated_at=None)
    entity2 = DummyEntity(entity_id=id_, created_at=None, updated_at=None)
    entity3 = DummyEntity(entity_id=None, created_at=None, updated_at=None)

    assert entity1 == entity2
    assert entity1 != entity3
    assert entity1 != "string"


def test_entity_repr():
    """Testa a representação em string da entidade."""
    id_ = uuid4()
    entity = DummyEntity(entity_id=id_, created_at=None, updated_at=None)

    expected = f"DummyEntity(entity_id={id_})"
    assert repr(entity) == expected
