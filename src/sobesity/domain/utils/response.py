from http import HTTPStatus

from pydantic import BaseModel

from sobesity.domain.serializers import BadRequestSerializer, NotFoundSerializer


def bad_request_maker(serializer: BaseModel) -> tuple[dict, int]:
    serializer_map = {
        NotFoundSerializer: HTTPStatus.NOT_FOUND,
        BadRequestSerializer: HTTPStatus.BAD_REQUEST,
    }
    code = serializer_map[type(serializer)]
    response = serializer.dict()
    return response, code
