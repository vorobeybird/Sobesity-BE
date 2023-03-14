from abc import ABC, abstractclassmethod
from typing import Optional

from sobesity.domain.entities import AnswerEntity, AnswerFilterEnitity, AnswerId


class IAnswerRepository(ABC):
    @abstractclassmethod
    def get_list(
        self, answer_filter: Optional[AnswerFilterEnitity] = None
    ) -> list[AnswerEntity]:
        pass

    @abstractclassmethod
    def batch_create(self, answers: list[AnswerEntity]) -> None:
        pass

    @abstractclassmethod
    def update(
        self, old_answer: AnswerEntity, update: AnswerFilterEnitity
    ) -> list[AnswerId]:
        pass

    @abstractclassmethod
    def delete(self, answers_ids: list[AnswerId]) -> None:
        pass
