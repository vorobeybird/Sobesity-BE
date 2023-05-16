from http import HTTPStatus

from dependency_injector.wiring import Provide, inject
from flask import Response
from flask_openapi3 import APIBlueprint, Tag

from sobesity.domain.serializers import (
    ThemeQuery,
    DefineKnowledgeSerializer,
    ScoringQuery,
    ScoringSerializer,
)

from sobesity.domain.services.generate_questions import take_question_for_theme

from sobesity.domain.services.scoring import scoring

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


@define_knowledge_bp.get("", responses={"200": DefineKnowledgeSerializer})
def get_generate_questions(query: ThemeQuery):
    list_questions = take_question_for_theme(query.theme, query.level)

    return list_questions


@define_knowledge_bp.get("/scoring", responses={"200": ScoringSerializer})
def get_result_of_scoring(query: ScoringQuery):
    percent = scoring(query.question_with_list_answer)
    return percent
