from sobesity.domain.entities import UserFilter
from sobesity.domain.exceptions.base import DomainException, EntityNotFound


class InvalidEmail(DomainException):
    def __init__(self, email, debug_exc=None) -> None:
        self.debug_exc = debug_exc
        self.message = f"{email} is invalid email."
        if debug_exc is not None:
            self.message = f"{self.message} Reason: {debug_exc.args[0]}"
        super().__init__(self.message)


class UserNotFound(EntityNotFound):
    def __init__(self, search_params: UserFilter) -> None:
        self.message = f"User not found with params ({search_params})"
        self.search_params = search_params
        super().__init__(self.message)


class PasswordNotMatch(DomainException):
    def __init__(self) -> None:
        self.message = "Password doesn't match"
        super().__init__(self.message)


class EmailNotExists(DomainException):
    def __init__(self, email: str) -> None:
        self.message = f"Email ({email}) doesn't exists"
        super().__init__(self.message)
