import random
from contextlib import contextmanager

import email_validator
import pytest
from http_constants.headers import HttpHeaders

from sobesity.domain.entities import UserFilter, UserId
from sobesity.webapp import create_app
from tests.factories import (
    AnswerEntityFactory,
    CreateUserFactory,
    QuestionEntityFactory,
    SkillEntityFactory,
    UserEntityFactory,
    TypeEntityFactory,
)
from sobesity.domain.entities import (
    SkillFilterEnitity,
    QuestionFilterEnitity,
)

from sobesity.domain.constants import TypeName

email_validator.TEST_ENVIRONMENT = True


@pytest.fixture
def di(app):
    return app.container


@pytest.fixture(autouse=True)
def db(di):
    with di.resources.datasource()() as connection:

        @contextmanager
        def rollback_conn():
            yield connection

        yield di.resources.datasource.override(rollback_conn)

        connection.rollback()


@pytest.fixture
def app():
    app = create_app()
    yield app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def user_for_create():
    return CreateUserFactory()


@pytest.fixture
def user_factory():
    return UserEntityFactory


@pytest.fixture
def create_user_factory():
    return CreateUserFactory


@pytest.fixture
def user_entity():
    return UserEntityFactory()


@pytest.fixture
def skills():
    return [SkillEntityFactory() for _ in range(random.randint(3, 5))]


@pytest.fixture
def skill(skills):
    return skills[0]


@pytest.fixture
def created_user(user_service, user_for_create):
    user_service.create_user(user_for_create)
    return user_service.get_user(UserFilter(nickname=user_for_create.nickname))


@pytest.fixture
def skill_repository(di):
    return di.repositories.skill()


@pytest.fixture
def user_service(di):
    return di.services.user()


@pytest.fixture
def login_body(created_user, user_for_create):
    return {"email": user_for_create.email, "password": user_for_create.password}


@pytest.fixture
def jwt_resource(di):
    return di.resources.jwt()


@pytest.fixture
def jwt_token(jwt_resource):
    user_id = UserId(1111)
    return jwt_resource.encode_jwt(user_id)


@pytest.fixture
def auth_header(jwt_token):
    return {HttpHeaders.AUTHORIZATION: f"Bearer {jwt_token}"}


@pytest.fixture
def valid_user_create_body(user_for_create):
    return {
        "password": user_for_create.password,
        "nickname": user_for_create.nickname,
        "email": user_for_create.email,
        "firstName": user_for_create.first_name,
        "lastName": user_for_create.last_name,
    }


@pytest.fixture
def enable_email_validation():
    email_validator.TEST_ENVIRONMENT = False
    yield
    email_validator.TEST_ENVIRONMENT = True


@pytest.fixture
def question_repository(di):
    return di.repositories.question()


@pytest.fixture
def questions():
    return [QuestionEntityFactory() for _ in range(3)]


@pytest.fixture
def question(questions):
    return questions[0]


@pytest.fixture
def answer_repository(di):
    return di.repositories.answer()


@pytest.fixture
def answers():
    return [AnswerEntityFactory() for _ in range(12)]


@pytest.fixture
def answer(answers):
    return answers[0]


@pytest.fixture
def type_repository(di):
    return di.repositories.type()


@pytest.fixture
def types():
    return [
        TypeEntityFactory(name=TypeName.MULTIPLY),
        TypeEntityFactory(name=TypeName.SINGLE),
    ]


@pytest.fixture
def type(types):
    return types[0]


@pytest.fixture
def valid_scoring_50_body(created_answers, question_service):
    list_question_with_all_answers = {}
    questions = random.sample(question_service.get_list(), 2)
    list_false_answers_for_this_question = take_all_false_answer_id(
        questions[0].question_id, created_answers
    )
    list_right_answers_for_this_question = take_all_right_answer_id(
        questions[1].question_id, created_answers
    )
    list_question_with_all_answers[
        f"{questions[0].question_id}"
    ] = list_false_answers_for_this_question
    list_question_with_all_answers[
        f"{questions[1].question_id}"
    ] = list_right_answers_for_this_question

    return {"question_with_list_answer": list_question_with_all_answers}


@pytest.fixture
def valid_scoring_0_body(created_answers, question_service):
    list_question_with_false_answers = {}
    questions = question_service.get_list()
    for question in questions:
        list_false_answers_for_this_question = take_all_false_answer_id(
            question.question_id, created_answers
        )
        list_question_with_false_answers[
            f"{question.question_id}"
        ] = list_false_answers_for_this_question

    return {"question_with_list_answer": list_question_with_false_answers}


def take_all_false_answer_id(question_id, answers):
    list_answers_with_false_answers = []
    for answer in answers:
        if answer.question_id == question_id:
            if not answer.right:
                list_answers_with_false_answers.append(answer.answer_id)
    return list_answers_with_false_answers


@pytest.fixture
def valid_scoring_100_body(created_answers, question_service):
    list_question_with_right_answers = {}
    questions = question_service.get_list()
    for question in questions:
        list_right_answers_for_this_question = take_all_right_answer_id(
            question.question_id, created_answers
        )
        list_question_with_right_answers[
            f"{question.question_id}"
        ] = list_right_answers_for_this_question

    return {"question_with_list_answer": list_question_with_right_answers}


def take_all_right_answer_id(question_id, answers):
    list_answers_with_right_answers = []
    for answer in answers:
        if answer.question_id == question_id:
            if answer.right:
                list_answers_with_right_answers.append(answer.answer_id)
    return list_answers_with_right_answers


@pytest.fixture
def take_all_not_right_answer_id(question_id, answers):
    list_answers_with_right_answers = []
    for answer in answers:
        if answer.question_id == question_id:
            if not answer.right:
                list_answers_with_right_answers.append(answer.answer_id)
    return list_answers_with_right_answers


@pytest.fixture
def question_service(di):
    return di.services.question()


@pytest.fixture
def skill_service(di):
    return di.services.skill()


@pytest.fixture
def answer_service(di):
    return di.services.answer()


@pytest.fixture
def exist_skill(skill_service, question_service):
    def skill_sercher(answer):
        question = question_service.get_list(
            QuestionFilterEnitity(question_ids=[answer.question_id])
        )
        skill = skill_service.get_list(
            SkillFilterEnitity(skill_ids=[question[0].skill_id])
        )
        return skill

    return skill_sercher


@pytest.fixture
def not_valid_scoring_not_exit_question_body(created_answers, question_service):
    list_question_with_right_answers = {}
    questions = question_service.get_list()
    for question in questions:
        list_right_answers_for_this_question = take_all_right_answer_id(
            question.question_id, created_answers
        )
        list_question_with_right_answers["0"] = list_right_answers_for_this_question

    return {"question_with_list_answer": list_question_with_right_answers}


@pytest.fixture
def not_valid_scoring_not_exit_answer_body(created_answers, question_service):
    list_question_with_right_answers = {}
    questions = question_service.get_list()
    for question in questions:
        list_right_answers_for_this_question = take_all_right_answer_id(
            question.question_id, created_answers
        )
        list_question_with_right_answers[f"{question.question_id}"] = [0]

    return {"question_with_list_answer": list_question_with_right_answers}
