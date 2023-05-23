from abc import ABC, abstractclassmethod
from typing import Optional

from sobesity.domain.entities import LevelEntity, LevelilterEnitity, LevelId


class ILevelRepository(ABC):
    @abstractclassmethod
    def get_list(
        self, level_filter: Optional[LevelilterEnitity] = None
    ) -> list[LevelEntity]:
        pass

    @abstractclassmethod
    def batch_create(self, skills: list[LevelEntity]) -> None:
        pass

    @abstractclassmethod
    def update(
        self, old_level: LevelEntity, update: LevelilterEnitity
    ) -> list[LevelId]:
        pass

    @abstractclassmethod
    def delete(self, level_ids: list[LevelId]) -> None:
        pass
