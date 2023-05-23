from http import HTTPStatus

from dependency_injector.wiring import Provide, inject
from flask import Response
from flask_openapi3 import APIBlueprint, Tag

from sobesity.containers import Services
from sobesity.domain.entities import LevelFilterEnitity
from sobesity.domain.exceptions.skill import LevelNameUniqueViolation
from sobesity.domain.interfaces.services import ILevelService
from sobesity.domain.serializers import (
    BadRequestSerializer,
    DeleteLevelBody,
    GetLevels,
    NotFoundSerializer,
    PatchLevelBody,
    PathLevelId,
    PostLevelBody,
    LevelIdsSerializer,
    LevelSerializer,
)
from sobesity.domain.utils.response import bad_request_maker

level_bp = APIBlueprint(
    "level",
    __name__,
    url_prefix="/api/level",
    abp_tags=[Tag(name="skill", description="User's levels")],
    doc_ui=True,
    abp_security=[{"jwt": []}],
)


@level_bp.get("", responses={"200": GetLevels})
@inject
def get_levels(level_service: ILevelService = Provide[Services.level]):
    return level_service.get_list()


@level_bp.get("/<int:levelId>", responses={"200": LevelSerializer})
@inject
def get_level(
    path: PathLevelId, level_service: ILevelService = Provide[Services.level]
):
    levels = level_service.get_list(LevelFilterEnitity(level_ids=[path.level_id]))
    if not levels:
        return bad_request_maker(NotFoundSerializer(message="Level not exists"))
    return LevelSerializer.from_domain(levels[0]).dict()


@level_bp.post("", responses={"201": None, "400": BadRequestSerializer})
@inject
def create_levels(
    body: PostLevelBody, level_service: ILevelService = Provide[Services.level]
):
    try:
        level_service.batch_create(body.to_domain())
    except LevelNameUniqueViolation as exc:
        return bad_request_maker(BadRequestSerializer(message=exc.message))
    return Response(), HTTPStatus.CREATED


@level_bp.delete("", responses={"204": None})
@inject
def delete_levels(
    body: DeleteLevelBody, level_service: ILevelService = Provide[Services.level]
):
    level_service.delete(body.to_domain())
    return Response(), HTTPStatus.NO_CONTENT


@level_bp.patch("", responses={"200": LevelIdsSerializer})
@inject
def update_levels(
    body: PatchLevelBody, level_service: ILevelService = Provide[Services.level]
):
    return level_service.update(body.get_to_set(), body.get_where())
