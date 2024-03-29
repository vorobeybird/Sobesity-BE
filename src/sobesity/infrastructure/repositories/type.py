import logging
from dataclasses import asdict
from typing import Optional

from psycopg2.errors import UniqueViolation
from sqlalchemy import delete, insert, select, update
from sqlalchemy.exc import IntegrityError

from sobesity.domain.entities import TypeEntity, TypeFilterEnitity, TypeId
from sobesity.domain.exceptions import TypeNameUniqueViolation
from sobesity.domain.interfaces.repositories import ITypeRepository
from sobesity.infrastructure.constants import ModelFields
from sobesity.infrastructure.models import type_table
from sobesity.infrastructure.repositories.mapper import build_type_entity

logger = logging.getLogger(__name__)


class TypeRepository(ITypeRepository):
    def __init__(self, datasource) -> None:
        self.datasource = datasource

    def _patch_query(self, query, type_filter: TypeFilterEnitity):
        if type_filter.type_ids is not None:
            query = query.where(type_table.c.type_id.in_(type_filter.type_ids))
        if type_filter.names is not None:
            query = query.where(type_table.c.name.in_(type_filter.names))
        return query

    def get_list(
        self, type_filter: Optional[TypeFilterEnitity] = None
    ) -> list[TypeEntity]:
        query = select(type_table)

        logger.info("Going to get types")
        if type_filter is not None:
            query = self._patch_query(query, type_filter)

        with self.datasource() as conn:
            result = conn.execute(query).fetchall()

        logger.info("Got Types")
        return [build_type_entity(cur) for cur in result]

    def batch_create(self, types: list[TypeEntity]) -> None:
        values = []
        for type in types:
            type_value = asdict(type)
            type_value.pop(ModelFields.TYPE_ID)
            values.append(type_value)

        query = insert(type_table).values(values)
        with self.datasource() as conn:
            try:
                conn.execute(query)
            except IntegrityError as exc:
                if isinstance(exc.orig, UniqueViolation):
                    logger.exception(exc)
                    raise TypeNameUniqueViolation()

    def update(
        self,
        to_set: TypeEntity,
        where: TypeFilterEnitity,
    ) -> list[TypeId]:
        query = update(type_table)

        query = self._patch_query(query, where)
        query = query.values({"name": to_set.name}).returning(type_table.c.type_id)

        with self.datasource() as conn:
            result = conn.execute(query)
        return [TypeId(res.type_id) for res in result]

    def delete(self, type_ids: list[TypeId]) -> None:
        query = delete(type_table).where(type_table.c.type_id.in_(type_ids))

        with self.datasource() as conn:
            conn.execute(query)
