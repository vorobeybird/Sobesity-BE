import logging
from dataclasses import asdict
from typing import Optional

from sqlalchemy import delete, insert, select, update
from sqlalchemy.exc import IntegrityError

from sobesity.domain.entities import (
    KnowledgeEntity,
    KnowledgeFilterEnitity,
    KnowledgeId,
)
from sobesity.domain.exceptions import (
    LevelNotExistViolation,
    SkillExistViolation,
    UserNotExist,
    LevelNotExistViolation,
LevelNotFound,
)
from sobesity.domain.interfaces import IKnowledgeRepository
from sobesity.infrastructure.constants import ModelFields
from sobesity.infrastructure.models import knowledge_table
from sobesity.infrastructure.repositories.mapper import build_knowledge_entity

logger = logging.getLogger(__name__)


class KnowledgeRepository(IKnowledgeRepository):
    def __init__(self, datasource) -> None:
        self.datasource = datasource

    def _patch_query(self, query, knowledge_filter: KnowledgeFilterEnitity):
        if knowledge_filter.knowledge_ids is not None:
            query = query.where(
                knowledge_table.c.knowledge_id.in_(knowledge_filter.knowledge_ids)
            )
        if knowledge_filter.skill_ids is not None:
            query = query.where(
                knowledge_table.c.skill_id.in_(knowledge_filter.skill_ids)
            )
        if knowledge_filter.level_ids is not None:
            query = query.where(
                knowledge_table.c.level_id.in_(knowledge_filter.level_ids)
            )
        if knowledge_filter.user_ids is not None:
            query = query.where(
                knowledge_table.c.user_id.in_(knowledge_filter.user_ids)
            )

        return query

    def get_list(
        self, knowledge_filter: Optional[KnowledgeFilterEnitity] = None
    ) -> list[KnowledgeEntity]:
        query = select(knowledge_table)

        if knowledge_filter is not None:
            query = self._patch_query(query, knowledge_filter)

        with self.datasource() as conn:
            result = conn.execute(query).fetchall()

        return [build_knowledge_entity(cur) for cur in result]

    def batch_create(self, knowledges: list[KnowledgeEntity]) -> None:
        values = []
        for knowledge in knowledges:
            knowledge_value = asdict(knowledge)
            knowledge_value.pop(ModelFields.KNOWLEDGE_ID)
            values.append(knowledge_value)

        query = insert(knowledge_table).values(values)

        with self.datasource() as conn:
            try:
                conn.execute(query)
            except IntegrityError as exc:
                if 'table "skill"' in str(exc.orig):
                    logger.exception(exc)
                    raise SkillExistViolation()
                elif 'table "user"' in str(exc.orig):
                    logger.exception(exc)
                    raise UserNotExist()
                elif 'table "level"' in str(exc.orig):
                    logger.exception(exc)
                    raise LevelNotExistViolation()
                raise

    def update(
        self,
        to_set: KnowledgeEntity,
        where: KnowledgeFilterEnitity,
    ) -> list[KnowledgeId]:
        query = update(knowledge_table)

        query = self._patch_query(query, where)
        query = query.values(
            {
                "skill_id": to_set.skill_id,
                "level_id": to_set.level_id,
                "user_id": to_set.user_id,
            }
        ).returning(knowledge_table.c.knowledge_id)

        with self.datasource() as conn:
            try:
                result = conn.execute(query)
            except IntegrityError as exc:
                if 'table "skill"' in str(exc.orig):
                    logger.exception(exc)
                    raise SkillExistViolation()
                elif 'table "user"' in str(exc.orig):
                    logger.exception(exc)
                    raise UserNotExist()
                elif 'table "level"' in str(exc.orig):
                    logger.exception(exc)
                    raise LevelNotExistViolation()
            return [KnowledgeId(res.knowledge_id) for res in result]

    def delete(self, knowledge_ids: list[KnowledgeId]) -> None:
        query = delete(knowledge_table).where(
            knowledge_table.c.knowledge_id.in_(knowledge_ids)
        )

        with self.datasource() as conn:
            conn.execute(query)

    def get_level_for_user_or_skill(self, knowledge_filter: KnowledgeFilterEnitity) -> KnowledgeEntity:
        query = self._patch_query(select(knowledge_table), knowledge_filter)

        with self._datasource() as conn:
            cursor = conn.execute(query).fetchone()

        if cursor is None:
            raise LevelNotFound(knowledge_filter)

        return build_knowledge_entity(cursor)