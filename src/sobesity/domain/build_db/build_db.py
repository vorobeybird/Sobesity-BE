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

with open("data/fixture.yaml") as f:
    templates = yaml.safe_load(f)

conteiner = init_dependency()
question_service = conteiner.services.question()
skill_service = conteiner.services.skill()
answer_service = conteiner.services.answer()

for skill in templates:
    exist_skill = skill_service.get_list(SkillFilterEnitity(names=[skill]))
    if not exist_skill:
        skill_to_create = [SkillEntity(skill_id=None, name=skill)]
        skill_service.batch_create(skill_to_create)

    created_skill = skill_service.get_list(SkillFilterEnitity(names=[skill]))

    questions_with_answers = templates.get(skill)["questions"]

    for question_with_answers in questions_with_answers:
        question = question_with_answers["question"]

        exist_questions_for_all_skills = question_service.get_list(QuestionFilterEnitity(questions=[question],skill_ids=[created_skill[0].skill_id]))

        if not exist_questions_for_all_skills:
            type_of_question = question_with_answers["type"]
            code = question_with_answers.get("code")
            question_to_create = [
                QuestionEntity(
                    question_id=None,
                    question=question,
                    type=type_of_question,
                    code=code,
                    skill_id=created_skill[0].skill_id,
                )
            ]
            question_service.batch_create(question_to_create)
        answers_for_this_question = question_with_answers["answers"]
        created_question = question_service.get_list(
            QuestionFilterEnitity(questions=[question], skill_ids=[created_skill[0].skill_id])
        )

        answers_to_create = []

        for answer_with_right in answers_for_this_question:

            answer = answer_with_right["answer"]
            exist_answer = answer_service.get_list(AnswerFilterEnitity(answers=[answer], question_ids=[created_question[0].question_id]))
            if not exist_answer:
                try:
                    right = answer_with_right["right"]
                except (KeyError):
                    right = False

                answers_to_create.append(
                    AnswerEntity(
                        answer_id=None,
                        answer=answer,
                        right=right,
                        question_id=created_question[0].question_id,
                    )
                )
                answer_service.batch_create(answers_to_create)




