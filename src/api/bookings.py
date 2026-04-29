from fastapi import APIRouter

from src.schemas.bookings import BookingAddRequest
from src.api.dependencies import UserIdDep, DBDep
from src.exceptions import (
    NoAvailableRoomsException,
    RoomNotFoundException,
    NoAvailableRoomsHTTPException,
    RoomNotFoundHTTPException,
    BookingNotFoundException,
    BookingNotFoundHTTPException,
)
from src.services.bookings import BookingService


router = APIRouter(prefix="/bookings", tags=["bookings"])


@router.get("")
async def get_bookings(
    db: DBDep,
):
    return await BookingService(db).get_all_bookings()


@router.get("/me")
async def get_user_bookings(
    db: DBDep,
    user_id: UserIdDep,
):
    return await BookingService(db).get_user_bookings(user_id)


@router.post("")
async def create_booking(
    user_id: UserIdDep,
    db: DBDep,
    data: BookingAddRequest,
):
    try:
        booking = await BookingService(db).add_booking(user_id, data)
    except RoomNotFoundException:
        raise RoomNotFoundHTTPException
    except NoAvailableRoomsException:
        raise NoAvailableRoomsHTTPException

    return {"status": "OK", "data": booking}


@router.delete("/{booking_id}")
async def delete_booking(
    db: DBDep,
    booking_id: int,
):
    try:
        await BookingService(db).delete_booking(booking_id)
    except BookingNotFoundException:
        raise BookingNotFoundHTTPException
    return {"status": "OK"}
