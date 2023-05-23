import factory

from sobesity.domain.entities import (
    KnowledgeEntity,
    KnowledgeId,
    SkillId,
    UserId,
    LevelId,
)


class KnowledgeEntityFactory(factory.Factory):
    class Meta:
        model = KnowledgeEntity

    knowledge_id = factory.Sequence(lambda n: KnowledgeId(n))
    user_id = factory.Sequence(lambda n: UserId(n))
    skill_id = factory.Sequence(lambda n: SkillId(n))
    level_id = factory.Sequence(lambda n: LevelId(n))
