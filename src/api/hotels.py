from datetime import date

from fastapi import Body, Query, APIRouter
from fastapi_cache.decorator import cache

from src.exceptions import (
    HotelNotFoundException,
    HotelNotFoundHTTPException,
    EmptyUpdateDataException,
    EmptyUpdateDataHTTPException,
)
from src.schemas.hotels import HotelPatch, HotelAdd, HotelPut
from src.api.dependencies import PaginationDep, DBDep
from src.services.hotels import HotelService

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
    return await HotelService(db).get_filtered_by_time(
        pagination,
        date_from,
        date_to,
        title,
        location,
    )


@router.get("/{hotel_id}")
async def get_hotel(
    db: DBDep,
    hotel_id: int,
):
    try:
        return await HotelService(db).get_hotel(hotel_id=hotel_id)
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException


@router.post("")
async def create_hotel(
    db: DBDep,
    hotel_data: HotelAdd = Body(
        openapi_examples={
            "1": {
                "summary": "Underhill",
                "value": {
                    "title": "Luxury hotel Underhill",
                    "location": "street Martynovicha 4",
                },
            },
            "2": {
                "summary": "Provance",
                "value": {
                    "title": "Magnificent hotel Provance",
                    "location": "street Popovicha 12",
                },
            },
        }
    ),
):
    hotel = await HotelService(db).create_hotel(hotel_data)
    return {"status": "OK", "data": hotel}


@router.put("/{hotel_id}")
async def update_hotel(
    db: DBDep,
    hotel_id: int,
    hotel_data: HotelPut,
):
    try:
        await HotelService(db).update_hotel(hotel_id=hotel_id, data=hotel_data)
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException
    return {"status": "OK"}


@router.patch("/{hotel_id}")
async def partial_update_hotel(
    db: DBDep,
    hotel_id: int,
    hotel_data: HotelPatch,
):
    try:
        await HotelService(db).partial_update_hotel(hotel_id=hotel_id, data=hotel_data)
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException
    except EmptyUpdateDataException:
        raise EmptyUpdateDataHTTPException
    return {"status": "OK"}


@router.delete("/{hotel_id}")
async def delete_hotel(
    db: DBDep,
    hotel_id: int,
):
    try:
        await HotelService(db).delete_hotel(hotel_id=hotel_id)
    except HotelNotFoundException:
        raise HotelNotFoundHTTPException
    return {"status": "OK"}
