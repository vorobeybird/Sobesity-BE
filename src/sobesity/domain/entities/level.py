from dataclasses import dataclass
from typing import NewType, Optional

from sobesity.domain.entities.base import BaseEntity

LevelId = NewType("LevelId", int)


@dataclass
class LevelEntity(BaseEntity):
    level_id: Optional[LevelId]
    name: str


@dataclass
class LevelFilterEnitity:
    level_ids: Optional[list[LevelId]] = None
    names: Optional[list[str]] = None
