from contextlib import contextmanager
from datetime import datetime

import pytest

from sobesity.domain.entities import CreateUserEntity, UserEntity
from sobesity.domain.entities.user import UserId
from sobesity.webapp import create_app


@pytest.fixture
def di(app):
    return app.container


@pytest.fixture(autouse=True)
def db(di):
    with di.resources.datasource()() as connection:

        @contextmanager
        def rollback_conn():
            yield connection

        yield di.resources.datasource.override(rollback_conn)

        connection.rollback()


@pytest.fixture
def app():
    app = create_app()
    yield app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def user_for_create():
    return CreateUserEntity(
        nickname="someuser1",
        email="valid@test.com",
        password="Foo#boo2",
    )


@pytest.fixture
def user_entity():
    return UserEntity(
        user_id=UserId(4),
        nickname="someuser1",
        email="valid@test.com",
        registered_at=datetime(2023, 2, 2, 17, 47, 25),
        hashed_password="$2b$12$yEadIhUHE2FrG9UPoacMQuNvH6CpEha4QjNEFaM2zzkRvVd1ly686",
        salt="$2b$12$yEadIhUHE2FrG9UPoacMQu",
    )
