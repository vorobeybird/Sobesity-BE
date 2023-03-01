from dataclasses import asdict

from dependency_injector.wiring import Provide, inject
from flask import Response
from flask_openapi3 import APIBlueprint, Tag

from sobesity.containers import Services
from sobesity.domain.entities.answer import AnswerFilterEnitity
from sobesity.domain.interfaces.services.answer import IAnswerService
from sobesity.domain.serializers import (
    DeleteAnswerBody,
    GetAnswers,
    PatchAnswerBody,
    PathAnswerId,
    PostAnswerBody,
    AnswerIdsSerializer,
    AnswerSerializer,
)

answer_bp = APIBlueprint(
    "answer",
    __name__,
    url_prefix="/api/answer",
    abp_tags=[Tag(name="answer", description="Answers")],
    doc_ui=True,
    abp_security=[{"jwt": []}],
)


@answer_bp.get("", responses={"200": GetAnswers})
@inject
def get_answers(answer_service: IAnswerService = Provide[Services.answer]):
    return answer_service.get_list()


@answer_bp.get("/<int:answer_id>", responses={"200": AnswerSerializer})
@inject
def get_answer(
    path: PathAnswerId, answer_service: IAnswerService = Provide[Services.answer]
):
    answer = answer_service.get_list(AnswerFilterEnitity(answer_ids=[path.answer_id]))[0]
    return AnswerSerializer(**asdict(answer)).dict()


@answer_bp.post("", responses={"201": None})
@inject
def create_answers(
    body: PostAnswerBody, answer_service: IAnswerService = Provide[Services.answer]
):
    answer_service.batch_create(body.to_domain())
    return Response(), 201


@answer_bp.delete("", responses={"204": None})
@inject
def delete_answers(
    body: DeleteAnswerBody, answer_service: IAnswerService = Provide[Services.answer]
):
    answer_service.delete(body.to_domain())
    return Response(), 204


@answer_bp.patch("", responses={"200": AnswerIdsSerializer})
@inject
def update_answer(
    body: PatchAnswerBody, answer_service: IAnswerService = Provide[Services.answer]
):
    return answer_service.update(body.get_to_set(), body.get_where())
