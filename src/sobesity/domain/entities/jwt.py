from dataclasses import dataclass
from datetime import datetime
from typing import NewType

from sobesity.domain.entities.user import UserId

JWTToken = NewType("JWTToken", str)


@dataclass
class JWTEntity:
    sub: UserId
    exp: datetime
    iat: datetime
