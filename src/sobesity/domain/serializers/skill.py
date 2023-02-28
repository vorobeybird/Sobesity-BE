from pydantic import BaseModel, Field

from sobesity.domain.entities.skill import (SkillEntity, SkillFilterEnitity,
                                            SkillId)

skill_id_field = Field(..., alias="skillId")


class SkillSerializer(BaseModel):
    skill_id: SkillId = skill_id_field
    name: str

    def to_domain(self) -> SkillEntity:
        return SkillEntity(skill_id=self.skill_id, name=self.name)


class SkillBodyElem(BaseModel):
    name: str

    def to_domain(self) -> SkillEntity:
        return SkillEntity(skill_id=None, name=self.name)


class PostSkillBody(BaseModel):
    __root__: list[SkillBodyElem]

    def to_domain(self) -> list[SkillEntity]:
        return [skill.to_domain() for skill in self.__root__]


class GetSkills(BaseModel):
    __root__: list[SkillSerializer]


class PathSkillId(BaseModel):
    skill_id: SkillId = skill_id_field

    def to_domain(self) -> SkillId:
        return SkillId(self.skill_id)


class SkillIdsSerializer(BaseModel):
    skill_ids: list[SkillId] = Field(..., alias="skillIds")

    def to_domain(self) -> list[SkillId]:
        return [SkillId(skill_id) for skill_id in self.skill_ids]


class DeleteSkillBody(SkillIdsSerializer):
    pass


class PatchSkillBody(BaseModel):
    skill_id: SkillId = skill_id_field
    name: str

    def get_to_set(self):
        return SkillEntity(skill_id=None, name=self.name)

    def get_where(self) -> list[SkillFilterEnitity]:
        return SkillFilterEnitity(skill_ids=[self.skill_id])
