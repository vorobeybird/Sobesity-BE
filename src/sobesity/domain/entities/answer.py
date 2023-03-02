from dataclasses import dataclass
from typing import NewType, Optional

AnswerId = NewType("AnswerId", int)


@dataclass
class AnswerEntity:
    answer_id: AnswerId
    answer: str
    right: bool
    question_id: int


@dataclass
class AnswerFilterEnitity:
    answers_ids: Optional[list[AnswerId]] = None
    answers: Optional[list[str]] = None
    right: Optional[list[bool]] = None
    question_ids: Optional[list[int]] = None
