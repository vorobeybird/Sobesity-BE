from dependency_injector import containers, providers


class Repositories(containers.DeclarativeContainer):
    pass


class Services(containers.DeclarativeContainer):
    repositories = providers.DependenciesContainer()


class Application(containers.DeclarativeContainer):
    repositories = providers.Container(Repositories)
    services = providers.Container(Services, repositories=repositories)
