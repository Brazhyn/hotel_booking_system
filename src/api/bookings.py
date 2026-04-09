from fastapi import APIRouter, HTTPException

from src.schemas.rooms import Room
from src.schemas.bookings import Booking, BookingAddRequest, BookingAdd
from src.api.dependencies import UserIdDep, DBDep
from src.exceptions import ObjectNotFoundException, NoAvailableRoomsException


router = APIRouter(prefix="/bookings", tags=["bookings"])


@router.get("")
async def get_bookings(
    db: DBDep,
):
    return await db.bookings.get_all()


@router.get("/me")
async def get_user_bookings(
    db: DBDep,
    user_id: UserIdDep,
):
    return await db.bookings.get_filtered(user_id=user_id)


@router.post("")
async def create_booking(
    user_id: UserIdDep,
    db: DBDep,
    data: BookingAddRequest,
):
    try:
        room: Room = await db.rooms.get_one(id=data.room_id)
    except ObjectNotFoundException:
        raise HTTPException(status_code=400, detail="Room not found")
    
    try:
        booking = await db.bookings.add_booking(
            BookingAdd(user_id=user_id, price=room.price, **data.model_dump()),
            hotel_id=room.hotel_id,
        )
    except NoAvailableRoomsException as ex:
        raise HTTPException(status_code=409, detail=ex.detail)
    
    await db.commit()
    return {"status": "OK", "data": booking}


@router.delete("/{booking_id}")
async def delete_booking(
    db: DBDep,
    booking_id: int,
):
    await db.bookings.delete(id=booking_id)
    await db.commit()

    return {"status": "OK"}
