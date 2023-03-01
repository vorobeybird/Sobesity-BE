"""add_column_right_to_answer

Revision ID: 20242755f6c1
Revises: 975f6f1d8fee
Create Date: 2023-03-01 15:30:55.801033

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '20242755f6c1'
down_revision = '975f6f1d8fee'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('answer', sa.Column('right', sa.Boolean()))


def downgrade() -> None:
    op.drop_column('answer', 'right')
