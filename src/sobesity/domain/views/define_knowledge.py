
from dependency_injector.wiring import inject
from flask import current_app
from flask_openapi3 import APIBlueprint, Tag

from sobesity.domain.exceptions import (
    AnswerNotExistViolation,
    QuestionExistViolation,
    QuestionsNotExistViolation,
    SkillExistViolation,
)
from sobesity.domain.serializers import (
    BadRequestSerializer,
    DefineKnowledgeSerializer,
    ScoringBody,
    ScoringSerializer,
    ThemeQuery,
)
from sobesity.domain.utils.response import bad_request_maker

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
    except QuestionExistViolation as exc:
        return bad_request_maker(BadRequestSerializer(message=exc.message))
    except AnswerNotExistViolation as exc:
        return bad_request_maker(BadRequestSerializer(message=exc.message))
    result = ScoringSerializer(percent=percent).dict()
    return result
