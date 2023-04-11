"""create answer table

Revision ID: 23bed438f3a8
Revises: a2e479e35086
Create Date: 2023-02-23 08:23:33.573279

"""
from alembic import op
import sqlalchemy as sa
from sobesity.infrastructure.models.answer import answer_id_seq

# revision identifiers, used by Alembic.
revision = "23bed438f3a8"
down_revision = "a2e479e35086"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute(sa.schema.CreateSequence(answer_id_seq))
    op.create_table(
        "answer",
        sa.Column(
            "answer_id",
            sa.Integer,
            answer_id_seq,
            primary_key=True,
            server_default=sa.text(f"nextval('{answer_id_seq.name}'::regclass)"),
        ),
        sa.Column("answer", sa.String(50), nullable=False, unique=False),
    )


def downgrade() -> None:
    op.drop_table("answer")
