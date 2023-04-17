from typing import Optional

from sobesity.domain.entities import TypeEntity, TypeFilterEnitity, TypeId
from sobesity.domain.interfaces.repositories import ITypeRepository
from sobesity.domain.interfaces.services import ITypeService


class TypeService(ITypeService):
    def __init__(self, type_repository: ITypeRepository) -> None:
        self._type_repository = type_repository

    def get_list(
        self, type_filter: Optional[TypeFilterEnitity] = None
    ) -> list[TypeEntity]:
        return self._type_repository.get_list(type_filter)

    def batch_create(self, types: list[TypeEntity]) -> None:
        return self._type_repository.batch_create(types)

    def update(self, old_type: TypeEntity, update: TypeFilterEnitity) -> list[TypeId]:
        return self._type_repository.update(old_type, update)

    def delete(self, type_ids: list[TypeId]) -> None:
        return self._type_repository.delete(type_ids)
