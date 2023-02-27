from pydantic import BaseModel


class BaseBadRequest(BaseModel):
    message: str


class NotFoundSerializer(BaseBadRequest):
    pass


class BadRequestSerializer(BaseBadRequest):
    pass
