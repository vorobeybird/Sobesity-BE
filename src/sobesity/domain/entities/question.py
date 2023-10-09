from dataclasses import dataclass, field
from typing import NewType, Optional, Union

from sobesity.domain.entities.answer import AnswerEntity
from sobesity.domain.entities.base import BaseEntity, Unset, unset
from sobesity.domain.entities.level import LevelEntity
from sobesity.domain.entities.question_type import QuestionTypeEntity
from sobesity.domain.entities.skill import SkillEntity

QuestionId = NewType("QuestionId", int)


@dataclass
class QuestionEntity(BaseEntity):
    question_id: QuestionId
    question: str
    question_type: QuestionTypeEntity
    code: str
    skill: SkillEntity
    level: LevelEntity
    answers: list[AnswerEntity] = field(default_factory=list)


@dataclass
class UpdateQuestionEntity:
    question_id: QuestionId
    question: Union[str, None, Unset] = unset
    code: Union[str, None, Unset] = unset

@dataclass
class QuestionFilterEnitity:
    question_ids: Optional[list[QuestionId]] = None
    questions: Optional[list[str]] = None
    skill_ids: Optional[list[int]] = None
    type_ids: Optional[list[int]] = None
    codes: Optional[list[str]] = None
    level_ids: Optional[list[int]] = None
