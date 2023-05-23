"""create table users define

Revision ID: 3cda5e1eaa3c
Revises: d3cdadbec5ab
Create Date: 2023-05-23 11:26:40.963694

"""
from alembic import op
import sqlalchemy as sa
from sobesity.infrastructure.models.knowledge import knowledge_id_seq

# revision identifiers, used by Alembic.
revision = "3cda5e1eaa3c"
down_revision = "d3cdadbec5ab"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute(sa.schema.CreateSequence(knowledge_id_seq))
    op.create_table(
        "knowledge",
        sa.Column(
            "knowledge_id",
            sa.Integer,
            knowledge_id_seq,
            primary_key=True,
            server_default=sa.text(f"nextval('{knowledge_id_seq.name}'::regclass)"),
        ),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("user.user_id")),
        sa.Column("level_id", sa.Integer(), sa.ForeignKey("level.level_id")),
        sa.Column("skill_id", sa.Integer(), sa.ForeignKey("skill.skill_id")),
    )


def downgrade() -> None:
    op.drop_table("users_knowledge")
