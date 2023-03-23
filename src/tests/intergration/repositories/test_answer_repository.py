import pytest

from sobesity.domain.entities.answer import AnswerEntity, AnswerFilterEnitity


def test_get_list__empty_db__return_nothing(answer_repository):
    assert answer_repository.get_list() == []


def test_batch_create__get_all_rows(
    create_questions, answer_repository, answers, question_repository
):
    created_questions = question_repository.get_list()
    for answer in answers:
        answer.question_id = created_questions[0].question_id

    answer_repository.batch_create(answers)
    created_answers = answer_repository.get_list()
    created_answers_map = {answer.answer: answer for answer in created_answers}
    assert len(created_answers) == len(answers)
    for answer in answers:
        assert answer.answer in created_answers_map


def test_update__particular_rows_updated(
    create_questions, answer_repository, answers, question_repository
):
    created_questions = question_repository.get_list()
    for answer in answers:
        answer.question_id = created_questions[0].question_id

    answer_repository.batch_create(answers)
    answer_before = answer_repository.get_list()[0]

    to_set = answers[1]
    where = AnswerFilterEnitity(answer_ids=[answer_before.answer_id])
    updated_ids = answer_repository.update(to_set, where)

    answer_after = answer_repository.get_list()[-1]

    assert answer_before.answer_id == answer_after.answer_id == updated_ids[0]
    assert answer_after.answer == to_set.answer


def test_delete__particular_rows_deleted(
    create_questions, answer_repository, answers, question_repository
):
    created_questions = question_repository.get_list()
    for answer in answers:
        answer.question_id = created_questions[0].question_id

    answer_repository.batch_create(answers)
    created_answers_before = answer_repository.get_list()
    to_delete = [answer.answer_id for answer in created_answers_before[:2]]

    answer_repository.delete(to_delete)

    created_answers_after = answer_repository.get_list()

    assert (len(created_answers_before) - len(created_answers_after)) == len(to_delete)

    for answer in created_answers_after:
        assert answer.answer_id not in to_delete


@pytest.fixture()
def create_questions(skill_repository, skill, question_repository, question):
    skill_to_create = [skill]
    skill_repository.batch_create(skill_to_create)
    created_skill = skill_repository.get_list()

    question.skill_id = created_skill[0].skill_id

    question_to_create = [question]
    question_repository.batch_create(question_to_create)
