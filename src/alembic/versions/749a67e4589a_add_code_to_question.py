"""add code to question

Revision ID: 749a67e4589a
Revises: 9b1b908d7f3b
Create Date: 2023-04-03 10:55:25.506159

"""
import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "749a67e4589a"
down_revision = "9b1b908d7f3b"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("question", sa.Column("code", sa.String()))


def downgrade() -> None:
    op.drop_column("question", "code")
