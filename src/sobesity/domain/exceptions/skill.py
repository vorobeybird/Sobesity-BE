class SkillNameUniqueViolation(Exception):
    def __init__(self) -> None:
        self.message = "Skill names must be unique"
        super().__init__(self.message)
