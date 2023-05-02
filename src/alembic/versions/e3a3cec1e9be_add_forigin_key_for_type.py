"""Add forigin key for type

Revision ID: e3a3cec1e9be
Revises: 735884864322
Create Date: 2023-04-13 09:56:10.600039

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "e3a3cec1e9be"
down_revision = "735884864322"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_foreign_key(
        "fk_question_type", "question", "type", ["type_id"], ["type_id"]
    )


def downgrade() -> None:
    op.drop_constraint("fk_question_type", "question", type_="foreignkey")
