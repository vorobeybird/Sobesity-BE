from sobesity.domain.entities import (
    AnswerEntity,
    KnowledgeEntity,
    LevelEntity,
    QuestionEntity,
    QuestionTypeEntity,
    SkillEntity,
    UserEntity,
)


def build_skill_entity(cursor) -> SkillEntity:
    return SkillEntity(
        skill_id=cursor.skill_id,
        name=cursor.name,
    )


def build_question_entity(cursor) -> QuestionEntity:
    # breakpoint()
    return QuestionEntity(
        question_id=cursor.question_id,
        question=cursor.question,
        question_type=build_type_entity(cursor),
        code=cursor.code,
        skill=build_skill_entity(cursor),
        level=build_level_entity(cursor),
    )


def build_answer_entity(cursor) -> AnswerEntity:
    return AnswerEntity(
        answer_id=cursor.answer_id,
        answer=cursor.answer,
        right=cursor.right,
        question_id=cursor.question_id,
    )


def build_type_entity(cursor) -> QuestionTypeEntity:
    return QuestionTypeEntity(
        type_id=cursor.type_id,
        name=cursor.name,
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


def build_level_entity(cursor) -> LevelEntity:
    return LevelEntity(
        level_id=cursor.level_id,
        name=cursor.name,
    )


def build_knowledge_entity(cursor) -> KnowledgeEntity:
    return KnowledgeEntity(
        knowledge_id=cursor.knowledge_id,
        user_id=cursor.user_id,
        skill_id=cursor.skill_id,
        level_id=cursor.level_id,
    )
