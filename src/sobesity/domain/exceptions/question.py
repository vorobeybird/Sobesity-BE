class QuestionNameUniqueViolation(Exception):
    def __init__(self) -> None:
        self.message = "Question must be unique"
        super().__init__(self.message)


class QuestionSkillIdExistViolation(Exception):
    def __int__(self) -> None:
        self.message = "Skill_id not exist"
        super().__init__(self.message)


class QuestionExistViolation(Exception):
    def __int__(self) -> None:
        self.message = "Question not exist"
        super().__init__(self.message)
