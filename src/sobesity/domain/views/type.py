from http import HTTPStatus

from dependency_injector.wiring import Provide, inject
from flask import Response
from flask_openapi3 import APIBlueprint, Tag

from sobesity.containers import Services
from sobesity.domain.entities import TypeFilterEnitity
from sobesity.domain.exceptions.type import TypeNameUniqueViolation
from sobesity.domain.interfaces.services import ITypeService
from sobesity.domain.serializers import (
    BadRequestSerializer,
    DeleteTypeBody,
    GetTypes,
    NotFoundSerializer,
    PatchTypeBody,
    PathTypeId,
    PostTypeBody,
    TypeIdsSerializer,
    TypeSerializer,
)
from sobesity.domain.utils.response import bad_request_maker

type_bp = APIBlueprint(
    "type",
    __name__,
    url_prefix="/api/type",
    abp_tags=[Tag(name="type", description="Type's of questions")],
    doc_ui=True,
    abp_security=[{"jwt": []}],
)


@type_bp.get("", responses={"200": GetTypes})
@inject
def get_types(type_service: ITypeService = Provide[Services.type]):
    return type_service.get_list()


@type_bp.get("/<int:typeId>", responses={"200": TypeSerializer})
@inject
def get_type(path: PathTypeId, type_service: ITypeService = Provide[Services.type]):
    types = type_service.get_list(TypeFilterEnitity(type_ids=[path.type_id]))
    if not types:
        return bad_request_maker(NotFoundSerializer(message="Type not exists"))
    return TypeSerializer.from_domain(types[0]).dict()


@type_bp.post("", responses={"201": None, "400": BadRequestSerializer})
@inject
def create_types(
    body: PostTypeBody, type_service: ITypeService = Provide[Services.type]
):
    try:
        type_service.batch_create(body.to_domain())
    except TypeNameUniqueViolation as exc:
        return bad_request_maker(BadRequestSerializer(message=exc.message))
    return Response(), HTTPStatus.CREATED


@type_bp.delete("", responses={"204": None})
@inject
def delete_types(
    body: DeleteTypeBody, type_service: ITypeService = Provide[Services.type]
):
    type_service.delete(body.to_domain())
    return Response(), HTTPStatus.NO_CONTENT


@type_bp.patch("", responses={"200": TypeIdsSerializer})
@inject
def update_skills(
    body: PatchTypeBody, type_service: ITypeService = Provide[Services.type]
):
    return type_service.update(body.get_to_set(), body.get_where())
