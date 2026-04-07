from fastapi import APIRouter, HTTPException

from src.schemas.rooms import Room
from src.schemas.bookings import Booking, BookingAddRequest, BookingAdd
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
    try:
        room: Room | None = await db.rooms.get_one_or_none(id=data.room_id)
        booking: Booking | None = await db.bookings.add_booking(
            BookingAdd(user_id=user_id, price=room.price, **data.model_dump()),
            hotel_id=room.hotel_id,
        )
        await db.commit()
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

    return {"status": "OK", "data": booking}


@router.delete("/{booking_id}")
async def delete_booking(
    db: DBDep,
    booking_id: int,
):
    await db.bookings.delete(id=booking_id)
    await db.commit()

    return {"status": "OK"}
