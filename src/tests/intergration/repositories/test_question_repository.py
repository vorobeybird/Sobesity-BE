import pytest

from sobesity.domain.entities.question import QuestionEntity, QuestionFilterEnitity


def test_get_list__empty_db__return_nothing(question_repository):
    assert question_repository.get_list() == []


def test_batch_create__get_all_rows(question_repository):
    questions_to_create = [
        QuestionEntity(question_id=None, question="What", skill_id=None),
        QuestionEntity(question_id=None, question="Where", skill_id=None),
        QuestionEntity(question_id=None, question="Who", skill_id=None),
    ]
    question_repository.batch_create(questions_to_create)
    created_questions = question_repository.get_list()
    created_questions_map = {
        question.question: question for question in created_questions
    }

    assert len(created_questions) == len(questions_to_create)
    for question in questions_to_create:
        assert question.question in created_questions_map


def test_update__particular_rows_updated(question_repository):
    questions_to_create = [
        QuestionEntity(question_id=None, question="What", skill_id=None),
    ]
    question_repository.batch_create(questions_to_create)
    question_before = question_repository.get_list()[0]

    to_set = QuestionEntity(question_id=None, question="Where", skill_id=None)
    where = QuestionFilterEnitity(question_ids=[question_before.question_id])
    updated_ids = question_repository.update(to_set, where)

    question_after = question_repository.get_list()[0]

    assert question_before.question_id == question_after.question_id == updated_ids[0]
    assert question_after.question == to_set.question


def test_delete__particular_rows_deleted(question_repository):
    questions_to_create = [
        QuestionEntity(question_id=None, question="What", skill_id=None),
        QuestionEntity(question_id=None, question="Where", skill_id=None),
        QuestionEntity(question_id=None, question="Who", skill_id=None),
    ]
    question_repository.batch_create(questions_to_create)
    created_questions_before = question_repository.get_list()
    to_delete = [quesiton.question_id for quesiton in created_questions_before[:2]]

    question_repository.delete(to_delete)

    created_questions_after = question_repository.get_list()

    assert (len(created_questions_before) - len(created_questions_after)) == len(
        to_delete
    )

    for question in created_questions_after:
        assert question.question_id not in to_delete
