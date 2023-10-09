from sqlalchemy import Column, Integer, Sequence, String, Table

from sobesity.infrastructure.datasource import metadata

type_id_seq = Sequence("type_id_seq")
question_type_table = Table(
    "type",
    metadata,
    Column("type_id", Integer, type_id_seq, primary_key=True),
    Column("name", String),
)
