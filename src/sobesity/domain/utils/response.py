from pydantic import BaseModel
from sobesity.domain.serializers import NotFoundSerializer, BadRequestSerializer

from http import HTTPStatus

def bad_request_maker(serializer: BaseModel) -> tuple[dict, int]:
    serializer_map = {
        NotFoundSerializer: HTTPStatus.NOT_FOUND,
        BadRequestSerializer: HTTPStatus.BAD_REQUEST
    }
    code = serializer_map[type(serializer)]
    response = serializer.dict()
    return response, code
