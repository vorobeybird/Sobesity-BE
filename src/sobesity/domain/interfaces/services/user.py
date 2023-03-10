from abc import ABC, abstractclassmethod

from sobesity.domain.entities import CreateUserEntity, UserEntity, UserFilter


class IUserService(ABC):
    @abstractclassmethod
    def create_user(self, user: CreateUserEntity) -> None:
        pass

    @abstractclassmethod
    def get_user(self, user_filter: UserFilter) -> UserEntity:
        pass
