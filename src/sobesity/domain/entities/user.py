from dataclasses import dataclass
from datetime import datetime
from typing import NewType, Optional

UserId = NewType("UserId", int)


@dataclass(kw_only=True)
class UserEntity:
    user_id: Optional[UserId] = None
    nickname: str
    email: str
    registered_at: Optional[datetime] = None
    hashed_password: Optional[str] = None
    salt: Optional[str] = None


@dataclass(kw_only=True)
class CreateUserEntity(UserEntity):
    password: str


@dataclass
class UserFilter:
    user_id: Optional[UserId] = None
    email: Optional[str] = None
    nickname: Optional[str] = None

    def __post_init__(self):
        if not any((self.user_id, self.email, self.nickname)):
            raise ValueError("One of parameters must be specified")


@dataclass
class LoginUserEntity:
    email: str
    password: str
