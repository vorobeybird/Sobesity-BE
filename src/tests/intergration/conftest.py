import random

import pytest

from sobesity.domain.entities import (
    TypeFilterEnitity,
)

@pytest.fixture
def created_questions(
    created_skills, question_repository, questions, type_repository, types
):
    types[0].name = 'single'
    types[1].name = 'multiple'
    type_repository.batch_create(types)
    created_types = type_repository.get_list()

    for question in questions:
        question.skill_id = created_skills[0].skill_id
        question.type_id = created_types[random.randint(0, 1)].type_id

    question_repository.batch_create(questions)
    return question_repository.get_list()


@pytest.fixture
def created_answers(created_questions, answer_repository, question_repository, answers, type_repository):
    for question in created_questions:
        answers_for_create = random.sample(answers, 4)

        type_of_question = type_repository.get_list(
            TypeFilterEnitity(type_ids=[question.type_id])
        )

        for answer in answers_for_create:
            answer.question_id = question.question_id
            answer.right = False
        answers_for_create[random.randint(0, 3)].right = True

        add_second_right_answer_to_list = False

        if type_of_question[0].name == 'multiple':
            while add_second_right_answer_to_list == False:
                second_right_answer_for_multiple = answers_for_create[random.randint(0, 3)]
                if second_right_answer_for_multiple.right == False:
                    second_right_answer_for_multiple.right = True
                    add_second_right_answer_to_list = True

        answer_repository.batch_create(answers_for_create)
    return answer_repository.get_list()


@pytest.fixture
def created_skills(skill_repository, skills):
    skill_repository.batch_create(skills)
    return skill_repository.get_list()
