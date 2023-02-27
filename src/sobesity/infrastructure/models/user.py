from sqlalchemy import Column, DateTime, Integer, Sequence, String, Table

from sobesity.infrastructure.datasource import metadata

user_id_seq = Sequence("user_id_seq")
user_table = Table(
    "user",
    metadata,
    Column("user_id", Integer, user_id_seq, primary_key=True),
    Column("nickname", String(20)),
    Column("hashed_password", String(64)),
    Column("salt", String(32)),
    Column("email", String),
    Column("registered_at", DateTime),
    Column("first_name", String(32)),
    Column("last_name", String(32)),
)
