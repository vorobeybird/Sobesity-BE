import pytest

from sobesity.domain.entities import UserFilter
from sobesity.domain.exceptions import InvalidEmail


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
