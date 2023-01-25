from sobesity.domain.entities.skill import SkillEntity


def build_skill_entity(cursor) -> SkillEntity:
    return SkillEntity(
        skill_id=cursor.skill_id,
        name=cursor.name,
    )
