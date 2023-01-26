"""create skill table

Revision ID: f84c64349c87
Revises: 
Create Date: 2023-01-25 11:23:17.451504

"""
import sqlalchemy as sa

from alembic import op
from sobesity.infrastructure.models.skill import skill_id_seq

# revision identifiers, used by Alembic.
revision = "f84c64349c87"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute(sa.schema.CreateSequence(skill_id_seq))
    op.create_table(
        "skill",
        sa.Column(
            "skill_id",
            sa.Integer,
            skill_id_seq,
            primary_key=True,
            server_default=sa.text(f"nextval('{skill_id_seq.name}'::regclass)"),
        ),
        sa.Column("name", sa.String(50), nullable=False, unique=True),
    )


def downgrade() -> None:
    op.drop_table("skill")
