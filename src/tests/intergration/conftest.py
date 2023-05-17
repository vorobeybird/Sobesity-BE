import pytest


@pytest.fixture
def created_questions(
    skill_repository, skill, question_repository, questions, type_repository, type
):
    skill_repository.batch_create([skill])
    created_skill = skill_repository.get_list()

    type_repository.batch_create([type])
    created_type = type_repository.get_list()

    for question in questions:
        question.skill_id = created_skill[0].skill_id
        question.type_id = created_type[0].type_id

    question_repository.batch_create(questions)
    return question_repository.get_list()


@pytest.fixture
def created_answers(
    created_questions, answer_repository, answers
):
    for answer in answers:
        answer.question_id = created_questions[0].question_id

    answer_repository.batch_create(answers)
    return answer_repository.get_list()
