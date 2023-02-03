from flask import Flask
from flask_openapi3 import Info, OpenAPI, HTTPBearer

from sobesity.containers import Application
from sobesity.domain.views import skill, user
from sobesity.jwt import verify_jwt


def register_views(app):
    app.register_api(skill.skill_bp)
    app.register_api(user.user_bp)


def init_dependency(app):
    container = Application()
    container.services.wire([skill, user])
    app.container = container

def enable_jwt_check(app):
    app.before_request(verify_jwt)

def prepare_swagger() ->Flask:
    info = Info(title="Sobesity API", version="0.0.1")
    security_schemes = {"jwt": HTTPBearer(bearerFormat="JWT")}

    return OpenAPI(__name__, info=info, security_schemes=security_schemes)

def create_app():
    app = prepare_swagger()

    init_dependency(app)
    register_views(app)
    enable_jwt_check(app)

    return app
