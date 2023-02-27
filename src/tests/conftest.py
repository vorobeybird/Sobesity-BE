from contextlib import contextmanager
from datetime import datetime

import pytest
from http_constants.headers import HttpHeaders

from sobesity.domain.entities import CreateUserEntity, UserEntity, UserFilter, UserId
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
        first_name="Some",
        last_name="Userov",
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


@pytest.fixture
def created_user(user_service, user_for_create):
    # TODO replace with factory
    user_service.create_user(user_for_create)
    return user_service.get_user(UserFilter(nickname=user_for_create.nickname))


@pytest.fixture
def skill_repository(di):
    return di.repositories.skill()


@pytest.fixture
def user_service(di):
    return di.services.user()


@pytest.fixture
def login_body(created_user, user_for_create):
    return {"email": user_for_create.email, "password": user_for_create.password}


@pytest.fixture
def jwt_resource(di):
    return di.resources.jwt()


@pytest.fixture
def jwt_token(jwt_resource):
    user_id = UserId(1111)
    return jwt_resource.encode_jwt(user_id)


@pytest.fixture
def auth_header(jwt_token):
    return {HttpHeaders.AUTHORIZATION: f"Bearer {jwt_token}"}
