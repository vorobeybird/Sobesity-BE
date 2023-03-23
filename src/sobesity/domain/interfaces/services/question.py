from abc import ABC, abstractclassmethod
from typing import Optional

from sobesity.domain.entities import QuestionEntity, QuestionFilterEnitity, QuestionId


class IQuestionService(ABC):
    @abstractclassmethod
    def get_list(
        self, question_filter: Optional[QuestionFilterEnitity] = None
    ) -> list[QuestionEntity]:
        pass

    @abstractclassmethod
    def batch_create(self, questions: list[QuestionEntity]) -> None:
        pass

    @abstractclassmethod
    def update(
        self, old_question: QuestionEntity, update: QuestionFilterEnitity
    ) -> list[QuestionId]:
        pass

    @abstractclassmethod
    def delete(self, question_ids: list[QuestionId]) -> None:
        pass
