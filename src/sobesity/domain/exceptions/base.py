class DomainException(Exception):
    message: str


class EntityNotFound(DomainException):
    pass
