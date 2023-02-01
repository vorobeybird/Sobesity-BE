import pytest

from sobesity.domain.entities import CreateUserEntity


@pytest.fixture
def skill_repository(di):
    return di.repositories.skill()


@pytest.fixture
def user_service(di):
    return di.services.user()


@pytest.fixture
def user_for_create():
    return CreateUserEntity(
        nickname="someuser1",
        email="valid@test.com",
        password="Foo#boo2",
    )
