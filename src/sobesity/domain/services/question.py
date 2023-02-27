from typing import Optional

from sobesity.domain.entities import QuestionEntity, QuestionFilterEnitity, QuestionId
from sobesity.domain.interfaces.repositories import IQuestionRepository
from sobesity.domain.interfaces.services import IQuestionService


class QuestionService(IQuestionService):
    def __init__(self, question_repository: IQuestionRepository) -> None:
        self._question_repository = question_repository

    def get_list(
        self, question_filter: Optional[QuestionFilterEnitity] = None
    ) -> list[QuestionEntity]:
        return self._question_repository.get_list(question_filter)

    def batch_create(self, questions: list[QuestionEntity]) -> None:
        return self._question_repository.batch_create(questions)

    def update(
        self, old_question: QuestionEntity, update: QuestionFilterEnitity
    ) -> list[QuestionId]:
        return self._question_repository.update(old_question, update)

    def delete(self, questions_ids: list[QuestionId]) -> None:
        return self._question_repository.delete(questions_ids)
