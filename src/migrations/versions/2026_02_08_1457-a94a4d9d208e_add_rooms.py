"""added_rooms

Revision ID: a94a4d9d208e
Revises: 000f2dcf3d03
Create Date: 2026-02-08 14:57:40.871663

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "a94a4d9d208e"
down_revision: Union[str, Sequence[str], None] = "000f2dcf3d03"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "rooms",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("hotel_id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("description", sa.String(), nullable=True),
        sa.Column("price", sa.Integer(), nullable=False),
        sa.Column("quantity", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["hotel_id"],
            ["hotels.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("rooms")
