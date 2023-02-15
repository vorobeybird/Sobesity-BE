from dataclasses import asdict
from http import HTTPStatus

from dependency_injector.wiring import Provide, inject
from flask import Response
from flask_openapi3 import APIBlueprint, Tag

from sobesity.containers import Services
from sobesity.domain.entities import SkillFilterEnitity
from sobesity.domain.interfaces.services import ISkillService
from sobesity.domain.serializers import (
    DeleteSkillBody,
    GetSkills,
    PatchSkillBody,
    PathSkillId,
    PostSkillBody,
    SkillIdsSerializer,
    SkillSerializer,
)

skill_bp = APIBlueprint(
    "skill",
    __name__,
    url_prefix="/api/skill",
    abp_tags=[Tag(name="skill", description="User's skills")],
    doc_ui=True,
    abp_security=[{"jwt": []}],
)


@skill_bp.get("", responses={"200": GetSkills})
@inject
def get_skills(skill_service: ISkillService = Provide[Services.skill]):
    return skill_service.get_list()


@skill_bp.get("/<int:skill_id>", responses={"200": SkillSerializer})
@inject
def get_skill(
    path: PathSkillId, skill_service: ISkillService = Provide[Services.skill]
):
    skill = skill_service.get_list(SkillFilterEnitity(skill_ids=[path.skill_id]))[0]
    return SkillSerializer(**asdict(skill)).dict()


@skill_bp.post("", responses={"201": None})
@inject
def create_skills(
    body: PostSkillBody, skill_service: ISkillService = Provide[Services.skill]
):
    skill_service.batch_create(body.to_domain())
    return Response(), HTTPStatus.CREATED


@skill_bp.delete("", responses={"204": None})
@inject
def delete_skills(
    body: DeleteSkillBody, skill_service: ISkillService = Provide[Services.skill]
):
    skill_service.delete(body.to_domain())
    return Response(), HTTPStatus.NO_CONTENT


@skill_bp.patch("", responses={"200": SkillIdsSerializer})
@inject
def update_skills(
    body: PatchSkillBody, skill_service: ISkillService = Provide[Services.skill]
):
    return skill_service.update(body.get_to_set(), body.get_where())
