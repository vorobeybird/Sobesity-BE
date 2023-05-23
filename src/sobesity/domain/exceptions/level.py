from sobesity.domain.exceptions.base import DomainException


class LevelNameUniqueViolation(DomainException):
    def __init__(self) -> None:
        self.message = "Level names must be unique"
        super().__init__(self.message)


class LevelNotExistViolation(Exception):
    def __init__(self) -> None:
        self.message = "Level not exist"
        super().__init__(self.message)
