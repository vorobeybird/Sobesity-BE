from pydantic import BaseModel, Field

from sobesity.domain.entities.answer import AnswerEntity, AnswerFilterEnitity, AnswerId

answer_id_field = Field(..., alias="AnswerId")

class AnswerSerializer(BaseModel):
    answer_id: AnswerId = answer_id_field
    answer: str
    right: bool
    question_id: int

    def to_domain(self) -> AnswerEntity:
        return AnswerEntity(
            answer_id=self.answer_id,
            answer=self.answer,
            right=self.right,
            question_id=self.question_id,
        )

    @classmethod
    def from_domain(cls, answer: AnswerEntity):
        return cls(
            answer_id=answer.answer_id,
            answer=answer.answer,
            right=answer.right,
            question_id=answer.question_id,
        )


class AnswerBodyElem(BaseModel):
    answer: str
    right: bool
    question_id: int

    def to_domain(self) -> AnswerEntity:
        return AnswerEntity(
            answer_id=None,
            answer=self.answer,
            right=self.right,
            question_id=self.question_id,
        )


class PostAnswerBody(BaseModel):
    __root__: list[AnswerBodyElem]

    def to_domain(self) -> list[AnswerEntity]:
        return [answer.to_domain() for answer in self.__root__]


class GetAnswers(BaseModel):
    __root__: list[AnswerSerializer]


class PathAnswerId(BaseModel):
    answer_id: AnswerId = answer_id_field

    def to_domain(self) -> AnswerId:
        return AnswerId(self.answer_id)


class AnswerIdsSerializer(BaseModel):
    answer_ids: list[AnswerId]

    def to_domain(self) -> list[AnswerId]:
        return [AnswerId(answer_id) for answer_id in self.answer_ids]


class DeleteAnswerBody(AnswerIdsSerializer):
    pass


class PatchAnswerBody(BaseModel):
    answer_id: AnswerId = answer_id_field
    answer: str
    right: bool
    question_id: int

    def get_to_set(self):
        return AnswerEntity(
            answer_id=None,
            answer=self.answer,
            right=self.right,
            question_id=self.question_id,
        )

    def get_where(self) -> list[AnswerFilterEnitity]:
        return AnswerFilterEnitity(answer_ids=[self.answer_id])
