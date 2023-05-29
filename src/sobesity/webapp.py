import logging

from flask import Flask
from flask_cors import CORS
from flask_openapi3 import HTTPBearer, Info, OpenAPI

from sobesity.containers import Application
from sobesity.domain.views import answer, define_knowledge, question, skill, type, user


def setup_logger(config):
    level = logging.getLevelNamesMapping()[config.app.logger_level()]
    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(process)d] [%(levelname)s] %(message)s",
        datefmt="[%Y-%m-%d %H:%M:%S %z]",
    )


def register_apis(app):
    apis = (
        skill.skill_bp,
        user.user_bp,
        question.question_bp,
        answer.answer_bp,
        type.type_bp,
        define_knowledge.define_knowledge_bp,
    )
    for api in apis:
        app.register_api(api)


def init_dependency():
    container = Application()
    container.services.wire([skill, user, question, answer, type])
    return container


def enable_jwt_check(app):
    app.before_request(app.container.resources.jwt().verify_jwt)


def prepare_swagger() -> Flask:
    info = Info(title="Sobesity API", version="0.0.1")
    security_schemes = {"jwt": HTTPBearer(bearerFormat="JWT")}

    return OpenAPI(__name__, info=info, security_schemes=security_schemes)


def create_app():
    app = prepare_swagger()

    container = init_dependency()
    app.container = container
    config = container.resources.config

    setup_logger(config)

    CORS(app, resources={r"/api/*": {"origins": "*"}})

    register_apis(app)
    enable_jwt_check(app)

    return app
