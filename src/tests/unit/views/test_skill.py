from sobesity.domain.entities import SkillEntity
from sobesity.domain.exceptions.skill import SkillNameUniqueViolation


def test_get__no_data__return_empty(client, mock_skill_repository, auth_header):
    mock_skill_repository.get_list.return_value = []

    response = client.get("/api/skill", headers=auth_header)
    assert response.status_code == 200
    assert response.json == []


def test_get__has_data__return_data(client, mock_skill_repository, auth_header):
    expected_json = [
        {"name": "Python", "skill_id": 10},
        {"name": "JavaScript", "skill_id": 15},
    ]
    skills = [SkillEntity(**data) for data in expected_json]
    mock_skill_repository.get_list.return_value = skills
    response = client.get("/api/skill", headers=auth_header)
    assert response.status_code == 200
    assert response.json == expected_json


def test_create(client, mock_skill_repository, auth_header):
    body = [{"name": "Ruby"}]
    response = client.post("/api/skill", json=body, headers=auth_header)

    assert response.status_code == 201
    assert mock_skill_repository.batch_create.called


def test_detele(client, mock_skill_repository, auth_header):
    body = {"skillIds": [1, 2, 3, 4]}
    response = client.delete("/api/skill", json=body, headers=auth_header)

    assert response.status_code == 204
    assert mock_skill_repository.delete.called


def test_update(client, mock_skill_repository, auth_header):
    skill_id = 10
    body = {"skillId": skill_id, "name": "Rust"}
    expected_affected_ids = [skill_id]
    mock_skill_repository.update.return_value = expected_affected_ids
    response = client.patch("/api/skill", json=body, headers=auth_header)

    assert response.status_code == 200
    assert mock_skill_repository.update.called
    assert response.json == expected_affected_ids


def test_create__unique_constraint_return_400(
    client, mock_skill_repository, auth_header
):
    mock_skill_repository.batch_create.side_effect = SkillNameUniqueViolation()
    body = [{"name": "Ruby"}]
    response = client.post("/api/skill", json=body, headers=auth_header)

    assert response.status_code == 400
