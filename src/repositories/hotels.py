from sqlalchemy import func, select

from src.repositories.base import BaseRepository
from src.schemas.hotels import Hotel
from src.models.hotels import HotelModel



class HotelRepository(BaseRepository):
    model = HotelModel
    schema = Hotel
    
    async def get_all(
        self,
        title,
        location,
        limit,
        offset,
    ) -> list[Hotel]:
        query = select(self.model)
        if title:
            query = query.where(func.lower(self.model.title).contains(title.lower()))
        if location:
            query = query.where(func.lower(self.model.location).contains(location.lower()))
        query = (
            query
            .limit(limit)
            .offset(offset)
        )
        result = await self.session.execute(query)
        return [self.schema.model_validate(hotel, from_attributes=True) for hotel in result.scalars().all()]
