from http import HTTPStatus


def question_to_json(question):
    return {"question": question.question, "skill_id": question.skill_id, "question_id": question.question_id}


def test_get__no_data__return_empty(client, mock_question_repository, auth_header):
    mock_question_repository.get_list.return_value = []

    response = client.get("/api/question", headers=auth_header)
    assert response.status_code == HTTPStatus.OK
    assert response.json == []


def test_get__has_data__return_data(client, mock_question_repository, auth_header, questions):
    expected_json = [question_to_json(question) for question in questions]
    mock_question_repository.get_list.return_value = questions
    response = client.get("/api/question", headers=auth_header)
    assert response.status_code == HTTPStatus.OK
    assert response.json == expected_json


def test_get_by_id__not_found__return_404(client, mock_question_repository, auth_header):
    mock_question_repository.get_list.return_value = []

    response = client.get("/api/question/123", headers=auth_header)
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_get__by_id__return_question(client, mock_question_repository, auth_header, question):
    mock_question_repository.get_list.return_value = [question]

    response = client.get("/api/question/123", headers=auth_header)
    assert response.status_code == HTTPStatus.OK
    assert response.json == question_to_json(question)


def test_create(client, mock_question_repository, auth_header):
    body = [{"question": "What", "skill_id": 1}]
    response = client.post("/api/question", json=body, headers=auth_header)

    assert response.status_code == HTTPStatus.CREATED
    assert mock_question_repository.batch_create.called


def test_delete(client, mock_question_repository, auth_header):
    body = {"questionIds": [1, 2, 3, 4]}
    response = client.delete("/api/question", json=body, headers=auth_header)

    assert response.status_code == HTTPStatus.NO_CONTENT
    assert mock_question_repository.delete.called


def test_update(client, mock_question_repository, auth_header):
    question_id = 10
    body = {"question": "string", "question_id": question_id, "skill_id": 1}
    expected_affected_ids = [question_id]
    mock_question_repository.update.return_value = expected_affected_ids
    response = client.patch("/api/question", json=body, headers=auth_header)

    assert response.status_code == HTTPStatus.OK
    assert mock_question_repository.update.called
    assert response.json == expected_affected_ids
