from dataclasses import asdict

from email_validator import EmailNotValidError, validate_email

from sobesity.domain.entities import (
    CreateUserEntity,
    JWTToken,
    LoginUserEntity,
    UserEntity,
    UserFilter,
)
from sobesity.domain.exceptions import InvalidEmail, UserNotFound
from sobesity.domain.interfaces.repositories import IUserRepository
from sobesity.domain.interfaces.resources import IJWTResource
from sobesity.domain.interfaces.services import IUserService
from sobesity.domain.utils.password import check_password, hash_password
from sobesity.infrastructure.constants import ModelFields


class UserService(IUserService):
    def __init__(
        self, user_repository: IUserRepository, jwt_resource: IJWTResource
    ) -> None:
        self._user_repository = user_repository
        self._jwt_resource = jwt_resource

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

    def check_password(self, password: str, hashed_password: str):
        if not check_password(password, hashed_password):
            raise ValueError("Invalid password")

    def login(self, login_user: LoginUserEntity) -> JWTToken:
        try:
            user = self.get_user(UserFilter(email=login_user.email))
        except UserNotFound:
            raise ValueError("Incorrect email")
        self.check_password(login_user.password, user.hashed_password)
        return self._jwt_resource.encode_jwt(user.user_id)
