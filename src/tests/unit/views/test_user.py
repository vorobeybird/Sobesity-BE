from copy import deepcopy
from http import HTTPStatus

from sobesity.domain.entities.user import UserFilter
from sobesity.domain.exceptions import UserNotFound


def test_get_user_by_filter__not_found__return_404(client, mock_user_repository):
    response = client.get("api/user")
    assert response.status_code == HTTPStatus.BAD_REQUEST

    mock_user_repository.get_user.side_effect = UserNotFound(UserFilter(user_id=11))
    response = client.get("api/user?userId=11")
    assert response.status_code == HTTPStatus.NOT_FOUND

    response = client.get("api/user?email=some@email.com")
    assert response.status_code == HTTPStatus.NOT_FOUND

    response = client.get("api/user?nickname=sad")
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_create_user__invalid_body__return_422(client, valid_user_create_body):
    invalid_body_incorrect_email = deepcopy(valid_user_create_body)
    invalid_body_incorrect_email["email"] = "no_domain"
    response = client.post("api/user", json=invalid_body_incorrect_email)
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

    fields_to_exclude = ["password", "email", "nickname"]
    for field_to_exclude in fields_to_exclude:
        invalid_body = deepcopy(valid_user_create_body)
        invalid_body.pop(field_to_exclude)
        response = client.post("api/user", json=invalid_body)
        assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
