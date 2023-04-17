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
from sobesity.infrastructure.repositories.mapper import build_skill_entity

logger = logging.getLogger(__name__)


class SkillRepository(ISkillRepository):
    def __init__(self, datasource) -> None:
        self.datasource = datasource

    def _patch_query(self, query, skill_filter: SkillFilterEnitity):
        if skill_filter.skill_ids is not None:
            query = query.where(skill_table.c.skill_id.in_(skill_filter.skill_ids))
        if skill_filter.names is not None:
            query = query.where(skill_table.c.name.in_(skill_filter.names))
        return query

    def get_list(
        self, skill_filter: Optional[SkillFilterEnitity] = None
    ) -> list[SkillEntity]:
        query = select(skill_table)

        logger.info("Going to get skills")
        if skill_filter is not None:
            query = self._patch_query(query, skill_filter)

        with self.datasource() as conn:
            result = conn.execute(query).fetchall()

        logger.info("Got Skills")
        return [build_skill_entity(cur) for cur in result]

    def batch_create(self, skills: list[SkillEntity]) -> None:
        values = []
        for skill in skills:
            skill_value = asdict(skill)
            skill_value.pop(ModelFields.SKILL_ID)
            values.append(skill_value)

        query = insert(skill_table).values(values)
        with self.datasource() as conn:
            try:
                conn.execute(query)
            except IntegrityError as exc:
                if isinstance(exc.orig, UniqueViolation):
                    logger.exception(exc)
                    raise SkillNameUniqueViolation()

    def update(
        self,
        to_set: SkillEntity,
        where: SkillFilterEnitity,
    ) -> list[SkillId]:
        query = update(skill_table)

        query = self._patch_query(query, where)
        query = query.values({"name": to_set.name}).returning(skill_table.c.skill_id)

        with self.datasource() as conn:
            result = conn.execute(query)
        return [SkillId(res.skill_id) for res in result]

    def delete(self, skill_ids: list[SkillId]) -> None:
        query = delete(skill_table).where(skill_table.c.skill_id.in_(skill_ids))

        with self.datasource() as conn:
            conn.execute(query)
