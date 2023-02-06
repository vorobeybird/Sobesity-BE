from http import HTTPStatus
from dependency_injector.wiring import Provide, inject
from flask import Response
from flask_openapi3 import APIBlueprint, Tag

from sobesity.containers import Services
from sobesity.domain.exceptions import InvalidEmail, UserNotFound
from sobesity.domain.interfaces.services import IUserService
from sobesity.domain.serializers import (
    BadRequestSerializer,
    GetUserSerializer,
    NotFoundSerializer,
    PostUserSerializer,
    UserQuery,
)

user_bp = APIBlueprint(
    "user",
    __name__,
    url_prefix="/api/user",
    abp_tags=[Tag(name="user", description="User management APIs")],
    doc_ui=True,
)


@user_bp.get("", responses={"200": GetUserSerializer, "404": NotFoundSerializer})
@inject
def get_user(query: UserQuery, user_service: IUserService = Provide[Services.user]):
    try:
        user = user_service.get_user(query.to_domain())
    except UserNotFound as exc:
        return NotFoundSerializer(message=exc.message).dict(), HTTPStatus.NOT_FOUND
    return GetUserSerializer.from_domain(user).dict()


@user_bp.post("", responses={"201": None, "400": BadRequestSerializer})
@inject
def create_user(
    body: PostUserSerializer, user_service: IUserService = Provide[Services.user]
):
    try:
        user_service.create_user(body.to_domain())
    except InvalidEmail as exc:
        return BadRequestSerializer(message=exc.message).dict(), HTTPStatus.BAD_REQUEST
    return Response(), HTTPStatus.CREATED


# TODO add login view and refresh token
