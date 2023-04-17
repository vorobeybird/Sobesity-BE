"""create table types. Edit column type to forigin key on question table

Revision ID: 7d44a4a3adcd
Revises: a990ffce9c9d
Create Date: 2023-04-13 08:25:54.041072

"""
from alembic import op
import sqlalchemy as sa
from sobesity.infrastructure.models.type import type_id_seq


# revision identifiers, used by Alembic.
revision = "7d44a4a3adcd"
down_revision = "a990ffce9c9d"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute(sa.schema.CreateSequence(type_id_seq))
    op.create_table(
        "type",
        sa.Column(
            "type_id",
            sa.Integer,
            type_id_seq,
            primary_key=True,
            server_default=sa.text(f"nextval('{type_id_seq.name}'::regclass)"),
        ),
        sa.Column("name", sa.String(), nullable=False, unique=True),
    )


def downgrade() -> None:
    op.drop_table("type")
