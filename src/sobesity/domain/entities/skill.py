from dataclasses import dataclass
from typing import NewType, Optional

SkillId = NewType("SkillId", int)


@dataclass
class SkillEntity:
    skill_id: Optional[SkillId]
    name: str


@dataclass
class SkillFilterEnitity:
    skill_ids: Optional[list[SkillId]] = None
    names: Optional[list[str]] = None
