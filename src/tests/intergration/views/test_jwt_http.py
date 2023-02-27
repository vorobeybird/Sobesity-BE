from datetime import datetime, timedelta
from http import HTTPStatus

from freezegun import freeze_time
from http_constants.headers import HttpHeaders


def test_outdated_token(client, auth_header):
    with freeze_time(datetime.now()) as frozen_time:
        response = client.get("api/skill", headers=auth_header)
        assert response.status_code == HTTPStatus.OK

        frozen_time.move_to(datetime.now() + timedelta(days=60))
        response = client.get("api/skill", headers=auth_header)
        assert response.status_code == HTTPStatus.UNAUTHORIZED


def test_corrupted_token(client, auth_header):
    response = client.get("api/skill", headers=auth_header)
    assert response.status_code == HTTPStatus.OK

    auth_header[HttpHeaders.AUTHORIZATION] = auth_header[HttpHeaders.AUTHORIZATION][:-2]
    response = client.get("api/skill", headers=auth_header)
    assert response.status_code == HTTPStatus.UNAUTHORIZED

    auth_header[HttpHeaders.AUTHORIZATION] = (
        auth_header[HttpHeaders.AUTHORIZATION] + "OO"
    )
    response = client.get("api/skill", headers=auth_header)
    assert response.status_code == HTTPStatus.UNAUTHORIZED
