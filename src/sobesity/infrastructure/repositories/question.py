import logging
from dataclasses import asdict
from typing import Optional

from sqlalchemy import delete, insert, select, update
from sqlalchemy.exc import IntegrityError

from sobesity.domain.entities import QuestionEntity, QuestionFilterEnitity, QuestionId
from sobesity.domain.exceptions import (
    LevelNotExistViolation,
    SkillExistViolation,
    TypeNotExist,
)
from sobesity.domain.interfaces import IQuestionRepository
from sobesity.infrastructure.constants import ModelFields
from sobesity.infrastructure.models import question_table
from sobesity.infrastructure.repositories.mapper import build_question_entity

logger = logging.getLogger(__name__)


class QuestionRepository(IQuestionRepository):
    def __init__(self, datasource) -> None:
        self.datasource = datasource

    def _patch_query(self, query, question_filter: QuestionFilterEnitity):
        if question_filter.question_ids is not None:
            query = query.where(
                question_table.c.question_id.in_(question_filter.question_ids)
            )
        if question_filter.questions is not None:
            query = query.where(
                question_table.c.question.in_(question_filter.questions)
            )
        if question_filter.skill_ids is not None:
            query = query.where(
                question_table.c.skill_id.in_(question_filter.skill_ids)
            )
        if question_filter.codes is not None:
            query = query.where(question_table.c.code.in_(question_filter.codes))
        if question_filter.level_ids is not None:
            query = query.where(
                question_table.c.level_id.in_(question_filter.level_ids)
            )
        if question_filter.type_ids is not None:
            query = query.where(question_table.c.type_id.in_(question_filter.type_ids))

        return query

    def get_list(
        self, question_filter: Optional[QuestionFilterEnitity] = None
    ) -> list[QuestionEntity]:
        query = select(question_table)

        if question_filter is not None:
            query = self._patch_query(query, question_filter)

        with self.datasource() as conn:
            result = conn.execute(query).fetchall()

        return [build_question_entity(cur) for cur in result]

    def batch_create(self, questions: list[QuestionEntity]) -> None:
        values = []
        for question in questions:
            question_value = asdict(question)
            question_value.pop(ModelFields.QUESTION_ID)
            values.append(question_value)

        query = insert(question_table).values(values)

        with self.datasource() as conn:
            try:
                conn.execute(query)
            except IntegrityError as exc:
                if 'table "skill"' in str(exc.orig):
                    logger.exception(exc)
                    raise SkillExistViolation()
                elif 'table "type"' in str(exc.orig):
                    logger.exception(exc)
                    raise TypeNotExist()
                elif 'table "level"' in str(exc.orig):
                    logger.exception(exc)
                    raise LevelNotExistViolation()
                raise

    def update(
        self,
        to_set: QuestionEntity,
        where: QuestionFilterEnitity,
    ) -> list[QuestionId]:
        query = update(question_table)

        query = self._patch_query(query, where)
        query = query.values(
            {
                "question": to_set.question,
                "skill_id": to_set.skill_id,
                "level_id": to_set.level_id,
                "type_id": to_set.type_id,
                "code": to_set.code,
            }
        ).returning(
            question_table.c.question_id,
            question_table.c.skill_id,
            question_table.c.level_id,
        )

        with self.datasource() as conn:
            try:
                result = conn.execute(query)
            except IntegrityError as exc:
                if 'table "skill"' in str(exc.orig):
                    logger.exception(exc)
                    raise SkillExistViolation()
                elif 'table "type"' in str(exc.orig):
                    logger.exception(exc)
                    raise TypeNotExist()
                elif 'table "level"' in str(exc.orig):
                    logger.exception(exc)
                    raise LevelNotExistViolation()
            return [QuestionId(res.question_id) for res in result]

    def delete(self, question_ids: list[QuestionId]) -> None:
        query = delete(question_table).where(
            question_table.c.question_id.in_(question_ids)
        )

        with self.datasource() as conn:
            conn.execute(query)
