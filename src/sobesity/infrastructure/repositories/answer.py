import logging
from dataclasses import asdict
from typing import Optional

from psycopg2.errors import ForeignKeyViolation
from sqlalchemy import delete, insert, select, update
from sqlalchemy.exc import IntegrityError

from sobesity.domain.entities import AnswerEntity, AnswerFilterEnitity, AnswerId
from sobesity.domain.exceptions import QuestionExistViolation
from sobesity.domain.interfaces import IAnswerRepository
from sobesity.infrastructure.constants import ModelFields
from sobesity.infrastructure.models import answer_table
from sobesity.infrastructure.repositories.mapper import build_answer_entity

logger = logging.getLogger(__name__)


class AnswerRepository(IAnswerRepository):
    def __init__(self, datasource) -> None:
        self.datasource = datasource

    def _patch_query(self, query, answer_filter: AnswerFilterEnitity):
        if answer_filter.answer_ids is not None:
            query = query.where(answer_table.c.answer_id.in_(answer_filter.answer_ids))
        if answer_filter.answers is not None:
            query = query.where(answer_table.c.answer.in_(answer_filter.answers))
        if answer_filter.question_ids is not None:
            query = query.where(
                answer_table.c.question_id.in_(answer_filter.question_ids)
            )
        return query

    def get_list(
        self, answer_filter: Optional[AnswerFilterEnitity] = None
    ) -> list[AnswerEntity]:
        query = select(answer_table)

        if answer_filter is not None:
            query = self._patch_query(query, answer_filter)

        with self.datasource() as conn:
            result = conn.execute(query).fetchall()

        return [build_answer_entity(cur) for cur in result]

    def batch_create(self, answers: list[AnswerEntity]) -> None:
        values = []
        for answer in answers:
            answer_value = asdict(answer)
            answer_value.pop(ModelFields.ANSWER_ID)
            values.append(answer_value)

        query = insert(answer_table).values(values)
        with self.datasource() as conn:
            try:
                conn.execute(query)
            except IntegrityError as exc:
                if isinstance(exc.orig, ForeignKeyViolation):
                    logger.exception(exc)
                    raise QuestionExistViolation()

    def update(
        self,
        to_set: AnswerEntity,
        where: AnswerFilterEnitity,
    ) -> list[AnswerId]:
        query = update(answer_table)

        query = self._patch_query(query, where)
        query = query.values({"answer": to_set.answer,
                              "question_id": to_set.question_id,
                              "right": to_set.right}).returning(
            answer_table.c.answer_id,
            answer_table.c.question_id,
            answer_table.c.right
        )

        with self.datasource() as conn:
            result = conn.execute(query)
        return [AnswerId(res.answer_id) for res in result]

    def delete(self, answer_ids: list[AnswerId]) -> None:
        query = delete(answer_table).where(answer_table.c.answer_id.in_(answer_ids))

        with self.datasource() as conn:
            conn.execute(query)
