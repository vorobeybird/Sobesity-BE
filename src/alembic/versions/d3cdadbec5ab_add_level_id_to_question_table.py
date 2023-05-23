"""add level_id to question_table

Revision ID: d3cdadbec5ab
Revises: 67e9b7ec96be
Create Date: 2023-05-23 10:43:40.823987

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd3cdadbec5ab'
down_revision = '67e9b7ec96be'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "question",
        sa.Column("level_id", sa.Integer(), sa.ForeignKey("level.level_id")),
    )


def downgrade() -> None:
    op.drop_column("question", "level_id")
