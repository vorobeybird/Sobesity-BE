import yaml
from pprint import pprint
from sobesity.domain.entities import (
    SkillEntity,
    SkillFilterEnitity,
    SkillId,
    QuestionEntity,
    QuestionFilterEnitity,
    QuestionId,
    AnswerEntity,
    AnswerFilterEnitity,
    AnswerId,
)
from sobesity.domain.services import SkillService, QuestionService, AnswerService
from sobesity.webapp import init_dependency

with open("sobesity/domain/build_db/format.yaml") as f:
    templates = yaml.safe_load(f)

for skill in templates:
    skill_to_create = [SkillEntity(skill_id=None, name=skill)]

    conteiner = init_dependency()
    skill_service = conteiner.services.skill()
    skill_service.batch_create(skill_to_create)

    created_skill = skill_service.get_list(SkillFilterEnitity(names=[skill]))

    questions_with_answers = templates.get(skill)["questions"]

    for question_with_answers in questions_with_answers:
        type_of_question = question_with_answers["type"]
        question = question_with_answers["question"]
        question_to_create = [
            QuestionEntity(
                question_id=None,
                question=question,
                type=type_of_question,
                skill_id=created_skill[0].skill_id,
            )
        ]

        question_service = conteiner.services.question()
        question_service.batch_create(question_to_create)

        answers_for_this_question = question_with_answers["answers"]
        created_question = question_service.get_list(
            QuestionFilterEnitity(questions=[question])
        )

        answers_to_create = []

        for answer_with_right in answers_for_this_question:

            try:
                right = answer_with_right["right"]
            except (KeyError):
                right = False

            answers_to_create.append(
                AnswerEntity(
                    answer_id=None,
                    answer=answer_with_right["answer"],
                    right=right,
                    question_id=created_question[0].question_id,
                )
            )

        answer_service = conteiner.services.answer()
        answer_service.batch_create(answers_to_create)
