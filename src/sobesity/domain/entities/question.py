from dataclasses import dataclass
from typing import NewType, Optional

QuestionId = NewType("QuestionId", int)


@dataclass
class QuestionEntity:
    question_id: QuestionId
    question: str
    type_id: int
    code: str
    skill_id: int


@dataclass
class QuestionFilterEnitity:
    question_ids: Optional[list[QuestionId]] = None
    questions: Optional[list[str]] = None
    skill_ids: Optional[list[int]] = None
    type_ids: Optional[list[int]] = None
