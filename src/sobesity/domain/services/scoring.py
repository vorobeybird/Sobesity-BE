import logging

from sobesity.domain.constants import TypeName
from sobesity.domain.entities import (
    AnswerFilterEnitity,
    QuestionFilterEnitity,
    TypeFilterEnitity,
)
from sobesity.domain.exceptions import AnswerNotExistViolation, QuestionExistViolation

logger = logging.getLogger(__name__)


class ScoringService:
    def __init__(self, question_service, skill_service, answer_service, type_service):
        self.question_service = question_service
        self.skill_service = skill_service
        self.answer_service = answer_service
        self.type_service = type_service

    def scoring(self, dict_with_questions_and_answers):
        total_score_right = 0
        for question_id in dict_with_questions_and_answers:
            question = self.question_service.get_list(
                QuestionFilterEnitity(question_ids=[question_id])
            )
            if question:
                type_of_question = self.type_service.get_list(
                    TypeFilterEnitity(type_ids=[question[0].type_id])
                )

                if type_of_question[0].name == TypeName.MULTIPLY:
                    logger.info("When type multiple:")
                    percent = self.get_percent_when_question_multiple(
                        question, dict_with_questions_and_answers[question_id]
                    )
                    if percent > 0:
                        total_score_right += percent
                else:
                    logger.info("When type single:")
                    answer = self.answer_service.get_list(
                        AnswerFilterEnitity(
                            answer_ids=[dict_with_questions_and_answers[question_id][0]]
                        )
                    )
                    logger.info(f"Take  answer: {answer}")
                    if answer:
                        if answer[0].right:
                            total_score_right += 1
                    else:
                        logger.info("Can't fined answer: '")
                        raise AnswerNotExistViolation()
            else:
                logger.info("Can't fined question: '")
                raise QuestionExistViolation()
        total_score_percent = (
            total_score_right / len(dict_with_questions_and_answers) * 100
        )
        logger.info(f"TOTAL PRECENT:{total_score_percent}")
        return total_score_percent

    def get_percent_when_question_multiple(self, question, array_selected_answers):
        answers = self.answer_service.get_list(
            AnswerFilterEnitity(question_ids=[question[0].question_id])
        )
        array_only_right_answers = []
        available_answers = {answer.answer_id for answer in answers}
        chosen_answers_exitst = (available_answers & set(array_only_right_answers)) == len(available_answers)

        if not answers or not chosen_answers_exitst:
            raise AnswerNotExistViolation()
        for answer in answers:
            if answer.right:
                array_only_right_answers.append(answer.answer_id)
                logger.info(
                    f"Add answer '{answer.answer}' in array with right answers:"
                )
        percent = len(
            set(array_selected_answers) & set(array_only_right_answers)
        ) / len(array_only_right_answers)
        return percent
