import pytest

from sobesity.domain.entities import UserId


@pytest.fixture
def jwt_token(jwt_resource):
    user_id = UserId(1111)
    return jwt_resource.encode_jwt(user_id)
