from dependency_injector import containers, providers

from sobesity.config import Settings
from sobesity.domain.access_managers import UserAccessManager
from sobesity.domain.services import (
    AnswerService,
    QuestionService,
    SkillService,
    UserService,
    TypeService,
)
from sobesity.infrastructure.datasource import datasource
from sobesity.infrastructure.repositories import (
    AnswerRepository,
    QuestionRepository,
    SkillRepository,
    UserRepository,
    TypeRepository,
)
from sobesity.infrastructure.resources import JWTResource


class Resources(containers.DeclarativeContainer):
    config = providers.Configuration(pydantic_settings=[Settings()])
    datasource = providers.Callable(datasource)
    jwt = providers.Singleton(
        JWTResource,
        config.jwt.secret,
        config.jwt.access_token_duration_days,
        config.jwt.refresh_token_duration_days,
    )


class Repositories(containers.DeclarativeContainer):
    resources = providers.DependenciesContainer()
    question = providers.Singleton(QuestionRepository, resources.datasource)
    answer = providers.Singleton(AnswerRepository, resources.datasource)
    type = providers.Singleton(TypeRepository, resources.datasource)
    skill = providers.Singleton(SkillRepository, resources.datasource)
    user = providers.Singleton(UserRepository, resources.datasource)


class Services(containers.DeclarativeContainer):
    repositories = providers.DependenciesContainer()
    question = providers.Singleton(QuestionService, repositories.question)
    answer = providers.Singleton(AnswerService, repositories.answer)
    type = providers.Singleton(TypeService, repositories.type)
    skill = providers.Singleton(SkillService, repositories.skill)
    user = providers.Singleton(UserService, repositories.user)


class AccessManagers(containers.DeclarativeContainer):
    resources = providers.DependenciesContainer()
    services = providers.DependenciesContainer()
    user = providers.Singleton(
        UserAccessManager,
        user_service=services.user,
        jwt_resource=resources.jwt,
    )


class Application(containers.DeclarativeContainer):
    resources = providers.Container(Resources)
    repositories = providers.Container(Repositories, resources=resources)
    services = providers.Container(Services, repositories=repositories)
    access_managers = providers.Container(
        AccessManagers, resources=resources, services=services
    )
