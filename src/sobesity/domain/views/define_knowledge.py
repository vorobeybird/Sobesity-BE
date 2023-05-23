from http import HTTPStatus

from dependency_injector.wiring import Provide, inject
from flask import Response
from flask_openapi3 import APIBlueprint, Tag

from sobesity.domain.serializers import (
    ThemeQuery,
    DefineKnowledgeSerializer,
    ScoringBody,
    ScoringSerializer,
    BadRequestSerializer,
)

from sobesity.domain.utils.response import bad_request_maker

from sobesity.containers import Services

from flask import current_app

from sobesity.domain.exceptions import QuestionsNotExistViolation, SkillExistViolation

define_knowledge_bp = APIBlueprint(
    "define_knowledge",
    __name__,
    url_prefix="/api/define_knowledge",
    abp_tags=[
        Tag(name="define_knowledge", description="Generate questions and scoring")
    ],
    doc_ui=True,
    abp_security=[{"jwt": []}],
)


@define_knowledge_bp.get(
    "generate_questions", responses={"200": DefineKnowledgeSerializer}
)
@inject
def get_generate_questions(query: ThemeQuery):

    generate_question_service = current_app.container.services.question_generator()
    try:
        list_questions = generate_question_service.take_question_for_theme(
            query.theme, query.level
        )
    except QuestionsNotExistViolation as exc:
        return bad_request_maker(BadRequestSerializer(message=exc.message))
    except SkillExistViolation as exc:
        return bad_request_maker(BadRequestSerializer(message=exc.message))
    return list_questions


@define_knowledge_bp.post("scoring", responses={"200": ScoringSerializer})
def get_result_of_scoring(body: ScoringBody):
    scoring_service = current_app.container.services.scoring()
    try:
        percent = scoring_service.scoring(body.question_with_list_answer)
    except ValueError as exc:
        return bad_request_maker(BadRequestSerializer(message="Question not exist"))
    except IndexError as exc:
        return bad_request_maker(BadRequestSerializer(message="Answer not exist"))
    result = ScoringSerializer(percent=percent).dict()
    return result
