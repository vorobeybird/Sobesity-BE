from enum import Enum


class ModelFields(str, Enum):
    SKILL_ID = "skill_id"
    QUESTION_ID = "question_id"
    TYPE_ID = "type_id"
    ANSWER_ID = "answer_id"
    USER_ID = "user_id"
    REGISTERED_AT = "registered_at"
    PASSWORD = "password"
