"""Tipos de Status de Documento."""

from enum import Enum


class DocumentStatus(Enum):
    """Status de um Documento."""

    DRAFT = "Rascunho"
    PUBLISHED = "Publicado"
    ARCHIVED = "Arquivado"
    DELETED = "Excluído"

    def __str__(self):
        return self.value
