from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import selectinload

from src.exceptions import RoomNotFoundException
from src.repositories.mappers.mappers import RoomMapper, RoomWithRelsMapper
from src.repositories.base import BaseRepository
from src.repositories.utils import get_rooms_ids_for_booking
from src.models.rooms import RoomModel


class RoomRepository(BaseRepository):
    model = RoomModel
    mapper = RoomMapper

    async def get_filtered_by_time(
        self,
        hotel_id,
        date_from,
        date_to,
    ):
        rooms_ids_to_get = get_rooms_ids_for_booking(date_from, date_to, hotel_id)
        query = (
            select(self.model)
            .options(selectinload(self.model.facilities))
            .filter(self.model.id.in_(rooms_ids_to_get))
        )
        result = await self.session.execute(query)
        return [RoomWithRelsMapper.map_to_domain_entity(model) for model in result.scalars().all()]

    async def get_one_with_rels(self, **filter_by):
        query = (
            select(self.model).options(selectinload(self.model.facilities)).filter_by(**filter_by)
        )
        result = await self.session.execute(query)
        try:
            room = result.scalar_one()
        except NoResultFound:
            raise RoomNotFoundException
        return RoomWithRelsMapper.map_to_domain_entity(room)
