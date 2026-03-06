from datetime import date

from sqlalchemy import select, func

from src.models.rooms import RoomModel
from src.repositories.base import BaseRepository
from src.models.bookings import BookingModel
from src.schemas.rooms import Room
from src.database import engine
from src.repositories.utils import get_rooms_ids_for_booking


class RoomRepository(BaseRepository):
    model = RoomModel
    schema = Room
    
    async def get_filtered_by_time(
        self,
        hotel_id,
        date_from,
        date_to,
    ):  
        rooms_ids_to_get = get_rooms_ids_for_booking(
            date_from,
            date_to,
            hotel_id,
        )
        
        return await self.get_filtered(RoomModel.id.in_(rooms_ids_to_get))
        
    
        
        
        