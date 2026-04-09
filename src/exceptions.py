from datetime import date

from fastapi import HTTPException


class HotelBookingException(Exception):
    detail = "Unexpected error"

    def __init__(self, *args, **kwargs):
        super().__init__(self.detail, *args, **kwargs)


class ObjectNotFoundException(HotelBookingException):
    detail = "Object not found"
    
    
class NoAvailableRoomsException(HotelBookingException):
    detail = "No rooms available for the given dates"    
    
    
class ObjectAlreadyExistsException(HotelBookingException):
    detail = "Object with the same parameters already exists"
    
    
def check_date_to_after_date_from(date_from: date, date_to: date) -> None:
    if date_to <= date_from:
        raise HTTPException(status_code=422, detail="Date departure must be greater than date arrival")
    
    
class HotelBookingHTTPException(HTTPException):
    status_code = 500
    detail = "Unexpected error"
    
    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)
    
    
class HotelNotFoundHTTPException(HotelBookingHTTPException):
    status_code = 404
    detail = "Hotel not found"
    
    
class RoomNotFoundHTTPException(HotelBookingHTTPException):
    status_code = 404
    detail = "Room not found"
    

    