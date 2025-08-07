"""Tipos de Status de Documento."""

from enum import Enum


class DocumentStatus(Enum):
    """Status de um Documento.

    Values:
        DRAFT: Documento em rascunho.
        PUBLISHED: Documento publicado.
        ARCHIVED: Documento arquivado.
        DELETED: Documento excluído.
    """

    DRAFT = "Rascunho"
    PUBLISHED = "Publicado"
    ARCHIVED = "Arquivado"
    DELETED = "Excluído"

    def __str__(self):
        return self.value
