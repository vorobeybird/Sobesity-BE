from abc import ABC, abstractclassmethod
from typing import Optional

from sobesity.domain.entities import (
    QuestionTypeEntity,
    QuestionTypeFilterEnitity,
    QuestionTypeId,
)


class ITypeRepository(ABC):
    @abstractclassmethod
    def get_list(
        self, type_filter: Optional[QuestionTypeFilterEnitity] = None
    ) -> list[QuestionTypeEntity]:
        pass

    @abstractclassmethod
    def batch_create(self, types: list[QuestionTypeEntity]) -> None:
        pass

    @abstractclassmethod
    def update(
        self, old_type: QuestionTypeEntity, update: QuestionTypeFilterEnitity
    ) -> list[QuestionTypeId]:
        pass

    @abstractclassmethod
    def delete(self, type_ids: list[QuestionTypeId]) -> None:
        pass
