from flask_openapi3 import Info, OpenAPI

from sobesity.containers import Application
from sobesity.domain.views import skill, question, answer


def create_app():
    info = Info(title="Sobesity API", version="0.0.1")
    app = OpenAPI(__name__, info=info)

    container = Application()
    container.services.wire([skill])
    container.services.wire([question])
    container.services.wire([answer])
    app.container = container

    app.register_api(skill.skill_bp)
    app.register_api(question.question_bp)
    app.register_api(answer.answer_bp)
    return app
