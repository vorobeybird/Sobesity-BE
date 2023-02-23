class BaseException(Exception):
    message: str


class DomainException(BaseException):
    pass


class EntityNotFound(DomainException):
    pass


class AuthException(BaseException):
    pass
