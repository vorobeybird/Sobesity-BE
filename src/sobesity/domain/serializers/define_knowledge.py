from pydantic import BaseModel


class AnswerSerializer(BaseModel):
    answer: str
    right: bool


class DefineKnowledgeSerializer(BaseModel):
    question: str
    type: str
    code: str
    answers: list[AnswerSerializer]


class ThemeQuery(BaseModel):
    theme: str
    level: str


class ScoringBody(BaseModel):
    question_with_list_answer: dict[int, list[int]]


class ScoringSerializer(BaseModel):
    percent: float
