from sqlalchemy import Column, Integer, Sequence, String, Table

from sobesity.infrastructure.datasource import metadata

level_id_seq = Sequence("level_id_seq")
level_table = Table(
    "level",
    metadata,
    Column("level_id", Integer, level_id_seq, primary_key=True),
    Column("name", String, unique=True, nullable=False),
)
