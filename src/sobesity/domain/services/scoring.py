import logging

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


def scoring(dict_with_questions_and_answers):
    from sobesity.webapp import init_dependency

    conteiner = init_dependency()
    answer_service = conteiner.services.answer()
    type_service = conteiner.services.type()
    question_service = conteiner.services.question()

    total_score_right = 0
    for question_id in dict_with_questions_and_answers:
        question = question_service.get_list(
            QuestionFilterEnitity(question_ids=[question_id])
        )
        type_of_question = type_service.get_list(
            TypeFilterEnitity(type_ids=[question[0].type_id])
        )

        if type_of_question[0].name == "multiple":
            logger.info(f"When type multiple:")
            percent = get_percent_when_question_multiple(
                question, dict_with_questions_and_answers[question_id], answer_service
            )
            if percent > 0:
                total_score_right += percent
        else:
            logger.info(f"When type single:")
            answer = answer_service.get_list(
                AnswerFilterEnitity(
                    answer_ids=[dict_with_questions_and_answers[question_id][0]]
                )
            )
            logger.info(f"Take  answer: {answer}")
            if answer[0].right:
                total_score_right += 1

    total_score_percent = total_score_right / len(dict_with_questions_and_answers) * 100
    logger.info(f"TOTAL PRECENT:{total_score_percent}")
    return str(total_score_percent)


def get_percent_when_question_multiple(
    question, array_selected_answers, answer_service
):
    answers = answer_service.get_list(
        AnswerFilterEnitity(question_ids=[question[0].question_id])
    )
    array_only_right_answers = []
    if not answers:
        return bad_request_maker(NotFoundSerializer(message="Answers not exists"))
    for answer in answers:
        if answer.right:
            array_only_right_answers.append(answer.answer_id)
            logger.info(f"Add answer '{answer.answer}' in array with right answers:")
    percent = len(set(array_selected_answers) & set(array_only_right_answers)) / len(
        array_only_right_answers
    )
    return percent


if __name__ == "__main__":
    scoring(
        dict_with_questions_and_answers={
            1: [4, 3],
            3: [9],
            5: [17],
        }
    )
