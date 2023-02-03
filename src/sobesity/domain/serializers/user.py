from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field

from sobesity.domain.entities import CreateUserEntity, UserEntity, UserFilter, UserId


class GetUserSerializer(BaseModel):
    user_id: UserId = Field(..., alias="userId")
    nickname: str
    email: EmailStr
    registered_at: datetime = Field(..., alias="registeredAt")

    @classmethod
    def from_domain(cls, user: UserEntity):
        return cls(
            userId=user.user_id,
            nickname=user.nickname,
            email=user.email,
            registeredAt=user.registered_at,
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


class PostUserSerializer(BaseModel):
    nickname: str
    email: EmailStr
    password: str = Field(..., min_length=6)

    def to_domain(self) -> CreateUserEntity:
        return CreateUserEntity(
            nickname=self.nickname,
            email=self.email,
            password=self.password,
        )
