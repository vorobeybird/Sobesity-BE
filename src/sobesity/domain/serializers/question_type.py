from pydantic import BaseModel, Field

from sobesity.domain.entities import (
    QuestionTypeEntity,
    QuestionTypeFilterEnitity,
    QuestionTypeId,
)

question_type_id_field = Field(..., alias="QuestionTypeId")


class QuestionTypeSerializer(BaseModel):
    question_type_id: QuestionTypeId = question_type_id_field
    name: str

    class Config:
        allow_population_by_field_name = True

    def to_domain(self) -> QuestionTypeEntity:
        return QuestionTypeEntity(type_id=self.question_type_id, name=self.name)

    @classmethod
    def from_domain(cls, type: QuestionTypeEntity):
        return cls(
            typeId=type.skill_id,
            name=type.name,
        )


class QuestionTypeBodyElem(BaseModel):
    name: str

    def to_domain(self) -> QuestionTypeEntity:
        return QuestionTypeEntity(type_id=None, name=self.name)


class PostQuestionTypeBody(BaseModel):
    __root__: list[QuestionTypeBodyElem]

    def to_domain(self) -> list[QuestionTypeEntity]:
        return [type.to_domain() for type in self.__root__]


class GetQuestionTypes(BaseModel):
    __root__: list[QuestionTypeSerializer]


class PathQuestionTypeId(BaseModel):
    question_type_id: QuestionTypeId = question_type_id_field

    def to_domain(self) -> QuestionTypeId:
        return QuestionTypeId(self.question_type_id)


class QuestionTypeIdsSerializer(BaseModel):
    question_type_ids: list[QuestionTypeId] = Field(..., alias="typeIds")

    def to_domain(self) -> list[QuestionTypeId]:
        return [
            QuestionTypeId(question_type_id)
            for question_type_id in self.question_type_ids
        ]


class DeleteQuestionTypeBody(QuestionTypeIdsSerializer):
    pass


class PatchQuestionTypeBody(BaseModel):
    question_type_id: QuestionTypeId = question_type_id_field
    name: str

    def get_to_set(self):
        return QuestionTypeEntity(type_id=None, name=self.name)

    def get_where(self) -> list[QuestionTypeFilterEnitity]:
        return QuestionTypeFilterEnitity(type_ids=[self.question_type_id])
