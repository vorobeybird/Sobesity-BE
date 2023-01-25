from contextlib import contextmanager
import pytest

from sobesity.containers import Application

@pytest.fixture
def di():
    return Application()

@pytest.fixture(autouse=True)
def db(di):
    with di.resources.datasource()() as connection:
        @contextmanager
        def rollback_conn():
            yield connection

        yield di.resources.datasource.override(rollback_conn)

        connection.rollback()



