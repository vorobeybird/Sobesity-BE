import logging
import random
import json

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
    TypeEntity,
    TypeFilterEnitity,
    TypeId,
)
from sobesity.domain.serializers import NotFoundSerializer
from sobesity.domain.utils.response import bad_request_maker


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def take_question_for_theme(theme, level=None):
    if not level:
        questions = generate_questions(theme, 3)
    else:
        questions = generate_questions(theme, 5)
    return questions


def generate_questions(theme, quantity):
    from sobesity.webapp import init_dependency

    conteiner = init_dependency()
    question_service = conteiner.services.question()
    skill_service = conteiner.services.skill()
    answer_service = conteiner.services.answer()
    type_service = conteiner.services.type()

    skill = skill_service.get_list(SkillFilterEnitity(names=[theme]))
    logger.info(f"Fined skill: '{skill}'")
    all_questions = question_service.get_list(
        QuestionFilterEnitity(skill_ids=[skill[0].skill_id])
    )
    logger.info("Take questions")
    if not all_questions:
        return bad_request_maker(NotFoundSerializer(message="Questions not exists"))
    questions = random.sample(all_questions, quantity)
    output_questions = []
    for question in questions:
        output_answers = []
        answers_for_this_question = answer_service.get_list(
            AnswerFilterEnitity(question_ids=[question.question_id])
        )
        logger.info(f"Fined the answers for question: '{question}'")

        type = type_service.get_list(TypeFilterEnitity(type_ids=[question.type_id]))
        logger.info(f"Fined the type of this question: '{type}'")

        for answer in answers_for_this_question:
            answer = {"answer": answer.answer, "right": answer.right}
            logger.info(f"Gathered the answer: '{answer}'")
            output_answers.append(answer)
            logger.info("Append the answer to list answers")
        question_for_output = {
            "question": question.question,
            "type": type[0].name,
            "answers": output_answers,
        }
        logger.info(f"Gathered the question: '{question_for_output}'")
        output_questions.append(question_for_output)
        logger.info("Append the question to list questions")
    return output_questions


if __name__ == "__main__":
    take_question_for_theme(theme="Python")
