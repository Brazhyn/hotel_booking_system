"""make email unique

Revision ID: c0b269629261
Revises: 5b4a2deff8bf
Create Date: 2026-02-16 12:41:23.350118

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "c0b269629261"
down_revision: Union[str, Sequence[str], None] = "5b4a2deff8bf"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_unique_constraint(None, "users", ["email"])


def downgrade() -> None:
    op.drop_constraint(None, "users", type_="unique")
