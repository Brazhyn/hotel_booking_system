from datetime import date

from src.exceptions import ObjectNotFoundException, RoomNotFoundException, FacilityNotFoundException
from src.services.base import BaseService
from src.schemas.rooms import Room, RoomAddRequest, RoomAdd, RoomPatch, RoomPatchRequest
from src.schemas.facilities import RoomFacilityAdd
from src.services.hotels import HotelService


class RoomService(BaseService):
    async def get_filtered_by_time(
        self,
        hotel_id: int,
        date_from: date,
        date_to: date,
    ):
        await HotelService(self.db).get_hotel_with_check(hotel_id)
        
        return await self.db.rooms.get_filtered_by_time(
            hotel_id=hotel_id, date_from=date_from, date_to=date_to
        )

    async def get_room(self, hotel_id: int, room_id: int):        
        return await self.db.rooms.get_one_with_rels(id=room_id, hotel_id=hotel_id)

    async def create_room(self, hotel_id: int, data: RoomAddRequest):
        await HotelService(self.db).get_hotel_with_check(hotel_id)

        room_data_dict = data.model_dump()
        await self.check_existing_facilities(room_data_dict["facilities_ids"])
            
        room_data = RoomAdd(hotel_id=hotel_id, **room_data_dict)
        room = await self.db.rooms.add(room_data)

        await self.get_room_with_check(room.id)

        if room_data_dict["facilities_ids"]:
            room_facilities_data = [
                RoomFacilityAdd(room_id=room.id, facility_id=f_id)
                for f_id in room_data_dict["facilities_ids"]
            ]
            await self.db.room_facilities.add_bulk(room_facilities_data)
        await self.db.commit()

        return room

    async def update_room(self, hotel_id: int, room_id: int, data: RoomAddRequest):
        await HotelService(self.db).get_hotel_with_check(hotel_id)
        await self.get_room_with_check(room_id)

        room_data_dict = data.model_dump()
        await self.check_existing_facilities(room_data_dict["facilities_ids"])
            
        room_data = RoomAdd(hotel_id=hotel_id, **data.model_dump())
        room = await self.db.rooms.edit(room_data, id=room_id, hotel_id=hotel_id)

        await self.db.room_facilities.set_room_facilities(
            room_id=room.id, facilities_ids=room_data_dict["facilities_ids"]
        )
        await self.db.commit()

    async def partial_update_room(
        self,
        hotel_id: int,
        room_id: int,
        data: RoomPatchRequest,
    ):
        await HotelService(self.db).get_hotel_with_check(hotel_id)
        await self.get_room_with_check(room_id)

        room_data_dict = data.model_dump(exclude_unset=True)
        if "facilities_ids" in room_data_dict:
            await self.check_existing_facilities(room_data_dict["facilities_ids"])
            
        _room_data = RoomPatch(hotel_id=hotel_id, **room_data_dict)
        room = await self.db.rooms.edit(
            _room_data,
            id=room_id,
            hotel_id=hotel_id,
            exclude_unset=True,
        )
        if "facilities_ids" in room_data_dict:
            await self.db.room_facilities.set_room_facilities(
                room_id=room.id, facilities_ids=data.facilities_ids
            )
        await self.db.commit()

    async def delete_room(self, hotel_id: int, room_id: int):
        await HotelService(self.db).get_hotel_with_check(hotel_id)
        await self.get_room_with_check(room_id)

        await self.db.rooms.delete(id=room_id, hotel_id=hotel_id)
        await self.db.commit()

    async def get_room_with_check(self, room_id: int) -> Room:
        try:
            return await self.db.rooms.get_one(id=room_id)
        except ObjectNotFoundException as ex:
            raise RoomNotFoundException from ex
        
    async def check_existing_facilities(self, ids: list[int]):
        if ids:
            existing_facilities_ids = await self.db.facilities.get_existing_ids(ids)
            missing = set(ids) - existing_facilities_ids
            if missing:
                raise FacilityNotFoundException