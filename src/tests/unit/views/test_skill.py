import json

from sobesity.domain.entities import SkillEntity


def test_get__no_data__return_empty(client, mock_skill_repository):
    mock_skill_repository.get_list.return_value = []

    response = client.get("/api/skill")
    assert response.status_code == 200
    assert response.json == []


def test_get__has_data__return_data(client, mock_skill_repository):
    expected_json = [
        {"name": "Python", "skill_id": 10},
        {"name": "JavaScript", "skill_id": 15},
    ]
    skills = [SkillEntity(**data) for data in expected_json]
    mock_skill_repository.get_list.return_value = skills
    response = client.get("/api/skill")
    assert response.status_code == 200
    assert response.json == expected_json


def test_create(client, mock_skill_repository):
    body = [{"name": "Ruby"}]
    response = client.post("/api/skill", json=json.dumps(body))

    assert response.status_code == 201
    assert mock_skill_repository.batch_create.called


def test_detele(client, mock_skill_repository):
    body = {"skill_ids": [1, 2, 3, 4]}
    response = client.delete("/api/skill", json=json.dumps(body))

    assert response.status_code == 204
    assert mock_skill_repository.delete.called


def test_update(client, mock_skill_repository):
    skill_id = 10
    body = {"skill_id": skill_id, "name": "Rust"}
    expected_affected_ids = [skill_id]
    mock_skill_repository.update.return_value = expected_affected_ids
    response = client.patch("/api/skill", json=json.dumps(body))

    assert response.status_code == 200
    assert mock_skill_repository.update.called
    assert response.json == expected_affected_ids
