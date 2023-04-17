from sobesity.domain.exceptions.base import DomainException


class TypeNameUniqueViolation(DomainException):
    def __init__(self) -> None:
        self.message = "Types names must be unique"
        super().__init__(self.message)


class TypeExistViolation(Exception):
    def __init__(self) -> None:
        self.message = "Type not exist"
        super().__init__(self.message)
