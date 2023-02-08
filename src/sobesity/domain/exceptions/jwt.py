from sobesity.domain.exceptions.base import AuthException


class ExpiredToken(AuthException):
    def __init__(self):
        self.message = "JWT token signature has expired"
        super().__init__(self.message)


class CorruptedToken(AuthException):
    def __init__(self):
        self.message = "JWT token is corrupted"
        super().__init__(self.message)
