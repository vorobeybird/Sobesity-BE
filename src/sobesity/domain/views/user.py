from http import HTTPStatus

from dependency_injector.wiring import Provide, inject
from flask import Response, current_app
from flask_openapi3 import APIBlueprint, Tag

from sobesity.containers import Services
from sobesity.domain.exceptions import (
    EmailNotExists,
    EmailUniqueViolation,
    InvalidEmail,
    NicknameUniqueViolation,
    PasswordNotMatch,
    UserFilterParamError,
    UserNotFound,
)
from sobesity.domain.interfaces.access_managers import IUserAccessManager
from sobesity.domain.interfaces.services import IUserService
from sobesity.domain.serializers import (
    AccessGrantedSerializer,
    BadRequestSerializer,
    CreateUserSerializer,
    GetUserSerializer,
    LoginUserSerializer,
    NotFoundSerializer,
    UserQuery,
)
from sobesity.domain.utils.response import bad_request_maker

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
        return bad_request_maker(NotFoundSerializer(message=exc.message))
    except  UserFilterParamError as exc:
        return bad_request_maker(BadRequestSerializer(message=exc.message))
    return GetUserSerializer.from_domain(user).dict()


@user_bp.post("", responses={"201": None, "400": BadRequestSerializer})
@inject
def create_user(
    body: CreateUserSerializer, user_service: IUserService = Provide[Services.user]
):
    try:
        user_service.create_user(body.to_domain())
    except (InvalidEmail, NicknameUniqueViolation, EmailUniqueViolation) as exc:
        return bad_request_maker(BadRequestSerializer(message=exc.message))
    return Response(), HTTPStatus.CREATED


@user_bp.post(
    "login", responses={"200": AccessGrantedSerializer, "400": BadRequestSerializer}
)
def login(
    body: LoginUserSerializer,
):
    # TODO must be implemented with Provide
    user_access_manager: IUserAccessManager = (
        current_app.container.access_managers.user()
    )
    try:
        token = user_access_manager.login(body.to_domain())
    except (EmailNotExists, PasswordNotMatch):
        return bad_request_maker(
            BadRequestSerializer(message="Invalid email or password")
        )
    return AccessGrantedSerializer(access_token=token).dict()


@user_bp.get(
    "current_user", responses={"200": GetUserSerializer}, security=[{"jwt": []}]
)
def current_user():
    # TODO must be implemented with Provide
    user_access_manager: IUserAccessManager = (
        current_app.container.access_managers.user()
    )
    user = user_access_manager.get_current_user()
    return GetUserSerializer.from_domain(user).dict()
