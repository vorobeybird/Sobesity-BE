import logging
from dataclasses import asdict
from typing import Optional

from psycopg2.errors import UniqueViolation
from sqlalchemy import delete, insert, select, update
from sqlalchemy.exc import IntegrityError

from sobesity.domain.entities import QuestionEntity, QuestionFilterEnitity, QuestionId
from sobesity.domain.exceptions import QuestionNameUniqueViolation
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
            query = query.where(question_table.c.question_id.in_(question_filter.question_ids))
        if question_filter.names is not None:
            query = query.where(question_table.c.name.in_(question_filter.names))
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
                if isinstance(exc.orig, UniqueViolation):
                    logger.exception(exc)
                    raise QuestionNameUniqueViolation()

    def update(
        self,
        to_set: QuestionEntity,
        where: QuestionFilterEnitity,
    ) -> list[QuestionId]:
        query = update(question_table)

        query = self._patch_query(query, where)
        query = query.values({"question": to_set.question}).returning(question_table.c.question_id)

        with self.datasource() as conn:
            result = conn.execute(query)
        return [QuestionId(res.question_id) for res in result]

    def delete(self, question_ids: list[QuestionId]) -> None:
        query = delete(question_table).where(question_table.c.question_id.in_(question_ids))

        with self.datasource() as conn:
            conn.execute(query)
