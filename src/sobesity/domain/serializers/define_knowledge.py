from pydantic import BaseModel, Field


class AnswerSerializer(BaseModel):
    answer: str
    right: bool


class DefineKnowledgeSerializer(BaseModel):
    question: str
    type: str
    answers: list[AnswerSerializer]


class ThemeQuery(BaseModel):
    theme: str
    level: str


class QuestionIdSerializer(BaseModel):
    question_id: int


class AnswerIdSerializer(BaseModel):
    answer_id: int


class ScoringQuery(BaseModel):
    question_with_list_answer: dict[QuestionIdSerializer, list[AnswerIdSerializer]]


class ScoringSerializer(BaseModel):
    percent: int
