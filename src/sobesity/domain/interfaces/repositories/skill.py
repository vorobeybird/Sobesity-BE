from abc import ABC, abstractclassmethod
from typing import Optional

from sobesity.domain.entities import SkillEntity, SkillFilterEnitity, SkillId




class ISkillRepository(ABC):
    @abstractclassmethod
    def get_list(self, skill_filter: Optional[SkillFilterEnitity] = None) -> list[SkillEntity]:
        pass

    @abstractclassmethod
    def create(self, skill: SkillEntity) -> None:
        pass

    @abstractclassmethod
    def update(self, old_skill: SkillEntity, update: SkillFilterEnitity) -> list[SkillId]:
        pass

    @abstractclassmethod
    def delete(self, skill_id: SkillId) -> None:
        pass
