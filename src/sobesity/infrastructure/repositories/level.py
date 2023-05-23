import logging
from dataclasses import asdict
from typing import Optional

from psycopg2.errors import UniqueViolation
from sqlalchemy import delete, insert, select, update
from sqlalchemy.exc import IntegrityError

from sobesity.domain.entities import LevelEntity, LevelFilterEnitity, LevelId
from sobesity.domain.exceptions import LevelNameUniqueViolation
from sobesity.domain.interfaces.repositories import ILevelRepository
from sobesity.infrastructure.constants import ModelFields
from sobesity.infrastructure.models import level_table
from sobesity.infrastructure.repositories.mapper import build_level_entity

logger = logging.getLogger(__name__)


class LevelRepository(ILevelRepository):
    def __init__(self, datasource) -> None:
        self.datasource = datasource

    def _patch_query(self, query, level_filter: LevelFilterEnitity):
        if level_filter.level_ids is not None:
            query = query.where(level_table.c.level_id.in_(level_filter.level_ids))
        if level_filter.names is not None:
            query = query.where(level_table.c.name.in_(level_filter.names))
        return query

    def get_list(
        self, level_filter: Optional[LevelFilterEnitity] = None
    ) -> list[LevelEntity]:
        query = select(level_table)

        logger.info("Going to get levels")
        if level_filter is not None:
            query = self._patch_query(query, level_filter)

        with self.datasource() as conn:
            result = conn.execute(query).fetchall()

        logger.info("Got Levels")
        return [build_level_entity(cur) for cur in result]

    def batch_create(self, levels: list[LevelEntity]) -> None:
        values = []
        for level in levels:
            level_value = asdict(level)
            level_value.pop(ModelFields.LEVEL_ID)
            values.append(level_value)

        query = insert(level_table).values(values)
        with self.datasource() as conn:
            try:
                conn.execute(query)
            except IntegrityError as exc:
                if isinstance(exc.orig, UniqueViolation):
                    logger.exception(exc)
                    raise LevelNameUniqueViolation()

    def update(
        self,
        to_set: LevelEntity,
        where: LevelFilterEnitity,
    ) -> list[LevelId]:
        query = update(level_table)

        query = self._patch_query(query, where)
        query = query.values({"name": to_set.name}).returning(level_table.c.level_id)

        with self.datasource() as conn:
            result = conn.execute(query)
        return [LevelId(res.level_id) for res in result]

    def delete(self, level_ids: list[LevelId]) -> None:
        query = delete(level_table).where(level_table.c.level_id.in_(level_ids))

        with self.datasource() as conn:
            conn.execute(query)
