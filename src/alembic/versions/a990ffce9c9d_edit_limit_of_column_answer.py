"""edit limit of column answer

Revision ID: a990ffce9c9d
Revises: 6bde77595527
Create Date: 2023-04-12 18:23:41.157992

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a990ffce9c9d'
down_revision = '6bde77595527'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.alter_column('answer', 'answer', type_=sa.String())


def downgrade() -> None:
    op.alter_column('answer', 'answer', type_=sa.String(50))
