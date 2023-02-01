"""create user table

Revision ID: 3801542386f4
Revises: f84c64349c87
Create Date: 2023-01-31 17:28:55.985460

"""
import sqlalchemy as sa

from alembic import op
from sobesity.infrastructure.models.user import user_id_seq

# revision identifiers, used by Alembic.
revision = "3801542386f4"
down_revision = "f84c64349c87"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute(sa.schema.CreateSequence(user_id_seq))
    op.create_table(
        "user",
        sa.Column(
            "user_id",
            sa.Integer,
            user_id_seq,
            primary_key=True,
            server_default=sa.text(f"nextval('{user_id_seq.name}'::regclass)"),
        ),
        sa.Column("nickname", sa.String(20), nullable=False, unique=True),
        sa.Column("hashed_password", sa.String(64), nullable=False),
        sa.Column("salt", sa.String(32), nullable=False),
        sa.Column("email", sa.String, nullable=False, unique=True),
        sa.Column("registered_at", sa.DateTime),
    )


def downgrade() -> None:
    op.drop_table("user")
