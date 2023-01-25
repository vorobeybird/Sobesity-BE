from sobesity.domain.entities.skill import SkillEntity


def test_get_list__empty_db__return_nothing(skill_repository):
    assert skill_repository.get_list() == []

def test_get_list__created_few_rows__return_rows(skill_repository):
    assert skill_repository.get_list() == []

def test_create__get_row(skill_repository):
    entity = SkillEntity(skill_id=None, name='Python')
    skill_repository.create(entity)
    skills = skill_repository.get_list()
    assert skills[0].name == entity.name
