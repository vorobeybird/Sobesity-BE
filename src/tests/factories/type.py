import random

import factory

from sobesity.domain.entities import TypeEntity, TypeId


class TypeEntityFactory(factory.Factory):
    class Meta:
        model = TypeEntity

    type_id = factory.Sequence(lambda n: TypeId(n))
    name = factory.Faker("word")


class KnownTypeEnityFactory(TypeEntityFactory):
    name = random.choice(["single", "multiple"])
