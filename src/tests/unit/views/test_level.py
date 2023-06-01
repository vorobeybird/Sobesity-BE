from http import HTTPStatus

from sobesity.domain.exceptions import LevelNameUniqueViolation


def level_to_json(level):
    return {"name": level.name, "level_id": level.level_id}


def test_get__no_data__return_empty(client, mock_level_repository, auth_header):
    mock_level_repository.get_list.return_value = []

    response = client.get("/api/level", headers=auth_header)
    assert response.status_code == HTTPStatus.OK
    assert response.json == []


def test_get__has_data__return_data(client, mock_level_repository, auth_header, levels):
    expected_json = [level_to_json(level) for level in levels]
    mock_level_repository.get_list.return_value = levels
    response = client.get("/api/level", headers=auth_header)
    assert response.status_code == HTTPStatus.OK
    assert response.json == expected_json


def test_get_by_id__not_found__return_404(client, mock_level_repository, auth_header):
    mock_level_repository.get_list.return_value = []

    response = client.get("/api/level/123", headers=auth_header)
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_get__by_id__return_level(client, mock_level_repository, auth_header, level):
    mock_level_repository.get_list.return_value = [level]

    response = client.get("/api/level/123", headers=auth_header)
    assert response.status_code == HTTPStatus.OK
    assert response.json == level_to_json(level)


def test_create(client, mock_level_repository, auth_header):
    body = [{"name": "Junior"}]
    response = client.post("/api/level", json=body, headers=auth_header)

    assert response.status_code == HTTPStatus.CREATED
    assert mock_level_repository.batch_create.called


def test_detele(client, mock_level_repository, auth_header):
    body = {"levelIds": [1, 2, 3, 4]}
    response = client.delete("/api/level", json=body, headers=auth_header)

    assert response.status_code == HTTPStatus.NO_CONTENT
    assert mock_level_repository.delete.called


def test_update(client, mock_level_repository, auth_header):
    level_id = 10
    body = {"levelId": level_id, "name": "Batia"}
    expected_affected_ids = [level_id]
    mock_level_repository.update.return_value = expected_affected_ids
    response = client.patch("/api/level", json=body, headers=auth_header)

    assert response.status_code == HTTPStatus.OK
    assert mock_level_repository.update.called
    assert response.json == expected_affected_ids


def test_create__unique_constraint_return_400(
    client, mock_level_repository, auth_header
):
    mock_level_repository.batch_create.side_effect = LevelNameUniqueViolation()
    body = [{"name": "Batia"}]
    response = client.post("/api/level", json=body, headers=auth_header)

    assert response.status_code == HTTPStatus.BAD_REQUEST
