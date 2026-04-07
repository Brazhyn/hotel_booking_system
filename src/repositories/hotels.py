from sqlalchemy import func, select

from src.models.rooms import RoomModel
from src.repositories.base import BaseRepository
from src.schemas.hotels import Hotel
from src.models.hotels import HotelModel
from src.repositories.utils import get_rooms_ids_for_booking
from src.repositories.mappers.mappers import HotelMapper


class HotelRepository(BaseRepository):
    model = HotelModel
    mapper = HotelMapper

    async def get_filtered_by_time(
        self,
        title,
        location,
        limit,
        offset,
        date_from,
        date_to,
    ) -> list[Hotel]:
        rooms_ids_to_get = get_rooms_ids_for_booking(date_from=date_from, date_to=date_to)
        hotels_ids_to_get = (
            select(RoomModel.hotel_id)
            .select_from(RoomModel)
            .filter(RoomModel.id.in_(rooms_ids_to_get))
        )
        query = select(HotelModel).filter(HotelModel.id.in_(hotels_ids_to_get))

        if title:
            query = query.filter(func.lower(self.model.title).contains(title.lower()))
        if location:
            query = query.filter(func.lower(self.model.location).contains(location.lower()))

        query = query.limit(limit).offset(offset)

        result = await self.session.execute(query)
        return [self.mapper.map_to_domain_entity(model) for model in result.scalars().all()]
