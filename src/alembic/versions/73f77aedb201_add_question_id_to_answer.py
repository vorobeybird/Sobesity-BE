"""add_question_id_to_answer

Revision ID: 73f77aedb201
Revises: 20242755f6c1
Create Date: 2023-03-02 08:24:25.261460

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '73f77aedb201'
down_revision = '20242755f6c1'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('answer', sa.Column('question_id', sa.Integer(), sa.ForeignKey('question.question_id')))


def downgrade() -> None:
    op.drop_column('answer', 'question_id')
