from contextlib import contextmanager

from sqlalchemy import MetaData, create_engine

from sobesity.config import Settings

metadata = MetaData()

engine = create_engine(Settings().db.url)


@contextmanager
def get_connection():
    with engine.begin() as conn:
        yield conn
