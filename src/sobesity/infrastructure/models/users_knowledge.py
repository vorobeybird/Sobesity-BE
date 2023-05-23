from sqlalchemy import Column, ForeignKey, Integer, Sequence, String, Table

from sobesity.infrastructure.datasource import metadata

user_knowledge_id_seq = Sequence("user_knowledge_id_seq")
users_knowledge_table = Table(
    "users_knowledge",
    metadata,
    Column("user_knowledge_id", Integer, user_knowledge_id_seq, primary_key=True),
    Column("user_id", Integer, ForeignKey("user.user_id")),
    Column("level_id", Integer, ForeignKey("level.level_id")),
)
