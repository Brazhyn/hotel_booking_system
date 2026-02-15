import asyncio

from fastapi import Body, Query, APIRouter

from src.schemas.hotels import Hotel, HotelPatch, HotelAdd
from src.api.dependencies import PaginationDep
from src.database import async_session_maker, engine
from repositories.hotels import HotelRepository



router = APIRouter(prefix="/hotels", tags=["hotels"])


@router.get("")
async def get_hotels(
    pagination: PaginationDep,
    title: str | None = Query(default=None, description="Hotel name"),
    location: str | None = Query(default=None, description="Hotel location")
):
    per_page = pagination.per_page or 5
    async with async_session_maker() as session:
        return await HotelRepository(session).get_all(
            title=title,
            location=location,
            limit=per_page,
            offset=per_page * (pagination.page - 1),
        )
        

@router.get("/{hotel_id}")
async def get_hotel(hotel_id: int):
    async with async_session_maker() as session:
        return await HotelRepository(session).get_one_or_none(id=hotel_id)


@router.post("")
async def create_hotel(hotel_data: HotelAdd = Body(openapi_examples={
    "1": {"summary": "Underhill", "value": {
        "title": "Luxury hotel Underhill",
        "location": "street Martynovicha 4",
    }},
    "2": {"summary": "Provance", "value": {
        "title": "Magnificent hotel Provance",
        "location": "street Popovicha 12", 
    }}
})
):
    async with async_session_maker() as session:
        hotel = await HotelRepository(session).add(hotel_data)
        await session.commit()
    return {"status": "OK", "data": hotel}


@router.put("/{hotel_id}")
async def update_hotel(
    hotel_id: int,
    hotel_data: HotelPatch, 
):
    async with async_session_maker() as session:
        await HotelRepository(session).edit(hotel_data, id=hotel_id)
        await session.commit()

    return {"status": "OK"}


@router.patch("/{hotel_id}", summary="Часткове оновлення даних готелю")
async def partial_update_hotel(
    hotel_id: int,
    hotel_data: HotelPatch,
):
    async with async_session_maker() as session:
        await HotelRepository(session).edit(hotel_data, exclude_unset=True, id=hotel_id)
        await session.commit()
        
    return {"status": "OK"}


@router.delete("/{hotel_id}")
async def delete_hotel(hotel_id: int):
    async with async_session_maker() as session:
        await HotelRepository(session).delete(id=hotel_id)
        await session.commit()
    
    return {"status": "OK"}