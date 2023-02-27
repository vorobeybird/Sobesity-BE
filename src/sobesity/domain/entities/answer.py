from dataclasses import dataclass
from typing import NewType, Optional

AnswerId = NewType("AnswerId", int)


@dataclass
class AnswerEntity:
    answer_id: AnswerId
    answer: str


@dataclass
class AnswerFilterEnitity:
    answers_ids: Optional[list[AnswerId]] = None
    answers: Optional[list[str]] = None