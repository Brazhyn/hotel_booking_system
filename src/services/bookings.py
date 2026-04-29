from src.exceptions import (
    ObjectNotFoundException,
    RoomNotFoundException,
    BookingNotFoundException,
)
from src.schemas.rooms import Room
from src.services.base import BaseService
from src.schemas.bookings import BookingAdd, BookingAddRequest


class BookingService(BaseService):
    async def get_all_bookings(self):
        return await self.db.bookings.get_all()

    async def get_user_bookings(self, user_id: int):
        return await self.db.bookings.get_filtered(user_id=user_id)

    async def add_booking(self, user_id: int, data: BookingAddRequest):
        try:
            room: Room = await self.db.rooms.get_one(id=data.room_id)
        except ObjectNotFoundException:
            raise RoomNotFoundException

        booking = await self.db.bookings.add_booking(
            BookingAdd(user_id=user_id, price=room.price, **data.model_dump()),
            hotel_id=room.hotel_id,
        )
        await self.db.commit()
        return booking

    async def delete_booking(self, booking_id: int):
        await self.get_booking_with_check(booking_id)
        
        await self.db.bookings.delete(id=booking_id)
        await self.db.commit()
        
    async def get_booking_with_check(self, booking_id: int):
        try:
            await self.db.bookings.get_one(id=booking_id)
        except ObjectNotFoundException:
            raise BookingNotFoundException
