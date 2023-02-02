from pydantic import BaseModel


class NotFoundSerializer(BaseModel):
    message: str


class BadRequestSerializer(BaseModel):
    message: str
