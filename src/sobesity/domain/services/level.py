from typing import Optional

from sobesity.domain.entities import LevelEntity, LevelFilterEnitity, LevelId
from sobesity.domain.exceptions import LevelNotExistViolation
from sobesity.domain.interfaces.repositories import ILevelRepository
from sobesity.domain.interfaces.services import ILevelService


class LevelService(ILevelService):
    def __init__(self, level_repository: ILevelRepository) -> None:
        self._level_repository = level_repository

    def get_one(self, level_filter: Optional[LevelFilterEnitity] = None):
        levels = self.get_list(level_filter)
        if not levels:
            raise LevelNotExistViolation(level_filter)
        return levels[0]

    def get_list(
        self, level_filter: Optional[LevelFilterEnitity] = None
    ) -> list[LevelEntity]:
        return self._level_repository.get_list(level_filter)

    def batch_create(self, levels: list[LevelEntity]) -> None:
        return self._level_repository.batch_create(levels)

    def update(
        self, old_level: LevelEntity, update: LevelFilterEnitity
    ) -> list[LevelId]:
        return self._level_repository.update(old_level, update)

    def delete(self, level_ids: list[LevelId]) -> None:
        return self._level_repository.delete(level_ids)
