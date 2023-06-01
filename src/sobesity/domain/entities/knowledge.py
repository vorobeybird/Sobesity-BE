from dataclasses import dataclass
from typing import NewType, Optional

KnowledgeId = NewType("KnowledgeId", int)


@dataclass
class KnowledgeEntity:
    knowledge_id: KnowledgeId
    user_id: int
    level_id: int
    skill_id: int


@dataclass
class KnowledgeFilterEnitity:
    knowledge_ids: Optional[list[KnowledgeId]] = None
    user_ids: Optional[list[int]] = None
    level_ids: Optional[list[int]] = None
    skill_ids: Optional[list[int]] = None
