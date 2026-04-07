"""add ondelete to tables

Revision ID: 4d530bda5925
Revises: 508a7e7486c4
Create Date: 2026-03-08 19:51:22.128638

"""

from typing import Sequence, Union

from alembic import op

revision: str = "4d530bda5925"
down_revision: Union[str, Sequence[str], None] = "508a7e7486c4"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_constraint(op.f("bookings_user_id_fkey"), "bookings", type_="foreignkey")
    op.drop_constraint(op.f("bookings_room_id_fkey"), "bookings", type_="foreignkey")
    op.create_foreign_key(
        None, "bookings", "rooms", ["room_id"], ["id"], ondelete="CASCADE"
    )
    op.create_foreign_key(
        None, "bookings", "users", ["user_id"], ["id"], ondelete="CASCADE"
    )
    op.drop_constraint(op.f("rooms_hotel_id_fkey"), "rooms", type_="foreignkey")
    op.create_foreign_key(
        None, "rooms", "hotels", ["hotel_id"], ["id"], ondelete="CASCADE"
    )
    op.drop_constraint(
        op.f("rooms_facilities_room_id_fkey"), "rooms_facilities", type_="foreignkey"
    )
    op.drop_constraint(
        op.f("rooms_facilities_facility_id_fkey"),
        "rooms_facilities",
        type_="foreignkey",
    )
    op.create_foreign_key(
        None, "rooms_facilities", "rooms", ["room_id"], ["id"], ondelete="CASCADE"
    )
    op.create_foreign_key(
        None,
        "rooms_facilities",
        "facilities",
        ["facility_id"],
        ["id"],
        ondelete="CASCADE",
    )


def downgrade() -> None:
    op.drop_constraint(None, "rooms_facilities", type_="foreignkey")
    op.drop_constraint(None, "rooms_facilities", type_="foreignkey")
    op.create_foreign_key(
        op.f("rooms_facilities_facility_id_fkey"),
        "rooms_facilities",
        "facilities",
        ["facility_id"],
        ["id"],
    )
    op.create_foreign_key(
        op.f("rooms_facilities_room_id_fkey"),
        "rooms_facilities",
        "rooms",
        ["room_id"],
        ["id"],
    )
    op.drop_constraint(None, "rooms", type_="foreignkey")
    op.create_foreign_key(
        op.f("rooms_hotel_id_fkey"), "rooms", "hotels", ["hotel_id"], ["id"]
    )
    op.drop_constraint(None, "bookings", type_="foreignkey")
    op.drop_constraint(None, "bookings", type_="foreignkey")
    op.create_foreign_key(
        op.f("bookings_room_id_fkey"), "bookings", "rooms", ["room_id"], ["id"]
    )
    op.create_foreign_key(
        op.f("bookings_user_id_fkey"), "bookings", "users", ["user_id"], ["id"]
    )
