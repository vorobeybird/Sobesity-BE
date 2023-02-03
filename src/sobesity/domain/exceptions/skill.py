from sobesity.domain.exceptions.base import DomainException


class SkillNameUniqueViolation(DomainException):
    def __init__(self) -> None:
        self.message = "Skill names must be unique"
        super().__init__(self.message)
