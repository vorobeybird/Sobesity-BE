import factory.fuzzy

from sobesity.domain.constants import TypeName
from sobesity.domain.entities import QuestionTypeEntity, QuestionTypeId


class QuestionTypeEntityFactory(factory.Factory):
    class Meta:
        model = QuestionTypeEntity

    question_type_id = factory.Sequence(lambda n: QuestionTypeId(n))
    name = factory.fuzzy.FuzzyChoice([TypeName.SINGLE, TypeName.MULTIPLY])
