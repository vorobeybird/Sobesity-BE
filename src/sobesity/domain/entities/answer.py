from dataclasses import dataclass
from typing import NewType, Optional

from sobesity.domain.entities.base import BaseEntity

AnswerId = NewType("AnswerId", int)


@dataclass
class AnswerEntity(BaseEntity):
    answer_id: AnswerId
    answer: str
    right: bool
    question_id: int


@dataclass
class AnswerFilterEnitity:
    answer_ids: Optional[list[AnswerId]] = None
    answers: Optional[list[str]] = None
    question_ids: Optional[list[int]] = None
