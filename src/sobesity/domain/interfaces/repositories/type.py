from abc import ABC, abstractclassmethod
from typing import Optional

from sobesity.domain.entities import TypeEntity, TypeFilterEnitity, TypeId


class ITypeRepository(ABC):
    @abstractclassmethod
    def get_list(
        self, type_filter: Optional[TypeFilterEnitity] = None
    ) -> list[TypeEntity]:
        pass

    @abstractclassmethod
    def batch_create(self, types: list[TypeEntity]) -> None:
        pass

    @abstractclassmethod
    def update(self, old_type: TypeEntity, update: TypeFilterEnitity) -> list[TypeId]:
        pass

    @abstractclassmethod
    def delete(self, type_ids: list[TypeId]) -> None:
        pass
