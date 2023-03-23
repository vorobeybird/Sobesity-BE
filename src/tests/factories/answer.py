import factory

from sobesity.domain.entities import AnswerEntity, QuestionId, AnswerId


class AnswerEntityFactory(factory.Factory):
    class Meta:
        model = AnswerEntity

    answer_id = factory.Sequence(lambda n: AnswerId(n))
    answer = factory.Faker("word")
    right = factory.Faker("boolean")
    question_id = factory.Sequence(lambda n: QuestionId(n))
