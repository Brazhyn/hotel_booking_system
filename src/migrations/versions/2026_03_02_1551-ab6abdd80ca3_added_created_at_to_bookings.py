"""added created_at to bookings

Revision ID: ab6abdd80ca3
Revises: 53d348b646ed
Create Date: 2026-03-02 15:51:41.220128

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "ab6abdd80ca3"
down_revision: Union[str, Sequence[str], None] = "53d348b646ed"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "bookings",
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
    )


def downgrade() -> None:
    op.drop_column("bookings", "created_at")
