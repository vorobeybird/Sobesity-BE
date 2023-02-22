from dataclasses import dataclass
from typing import NewType, Optional

QuestionId = NewType("QuestionId", int)


@dataclass
class QuestionEntity:
    question_id: QuestionId
    question: str