from http import HTTPStatus
import pytest

def answer_to_json(answer):
    return {
        "answer": answer.answer,
        "answer_id": answer.answer_id,
        "question_id": answer.question_id,
        "right": answer.right,
    }


def test_get__no_data__return_empty(client, mock_answer_repository, auth_header):
    mock_answer_repository.get_list.return_value = []

    response = client.get("/api/answer", headers=auth_header)
    assert response.status_code == HTTPStatus.OK
    assert response.json == []


def test_get__has_data__return_data(
    client, mock_answer_repository, auth_header, answers
):
    expected_json = [answer_to_json(answer) for answer in answers]
    mock_answer_repository.get_list.return_value = answers
    response = client.get("/api/answer", headers=auth_header)
    assert response.status_code == HTTPStatus.OK
    assert response.json == expected_json


def test_get_by_id__not_found__return_404(client, mock_answer_repository, auth_header):
    mock_answer_repository.get_list.return_value = []

    response = client.get("/api/answer/123", headers=auth_header)
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_get__by_id__return_answer(client, mock_answer_repository, auth_header, answer):
    mock_answer_repository.get_list.return_value = [answer]

    response = client.get("/api/answer/123", headers=auth_header)
    assert response.status_code == HTTPStatus.OK
    assert response.json == answer_to_json(answer)


def test_create(client, mock_answer_repository, auth_header):
    body = [{"answer": "What", "question_id": 1, "right": True}]
    response = client.post("/api/answer", json=body, headers=auth_header)

    assert response.status_code == HTTPStatus.CREATED
    assert mock_answer_repository.batch_create.called


@pytest.mark.xfail
def test_delete(client, mock_answer_repository, auth_header):
    body = {"answerIds": [1, 2, 3, 4]}
    response = client.delete("/api/answer", json=body, headers=auth_header)

    assert response.status_code == HTTPStatus.NO_CONTENT
    assert mock_answer_repository.delete.called


def test_update(client, mock_answer_repository, auth_header):
    answer_id = 10
    body = {"answer": "string", "answer_id": answer_id, "question_id": 1, "right": True}
    expected_affected_ids = [answer_id]
    mock_answer_repository.update.return_value = expected_affected_ids
    response = client.patch("/api/answer", json=body, headers=auth_header)

    assert response.status_code == HTTPStatus.OK
    assert mock_answer_repository.update.called
    assert response.json == expected_affected_ids


def test_get__by_question_id_return_answers(
    client, mock_answer_repository, auth_header, answers
):
    expected_json = [answer_to_json(answer) for answer in answers]
    mock_answer_repository.get_list.return_value = answers
    response = client.get("/api/answer/find_answers/123", headers=auth_header)
    assert response.status_code == HTTPStatus.OK
    assert response.json == expected_json
