from sqlalchemy import Column, ForeignKey, Integer, Sequence, Table

from sobesity.infrastructure.datasource import metadata

knowledge_id_seq = Sequence("knowledge_id_seq")
knowledge_table = Table(
    "knowledge",
    metadata,
    Column("knowledge_id", Integer, knowledge_id_seq, primary_key=True),
    Column("user_id", Integer, ForeignKey("user.user_id")),
    Column("level_id", Integer, ForeignKey("level.level_id")),
    Column("skill_id", Integer, ForeignKey("skill.skill_id")),
)
