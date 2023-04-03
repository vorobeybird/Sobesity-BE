import random

import factory

from sobesity.domain.entities import QuestionEntity, QuestionId, SkillId


class QuestionEntityFactory(factory.Factory):
    class Meta:
        model = QuestionEntity

    question_id = factory.Sequence(lambda n: QuestionId(n))
    question = factory.Faker("word")
    type = random.choice(['single', 'multiple'])
    code = factory.Faker("sentence")
    skill_id = factory.Sequence(lambda n: SkillId(n))
