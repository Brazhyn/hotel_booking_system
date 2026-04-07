from sqlalchemy import select, delete, insert

from src.repositories.base import BaseRepository
from src.models.facilities import FacilityModel, RoomFacilityModel
from src.repositories.mappers.mappers import FacilityMapper
from src.repositories.mappers.mappers import RoomFacilityMapper


class FacilityRepository(BaseRepository):
    model = FacilityModel
    mapper = FacilityMapper


class RoomFacilityRepository(BaseRepository):
    model = RoomFacilityModel
    mapper = RoomFacilityMapper

    async def set_room_facilities(self, room_id: int, facilities_ids: list[int]):
        query = select(self.model.facility_id).filter_by(room_id=room_id)
        result = await self.session.execute(query)

        f_ids_existing = result.scalars().all()
        f_ids_incoming = [f_id for f_id in facilities_ids]

        ids_to_delete = list(set(f_ids_existing) - set(f_ids_incoming))
        ids_to_add = list(set(f_ids_incoming) - set(f_ids_existing))

        if ids_to_delete:
            delete_stmt = delete(self.model).filter(
                self.model.room_id == room_id, self.model.facility_id.in_(ids_to_delete)
            )
            await self.session.execute(delete_stmt)

        if ids_to_add:
            add_stmt = insert(self.model).values(
                [{"room_id": room_id, "facility_id": f_id} for f_id in ids_to_add]
            )
            await self.session.execute(add_stmt)
