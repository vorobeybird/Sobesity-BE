"""create level table

Revision ID: 67e9b7ec96be
Revises: e3a3cec1e9be
Create Date: 2023-05-23 09:20:07.761946

"""
from alembic import op
import sqlalchemy as sa
from sobesity.infrastructure.models.level import level_id_seq

# revision identifiers, used by Alembic.
revision = '67e9b7ec96be'
down_revision = 'e3a3cec1e9be'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute(sa.schema.CreateSequence(level_id_seq))
    op.create_table(
        "level",
        sa.Column(
            "level_id",
            sa.Integer,
            level_id_seq,
            primary_key=True,
            server_default=sa.text(f"nextval('{level_id_seq.name}'::regclass)"),
        ),
        sa.Column("name", sa.String(50), nullable=False, unique=True),
    )


def downgrade() -> None:
    op.drop_table("level")
