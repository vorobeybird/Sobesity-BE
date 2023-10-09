from dataclasses import dataclass
from typing import NewType, Optional

from sobesity.domain.entities.base import BaseEntity

SkillId = NewType("SkillId", int)


@dataclass
class SkillEntity(BaseEntity):
    skill_id: Optional[SkillId]
    name: str


@dataclass
class SkillFilterEnitity:
    skill_ids: Optional[list[SkillId]] = None
    names: Optional[list[str]] = None
