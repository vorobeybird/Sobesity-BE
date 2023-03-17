import factory

from sobesity.domain.entities import SkillEntity, SkillId


class SkillEntityFactory(factory.Factory):
    class Meta:
        model = SkillEntity

    skill_id = factory.Sequence(lambda n: SkillId(n)+1)
    name = factory.Faker("word")
