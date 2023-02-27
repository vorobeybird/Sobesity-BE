from typing import Optional

from sobesity.domain.entities import AnswerEntity, AnswerFilterEnitity, AnswerId
from sobesity.domain.interfaces.repositories import IAnswerRepository
from sobesity.domain.interfaces.services import IAnswerService


class AnswerService(IAnswerService):
    def __init__(self, answer_repository: IAnswerRepository) -> None:
        self._answer_repository = answer_repository

    def get_list(
        self, answer_filter: Optional[AnswerFilterEnitity] = None
    ) -> list[AnswerEntity]:
        return self._answer_repository.get_list(answer_filter)

    def batch_create(self, answers: list[AnswerEntity]) -> None:
        return self._answer_repository.batch_create(answers)

    def update(
        self, old_answer: AnswerEntity, update: AnswerFilterEnitity
    ) -> list[AnswerId]:
        return self._answer_repository.update(old_answer, update)

    def delete(self, answers_ids: list[AnswerId]) -> None:
        return self._answer_repository.delete(answers_ids)
