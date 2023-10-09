from dataclasses import dataclass
from typing import NewType, Optional

from sobesity.domain.entities.base import BaseEntity

QuestionTypeId = NewType("QuestionTypeId", int)


@dataclass
class QuestionTypeEntity(BaseEntity):
    question_type_id: Optional[QuestionTypeId]
    name: str


@dataclass
class QuestionTypeFilterEnitity:
    question_type_ids: Optional[list[QuestionTypeId]] = None
    names: Optional[list[str]] = None
