from abc import ABC, abstractclassmethod

from sobesity.domain.entities import JWTToken, UserId


class IJWTResource(ABC):
    @abstractclassmethod
    def verify_jwt(self):
        pass

    @abstractclassmethod
    def get_user_id_from_request(self) -> UserId:
        pass

    @abstractclassmethod
    def get_user_id_from_jwt(self, token) -> UserId:
        pass

    @abstractclassmethod
    def encode_jwt(self, user_id: UserId) -> JWTToken:
        pass
