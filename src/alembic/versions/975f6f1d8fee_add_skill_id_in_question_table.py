"""add skill_id in question table

Revision ID: 975f6f1d8fee
Revises: 23bed438f3a8
Create Date: 2023-02-27 07:51:43.667405

"""

import sqlalchemy as sa
from alembic import op



# revision identifiers, used by Alembic.
revision = '975f6f1d8fee'
down_revision = '23bed438f3a8'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('question',
                  sa.Column('skill_id', sa.integer(), sa.ForeignKey('skill.skill_id'))
                  )


def downgrade() -> None:
    op.drop_column('question', 'skill_id')
