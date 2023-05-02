from dataclasses import dataclass
from typing import NewType, Optional

TypeId = NewType("TypeId", int)


@dataclass
class TypeEntity:
    type_id: Optional[TypeId]
    name: str


@dataclass
class TypeFilterEnitity:
    type_ids: Optional[list[TypeId]] = None
    names: Optional[list[str]] = None
