from pydantic import BaseModel, Field

from sobesity.domain.entities.question import (
    QuestionEntity,
    QuestionFilterEnitity,
    QuestionId,
)

question_id_field = Field(..., alias="questionId")


class QuestionSerializer(BaseModel):
    question_id: QuestionId = question_id_field
    question: str
    type_id: int
    code: str
    skill_id: int

    def to_domain(self) -> QuestionEntity:
        return QuestionEntity(
            question_id=self.question_id,
            question=self.question,
            type_id=self.type_id,
            code=self.code,
            skill_id=self.skill_id,
        )

    @classmethod
    def from_domain(cls, question: QuestionEntity):
        return cls(
            questionId=question.question_id,
            question=question.question,
            type_id=question.type_id,
            code=question.code,
            skill_id=question.skill_id,
        )


class QuestionBodyElem(BaseModel):
    question: str
    type_id: int
    code: str
    skill_id: int

    def to_domain(self) -> QuestionEntity:
        return QuestionEntity(
            question_id=None,
            question=self.question,
            type_id=self.type_id,
            code=self.code,
            skill_id=self.skill_id,
        )


class PostQuestionBody(BaseModel):
    __root__: list[QuestionBodyElem]

    def to_domain(self) -> list[QuestionEntity]:
        return [question.to_domain() for question in self.__root__]


class GetQuestions(BaseModel):
    __root__: list[QuestionSerializer]


class PathQuestionId(BaseModel):
    question_id: QuestionId = question_id_field

    def to_domain(self) -> QuestionId:
        return QuestionId(self.question_id)


class QuestionIdsSerializer(BaseModel):
    question_ids: list[QuestionId] = Field(..., alias="questionIds")

    def to_domain(self) -> list[QuestionId]:
        return [QuestionId(question_id) for question_id in self.question_ids]


class DeleteQuestionBody(QuestionIdsSerializer):
    pass


class PatchQuestionBody(BaseModel):
    question_id: QuestionId = question_id_field
    question: str
    type_id: int
    code: str
    skill_id: int

    def get_to_set(self):
        return QuestionEntity(
            question_id=None,
            question=self.question,
            type_id=self.type_id,
            code=self.code,
            skill_id=self.skill_id,
        )

    def get_where(self) -> list[QuestionFilterEnitity]:
        return QuestionFilterEnitity(question_ids=[self.question_id])
