from dataclasses import asdict

from dependency_injector.wiring import Provide, inject
from flask import Response
from flask_openapi3 import APIBlueprint, Tag

from sobesity.containers import Services
from sobesity.domain.entities.question import QuestionFilterEnitity
from sobesity.domain.interfaces.services.question import IQuestionService
from sobesity.domain.serializers import (
    DeleteQuestionBody,
    GetQuestions,
    NotFoundSerializer,
    PatchQuestionBody,
    PathQuestionId,
    PostQuestionBody,
    QuestionIdsSerializer,
    QuestionSerializer,
)
from sobesity.domain.utils.response import bad_request_maker

question_bp = APIBlueprint(
    "question",
    __name__,
    url_prefix="/api/question",
    abp_tags=[Tag(name="question", description="Questions")],
    doc_ui=True,
    abp_security=[{"jwt": []}],
)


@question_bp.get("", responses={"200": GetQuestions})
@inject
def get_questions(question_service: IQuestionService = Provide[Services.question]):
    return question_service.get_list()


@question_bp.get("/<int:question_id>", responses={"200": QuestionSerializer})
@inject
def get_question(
    path: PathQuestionId, question_service: IQuestionService = Provide[Services.question]
):
    question = question_service.get_list(QuestionFilterEnitity(question_ids=[path.question_id]))
    if not question:
        return bad_request_maker(NotFoundSerializer(message="Question not exists"))
    return QuestionSerializer(**asdict(question[0])).dict()


@question_bp.post("", responses={"201": None})
@inject
def create_questions(
    body: PostQuestionBody, question_service: IQuestionService = Provide[Services.question]
):
    question_service.batch_create(body.to_domain())
    return Response(), 201


@question_bp.delete("", responses={"204": None})
@inject
def delete_questions(
    body: DeleteQuestionBody, question_service: IQuestionService = Provide[Services.question]
):
    question_service.delete(body.to_domain())
    return Response(), 204


@question_bp.patch("", responses={"200": QuestionIdsSerializer})
@inject
def update_question(
    body: PatchQuestionBody, question_service: IQuestionService = Provide[Services.question]
):
    return question_service.update(body.get_to_set(), body.get_where())
