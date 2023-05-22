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


class QuestionGeneratorService():
    def __init__(self, question_service, skill_service, answer_service, type_service):
        self.question_service = question_service
        self.skill_service = skill_service
        self.answer_service = answer_service
        self.type_service = type_service

    def generate_questions(self, theme, quantity):
        skill = self.skill_service.get_list(SkillFilterEnitity(names=[theme]))

        if skill:
            logger.info(f"Fined skill: '{skill}'")
            all_questions = self.question_service.get_list(
                QuestionFilterEnitity(skill_ids=[skill[0].skill_id])
            )
            logger.info("Take questions")
            if not all_questions:
                return bad_request_maker(NotFoundSerializer(message="Questions not exists"))
            questions = random.sample(all_questions, quantity)
            output_questions = []
            for question in questions:
                output_answers = []
                answers_for_this_question = self.answer_service.get_list(
                    AnswerFilterEnitity(question_ids=[question.question_id])
                )
                logger.info(f"Fined the answers for question: '{question}'")

                type = self.type_service.get_list(TypeFilterEnitity(type_ids=[question.type_id]))
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
        else:
            logger.info(f"Can't fined skill: '{skill}'")
            raise ValueError("Skill do not exist")
        return output_questions

    def take_question_for_theme(self, theme, level=None):
        if not level:
            questions = self.generate_questions(theme, 3)
        else:
            questions = self.generate_questions(theme, 3)
        return questions

