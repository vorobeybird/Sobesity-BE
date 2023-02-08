from dependency_injector import containers, providers

from sobesity.config import Settings
from sobesity.domain.services import SkillService, UserService
from sobesity.infrastructure.datasource import datasource
from sobesity.infrastructure.repositories import SkillRepository, UserRepository
from sobesity.infrastructure.resources import JWTResource


class Resource(containers.DeclarativeContainer):
    config = providers.Configuration(pydantic_settings=[Settings()])
    datasource = providers.Callable(datasource)
    jwt = providers.Factory(
        JWTResource,
        config.jwt.secret,
        config.jwt.access_token_duration_days,
        config.jwt.refresh_token_duration_days,
    )


class Repositories(containers.DeclarativeContainer):
    resources = providers.DependenciesContainer()
    skill = providers.Factory(SkillRepository, resources.datasource)
    user = providers.Factory(UserRepository, resources.datasource)


class Services(containers.DeclarativeContainer):
    resources = providers.DependenciesContainer()
    repositories = providers.DependenciesContainer()
    skill = providers.Factory(SkillService, repositories.skill)
    user = providers.Factory(UserService, repositories.user, resources.jwt)


class Application(containers.DeclarativeContainer):
    resources = providers.Container(Resource)
    repositories = providers.Container(Repositories, resources=resources)
    services = providers.Container(
        Services, repositories=repositories, resources=resources
    )
