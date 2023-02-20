from sobesity.domain.entities import SkillEntity, UserEntity


def build_skill_entity(cursor) -> SkillEntity:
    return SkillEntity(
        skill_id=cursor.skill_id,
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
