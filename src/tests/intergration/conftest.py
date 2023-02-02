import pytest

from sobesity.domain.entities import UserFilter


@pytest.fixture
def skill_repository(di):
    return di.repositories.skill()


@pytest.fixture
def user_service(di):
    return di.services.user()


@pytest.fixture
def created_user(user_service, user_for_create):
    user_service.create_user(user_for_create)
    return user_service.get_user(UserFilter(nickname=user_for_create.nickname))
