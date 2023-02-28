import factory

from sobesity.domain.entities import CreateUserEntity, UserEntity, UserId


class UserEntityFactory(factory.Factory):
    class Meta:
        model = UserEntity

    user_id = factory.Sequence(lambda n: UserId(n))
    nickname = factory.Faker("user_name")
    email = factory.Faker("email")
    registered_at = factory.Faker("date_time")
    hashed_password = None
    salt = None
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")


class CreateUserFactory(UserEntityFactory):
    class Meta:
        model = CreateUserEntity

    password = factory.Faker("password")
