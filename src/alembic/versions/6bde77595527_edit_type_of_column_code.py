"""edit type of column code

Revision ID: 6bde77595527
Revises: 749a67e4589a
Create Date: 2023-04-12 16:43:31.001579

"""
import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "6bde77595527"
down_revision = "749a67e4589a"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.alter_column("question", "code", type_=sa.Text())


def downgrade() -> None:
    op.alter_column("question", "code", type_=sa.String())
