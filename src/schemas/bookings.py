from datetime import date, datetime

from pydantic import BaseModel, ConfigDict


class BookingAddRequest(BaseModel):
    date_from: date
    date_to: date
    room_id: int
    
    
class BookingAdd(BaseModel):
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
    