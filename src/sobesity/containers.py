from dependency_injector import containers, providers

from sobesity.domain.services import SkillService
from sobesity.infrastructure.datasource import datasource
from sobesity.infrastructure.repositories import SkillRepository


class Resource(containers.DeclarativeContainer):
    datasource = providers.Callable(datasource)


class Repositories(containers.DeclarativeContainer):
    resources = providers.DependenciesContainer()
    skill = providers.Factory(SkillRepository, resources.datasource)


class Services(containers.DeclarativeContainer):
    repositories = providers.DependenciesContainer()
    skill = providers.Factory(SkillService, repositories.skill)


class Application(containers.DeclarativeContainer):
    resources = providers.Container(Resource)
    repositories = providers.Container(Repositories, resources=resources)
    services = providers.Container(Services, repositories=repositories)
