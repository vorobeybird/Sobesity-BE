import pytest

from sobesity.domain.entities.skill import SkillFilterEnitity
from sobesity.domain.exceptions import SkillNameUniqueViolation


def test_get_list__empty_db__return_nothing(skill_repository):
    assert skill_repository.get_list() == []


def test_batch_create__get_all_rows(skill_repository, skills):
    skill_repository.batch_create(skills)
    created_skills = skill_repository.get_list()
    created_skills_map = {skill.name: skill for skill in created_skills}

    assert len(created_skills) == len(skills)
    for skill in skills:
        assert skill.name in created_skills_map


def test_batch_create__only_unique__raise_error(skill_repository, skills):
    skills[0] = skills[1]
    with pytest.raises(SkillNameUniqueViolation):
        skill_repository.batch_create(skills)


def test_update__particular_rows_udated(skill_repository, skills):
    skill_repository.batch_create(skills[:1])
    skill_before = skill_repository.get_list()[0]

    to_set = skills[1]
    where = SkillFilterEnitity(skill_ids=[skill_before.skill_id])
    updated_ids = skill_repository.update(to_set, where)

    skill_after = skill_repository.get_list()[0]

    assert skill_before.skill_id == skill_after.skill_id == updated_ids[0]
    assert skill_after.name == to_set.name


def test_delete__particular_rows_deleted(skill_repository, skills):
    skill_repository.batch_create(skills)
    created_skills_before = skill_repository.get_list()
    to_delete = [skill.skill_id for skill in created_skills_before[:2]]

    skill_repository.delete(to_delete)

    created_skills_after = skill_repository.get_list()

    assert (len(created_skills_before) - len(created_skills_after)) == len(to_delete)

    for skill in created_skills_after:
        assert skill.skill_id not in to_delete
