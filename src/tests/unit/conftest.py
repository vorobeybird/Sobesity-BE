import pytest
from mock import Mock


def mock_with_di(dependency):
    mock_dependency = Mock(dependency())

    with dependency.override(mock_dependency):
        yield mock_dependency


@pytest.fixture
def mock_skill_repository(di):
    yield from mock_with_di(di.repositories.skill)


@pytest.fixture
def mock_user_repository(di):
    yield from mock_with_di(di.repositories.user)


