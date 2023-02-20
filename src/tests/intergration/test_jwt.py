from datetime import datetime, timedelta

import pytest
from freezegun import freeze_time

from sobesity.domain.entities import UserId
from sobesity.domain.exceptions import CorruptedToken, ExpiredToken


def test_jwt__encode_decode__pass(jwt_resource):
    user_id = UserId(1111)
    token = jwt_resource.encode_jwt(user_id)
    assert jwt_resource.get_user_id_from_jwt(token) == user_id


def test_jwt__verify_jwt__corrupted_signature__raise_error(jwt_resource, jwt_token):
    jwt_token = jwt_token[:-2]
    with pytest.raises(CorruptedToken):
        jwt_resource.get_user_id_from_jwt(jwt_token)

    jwt_token = jwt_token + "4j"
    with pytest.raises(CorruptedToken):
        jwt_resource.get_user_id_from_jwt(jwt_token)


def test_jwt__verify_jwt__time_out__raise_error(jwt_resource, jwt_token):
    jwt_resource.get_user_id_from_jwt(jwt_token)

    with freeze_time(datetime.now()) as frozen_time:
        frozen_time.move_to(datetime.now() + timedelta(days=60))
        with pytest.raises(ExpiredToken):
            jwt_resource.get_user_id_from_jwt(jwt_token)
