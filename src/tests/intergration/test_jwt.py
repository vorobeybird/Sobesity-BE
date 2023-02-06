from sobesity.domain.entities.user import UserId
from sobesity.jwt import encode_jwt, get_user_id_from_jwt


def test_jwt_encode_decode__pass():
    user_id = UserId(12345)
    token = encode_jwt(user_id)
    assert get_user_id_from_jwt(token) == user_id
