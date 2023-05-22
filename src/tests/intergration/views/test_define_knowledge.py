from http import HTTPStatus

from http_constants.headers import HttpHeaders


def test_generate_questions__return_200(
    client,
    auth_header,
    created_answers,
    exist_skill,
    skill_service,
):

    skill = exist_skill(created_answers[0])
    response = client.get(
        f"api/define_knowledge/generate_questions?theme={skill[0].name}&level=any",
        headers=auth_header,
    )
    assert response.status_code == HTTPStatus.OK

    response = client.get(
        f"api/define_knowledge/generate_questions?theme=NonExistTheme&level=any",
        headers=auth_header,
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json != []


def test_scoring_full_right_return_100(client, auth_header, valid_scoring_100_body):
    response = client.post(
        "api/define_knowledge/scoring",
        json=valid_scoring_100_body,
        headers=auth_header,
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json == {"percent": 100.0}


def test_scoring_full_false_return_0(client, auth_header, valid_scoring_0_body):
    response = client.post(
        "api/define_knowledge/scoring",
        json=valid_scoring_0_body,
        headers=auth_header,
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json == {"percent": 0}


def test_scoring_half_right_return_50(
    client,
    auth_header,
    valid_scoring_50_body,
    not_valid_scoring_not_exit_question_body,
    not_valid_scoring_not_exit_answer_body,
):
    response = client.post(
        "api/define_knowledge/scoring",
        json=valid_scoring_50_body,
        headers=auth_header,
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json == {"percent": 50}
    response = client.post(
        "api/define_knowledge/scoring",
        json=not_valid_scoring_not_exit_question_body,
        headers=auth_header,
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST
    response = client.post(
        "api/define_knowledge/scoring",
        json=not_valid_scoring_not_exit_answer_body,
        headers=auth_header,
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST
