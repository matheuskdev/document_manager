"""Testes"""

from uuid import uuid4

from src.core.domain.entities.document import Document
from src.core.domain.value_objects.doc_types import DocumentType

user_id = uuid4()
tenant_id = uuid4()

doc = Document(
    title="Documento de Exemplo",
    user_id=user_id,
    document_type=DocumentType.TUTORIAL,
    version=1,
    tenant_id=tenant_id,
)

print(doc.title)

try:
    doc.update_attribute("title", "o", user_id)
    print("Document updated successfully.")
except AttributeError as e:
    print(f"[AtributeError]: {e}")
except TypeError as e:
    print(f"[TypeError]: {e}")
