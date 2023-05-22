import random

import pytest


@pytest.fixture
def created_questions(
    created_skills, question_repository, questions, type_repository, type
):


    type_repository.batch_create([type])
    created_type = type_repository.get_list()

    for question in questions:
        question.skill_id = created_skills[0].skill_id
        question.type_id = created_type[0].type_id

    question_repository.batch_create(questions)
    return question_repository.get_list()


@pytest.fixture
def created_answers(created_questions, answer_repository, answers):
    for answer in answers:
        answer.question_id = created_questions[random.randint(0, 2)].question_id
    answer_repository.batch_create(answers)
    return answer_repository.get_list()


@pytest.fixture
def created_skills(skill_repository, skills):
    skill_repository.batch_create(skills)
    return skill_repository.get_list()
