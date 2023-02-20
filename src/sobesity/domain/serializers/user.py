from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field

from sobesity.domain.entities import (
    CreateUserEntity,
    LoginUserEntity,
    UserEntity,
    UserFilter,
    UserId,
)

user_id_field = Field(..., alias="userId")
first_name_field = Field(..., alias="firstName")
last_name_field = Field(..., alias="lastName")


class GetUserSerializer(BaseModel):
    user_id: UserId = user_id_field
    nickname: str
    email: EmailStr
    registered_at: datetime = Field(..., alias="registeredAt")
    fist_name: str = first_name_field
    last_name: str = last_name_field

    @classmethod
    def from_domain(cls, user: UserEntity):
        return cls(
            userId=user.user_id,
            nickname=user.nickname,
            email=user.email,
            registeredAt=user.registered_at,
            firstName=user.first_name,
            lastName=user.last_name,
        )


class UserQuery(BaseModel):
    user_id: Optional[UserId] = Field(None, alias="userId")
    email: Optional[EmailStr] = None
    nickname: Optional[str] = None

    def to_domain(self) -> UserFilter:
        return UserFilter(
            user_id=self.user_id,
            email=self.email,
            nickname=self.nickname,
        )


class CreateUserSerializer(BaseModel):
    nickname: str
    email: EmailStr
    password: str = Field(..., min_length=6)
    first_name: str = first_name_field
    last_name: str = last_name_field

    def to_domain(self) -> CreateUserEntity:
        return CreateUserEntity(
            nickname=self.nickname,
            email=self.email,
            password=self.password,
            first_name=self.first_name,
            last_name=self.last_name,
        )


class LoginUserSerializer(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6)

    def to_domain(self) -> LoginUserEntity:
        return LoginUserEntity(email=self.email, password=self.password)


class AccessGrantedSerializer(BaseModel):
    access_token: str
