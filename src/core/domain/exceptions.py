"""Exceções do domínio."""


class DocumentNotFoundException(Exception):
    """Exceção lançada quando um documento não é encontrado."""


class DocumentAlreadyExistsException(Exception):
    """Exceção lançada quando um documento já existe."""


class InvalidDocumentTypeException(Exception):
    """Exceção lançada quando o tipo de documento é inválido."""


class DocumentUpdateAttrException(AttributeError):
    """Exceção lançada quando ocorre um erro ao atualizar um documento."""


class DocumentTypeException(TypeError):
    """
    Exceção lançada quando o tipo de dado do atributo a ser atualizado
    é inválido.
    """
