from typing import Optional

from sobesity.domain.entities import (
    QuestionTypeEntity,
    QuestionTypeFilterEnitity,
    QuestionTypeId,
)
from sobesity.domain.interfaces.repositories import ITypeRepository
from sobesity.domain.interfaces.services import ITypeService


class TypeService(ITypeService):
    def __init__(self, type_repository: ITypeRepository) -> None:
        self._type_repository = type_repository

    def get_list(
        self, type_filter: Optional[QuestionTypeFilterEnitity] = None
    ) -> list[QuestionTypeEntity]:
        return self._type_repository.get_list(type_filter)

    def batch_create(self, types: list[QuestionTypeEntity]) -> None:
        return self._type_repository.batch_create(types)

    def update(
        self, old_type: QuestionTypeEntity, update: QuestionTypeFilterEnitity
    ) -> list[QuestionTypeId]:
        return self._type_repository.update(old_type, update)

    def delete(self, type_ids: list[QuestionTypeId]) -> None:
        return self._type_repository.delete(type_ids)
