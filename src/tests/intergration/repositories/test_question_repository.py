from sobesity.domain.entities.question import QuestionFilterEnitity


def test_get_list__empty_db__return_nothing(question_repository):
    assert question_repository.get_list() == []


def test_batch_create__get_all_rows(
    skill_repository,
    skill,
    question_repository,
    questions,
    type_repository,
    type,
    level_repository,
    level,
):
    skill_repository.batch_create([skill])
    created_skill = skill_repository.get_list()

    type_repository.batch_create([type])
    created_type = type_repository.get_list()

    level_repository.batch_create([level])
    created_level = level_repository.get_list()

    for question in questions:
        question.skill_id = created_skill[0].skill_id
        question.type_id = created_type[0].type_id
        question.level_id = created_level[0].level_id

    question_repository.batch_create(questions)
    created_questions = question_repository.get_list()
    created_questions_map = {
        question.question: question for question in created_questions
    }

    assert len(created_questions) == len(questions)
    for question in questions:
        assert question.question in created_questions_map


def test_update__particular_rows_updated(
    created_questions,
    question_repository,
    questions,
):

    question_before = created_questions[0]

    to_set = questions[1]
    where = QuestionFilterEnitity(question_ids=[question_before.question_id])
    updated_ids = question_repository.update(to_set, where)

    question_after = question_repository.get_list()[-1]

    assert question_before.question_id == question_after.question_id == updated_ids[0]
    assert question_after.question == to_set.question


def test_delete__particular_rows_deleted(
    created_questions,
    question_repository,
    questions,
    skill_repository,
    skill,
    type_repository,
    type,
):

    created_questions_before = created_questions
    to_delete = [quesiton.question_id for quesiton in created_questions_before[:2]]

    question_repository.delete(to_delete)

    created_questions_after = question_repository.get_list()

    assert (len(created_questions_before) - len(created_questions_after)) == len(
        to_delete
    )

    for question in created_questions_after:
        assert question.question_id not in to_delete
