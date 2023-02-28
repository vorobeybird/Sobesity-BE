from sobesity.domain.entities import (JWTToken, LoginUserEntity, UserEntity,
                                      UserFilter)
from sobesity.domain.entities.user import UserEntity, UserFilter
from sobesity.domain.exceptions import (EmailNotExists, PasswordNotMatch,
                                        UserNotFound)
from sobesity.domain.interfaces.access_managers import IUserAccessManager
from sobesity.domain.interfaces.resources import IJWTResource
from sobesity.domain.interfaces.services import IUserService
from sobesity.domain.utils.password import check_password


class UserAccessManager(IUserAccessManager):
    def __init__(self, jwt_resource: IJWTResource, user_service: IUserService):
        self._jwt_resource = jwt_resource
        self._user_service = user_service

    def get_current_user(self) -> UserEntity:
        user_id = self._jwt_resource.get_user_id_from_request()
        return self._user_service.get_user(UserFilter(user_id=user_id))

    def check_password(self, password: str, hashed_password: str):
        if not check_password(password, hashed_password):
            raise PasswordNotMatch()

    def login(self, login_user: LoginUserEntity) -> JWTToken:
        try:
            user = self._user_service.get_user(UserFilter(email=login_user.email))
        except UserNotFound:
            raise EmailNotExists(login_user.email)

        self.check_password(login_user.password, user.hashed_password)
        return self._jwt_resource.encode_jwt(user.user_id)
