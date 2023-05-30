from sobesity.domain.exceptions.base import DomainException, EntityNotFound


class LevelNameUniqueViolation(DomainException):
    def __init__(self) -> None:
        self.message = "Level names must be unique"
        super().__init__(self.message)


class LevelNotExistViolation(Exception):
    def __init__(self) -> None:
        self.message = "Level not exist"
        super().__init__(self.message)


class LevelNotFound(EntityNotFound):
    def __init__(self, search_params: "KnowledgeFilterEnitity") -> None:
        self.message = f"Level not found with params ({search_params})"
        self.search_params = search_params
        super().__init__(self.message)
