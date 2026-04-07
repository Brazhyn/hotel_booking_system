from src.repositories.mappers.base import DataMapper
from src.models.hotels import HotelModel
from src.models.rooms import RoomModel
from src.models.users import UserModel
from src.models.bookings import BookingModel
from src.models.facilities import FacilityModel, RoomFacilityModel
from src.schemas.hotels import Hotel
from src.schemas.rooms import Room, RoomWithRels
from src.schemas.users import User, UserWithHashedPassword
from src.schemas.bookings import Booking
from src.schemas.facilities import Facility, RoomFacility


class HotelMapper(DataMapper):
    model = HotelModel
    schema = Hotel


class RoomMapper(DataMapper):
    model = RoomModel
    schema = Room


class UserMapper(DataMapper):
    model = UserModel
    schema = User


class BookingMapper(DataMapper):
    model = BookingModel
    schema = Booking


class RoomWithRelsMapper(DataMapper):
    model = RoomModel
    schema = RoomWithRels


class UserWithHashedPasswordMapper(DataMapper):
    model = UserModel
    schema = UserWithHashedPassword


class FacilityMapper(DataMapper):
    model = FacilityModel
    schema = Facility


class RoomFacilityMapper(DataMapper):
    model = RoomFacilityModel
    schema = RoomFacility
