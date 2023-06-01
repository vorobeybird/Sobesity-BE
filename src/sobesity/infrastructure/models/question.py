from sqlalchemy import Column, ForeignKey, Integer, Sequence, String, Table

from sobesity.infrastructure.datasource import metadata

question_id_seq = Sequence("question_id_seq")
question_table = Table(
    "question",
    metadata,
    Column("question_id", Integer, question_id_seq, primary_key=True),
    Column("question", String),
    Column("type_id", Integer, ForeignKey("type.type_id")),
    Column("code", String),
    Column("skill_id", Integer, ForeignKey("skill.skill_id")),
    Column("level_id", Integer, ForeignKey("level.level_id")),
)
