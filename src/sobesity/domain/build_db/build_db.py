import logging

import yaml

from sobesity.domain.entities import (
    AnswerEntity,
    AnswerFilterEnitity,
    LevelEntity,
    LevelFilterEnitity,
    QuestionEntity,
    QuestionFilterEnitity,
    SkillEntity,
    SkillFilterEnitity,
    TypeEntity,
    TypeFilterEnitity,
)
from sobesity.webapp import init_dependency

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    with open("sobesity/domain/build_db/data/fixture.yaml") as f:
        templates = yaml.safe_load(f)

    conteiner = init_dependency()
    question_service = conteiner.services.question()
    skill_service = conteiner.services.skill()
    answer_service = conteiner.services.answer()
    type_service = conteiner.services.type()
    level_service = conteiner.services.level()

    for skill in templates:
        exist_skill = skill_service.get_list(SkillFilterEnitity(names=[skill]))
        if not exist_skill:
            skill_service.batch_create([SkillEntity(skill_id=None, name=skill)])
            logger.info(f"Create skill: '{skill}'")
        else:
            logger.info(f"Skill '{skill}' already created")

        created_skill = skill_service.get_list(SkillFilterEnitity(names=[skill]))

        questions_with_answers = templates.get(skill)["questions"]

        for question_with_answers in questions_with_answers:
            question = question_with_answers["question"]
            code = question_with_answers.get("code")

            exist_question = question_service.get_list(
                QuestionFilterEnitity(
                    questions=[question],
                    skill_ids=[created_skill[0].skill_id],
                    codes=[code],
                )
            )

            if not exist_question:
                type_of_question = question_with_answers["type"]

                exist_type = type_service.get_list(
                    TypeFilterEnitity(names=[type_of_question])
                )

                if not exist_type:
                    type_service.batch_create(
                        [TypeEntity(type_id=None, name=type_of_question)]
                    )
                    logger.info(f"Create type: '{type_of_question}'")
                else:
                    logger.info(f"Type '{type_of_question}' already created:")

                created_type = type_service.get_list(
                    TypeFilterEnitity(names=[type_of_question])
                )

                level_of_question = question_with_answers["level"]

                exist_level = level_service.get_list(
                    LevelFilterEnitity(names=[level_of_question])
                )

                if not exist_level:
                    level_service.batch_create(
                        [LevelEntity(level_id=None, name=level_of_question)]
                    )
                    logger.info(f"Create level: '{level_of_question}'")
                else:
                    logger.info(f"Level '{level_of_question}' already created:")

                created_level = level_service.get_list(
                    LevelFilterEnitity(names=[level_of_question])
                )

                question_to_create = [
                    QuestionEntity(
                        question_id=None,
                        question=question,
                        type_id=created_type[0].type_id,
                        code=code,
                        skill_id=created_skill[0].skill_id,
                        level_id=created_level[0].level_id,
                    )
                ]
                question_service.batch_create(question_to_create)
                logger.info(f"Create question '{question}'")
            else:
                logger.info(f"Question '{question}' already created")
            answers_for_this_question = question_with_answers["answers"]
            if not code:
                created_question = question_service.get_list(
                    QuestionFilterEnitity(
                        questions=[question], skill_ids=[created_skill[0].skill_id]
                    )
                )
            else:
                created_question = question_service.get_list(
                    QuestionFilterEnitity(
                        questions=[question],
                        skill_ids=[created_skill[0].skill_id],
                        codes=[code],
                    )
                )

            for answer_with_right in answers_for_this_question:

                answer = answer_with_right["answer"]
                exist_answer = answer_service.get_list(
                    AnswerFilterEnitity(
                        answers=[answer], question_ids=[created_question[0].question_id]
                    )
                )
                answers_to_create = []
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
                    logger.info(f"Create answer '{answer}'")
                else:
                    logger.info(f"Answer '{answer}' already created")

    logger.info("Successfully finished")


if __name__ == "__main__":
    main()
