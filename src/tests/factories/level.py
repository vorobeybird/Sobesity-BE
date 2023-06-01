import factory

from sobesity.domain.entities import LevelEntity, LevelId


class LevelEntityFactory(factory.Factory):
    class Meta:
        model = LevelEntity

    level_id = factory.Sequence(lambda n: LevelId(n))
    name = factory.Faker("word")
