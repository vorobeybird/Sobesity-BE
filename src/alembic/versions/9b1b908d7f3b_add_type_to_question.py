"""add type to question

Revision ID: 9b1b908d7f3b
Revises: 73f77aedb201
Create Date: 2023-04-03 10:33:37.570673

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "9b1b908d7f3b"
down_revision = "73f77aedb201"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("question", sa.Column("type", sa.String()))


def downgrade() -> None:
    op.drop_column("question", "type")
