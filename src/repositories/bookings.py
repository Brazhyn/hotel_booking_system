from datetime import date

from sqlalchemy import select

from src.repositories.base import BaseRepository
from src.models.bookings import BookingModel
from src.repositories.mappers.mappers import BookingMapper


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