from typing import Optional

from sobesity.domain.entities import SkillEntity, SkillFilterEnitity, SkillId
from sobesity.domain.interfaces.repositories import ISkillRepository
from sobesity.domain.interfaces.services import ISkillService


class SkillService(ISkillService):
    def __init__(self, skill_repository: ISkillRepository) -> None:
        self._skill_repository = skill_repository

    def get_list(
        self, skill_filter: Optional[SkillFilterEnitity] = None
    ) -> list[SkillEntity]:
        return self._skill_repository.get_list(skill_filter)

    def batch_create(self, skills: list[SkillEntity]) -> None:
        return self._skill_repository.batch_create(skills)

    def update(
        self, old_skill: SkillEntity, update: SkillFilterEnitity
    ) -> list[SkillId]:
        return self._skill_repository.update(old_skill, update)

    def delete(self, skill_ids: list[SkillId]) -> None:
        return self._skill_repository.delete(skill_ids)
