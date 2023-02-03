from sqlalchemy import Column, Integer, Sequence, String, Table

from sobesity.infrastructure.datasource import metadata

skill_id_seq = Sequence("skill_id_seq")
skill_table = Table(
    "skill",
    metadata,
    Column("skill_id", Integer, skill_id_seq, primary_key=True),
    Column("name", String, unique=True, nullable=False),
)
