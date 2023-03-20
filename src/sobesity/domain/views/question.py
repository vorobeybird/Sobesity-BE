from http import HTTPStatus

from dependency_injector.wiring import Provide, inject
from flask import Response
from flask_openapi3 import APIBlueprint, Tag

from sobesity.domain.exceptions import SkillExistViolation
from sobesity.containers import Services
from sobesity.domain.entities.question import QuestionFilterEnitity
from sobesity.domain.interfaces.services.question import IQuestionService
from sobesity.domain.serializers import (
    BadRequestSerializer,
    DeleteQuestionBody,
    GetQuestions,
    NotFoundSerializer,
    PatchQuestionBody,
    PathQuestionId,
    PathSkillId,
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


@question_bp.get("/<int:questionId>", responses={"200": QuestionSerializer})
@inject
def get_question(
    path: PathQuestionId,
    question_service: IQuestionService = Provide[Services.question],
):
    questions = question_service.get_list(
        QuestionFilterEnitity(question_ids=[path.question_id])
    )
    if not questions:
        return bad_request_maker(NotFoundSerializer(message="Question not exist"))
    return QuestionSerializer.from_domain(questions[0]).dict()


@question_bp.post("", responses={"201": None})
@inject
def create_questions(
    body: PostQuestionBody,
    question_service: IQuestionService = Provide[Services.question],
):
    try:
        question_service.batch_create(body.to_domain())
    except SkillExistViolation as exc:
        return bad_request_maker(BadRequestSerializer(message=exc.message))
    return Response(), HTTPStatus.CREATED


@question_bp.delete("", responses={"204": None})
@inject
def delete_questions(
    body: DeleteQuestionBody,
    question_service: IQuestionService = Provide[Services.question],
):
    question_service.delete(body.to_domain())
    return Response(), HTTPStatus.NO_CONTENT


@question_bp.patch("", responses={"200": QuestionIdsSerializer})
@inject
def update_question(
    body: PatchQuestionBody,
    question_service: IQuestionService = Provide[Services.question],
):
    try:
        return question_service.update(body.get_to_set(), body.get_where())
    except SkillExistViolation as exc:
        return bad_request_maker(BadRequestSerializer(message=exc.message))


@question_bp.get("find_questions/<int:skillId>", responses={"200": QuestionSerializer})
@inject
def find_question_to_skill(
    path: PathSkillId, question_service: IQuestionService = Provide[Services.question]
):
    questions = question_service.get_list(
        QuestionFilterEnitity(skill_ids=[path.skill_id])
    )
    if not questions:
        return bad_request_maker(NotFoundSerializer(message="Questions not exists"))
    return questions
