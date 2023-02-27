from sobesity.domain.entities.skill import SkillEntity
from sobesity.domain.entities.question import QuestionEntity
from sobesity.domain.entities.answer import AnswerEntity


def build_skill_entity(cursor) -> SkillEntity:
    return SkillEntity(
        skill_id=cursor.skill_id,
        name=cursor.name,
    )


def build_question_entity(cursor) -> QuestionEntity:
    return QuestionEntity(
        question_id=cursor.question_id,
        question=cursor.question,
    )

def build_answer_entity(cursor) -> AnswerEntity:
    return AnswerEntity(
        answer_id=cursor.answer_id,
        answer=cursor.answer,
    )