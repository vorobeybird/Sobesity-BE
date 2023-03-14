import pytest

from sobesity.domain.entities.answer import AnswerEntity, AnswerFilterEnitity


def test_get_list__empty_db__return_nothing(answer_repository):
    assert answer_repository.get_list() == []


def test_batch_create__get_all_rows(answer_repository):
    answers_to_create = [
        AnswerEntity(answer_id=None, answer="Nothing", right=True,  question_id=None,),
        AnswerEntity(answer_id=None, answer="Nobody", right=True,  question_id=None,),
        AnswerEntity(answer_id=None, answer="SMT", right=True,  question_id=None,),
    ]
    answer_repository.batch_create(answers_to_create)
    created_answers = answer_repository.get_list()
    created_answers_map = {answer.answer: answer for answer in created_answers}

    assert len(created_answers) == len(answers_to_create)
    for answer in answers_to_create:
        assert answer.answer in created_answers_map


def test_update__particular_rows_updated(answer_repository):
    answers_to_create = [
        AnswerEntity(answer_id=None, answer="Nothing", right=True,  question_id=None,),
    ]
    answer_repository.batch_create(answers_to_create)
    answer_before = answer_repository.get_list()[0]

    to_set = AnswerEntity(answer_id=None, answer="Nobody", right=True,  question_id=None,)
    where = AnswerFilterEnitity(answer_ids=[answer_before.answer_id])
    updated_ids = answer_repository.update(to_set, where)

    answer_after = answer_repository.get_list()[0]

    assert answer_before.answer_id == answer_after.answer_id == updated_ids[0]
    assert answer_after.answer == to_set.answer


def test_delete__particular_rows_deleted(answer_repository):
    answers_to_create = [
        AnswerEntity(answer_id=None, answer="Nothing", right=True, question_id=None, ),
        AnswerEntity(answer_id=None, answer="Nobody", right=True, question_id=None, ),
        AnswerEntity(answer_id=None, answer="SMT", right=True, question_id=None, ),
    ]
    answer_repository.batch_create(answers_to_create)
    created_answers_before = answer_repository.get_list()
    to_delete = [answer.answer_id for answer in created_answers_before[:2]]

    answer_repository.delete(to_delete)

    created_answers_after = answer_repository.get_list()

    assert (len(created_answers_before) - len(created_answers_after)) == len(to_delete)

    for answer in created_answers_after:
        assert answer.answer_id not in to_delete
