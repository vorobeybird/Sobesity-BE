from http import HTTPStatus

from dependency_injector.wiring import Provide, inject
from flask import Response
from flask_openapi3 import APIBlueprint, Tag

from sobesity.containers import Services
from sobesity.domain.entities.knowledge import KnowledgeFilterEnitity
from sobesity.domain.exceptions import (
    LevelNotExistViolation,
    SkillExistViolation,
    UserNotExist,
)
from sobesity.domain.interfaces.services.knowledge import IKnowledgeService
from sobesity.domain.serializers import (
    BadRequestSerializer,
    DeleteKnowledgeBody,
    KnowledgeIdsSerializer,
    KnowledgeSerializer,
    NotFoundSerializer,
    PathKnowledgeId,
    PostKnowledgeBody,
)
from sobesity.domain.utils.response import bad_request_maker

knowledge_bp = APIBlueprint(
    "knowledge",
    __name__,
    url_prefix="/api/knowledge",
    abp_tags=[Tag(name="knowledge", description="Knowledge of users")],
    doc_ui=True,
    abp_security=[{"jwt": []}],
)


@knowledge_bp.get("/<int:knowledgeId>", responses={"200": KnowledgeSerializer})
@inject
def get_knowledge(
    path: PathKnowledgeId,
    knowledge_service: IKnowledgeService = Provide[Services.knowledge],
):
    knowleges = knowledge_service.get_list(
        KnowledgeFilterEnitity(knowledge_ids=[path.knowledge_id])
    )
    if not knowleges:
        return bad_request_maker(NotFoundSerializer(message="Note not exist"))
    return KnowledgeSerializer.from_domain(knowleges[0]).dict()


@knowledge_bp.post("", responses={"201": None})
@inject
def create_knowledges(
    body: PostKnowledgeBody,
    knowledge_service: IKnowledgeService = Provide[Services.knowledge],
):
    try:
        knowledge_service.batch_create(body.to_domain())
    except (SkillExistViolation, UserNotExist, LevelNotExistViolation) as exc:
        return bad_request_maker(BadRequestSerializer(message=exc.message))

    return Response(), HTTPStatus.CREATED


@knowledge_bp.delete("", responses={"204": None})
@inject
def delete_questions(
    body: DeleteKnowledgeBody,
    knowledge_service: IKnowledgeService = Provide[Services.knowledge],
):
    knowledge_service.delete(body.to_domain())
    return Response(), HTTPStatus.NO_CONTENT


@knowledge_bp.patch("", responses={"200": KnowledgeIdsSerializer})
@inject
def update_question(
    body: DeleteKnowledgeBody,
    knowledge_service: IKnowledgeService = Provide[Services.knowledge],
):
    try:
        return knowledge_service.update(body.get_to_set(), body.get_where())
    except (SkillExistViolation, UserNotExist, LevelNotExistViolation) as exc:
        return bad_request_maker(BadRequestSerializer(message=exc.message))
