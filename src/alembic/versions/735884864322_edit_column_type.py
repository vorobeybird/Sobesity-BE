"""Edit column type to forigin key on question table

Revision ID: 735884864322
Revises: 7d44a4a3adcd
Create Date: 2023-04-13 08:48:44.912306

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "735884864322"
down_revision = "7d44a4a3adcd"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.alter_column(
        "question",
        "type",
        type_=sa.Integer(),
        new_column_name="type_id",
        postgresql_using="type::integer",
    )


def downgrade() -> None:
    op.alter_column(
        "question",
        "type_id",
        type_=sa.String(),
        new_column_name="type",
        postgresql_using="type::character varying",
    )
