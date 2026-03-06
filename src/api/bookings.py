from fastapi import APIRouter

from src.schemas.bookings import BookingAddRequest, BookingAdd
from src.api.dependencies import UserIdDep, DBDep


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
    room = await db.rooms.get_one_or_none(id=data.room_id)
    booking = await db.bookings.add(BookingAdd(
        user_id=user_id,
        price=room.price,
        **data.model_dump()
    ))
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
    
    