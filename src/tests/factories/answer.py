import factory

from sobesity.domain.entities import AnswerEntity, AnswerId, QuestionId


class AnswerEntityFactory(factory.Factory):
    class Meta:
        model = AnswerEntity

    answer_id = factory.Sequence(lambda n: AnswerId(n))
    answer = factory.Faker("word")
    right = factory.Faker("boolean")
    question_id = factory.Sequence(lambda n: QuestionId(n))
