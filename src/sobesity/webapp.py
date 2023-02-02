from flask_openapi3 import Info, OpenAPI

from sobesity.containers import Application
from sobesity.domain.views import skill, user


def register_views(app):
    app.register_api(skill.skill_bp)
    app.register_api(user.user_bp)


def init_dependency(app):
    container = Application()
    container.services.wire([skill, user])
    app.container = container


def create_app():
    info = Info(title="Sobesity API", version="0.0.1")
    app = OpenAPI(__name__, info=info)

    init_dependency(app)
    register_views(app)

    return app
