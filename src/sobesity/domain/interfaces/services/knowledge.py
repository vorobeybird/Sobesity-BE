from abc import ABC, abstractclassmethod
from typing import Optional

from sobesity.domain.entities import (
    KnowledgeEntity,
    KnowledgeFilterEnitity,
    KnowledgeId,
)


class IKnowledgeService(ABC):
    @abstractclassmethod
    def get_list(
        self, knowledge_filter: Optional[KnowledgeFilterEnitity] = None
    ) -> list[KnowledgeEntity]:
        pass

    @abstractclassmethod
    def batch_create(self, knowledges: list[KnowledgeEntity]) -> None:
        pass

    @abstractclassmethod
    def update(
        self, old_knowledge: KnowledgeEntity, update: KnowledgeFilterEnitity
    ) -> list[KnowledgeId]:
        pass

    @abstractclassmethod
    def delete(self, knowledge_ids: list[KnowledgeId]) -> None:
        pass
