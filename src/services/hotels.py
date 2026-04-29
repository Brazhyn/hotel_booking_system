from datetime import date

from src.exceptions import (
    HotelNotFoundException,
    ObjectNotFoundException,
    EmptyUpdateDataException,
    check_date_to_after_date_from,
)
from src.services.base import BaseService
from src.api.dependencies import PaginationDep
from src.schemas.hotels import HotelAdd, HotelPatch, HotelPut


class HotelService(BaseService):
    async def get_filtered_by_time(
        self,
        pagination: PaginationDep,
        date_from: date,
        date_to: date,
        title: str | None,
        location: str | None,
    ):
        check_date_to_after_date_from(date_from, date_to)
        per_page = pagination.per_page or 5
        return await self.db.hotels.get_filtered_by_time(
            title=title,
            location=location,
            limit=per_page,
            offset=per_page * (pagination.page - 1),
            date_from=date_from,
            date_to=date_to,
        )


    async def get_hotel(self, hotel_id: int):
        try:
            return await self.db.hotels.get_one(id=hotel_id)
        except ObjectNotFoundException:
            raise HotelNotFoundException


    async def create_hotel(self, data: HotelAdd):
        hotel = await self.db.hotels.add(data)
        await self.db.commit()
        return hotel


    async def update_hotel(self, hotel_id, data: HotelPut):
        await self.get_hotel_with_check(hotel_id=hotel_id)
        
        await self.db.hotels.edit(data, id=hotel_id)
        await self.db.commit()


    async def partial_update_hotel(self, hotel_id: int, data: HotelPatch):
        await self.get_hotel_with_check(hotel_id=hotel_id)
        if not data.model_dump(exclude_unset=True):
            raise EmptyUpdateDataException
        
        await self.db.hotels.edit(data, exclude_unset=True, id=hotel_id)
        await self.db.commit()


    async def delete_hotel(self, hotel_id: int):
        await self.get_hotel_with_check(hotel_id=hotel_id)
        
        await self.db.hotels.delete(id=hotel_id)
        await self.db.commit()


    async def get_hotel_with_check(self, hotel_id):
        try:
            await self.db.hotels.get_one(id=hotel_id)
        except ObjectNotFoundException:
            raise HotelNotFoundException
