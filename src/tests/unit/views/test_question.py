from http import HTTPStatus

import pytest


def test_get__no_data__return_empty(client, mock_question_repository, auth_header):
    mock_question_repository.get_list.return_value = []

    response = client.get("/api/question", headers=auth_header)
    assert response.status_code == HTTPStatus.OK
    assert response.json == []


def test_get__has_data__return_data(
    client, mock_question_repository, auth_header, questions
):
    expected_json = [question.to_dict() for question in questions]
    mock_question_repository.get_list.return_value = questions
    response = client.get("/api/question", headers=auth_header)
    assert response.status_code == HTTPStatus.OK
    assert response.json == expected_json


def test_get_by_id__not_found__return_404(
    client, mock_question_repository, auth_header
):
    mock_question_repository.get_list.return_value = []

    response = client.get("/api/question/123", headers=auth_header)
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_get__by_id__return_question(
    client, mock_question_repository, auth_header, question
):
    mock_question_repository.get_list.return_value = [question]

    response = client.get("/api/question/123", headers=auth_header)

    question.answers = []
    expected = question.to_dict()
    assert response.status_code == HTTPStatus.OK
    assert response.json == expected


def test_question_create(client, mock_question_repository, auth_header):
    body = [
        {
            "question": "What",
            "skill_id": 1,
            "type_id": 1,
            "code": "smt='hello' print('smt')",
            "level_id": 1,
        }
    ]
    response = client.post("/api/question", json=body, headers=auth_header)

    assert response.status_code == HTTPStatus.CREATED
    assert mock_question_repository.batch_create.called


@pytest.mark.xfail
def test_question_delete(client, mock_question_repository, auth_header):
    body = {"questionIds": [1, 2, 3, 4]}
    response = client.delete("/api/question", json=body, headers=auth_header)

    assert response.status_code == HTTPStatus.NO_CONTENT
    assert mock_question_repository.delete.called


def test_question_update(client, mock_question_repository, auth_header):
    question_id = 10
    body = {
        "question": "string",
        "questionId": question_id,
        "code": "smt='hello' print('smt')",
    }
    expected_affected_ids = [question_id]
    mock_question_repository.update.return_value = expected_affected_ids

    breakpoint()
    response = client.patch("/api/question", json=body, headers=auth_header)

    assert response.status_code == HTTPStatus.OK
    assert mock_question_repository.update.called
    assert response.json == expected_affected_ids


def test_get__by_skill_id_return_data(
    client, mock_question_repository, auth_header, questions
):
    expected_json = [question.to_dict() for question in questions]
    mock_question_repository.get_list.return_value = questions
    response = client.get("/api/question/find_questions/123", headers=auth_header)
    assert response.status_code == HTTPStatus.OK
    assert response.json == expected_json
