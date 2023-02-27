from flask import Flask
from flask_cors import CORS
from flask_openapi3 import HTTPBearer, Info, OpenAPI

from sobesity.containers import Application
from sobesity.domain.views import skill, user


def register_views(app):
    app.register_api(skill.skill_bp)
    app.register_api(user.user_bp)


def init_dependency():
    container = Application()
    container.services.wire([skill, user])
    return container


def enable_jwt_check(app):
    app.before_request(app.container.resources.jwt().verify_jwt)


def prepare_swagger() -> Flask:
    info = Info(title="Sobesity API", version="0.0.1")
    security_schemes = {"jwt": HTTPBearer(bearerFormat="JWT")}

    return OpenAPI(__name__, info=info, security_schemes=security_schemes)


def create_app():
    container = init_dependency()
    app = prepare_swagger()
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    app.container = container

    register_views(app)
    enable_jwt_check(app)

    return app
