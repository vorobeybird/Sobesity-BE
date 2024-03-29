class AnswerNameUniqueViolation(Exception):
    def __init__(self) -> None:
        self.message = "Answer must be unique"
        super().__init__(self.message)


class AnswerNotExistViolation(Exception):
    def __init__(self) -> None:
        self.message = "Answer not exist"
        super().__init__(self.message)
