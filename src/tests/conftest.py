from contextlib import contextmanager

import pytest

from sobesity.webapp import create_app


@pytest.fixture
def di(app):
    return app.container


@pytest.fixture(autouse=True)
def db(di):
    with di.resources.datasource()() as connection:

        @contextmanager
        def rollback_conn():
            yield connection

        yield di.resources.datasource.override(rollback_conn)

        connection.rollback()


@pytest.fixture
def app():
    app = create_app()
    yield app


@pytest.fixture
def client(app):
    return app.test_client()
