from http import HTTPStatus

from dependency_injector.wiring import Provide, inject
from flask import Response
from flask_openapi3 import APIBlueprint, Tag

from sobesity.containers import Services
from sobesity.domain.entities import SkillFilterEnitity
from sobesity.domain.exceptions.skill import SkillNameUniqueViolation
from sobesity.domain.interfaces.services import ISkillService
from sobesity.domain.serializers import (
    BadRequestSerializer,
    DeleteSkillBody,
    GetSkills,
    NotFoundSerializer,
    PatchSkillBody,
    PathSkillId,
    PostSkillBody,
    SkillIdsSerializer,
    SkillSerializer,
)
from sobesity.domain.utils.response import bad_request_maker

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


@skill_bp.get("/<int:skillId>", responses={"200": SkillSerializer})
@inject
def get_skill(
    path: PathSkillId, skill_service: ISkillService = Provide[Services.skill]
):
    skills = skill_service.get_list(SkillFilterEnitity(skill_ids=[path.skill_id]))
    if not skills:
        return bad_request_maker(NotFoundSerializer(message="Skill not exists"))
    return SkillSerializer.from_domain(skills[0]).dict()


@skill_bp.post("", responses={"201": None, "400": BadRequestSerializer})
@inject
def create_skills(
    body: PostSkillBody, skill_service: ISkillService = Provide[Services.skill]
):
    try:
        skill_service.batch_create(body.to_domain())
    except SkillNameUniqueViolation as exc:
        return bad_request_maker(BadRequestSerializer(message=exc.message))
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
