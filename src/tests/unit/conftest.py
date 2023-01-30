import pytest
from mock import Mock


@pytest.fixture
def mock_skill_repository(di):
    skill_repository = di.repositories.skill
    mock_skill_repository = Mock(skill_repository())

    with skill_repository.override(mock_skill_repository):
        yield mock_skill_repository
