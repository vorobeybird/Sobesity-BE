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


@pytest.fixture
def valid_user_create_body():
    return {
        "password": "FooBoo132",
        "nickname": "FooBoo",
        "email": "fooboo@google.com",
        "firstName": "Foo",
        "lastName": "Boo",
    }
