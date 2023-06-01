import factory

from sobesity.domain.entities import (
    LevelId,
    QuestionEntity,
    QuestionId,
    SkillId,
    TypeId,
)


class QuestionEntityFactory(factory.Factory):
    class Meta:
        model = QuestionEntity

    question_id = factory.Sequence(lambda n: QuestionId(n))
    question = factory.Faker("word")
    type_id = factory.Sequence(lambda n: TypeId(n))
    code = factory.Faker("sentence")
    skill_id = factory.Sequence(lambda n: SkillId(n))
    level_id = factory.Sequence(lambda n: LevelId(n))
