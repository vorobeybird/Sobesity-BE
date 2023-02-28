from contextlib import contextmanager
from datetime import datetime

import pytest
import email_validator
from http_constants.headers import HttpHeaders

from sobesity.domain.entities import CreateUserEntity, UserEntity, UserFilter, UserId
from sobesity.webapp import create_app
from tests.factories import CreateUserFactory, UserEntityFactory

email_validator.TEST_ENVIRONMENT = True

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
    return CreateUserFactory()


@pytest.fixture
def user_factory():
    return UserEntityFactory

@pytest.fixture
def create_user_factory():
    return CreateUserFactory

@pytest.fixture
def user_entity():
    return UserEntityFactory()


@pytest.fixture
def created_user(user_service, user_for_create):
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

@pytest.fixture
def valid_user_create_body(user_for_create):
    return {
        "password": user_for_create.password,
        "nickname": user_for_create.nickname,
        "email": user_for_create.email,
        "firstName": user_for_create.first_name,
        "lastName": user_for_create.last_name,
    }

@pytest.fixture
def enable_email_validation():
    email_validator.TEST_ENVIRONMENT = False
    yield
    email_validator.TEST_ENVIRONMENT = True
