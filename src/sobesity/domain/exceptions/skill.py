from sobesity.domain.entities import SkillId
from sobesity.domain.exceptions.base import DomainException, EntityNotFound


class SkillNameUniqueViolation(DomainException):
    def __init__(self) -> None:
        self.message = "Skill names must be unique"
        super().__init__(self.message)
