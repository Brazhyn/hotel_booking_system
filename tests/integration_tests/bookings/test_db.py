from datetime import date

from src.schemas.bookings import BookingAdd
from src.utils.db_manager import DBManager


async def test_booking_crud(db: DBManager):
    user_id = (await db.users.get_all())[0].id
    room_id = (await db.rooms.get_all())[0].id

    # Create booking
    booking_add_data = BookingAdd(
        user_id=user_id,
        room_id=room_id,
        date_from=date(year=2026, month=7, day=1),
        date_to=date(year=2026, month=7, day=10),
        price=1000
    )
    new_booking = await db.bookings.add(booking_add_data)
    
    # Read booking
    booking = await db.bookings.get_one_or_none(id=new_booking.id)
    assert booking
    assert booking.id == new_booking.id
    assert booking.room_id == new_booking.room_id
    
    # Edit booking
    booking_update_data = BookingAdd(
        user_id=user_id,
        room_id=room_id,
        date_from=date(year=2026, month=7, day=5),
        date_to=date(year=2026, month=7, day=15),
        price=1000
    )
    await db.bookings.edit(
        data=booking_update_data,
        id=booking.id
    )
    updated_booking = await db.bookings.get_one_or_none(id=new_booking.id)
    assert updated_booking
    assert updated_booking.id == new_booking.id
    assert updated_booking.date_to == booking_update_data.date_to
    
    # Delete booking
    await db.bookings.delete(id=booking.id)
    booking = await db.bookings.get_one_or_none(id=new_booking.id)
    assert not booking



