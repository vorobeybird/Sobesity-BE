import factory.fuzzy

from sobesity.domain.constants import TypeName
from sobesity.domain.entities import TypeEntity, TypeId


class TypeEntityFactory(factory.Factory):
    class Meta:
        model = TypeEntity

    type_id = factory.Sequence(lambda n: TypeId(n))
    name = factory.fuzzy.FuzzyChoice([TypeName.SINGLE, TypeName.MULTIPLY])
