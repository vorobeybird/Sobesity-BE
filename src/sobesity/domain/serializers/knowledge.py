from pydantic import BaseModel, Field

from sobesity.domain.entities.knowledge import (
    KnowledgeEntity,
    KnowledgeFilterEnitity,
    KnowledgeId,
)

knowledge_id_field = Field(..., alias="knowledgeId")


class KnowledgeSerializer(BaseModel):
    knowledge_id: KnowledgeId = knowledge_id_field
    user_id: int
    skill_id: int
    level_id: int

    def to_domain(self) -> KnowledgeEntity:
        return KnowledgeEntity(
            knowledge_id=self.knowledge_id,
            user_id=self.user_id,
            skill_id=self.skill_id,
            level_id=self.level_id,
        )

    @classmethod
    def from_domain(cls, knowledge: KnowledgeEntity):
        return cls(
            knowledgeId=knowledge.knowledge_id,
            user_id=knowledge.user_id,
            skill_id=knowledge.skill_id,
            level_id=knowledge.level_id,
        )


class KnowledgeBodyElem(BaseModel):
    user_id: int
    skill_id: int
    level_id: int

    def to_domain(self) -> KnowledgeEntity:
        return KnowledgeEntity(
            knowledge_id=None,
            user_id=self.user_id,
            skill_id=self.skill_id,
            level_id=self.level_id,
        )


class PostKnowledgeBody(BaseModel):
    __root__: list[KnowledgeBodyElem]

    def to_domain(self) -> list[KnowledgeEntity]:
        return [knowledge.to_domain() for knowledge in self.__root__]


class GetKnowledges(BaseModel):
    __root__: list[KnowledgeSerializer]


class PathKnowledgeId(BaseModel):
    knowledge_id: KnowledgeId = knowledge_id_field

    def to_domain(self) -> KnowledgeId:
        return KnowledgeId(self.knowledge_id)


class KnowledgeIdsSerializer(BaseModel):
    knowledge_ids: list[KnowledgeId] = Field(..., alias="knowledgeIds")

    def to_domain(self) -> list[KnowledgeId]:
        return [KnowledgeId(knowledge_id) for knowledge_id in self.knowledge_ids]


class DeleteKnowledgeBody(KnowledgeIdsSerializer):
    pass


class PatchKnowledgeBody(BaseModel):
    knowledge_id: KnowledgeId = knowledge_id_field
    user_id: int
    skill_id: int
    level_id: int

    def get_to_set(self):
        return KnowledgeEntity(
            knowledge_id=None,
            user_id=self.user_id,
            skill_id=self.skill_id,
            level_id=self.level_id,
        )

    def get_where(self) -> list[KnowledgeFilterEnitity]:
        return KnowledgeFilterEnitity(knowledge_ids=[self.knowledge_id])