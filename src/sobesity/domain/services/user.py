from dataclasses import asdict

from email_validator import EmailNotValidError, validate_email

from sobesity.domain.entities import CreateUserEntity, UserEntity, UserFilter
from sobesity.domain.exceptions import InvalidEmail
from sobesity.domain.interfaces.repositories import IUserRepository
from sobesity.domain.interfaces.services import IUserService
from sobesity.domain.utils.password import hash_password
from sobesity.infrastructure.constants import ModelFields


class UserService(IUserService):
    def __init__(self, user_repository: IUserRepository) -> None:
        self._user_repository = user_repository

    def validate_email(self, email):
        try:
            validate_email(email)
        except EmailNotValidError as exc:
            raise InvalidEmail(email, exc)

    def create_user(self, user: CreateUserEntity) -> None:
        self.validate_email(user.email)
        hashed_password, salt = hash_password(user.password, user.salt)

        user.hashed_password = hashed_password
        user.salt = salt
        user_params = asdict(user)
        user_params.pop(ModelFields.PASSWORD)
        hashed_user = UserEntity(**user_params)

        self._user_repository.create_user(hashed_user)

    def get_user(self, user_filter: UserFilter) -> UserEntity:
        return self._user_repository.get_user(user_filter)
