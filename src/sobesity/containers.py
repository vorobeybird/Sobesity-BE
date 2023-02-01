from dependency_injector import containers, providers

from sobesity.domain.services import SkillService, UserService
from sobesity.infrastructure.datasource import datasource
from sobesity.infrastructure.repositories import SkillRepository, UserRepository


class Resource(containers.DeclarativeContainer):
    datasource = providers.Callable(datasource)


class Repositories(containers.DeclarativeContainer):
    resources = providers.DependenciesContainer()
    skill = providers.Factory(SkillRepository, resources.datasource)
    user = providers.Factory(UserRepository, resources.datasource)


class Services(containers.DeclarativeContainer):
    repositories = providers.DependenciesContainer()
    skill = providers.Factory(SkillService, repositories.skill)
    user = providers.Factory(UserService, repositories.user)


class Application(containers.DeclarativeContainer):
    resources = providers.Container(Resource)
    repositories = providers.Container(Repositories, resources=resources)
    services = providers.Container(Services, repositories=repositories)
