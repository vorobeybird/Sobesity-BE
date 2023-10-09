import factory

from sobesity.domain.entities import (
    AnswerEntity,
    LevelEntity,
    QuestionEntity,
    QuestionId,
    QuestionTypeEntity,
    SkillEntity,
)
from tests.factories.answer import AnswerEntityFactory
from tests.factories.level import LevelEntityFactory
from tests.factories.question_type import QuestionTypeEntityFactory
from tests.factories.skill import SkillEntityFactory


class QuestionEntityFactory(factory.Factory):
    class Meta:
        model = QuestionEntity

    question_id = factory.Sequence(lambda n: QuestionId(n))
    question = factory.Faker("word")
    code = factory.Faker("sentence")
    question_type: QuestionTypeEntity = factory.SubFactory(QuestionTypeEntityFactory)
    skill: SkillEntity = factory.SubFactory(SkillEntityFactory)
    level: LevelEntity = factory.SubFactory(LevelEntityFactory)
    answers: list[AnswerEntity] = factory.List(
        [factory.SubFactory(AnswerEntityFactory) for _ in range(5)]
    )
