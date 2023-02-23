import pytest

from sobesity.domain.entities import UserFilter
from sobesity.domain.entities.user import CreateUserEntity
from sobesity.domain.exceptions import InvalidEmail
from sobesity.domain.exceptions import UserNotFound, NicknameUniqueViolation, EmailUniqueViolation


def test_create_user_valid_data__create_sucessfully(user_service, user_for_create):
    user_service.create_user(user_for_create)
    user = user_service.get_user(UserFilter(nickname=user_for_create.nickname))

    assert user.nickname == user_for_create.nickname
    assert user.email == user_for_create.email
    assert user.hashed_password != user_for_create.password


def test_create_user__invalid_email__raise_error(user_service, user_for_create):
    user_for_create.email = "totalinvalid_email"
    with pytest.raises(InvalidEmail):
        user_service.create_user(user_for_create)

    user_for_create.email = "invalid@dom.o"
    with pytest.raises(InvalidEmail):
        user_service.create_user(user_for_create)


def test_get_user__can_get_by_all_params__return_user(user_service, created_user):
    user_by_id = user_service.get_user(UserFilter(user_id=created_user.user_id))
    user_by_nickname = user_service.get_user(UserFilter(nickname=created_user.nickname))
    user_by_email = user_service.get_user(UserFilter(email=created_user.email))

    assert user_by_id == user_by_nickname == user_by_email == created_user

@pytest.mark.xfail
def test_create_user__same_email__raise_error(user_service, created_user, user_for_create, new_user):
    pass

@pytest.mark.xfail
def test_create_user__same_nickname__raise_error(user_service, created_user, user_for_create):
    pass
