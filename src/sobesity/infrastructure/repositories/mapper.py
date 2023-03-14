from sobesity.domain.entities.question import QuestionEntity
from sobesity.domain.entities.answer import AnswerEntity
from sobesity.domain.entities import SkillEntity, UserEntity


def build_skill_entity(cursor) -> SkillEntity:
    return SkillEntity(
        skill_id=cursor.skill_id,
        name=cursor.name,
    )


def build_question_entity(cursor) -> QuestionEntity:
    return QuestionEntity(
        question_id=cursor.question_id,
        question=cursor.question,
        skill_id=cursor.skill_id,
    )


def build_answer_entity(cursor) -> AnswerEntity:
    return AnswerEntity(
        answer_id=cursor.answer_id,
        answer=cursor.answer,
        right=cursor.right,
        question_id=cursor.question_id,
    )


def build_user_entity(cursor) -> UserEntity:
    return UserEntity(
        user_id=cursor.user_id,
        nickname=cursor.nickname,
        email=cursor.email,
        registered_at=cursor.registered_at,
        hashed_password=cursor.hashed_password,
        salt=cursor.salt,
        first_name=cursor.first_name,
        last_name=cursor.last_name,
    )
