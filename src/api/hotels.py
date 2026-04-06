from datetime import date

from fastapi import Body, Query, APIRouter
from fastapi_cache.decorator import cache

from src.schemas.hotels import Hotel, HotelPatch, HotelAdd
from src.api.dependencies import PaginationDep, DBDep


router = APIRouter(prefix="/hotels", tags=["hotels"])


@router.get("")
@cache(expire=10)
async def get_hotels(
    pagination: PaginationDep,
    db: DBDep,
    date_from: date = Query(examples=["2026-02-26"]),
    date_to: date = Query(examples=["2026-03-02"]),
    title: str | None = Query(default=None, description="Hotel name"),
    location: str | None = Query(default=None, description="Hotel location"),
):
    per_page = pagination.per_page or 5
    return await db.hotels.get_filtered_by_time(
        title=title,
        location=location,
        limit=per_page,
        offset=per_page * (pagination.page - 1),
        date_from=date_from,
        date_to=date_to
    )
        

@router.get("/{hotel_id}")
async def get_hotel(
    db: DBDep,
    hotel_id: int,
):
    return await db.hotels.get_one_or_none(id=hotel_id)


@router.post("")
async def create_hotel(db: DBDep, hotel_data: HotelAdd = Body(openapi_examples={
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
    hotel = await db.hotels.add(hotel_data)
    await db.commit()
    return {"status": "OK", "data": hotel}


@router.put("/{hotel_id}")
async def update_hotel(
    db: DBDep,
    hotel_id: int,
    hotel_data: HotelPatch, 
):
    await db.hotels.edit(hotel_data, id=hotel_id)
    await db.commit()

    return {"status": "OK"}


@router.patch("/{hotel_id}", summary="Часткове оновлення даних готелю")
async def partial_update_hotel(
    db: DBDep,
    hotel_id: int,
    hotel_data: HotelPatch,
):
    await db.hotels.edit(hotel_data, exclude_unset=True, id=hotel_id)
    await db.commit()
        
    return {"status": "OK"}


@router.delete("/{hotel_id}")
async def delete_hotel(
    db: DBDep,
    hotel_id: int,
):
    await db.hotels.delete(id=hotel_id)
    await db.commit()
    
    return {"status": "OK"}