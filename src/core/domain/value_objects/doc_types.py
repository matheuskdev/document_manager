"Tipos de documentos para o sistema de gerenciamento de documentos." ""

from enum import Enum


class DocumentType(Enum):
    """Enumeração para tipos de documentos.
    
    Values:
        REPORT: Relatório.
        CONTRACT: Contrato.
        PROTOCOL: Protocolo.
        POP: Procedimento Operacional Padrão.
        TUTORIAL: Tutorial.
        MANUAL: Manual.
        OTHER: Outro.
    """

    REPORT = "Relatório"
    CONTRACT = "Contrato"
    PROTOCOL = "Protocolo"
    POP = "POP"
    TUTORIAL = "Tutorial"
    MANUAL = "Manual"
    OTHER = "Outro"

    def __str__(self):
        return self.value
