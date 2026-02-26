from sqlalchemy import select, func

from src.repositories.base import BaseRepository
from src.models.rooms import RoomModel
from src.schemas.rooms import Room


class RoomRepository(BaseRepository):
    model = RoomModel
    schema = Room

    async def get_all(self, hotel_id: int, limit: int, offset: int):
        query = (
            select(self.model)
            .filter_by(hotel_id=hotel_id)
            .limit(limit)
            .offset(offset)
        )
        result = await self.session.execute(query)
        return [self.schema.model_validate(room) for room in result.scalars().all()]
    