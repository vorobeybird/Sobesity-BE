from http import HTTPStatus


def test_generate_questions__return_200(
    client,
    auth_header,
    created_answers,
    exist_skill,
    skill_service,
):

    skill = exist_skill(created_answers[0])
    level = "any"
    response = client.get(
        f"api/define_knowledge/generate_questions?theme={skill[0].name}&level={level}",
        headers=auth_header,
    )
    assert response.status_code == HTTPStatus.OK

    response = client.get(
        f"api/define_knowledge/generate_questions?theme=NonExistTheme&level={level}",
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


def test_scoring_half_right_return_50__response_200(
    client,
    auth_header,
    valid_scoring_50_body,
):
    response = client.post(
        "api/define_knowledge/scoring",
        json=valid_scoring_50_body,
        headers=auth_header,
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json == {"percent": 50}


def test_scoring_half_right__questions_not_exist__return_400(
    client,
    auth_header,
        not_valid_scoring_not_exit_question_body,
):
    response = client.post(
        "api/define_knowledge/scoring",
        json=not_valid_scoring_not_exit_question_body,
        headers=auth_header,
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST

def test_scoring_half_right__answer_not_exist__return_400(
    client,
    auth_header,
        not_valid_scoring_not_exit_answer_body,
):
    response = client.post(
        "api/define_knowledge/scoring",
        json=not_valid_scoring_not_exit_answer_body,
        headers=auth_header,
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST
