from dataclasses import asdict
from datetime import datetime

from psycopg2.errors import UniqueViolation
from sqlalchemy import insert, select
from sqlalchemy.exc import IntegrityError

from sobesity.domain.entities import UserEntity, UserFilter
from sobesity.domain.exceptions import (
    EmailUniqueViolation,
    NicknameUniqueViolation,
    UserNotFound,
)
from sobesity.domain.interfaces.repositories import IUserRepository
from sobesity.infrastructure.constants import ModelFields
from sobesity.infrastructure.models import user_table
from sobesity.infrastructure.repositories.mapper import build_user_entity


class UserRepository(IUserRepository):
    def __init__(self, datasource) -> None:
        self._datasource = datasource

    def _patch_query(self, query, user_filter: UserFilter):
        if user_filter.user_id:
            query = query.where(user_table.c.user_id == user_filter.user_id)
        if user_filter.email:
            query = query.where(user_table.c.email == user_filter.email)
        if user_filter.nickname:
            query = query.where(user_table.c.nickname == user_filter.nickname)
        return query

    def create_user(self, user: UserEntity) -> None:
        values = asdict(user)
        values.pop(ModelFields.USER_ID)
        values[ModelFields.REGISTERED_AT] = datetime.now()

        query = insert(user_table).values(**values)
        with self._datasource() as conn:
            try:
                conn.execute(query)
            except IntegrityError as exc:
                if isinstance(exc.orig, UniqueViolation):
                    exc_message = exc.orig.args[0]
                    if "user_email_key" in exc_message:
                        raise EmailUniqueViolation()
                    if "nickname" in exc_message:
                        raise NicknameUniqueViolation()
                    raise

    def get_user(self, user_filter: UserFilter) -> UserEntity:
        query = self._patch_query(select(user_table), user_filter)

        with self._datasource() as conn:
            cursor = conn.execute(query).fetchone()

        if cursor is None:
            raise UserNotFound(user_filter)

        return build_user_entity(cursor)
