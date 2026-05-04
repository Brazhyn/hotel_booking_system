from datetime import date, datetime

from pydantic import ConfigDict

from src.schemas.base import BaseSchema


class BookingAddRequest(BaseSchema):
    date_from: date
    date_to: date
    room_id: int


class BookingAdd(BaseSchema):
    user_id: int
    room_id: int
    date_from: date
    date_to: date
    price: int


class Booking(BookingAdd):
    id: int
    total_cost: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
