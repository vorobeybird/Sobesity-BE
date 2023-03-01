"""create question table

Revision ID: a2e479e35086
Revises: f84c64349c87
Create Date: 2023-02-17 11:22:39.831987

"""
from alembic import op
import sqlalchemy as sa
from sobesity.infrastructure.models.question import question_id_seq


# revision identifiers, used by Alembic.
revision = 'a2e479e35086'
down_revision = 'd4122e36b6dc'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute(sa.schema.CreateSequence(question_id_seq))
    op.create_table(
        "question",
        sa.Column(
            "question_id",
            sa.Integer,
            question_id_seq,
            primary_key=True,
            server_default=sa.text(f"nextval('{question_id_seq.name}'::regclass)"),
        ),
        sa.Column("question", sa.String(50), nullable=False, unique=True),
    )


def downgrade() -> None:
    op.drop_table("question")
