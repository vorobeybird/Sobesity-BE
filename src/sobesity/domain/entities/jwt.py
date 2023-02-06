from dataclasses import dataclass
from datetime import datetime

from sobesity.domain.entities.user import UserId


@dataclass
class JWTEntity:
    sub: UserId
    exp: datetime
    iat: datetime
