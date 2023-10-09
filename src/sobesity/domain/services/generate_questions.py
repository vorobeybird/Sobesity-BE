import logging
import random

from sobesity.domain.entities import (
    AnswerFilterEnitity,
    LevelFilterEnitity,
    QuestionFilterEnitity,
    QuestionTypeFilterEnitity,
    SkillFilterEnitity,
)
from sobesity.domain.exceptions import QuestionsNotExistViolation

logger = logging.getLogger(__name__)


class QuestionGeneratorService:
    def __init__(
        self,
        question_service,
        skill_service,
        answer_service,
        type_service,
        level_service,
    ):
        self.question_service = question_service
        self.skill_service = skill_service
        self.answer_service = answer_service
        self.type_service = type_service
        self.level_service = level_service

    def generate_questions(self, theme, prelevel, quantity):
        skill = self.skill_service.get_one(SkillFilterEnitity(names=[theme]))
        level = self.level_service.get_one(LevelFilterEnitity(names=[prelevel]))

        logger.debug(f"Finded skill: '{skill}'")

        all_questions = self.question_service.get_list(
            QuestionFilterEnitity(
                skill_ids=[skill.skill_id], level_ids=[level.level_id]
            )
        )

        if not all_questions:
            logger.info(f"Can't fined questions for this skill: '{skill}'")
            raise QuestionsNotExistViolation()

        questions = random.sample(all_questions, quantity)

        output_questions = []
        for question in questions:
            output_answers = []
            answers_for_this_question = self.answer_service.get_list(
                AnswerFilterEnitity(question_ids=[question.question_id])
            )
            logger.info(f"Fined the answers for question: '{question}'")

            type = self.type_service.get_list(
                QuestionTypeFilterEnitity(type_ids=[question.type_id])
            )
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
                "code": question.code,
            }
            logger.info(f"Gathered the question: '{question_for_output}'")
            output_questions.append(question_for_output)
            logger.info("Append the question to list questions")
        return output_questions

    def take_question_for_theme(self, theme, level):
        if not level == "junior":
            questions = self.generate_questions(theme, level, 5)
        else:
            questions = self.generate_questions(theme, level, 15)
        return questions
