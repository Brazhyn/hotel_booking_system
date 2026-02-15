"""add_users

Revision ID: 5b4a2deff8bf
Revises: a94a4d9d208e
Create Date: 2026-02-15 14:09:51.055522

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "5b4a2deff8bf"
down_revision: Union[str, Sequence[str], None] = "a94a4d9d208e"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("email", sa.String(length=200), nullable=False),
        sa.Column("first_name", sa.String(length=150), nullable=True),
        sa.Column("last_name", sa.String(length=150), nullable=True),
        sa.Column("hashed_password", sa.String(length=200), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("users")
