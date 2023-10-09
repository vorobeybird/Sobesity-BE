from pydantic import BaseModel, Field

from sobesity.domain.entities.level import LevelEntity, LevelFilterEnitity, LevelId

level_id_field = Field(..., alias="levelId")


class LevelSerializer(BaseModel):
    level_id: LevelId = level_id_field
    name: str

    class Config:
        allow_population_by_field_name = True

    def to_domain(self) -> LevelEntity:
        return LevelEntity(level_id=self.level_id, name=self.name)

    @classmethod
    def from_domain(cls, level: LevelEntity):
        return cls(
            levelId=level.level_id,
            name=level.name,
        )


class LevelBodyElem(BaseModel):
    name: str

    def to_domain(self) -> LevelEntity:
        return LevelEntity(level_id=None, name=self.name)


class PostLevelBody(BaseModel):
    __root__: list[LevelBodyElem]

    def to_domain(self) -> list[LevelEntity]:
        return [level.to_domain() for level in self.__root__]


class GetLevels(BaseModel):
    __root__: list[LevelSerializer]


class PathLevelId(BaseModel):
    level_id: LevelId = level_id_field

    def to_domain(self) -> LevelId:
        return LevelId(self.level_id)


class LevelIdsSerializer(BaseModel):
    level_ids: list[LevelId] = Field(..., alias="levelIds")

    def to_domain(self) -> list[LevelId]:
        return [LevelId(level_id) for level_id in self.level_ids]


class DeleteLevelBody(LevelIdsSerializer):
    pass


class PatchLevelBody(BaseModel):
    level_id: LevelId = level_id_field
    name: str

    def get_to_set(self):
        return LevelEntity(level_id=None, name=self.name)

    def get_where(self) -> list[LevelFilterEnitity]:
        return LevelFilterEnitity(level_ids=[self.level_id])
