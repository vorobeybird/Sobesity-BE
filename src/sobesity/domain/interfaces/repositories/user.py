from abc import ABC, abstractclassmethod

from sobesity.domain.entities import UserEntity, UserFilter


class IUserRepository(ABC):
    @abstractclassmethod
    def create_user(self, user: UserEntity) -> None:
        pass

    @abstractclassmethod
    def get_user(self, user_filter: UserFilter) -> UserEntity:
        pass
