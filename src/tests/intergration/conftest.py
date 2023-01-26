import pytest


@pytest.fixture
def skill_repository(di):
    return di.repositories.skill_repository()
