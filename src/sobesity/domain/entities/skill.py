from dataclasses import dataclass
from typing import NewType, Optional

SkillId = NewType("SkillId", int)


@dataclass
class SkillEntity:
    skill_id: SkillId
    name: str


@dataclass
class SkillFilterEnitity:
    skill_id: Optional[list[SkillId]] = None
    name: Optional[list[str]] = None
