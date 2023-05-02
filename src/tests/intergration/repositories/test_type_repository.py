import pytest

from sobesity.domain.entities.type import TypeEntity, TypeFilterEnitity
from sobesity.domain.exceptions import TypeNameUniqueViolation


def test_get_list__empty_db__return_nothing(type_repository):
    assert type_repository.get_list() == []


def test_batch_create__get_all_rows(type_repository, types):
    type_repository.batch_create(types)
    created_types = type_repository.get_list()
    created_types_map = {type.name: type for type in created_types}

    assert len(created_types) == len(types)
    for type in types:
        assert type.name in created_types_map


def test_batch_create__only_unique__raise_error(type_repository, types):
    types[0] = types[1]
    with pytest.raises(TypeNameUniqueViolation):
        type_repository.batch_create(types)


def test_update__particular_rows_udated(type_repository, types):
    type_repository.batch_create(types[:1])
    type_before = type_repository.get_list()[0]

    to_set = types[1]
    where = TypeFilterEnitity(type_ids=[type_before.type_id])
    updated_ids = type_repository.update(to_set, where)

    type_after = type_repository.get_list()[0]

    assert type_before.type_id == type_after.type_id == updated_ids[0]
    assert type_after.name == to_set.name


def test_delete__particular_rows_deleted(type_repository, types):
    type_repository.batch_create(types)
    created_types_before = type_repository.get_list()
    to_delete = [type.type_id for type in created_types_before[:2]]

    type_repository.delete(to_delete)

    created_types_after = type_repository.get_list()

    assert (len(created_types_before) - len(created_types_after)) == len(to_delete)

    for type in created_types_after:
        assert type.type_id not in to_delete
