from typing import Optional

from sobesity.domain.entities import (
    KnowledgeEntity,
    KnowledgeFilterEnitity,
    KnowledgeId,
)
from sobesity.domain.interfaces.repositories import IKnowledgeRepository
from sobesity.domain.interfaces.services import IKnowledgeService


class KnowledgeService(IKnowledgeService):
    def __init__(self, knowledge_repository: IKnowledgeRepository) -> None:
        self._knowledge_repository = knowledge_repository

    def get_list(
        self, knowledge_filter: Optional[KnowledgeFilterEnitity] = None
    ) -> list[KnowledgeEntity]:
        return self._knowledge_repository.get_list(knowledge_filter)

    def batch_create(self, knowledges: list[KnowledgeEntity]) -> None:
        return self._knowledge_repository.batch_create(knowledges)

    def update(
        self, old_knowledge: KnowledgeEntity, update: KnowledgeFilterEnitity
    ) -> list[KnowledgeId]:
        return self._knowledge_repository.update(old_knowledge, update)

    def delete(self, knowledge_ids: list[KnowledgeId]) -> None:
        return self._knowledge_repository.delete(knowledge_ids)
