from sqlalchemy import Column, Integer, Sequence, String, Table

from sobesity.infrastructure.datasource import metadata

answer_id_seq = Sequence("answer_id_seq")
answer_table = Table(
    "answer",
    metadata,
    Column("answer_id", Integer, answer_id_seq, primary_key=True),
    Column("answer", String),
)
