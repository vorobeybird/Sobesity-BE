"""add names to user

Revision ID: d4122e36b6dc
Revises: 3801542386f4
Create Date: 2023-02-15 18:48:53.777894

"""
import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "d4122e36b6dc"
down_revision = "3801542386f4"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("user", sa.Column("first_name", sa.String()))
    op.add_column("user", sa.Column("last_name", sa.String()))


def downgrade() -> None:
    op.drop_column("user", "first_name")
    op.drop_column("user", "last_name")
