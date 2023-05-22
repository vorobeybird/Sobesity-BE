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


def test_scoring_full_right_return_100(client, auth_header, valid_scoring_100_body, type_repository, question_service, answer_service):
    breakpoint()
    response = client.post("api/define_knowledge/scoring", json=valid_scoring_100_body, headers=auth_header,)
    assert response.status_code == HTTPStatus.OK


