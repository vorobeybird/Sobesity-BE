import pytest

from sobesity.domain.entities.level import LevelEntity, LevelFilterEnitity
from sobesity.domain.exceptions import LevelNameUniqueViolation


def test_get_list__empty_db__return_nothing(level_repository):
    assert level_repository.get_list() == []


def test_batch_create__get_all_rows(level_repository, levels):
    level_repository.batch_create(levels)
    created_levels = level_repository.get_list()
    created_levels_map = {level.name: level for level in created_levels}

    assert len(created_levels) == len(levels)
    for level in levels:
        assert level.name in created_levels_map


def test_batch_create__only_unique__raise_error(level_repository, levels):
    levels[0] = levels[1]
    with pytest.raises(LevelNameUniqueViolation):
        level_repository.batch_create(levels)


def test_update__particular_rows_udated(level_repository, levels):
    level_repository.batch_create(levels[:1])
    level_before = level_repository.get_list()[0]

    to_set = levels[1]
    where = LevelFilterEnitity(level_ids=[level_before.level_id])
    updated_ids = level_repository.update(to_set, where)

    level_after = level_repository.get_list()[0]

    assert level_before.level_id == level_after.level_id == updated_ids[0]
    assert level_after.name == to_set.name


def test_delete__particular_rows_deleted(level_repository, levels):
    level_repository.batch_create(levels)
    created_levels_before = level_repository.get_list()
    to_delete = [level.level_id for level in created_levels_before[:2]]

    level_repository.delete(to_delete)

    created_levels_after = level_repository.get_list()

    assert (len(created_levels_before) - len(created_levels_after)) == len(to_delete)

    for level in created_levels_after:
        assert level.level_id not in to_delete
