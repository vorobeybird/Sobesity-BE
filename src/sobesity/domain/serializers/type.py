from pydantic import BaseModel, Field

from sobesity.domain.entities.type import TypeEntity, TypeFilterEnitity, TypeId

type_id_field = Field(..., alias="TypeId")


class TypeSerializer(BaseModel):
    type_id: TypeId = type_id_field
    name: str

    def to_domain(self) -> TypeEntity:
        return TypeEntity(type_id=self.type_id, name=self.name)

    @classmethod
    def from_domain(cls, type: TypeEntity):
        return cls(
            typeId=type.skill_id,
            name=type.name,
        )


class TypeBodyElem(BaseModel):
    name: str

    def to_domain(self) -> TypeEntity:
        return TypeEntity(type_id=None, name=self.name)


class PostTypeBody(BaseModel):
    __root__: list[TypeBodyElem]

    def to_domain(self) -> list[TypeEntity]:
        return [type.to_domain() for type in self.__root__]


class GetTypes(BaseModel):
    __root__: list[TypeSerializer]


class PathTypeId(BaseModel):
    type_id: TypeId = type_id_field

    def to_domain(self) -> TypeId:
        return TypeId(self.type_id)


class TypeIdsSerializer(BaseModel):
    type_ids: list[TypeId] = Field(..., alias="typeIds")

    def to_domain(self) -> list[TypeId]:
        return [TypeId(type_id) for type_id in self.type_ids]


class DeleteTypeBody(TypeIdsSerializer):
    pass


class PatchTypeBody(BaseModel):
    type_id: TypeId = type_id_field
    name: str

    def get_to_set(self):
        return TypeEntity(type_id=None, name=self.name)

    def get_where(self) -> list[TypeFilterEnitity]:
        return TypeFilterEnitity(type_ids=[self.type_id])
