from sobesity.domain.exceptions.base import DomainException


class InvalidEmail(DomainException):
    def __init__(self, email, debug_exc=None) -> None:
        self.message = f"{email} is invalid email"
        self.debug_exc = debug_exc
        super().__init__(self.message)
