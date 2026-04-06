from datetime import date

from sqlalchemy import select, insert
from pydantic import BaseModel

from src.repositories.base import BaseRepository
from src.models.bookings import BookingModel
from src.repositories.mappers.mappers import BookingMapper
from src.repositories.utils import get_rooms_ids_for_booking
from src.schemas.bookings import BookingAdd


class BookingRepository(BaseRepository):
    model = BookingModel
    mapper = BookingMapper
    
    async def get_bookings_with_today_checkin(self):
        query = (
            select(BookingModel)
            .filter(BookingModel.date_from == date.today())
        )
        
        res = await self.session.execute(query)
        return [self.mapper.map_to_domain_entity(booking) for booking in res.scalars().all()]    
    
    
    async def add_booking(self, data: BookingAdd, hotel_id: int):
        query_room_ids = get_rooms_ids_for_booking(
            date_from=data.date_from,
            date_to=data.date_to,
            hotel_id=hotel_id,
        )
        res = await self.session.execute(query_room_ids)
        room_ids = res.scalars().all()
        
        if data.room_id not in room_ids:
            raise Exception("No rooms available for the given dates")
        
        new_booking = await self.add(data)
        return self.mapper.map_to_domain_entity(new_booking)