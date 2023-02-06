from copy import deepcopy

from sobesity.domain.entities.user import UserFilter
from sobesity.domain.exceptions import UserNotFound


def test_get_user_by_filter__not_found__return_404(client, mock_user_service):
    mock_user_service.get_user.side_effect = UserNotFound(UserFilter(user_id=11))
    response = client.get("api/user?userId=11")
    assert response.status_code == 404

    response = client.get("api/user?email=some@email.com")
    assert response.status_code == 404

    response = client.get("api/user?nickname=sad")
    assert response.status_code == 404


def test_create_user__valid_body__return_201(client, valid_user_create_body):
    response = client.post("api/user", json=valid_user_create_body)
    assert response.status_code == 201


def test_create_user__invalid_body__return_422(client, valid_user_create_body):
    invalid_body_incorrect_email = deepcopy(valid_user_create_body)
    invalid_body_incorrect_email["email"] = "no_domain"
    response = client.post("api/user", json=invalid_body_incorrect_email)
    assert response.status_code == 422

    fields_to_exclude = ["password", "email", "nickname"]
    for field_to_exclude in fields_to_exclude:
        invalid_body = deepcopy(valid_user_create_body)
        invalid_body.pop(field_to_exclude)
        response = client.post("api/user", json=invalid_body)
        assert response.status_code == 422
