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


class RoomNotFoundException(ObjectNotFoundException):
    detail = "Room not found"


class HotelNotFoundException(ObjectNotFoundException):
    detail = "Hotel not found"


class UserAlreadyExistsException(ObjectAlreadyExistsException):
    detail = "User with this email already exists"


class UserNotFoundException(ObjectNotFoundException):
    detail = "User not found"


class InvalidPasswordException(HotelBookingException):
    detail = "Password is incorrect"


class IncorrectTokenException(HotelBookingException):
    detail = "Token is incorrect"


def check_date_to_after_date_from(date_from: date, date_to: date) -> None:
    if date_to <= date_from:
        raise HTTPException(
            status_code=422, detail="Date departure must be greater than date arrival"
        )


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


class NoAvailableRoomsHTTPException(HotelBookingHTTPException):
    status_code = 409
    detail = "No rooms available for the given dates"


class UserAlreadyExistsHTTPException(HotelBookingHTTPException):
    status_code = 409
    detail = "User with this email already exists"


class UserNotFoundHTTPException(HotelBookingHTTPException):
    status_code = 401
    detail = "User not found"


class InvalidPasswordHTTPException(HotelBookingHTTPException):
    status_code = 401
    detail = "Password is incorrect"


class NoAccessTokenHTTPException(HotelBookingHTTPException):
    status_code = 401
    detail = "There is no authentication token!"
