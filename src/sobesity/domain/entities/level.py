from dataclasses import dataclass
from typing import NewType, Optional

LevelId = NewType("LevelId", int)


@dataclass
class LevelEntity:
    level_id: Optional[LevelId]
    name: str


@dataclass
class LevelFilterEnitity:
    level_ids: Optional[list[LevelId]] = None
    levels: Optional[list[str]] = None
