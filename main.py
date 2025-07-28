from uuid import uuid4

from src.core.domain.entities.document import Document
from src.core.domain.events.document import DocumentUpdatedEvent
from src.core.domain.value_objects.doc_types import DocumentType

doc = Document(
    title="Sample Document", document_type=DocumentType.REPORT, user_id=uuid4()
)
print(doc.title)

try:
    doc.update("title", 123, DocumentUpdatedEvent)
    print("Document updated successfully.")
except AttributeError as e:
    print(f"[AtributeError]: {e}")
except TypeError as e:
    print(f"[TypeError]: {e}")


print(doc.title)
