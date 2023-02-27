from sqlalchemy import Column, Integer, Sequence, String, Table

from sobesity.infrastructure.datasource import metadata

question_id_seq = Sequence("question_id_seq")
question_table = Table(
    "question",
    metadata,
    Column("question_id", Integer, question_id_seq, primary_key=True),
    Column("question", String),
    Column("skill_id", Integer)
)
