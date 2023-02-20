from abc import ABC, abstractclassmethod

from sobesity.domain.entities.jwt import JWTToken
from sobesity.domain.entities.user import LoginUserEntity, UserEntity


class IUserAccessManager(ABC):
    @abstractclassmethod
    def get_current_user() -> UserEntity:
        pass

    @abstractclassmethod
    def login(self, login_user: LoginUserEntity) -> JWTToken:
        pass
